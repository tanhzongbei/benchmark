#coding: utf8
# Author: Ilcwd@20110919

import time
from hashlib import md5
import config as _conf

from baseworker import Worker

import MySQLdb as m
import _mysql

def escape(sql):
    '''这里假定连接数据库都是使用utf8的。'''
    if sql is None:
        return ''
    if isinstance(sql, unicode):
        sql = sql.encode('utf8')
    return _mysql.escape_string(sql)

class TDProcWorker(Worker):
    def __init__(self):                
        self.params = {}
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR
        
        self.cur = None
        self.f = None
        
    def _do_work(self, userId, path):
        start_time = time.time()

        try:            
            path_slice = filter(len, path.split('/'))
            path_count = len(path_slice)            
            md5_slice = [md5(escape(unicode(fname).lower())).hexdigest()[0:16] for fname in path_slice]
            
            self.cur.callproc(_conf.MYSQL_TD_PROCEDURE, (path_count, int(userId) << 32, ''.join(md5_slice)))
            parents = []
            res = self.cur.fetchall()
            if res:
                parents.append(res[0])
            while self.cur.nextset():
                res = self.cur.fetchall()
                if res:
                    parents.append(res[0])

            #print path,parents
            cost_time = time.time() - start_time
            if parents:
                self.result = 'ok', start_time, cost_time
            else:
                self.result = 'empty result', start_time, cost_time
        except Exception, e:
            cost_time = time.time() - start_time
            self.result =  'UnhandleError : %s' % str(e), start_time, cost_time
            
    def before_run(self):
        if not self.cur:
            conn = m.connect(host=_conf.MYSQL_HOST,
                port=_conf.MYSQL_PORT,
                user=_conf.MYSQL_USER,
                passwd=_conf.MYSQL_PASSWORD,
                db=_conf.MYSQL_DB)
            self.cur = conn.cursor()
        if not self.f:
             self.f = open(_conf.TOP_DOWN_TEST_CASES, 'r')
             
        line = self.f.readline()
        if line:
            userid, fileids, filepath = line.split(':')
            self.params = {'userId': int(userid), 'path': filepath.rstrip()}
        else:
            self.f.close()
            self.f = None
        
        
    def __del__(self):
        if self.f: self.f.close()
        if self.cur: self.cur.close()
#        self.out.close()
    
if __name__ == '__main__':
    pass