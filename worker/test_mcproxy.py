#coding:utf8
'''
Created on 2013-6-7

@author: zhangyupeng
'''
from benchmark.worker.baseworker import Worker
import time
import random
import benchmark.config as _conf
import memcache
from benchmark.benchmark import WorkerManager, Analyser


class Pressuretest(Worker):
    def __init__(self):
        self.params = {}
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR
        self.mc = memcache.Client(['192.168.10.200:22123'], debug=0)
        self.userInfo = {
            "username":"test_shareref1356681366.35@126.com",
            "mobile":"","userid":200,
            "userregtime":1356653841,
            "emailstatus":1,
            "nickname":"test_shareref1356681366.35@126.com",
            "email":"test_shareref1356681366.35@126.com",
            "addtype":"T"
        }
            
    def _do_work(self):
        start_time = time.time()
        userid = str(random.randint(0, 999999999))
        self.mc.add(userid, self.userInfo, 600)
        userInfo = self.mc.get(userid)
        end_time = time.time()
        cost_time = end_time - start_time
                
        if not userInfo:
            self.result = 'mis', start_time, cost_time
        else:
            self.result = 'ok', start_time, cost_time
        
def main():
    test = Pressuretest()
    mgr = WorkerManager(test, _conf.DEFAULT_CONCURRENCY, _conf.DEFAULT_REQUEST_NUMBER)
    ql = mgr.start_benchmark()
    anr = Analyser(ql)
    anr.do()
        
if __name__ == '__main__':
    main()