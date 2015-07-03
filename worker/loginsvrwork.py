'''
Created on 2012-12-22

@author: xiaobei
'''
import json
import time
import random
import uuid

from baseworker import Worker
from utils.urltool import openUrlCurl
import config as _conf


class Pressuretest(Worker):
    def __init__(self):
        self.params = {}
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR
            
    def _do_work(self):
        start_time = time.time()
        try:
            username = 'test%s@testkingsoft.com' % uuid.uuid4().hex
            pwd = '123456'
            reg = request.register(username, pwd)
            reg_time = time.time()
            
            reg_cost = reg_time - start_time
            
            reg = json.loads(reg[1])
            if reg['_code_']['code'] != 10001:
                self.result = 'UnhandleError : loginsvr register %s' % reg, start_time, reg_cost
                print self.result
                return
            else:
                login = request.login(username, pwd)
                login_time = time.time()
                login_cost = login_time - start_time
                
                login = json.loads(login[1])
                if login['_code_']['code'] != 10001:
                    self.result = 'UnhandleError : loginsvr login %s' % login, start_time, login_cost
                    print self.result
                    return
                    
            cost_time = time.time() - start_time 
            self.result = 'ok', start_time, cost_time
        except Exception, e:
            print str(e)
            cost_time = time.time() - start_time
            self.result =  'UnhandleError : %s' % str(e), start_time, cost_time        

post_login = '<?xml version="1.0" encoding="utf-8"?><xLive><clientVersion>2.0</clientVersion><password>%s</password><user>%s</user><clientName>testclient</clientName><deviceId>%s</deviceId></xLive>'
post_reg = '<?xml version="1.0" encoding="utf-8"?><xLive><token>%s</token><password>%s</password><email>%s</email><addtype>X</addtype></xLive>'

class Pressuretest1(Worker):
    def __init__(self):
        self.params = {}
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR
        deviceid = uuid.uuid4().hex
        post_data = post_login % (_conf.SUPER_PWD, _conf.SUPER_USERNAME, deviceid)
        self.header = {'v' : 2}
        resCode, regData = openUrlCurl(_conf.DOCSVR_LOGIN_URL, post_data, self.header)
        self.suToken = self.getattr(regData, 'token') 
            
    def _do_work(self):
        start_time = time.time()
        try:
            username = 'test%s@testkingsoft.com' % uuid.uuid4().hex
            pwd = '123456'
            reg_post_data = post_reg % (self.suToken, pwd, username)
            regCode, regData = openUrlCurl(_conf.DOCSVR_REGISTER_URL, reg_post_data, self.header)
            reg_time = time.time()
            reg_cost = reg_time - start_time        
            code = self.getresult(regData)
    
            if code != 'ok':
                self.result = 'UnhandleError : docsvr register %s' % regData, start_time, reg_cost
                print self.result
                return
            else:
                deviceid = uuid.uuid4().hex
                login_post_data = post_login % (pwd, username, deviceid)
                loginCode, loginData = openUrlCurl(_conf.DOCSVR_LOGIN_URL, login_post_data, self.header)
                login_time = time.time()
                login_cost = login_time - start_time
                code = self.getresult(loginData)
                if code != 'ok':
                    self.result = 'UnhandleError : docsvr login %s' % loginData, start_time, login_cost
                    print self.result
                    return
            
            cost_time = time.time() - start_time 
            self.result = 'ok', start_time, cost_time
        except Exception, e:
            print str(e)
            cost_time = time.time() - start_time
            self.result =  'UnhandleError : %s' % str(e), start_time, cost_time        
    
    def getattr(self, res, attr):
        begin = '<%s>' % attr
        end = '</%s>' % attr
        beginpos = res.find(begin)
        endpos = res.find(end)
        str = res[beginpos + len(begin) : endpos]
        return str
    
    def getresult(self, res):
        keyword = 'xLive result="'
        beginpos = res.find(keyword)
        return res[beginpos + len(keyword) : beginpos + len(keyword) + 2]
    
    
