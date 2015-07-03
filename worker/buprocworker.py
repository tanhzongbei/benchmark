#coding: utf8
# Author: Ilcwd@20110919

import time
import config as _conf

from baseworker import Worker

import MySQLdb as m

class BUProcWorker(Worker):
    def __init__(self):                
        self.params = {}
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR
        
        self.cur = None
        self.f = None
        
    def _do_work(self, fileId):
        start_time = time.time()

        try:            
            self.cur.callproc(_conf.MYSQL_BU_PROCEDURE, (int(fileId),))
            parents = []
            parents.append(self.cur.fetchall()[0][0])
            while self.cur.nextset():
                res = self.cur.fetchall()
                if res:
                    parents.append(res[0][0])
            
#            self.out.write(str(parents)+'\n')
#            self.out.flush()

            cost_time = time.time() - start_time
            self.result = 'ok', start_time, cost_time
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
             self.f = open(_conf.FILE_ID_PATH, 'r')
             
        line = self.f.readline()
        self.params = {'fileId': int(line)}
        
        
    def __del__(self):
        if self.f: self.f.close()
        if self.cur: self.cur.close()
#        self.out.close()
    
if __name__ == '__main__':
    pass