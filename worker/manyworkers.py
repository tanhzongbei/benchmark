#coding: utf8
# Author: Ilcwd@20110919

import time

from openapi import OpenAPI
from utils.urltool import TimeoutException, \
                    openUrlCurl as _curl
import config as _conf
from baseworker import Worker


class OpenAPIWorker(Worker):
    def __init__(self, host, timeout):
        self.timeout = timeout
        self.api = OpenAPI(netloc = host, timeout = timeout)
        params = {'x_auth_username': _conf.KUAIPAN_USER, 
                  'x_auth_password': _conf.KUAIPAN_PASS, 
                  'x_auth_mode': 'client_auth'}
        code, ret = self.api.xAccessToken(**params)
        assert code == 200, ret
        self.root = ret['charged_dir']
        self.api.set_token(ret['oauth_token'], ret['oauth_token_secret'])

        print self.api.dir(file_id = self.root)
        print self.api.user()
        
        self.params = {}
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR
        
    def _do_work(self, **kw):
        func = kw.pop('function', _conf.DEFAULT_FUNCTION)
        start_time = time.time()
        try:            
            code, _ = getattr(self.api, func)(**kw)
            cost_time = time.time() - start_time
            self.result = code, start_time, cost_time
        except TimeoutException:
            self.result =  'Timeout', start_time, self.timeout
        except :
            cost_time = time.time() - start_time
            self.result =  'UnhandleError', start_time, cost_time


import redis
import random
class RedisRWWorker(Worker):
    def __init__(self, host, port, password):
        self.redis = redis.Redis(host = host, port = port, password = password)
        self.params = {}
        
    def _do_work(self, **kw):
        key = random.randint(0, 100000000)
        value = str({'a': 'b'*256, key: 'asdf'*10})
        start_time = time.time()
        try:
             
            self.redis.set(key, value)
            assert self.redis.get(key) == value
            cost_time = time.time() - start_time
            self.result = 'Success', start_time, cost_time
        except TimeoutException:
            self.result =  'Timeout', start_time, self.timeout
        except :
            cost_time = time.time() - start_time
            self.result =  'AccessError', start_time, cost_time
            

class RedisTransWorker(Worker):
    def __init__(self, host, port, password):
        self.redis = redis.Redis(host = host, port = port, password = password)
        self.params = {}
        
    def _do_work(self,):
            
import datetime
class WriteFileWorker(Worker):
    def __init__(self, path = '/data/logs/xsvr/test_log.log'):
        self.fp = open(path, 'a')
        self.params = {}
        global lock

        
    def _do_work(self, **kw):
        key = random.randint(0, 100000000)
        value = str({'a': 'b'*256, key: 'asdf'*10})
        start_time = time.time()
        try:

            self.fp.write('%s - function - args = %s \n' % (datetime.datetime.now(), value))
            cost_time = time.time() - start_time
            self.result = 'Success', start_time, cost_time
        except:
            cost_time = time.time() - start_time
            self.result =  'AccessError', start_time, cost_time
        finally:
            pass
            
    def __del__(self):
        self.fp.close()
        
        
        
import logging
import logging.config
from string import Template
logging.config.fileConfig('logging.conf')
class LogRequest():
    '''复写了write,日志级别为logging.WARNING = 30'''
    def __init__(self):
        _LOG_FORMAT = 'func=${Function} - res=${Result} - args=${Params} - time=${CostTime}'
        self.logFMT = Template(_LOG_FORMAT)
        self.logger = logging.getLogger('xsvrRequest')
        self.level = logging.WARNING
        
    def _filterResult(self, result):
        
        if isinstance(result, tuple):
            return result[0]
        else:
            return result
        
    def write(self, function, params, costtime, result):
        _result = self._filterResult(result)
        logInfo = self.logFMT.substitute(Function = function, Params = params, CostTime = costtime, Result = _result)
        self.logger.log(self.level, logInfo)
        
class LogServerWorker(Worker):
    def __init__(self):
        self.params = {}
        self.logger = LogRequest()
        
    def _do_work(self, **kw):
        key = random.randint(0, 100000000)
        value = str({'a': 'b'*256, key: 'asdf'*10})
        start_time = time.time()
        try:

            self.logger.write('function', value, time.time() - start_time, 'no except')
            cost_time = time.time() - start_time
            self.result = 'Success', start_time, cost_time
        except:
            cost_time = time.time() - start_time
            self.result =  'AccessError', start_time, cost_time
        finally:
            pass
    
    
class DocsvrWorker(Worker):
    LOGIN = '''\
<?xml version="1.0" encoding="utf-8"?>\
<xLive>\
<clientVersion>klive-1.0.487</clientVersion>\
<user>%s</user>\
<password>%s</password>\
<clientName>ys-computer-clientName</clientName>\
<deviceId>klive-1.0.487</deviceId>\
</xLive>
'''
    DIR = '''\
<?xml version="1.0" encoding="utf-8"?>\
<xLive><token>%s</token>
<fileId>
</fileId>
</xLive>
'''
    IP = '''\
<?xml version="1.0" encoding="utf-8"?>\
<xLive><token>%s</token>
<ip>%s</ip>
</xLive>
'''


    def __init__(self, host, user = 'ma4@126.com', passwd = '123456', ip='127.0.0.1'):
        self.ip = ip
        self.url = 'http://%s/xsvr/' % host
        code, ret = _curl(self.url + 'login', self.LOGIN % (user, passwd), {'v':2})
        assert code == 200, ret
        token = ret[ret.find('<token>')+len('<token>'):ret.rfind('</token>')]
        
        self.DIR = self.DIR % token
        self.IP = self.IP % (token, '%s')
        print  _curl(self.url + 'dir', self.DIR, {'v':2})
        assert self._dir() == 'ok'
        
    def _dir(self):
        code, ret = _curl(self.url + 'dir', self.DIR, {'v':2}, 1)
        if code != 200:
            return '%d %s' % (code, ret[:20])
        
        return ret[ret.find('result="')+len('result="'):ret.rfind('"><')]
    
    def _ip(self):
        code, ret = _curl(self.url + 'testIp', self.IP % self.ip, {'v':2}, 1)
        if code != 200:
            return '%d %s' % (code, ret[:20])
        
        return ret[ret.find('result="')+len('result="'):ret.rfind('"><')]
    
    def _do_work(self, **kw):
        start_time = time.time()
        try:
            self.result = self._ip(), start_time, time.time() - start_time
        except TimeoutException:
            cost_time = time.time() - start_time
            self.result =  'Timeout', start_time, cost_time
        except Exception, e:
            cost_time = time.time() - start_time
            self.result = str(e), start_time, cost_time
        finally:
            pass
    
if __name__ == '__main__':
    w = DocsvrWorker('192.168.10.200')
    w.run()
    print w.get_result()