class Pressuretest2(Worker):
    def __init__(self):
        self.params = {}
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR
            
    def _do_work(self):
        start_time = time.time()
        try:
            userid = random.randint(1, 2000 * 10000)
            reg = request.getuserinfo(userid)
            reg_time = time.time()
            
            reg_cost = reg_time - start_time
            
            reg = json.loads(reg[1])
            if reg['_code_']['code'] != 10001:
                self.result = 'UnhandleError : loginsvr register %s userid = %d' % (reg, userid), start_time, reg_cost
                print self.result
                return
                    
            cost_time = time.time() - start_time 
            self.result = 'ok', start_time, cost_time
        except Exception, e:
            print str(e)
            cost_time = time.time() - start_time
            self.result =  'UnhandleError : %s' % str(e), start_time, cost_time        
            

class Pressuretest3(Worker):
    def __init__(self):
        self.params = {}
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR
            
    def _do_work(self):
        start_time = time.time()
        try:
            username = 'test%s@testkingsoft.com' % uuid.uuid4().hex
            pwd = '123456'
            regres = request.register(username, pwd)
            reg_time = time.time()
            
            reg_cost = reg_time - start_time
            
            regres = json.loads(regres[1])
            if regres['_code_']['code'] != 10001:
                self.result = 'UnhandleError : loginsvr register %s' % regres, start_time, reg_cost
                print self.result
                return
            else:
                loginres  = request.login(username, pwd)
                login_time = time.time()
                login_cost = login_time - start_time
                
                loginres = json.loads(loginres[1])
                if loginres['_code_']['code'] != 10001:
                    self.result = 'UnhandleError : loginsvr login %s' % loginres, start_time, login_cost
                    print self.result
                    return
                else:
                    token = loginres['_result_']['token']
                    queryres = request.querysid(token)
                    query_cost = time.time() - start_time
                    queryres = json.loads(queryres[1])
                    if queryres['_code_']['code'] != 10001:
                        self.result = 'UnhandleError : loginsvr querysid %s' % queryres, start_time, query_cost
                        print self.result
                        return
                    
            cost_time = time.time() - start_time 
            self.result = 'ok', start_time, cost_time
        except Exception, e:
            print str(e)
            cost_time = time.time() - start_time
            self.result =  'UnhandleError : %s' % str(e), start_time, cost_time        

class request():
    def register(self, username, pwd):
        reg_post_data = {'_params_' : {'username' :username, 'password' : pwd, 'ip' : '127.0.0.1', 'nickname' : username, 'activationstate' : 1, 'registfrom' : 'X'}}
        reg_post_data = json.dumps(reg_post_data)                    
        reg = openUrlCurl(_conf.LOGINSVR_URI + _conf.LOGINSVR_REGISTER_URI, reg_post_data)
        return reg
    
    
    def login(self, username, pwd):             
        login_post_data = {'_params_' : {'username' : username, 'password' : pwd, 'deviceid' : 'dev-1', 'ip' : '127.0.0.1', 'secureflag' : 0}}
        login_post_data = json.dumps(login_post_data)
        login = openUrlCurl(_conf.LOGINSVR_URI + _conf.LOGINSVR_LOGIN_URI, login_post_data)
        return login
    
    
    def getuserinfo(self, userid):
        userinfo_post_data = {'_params_' : {'userid' : userid}}
        userinfo_post_data = json.dumps(userinfo_post_data)                    
        userinfo = openUrlCurl(_conf.LOGINSVR_URI + _conf.LOGINSVR_GETUSERINFO_URI, userinfo_post_data)
        return userinfo
    
    def querysid(self, token):
        query_post_data = {'_params_' : {'token' : token, 'secureflag' : 0}}
        query_post_data = json.dumps(query_post_data)                    
        query = openUrlCurl(_conf.LOGINSVR_URI + _conf.LOGINSVR_QUERYSIDINFO_URI, query_post_data)
        return query    


request = request()


if __name__ == '__main__':
    p = Pressuretest()
    p._do_work()        