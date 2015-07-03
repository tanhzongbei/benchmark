#coding:utf8
# Author: Ilcwd
# Created on: 2011/05/18

import sys
reload(sys)
sys.setdefaultencoding('utf8')


import time
import os
import signal
from multiprocessing import Process, Queue

import config as _conf
from worker.baseworker import Worker

stop = False
def exitHandler(signum, frame):
    global stop
    stop = True
    print "=============== STOP TESTING ==============="

signal.signal(signal.SIGTERM, exitHandler)
signal.signal(signal.SIGQUIT, exitHandler)
signal.signal(signal.SIGHUP, exitHandler)
signal.signal(signal.SIGINT, exitHandler)
    
class WorkerManager():
    def __init__(self, worker, concurrency, request_number):
        assert isinstance(worker, Worker), ('expect an instance of Worker class but a %s.' % type(worker))
        self.worker = worker
        self.co = concurrency
        self.rn = request_number
        global stop
        stop = False

    def start_benchmark(self):
        plist = []   
        queue_list = {}
        for _i in xrange(self.co):
            result_queue = Queue()
            process = Process(target = self._start_worker, args = (result_queue,))
            plist.append(process)
            process.start()
            print "=========== WorkerManager, Process %d start ===========" % process.pid
            queue_list[process.pid] = result_queue
        #map(Process.join, plist)
        return queue_list
    
    def _start_worker(self, result_queue):
        global stop
        st = time.time()
        for _i in xrange(self.rn):
            if stop: break
            self.worker.run()
            result_queue.put(self.worker.get_result())
        et = time.time()
        print "=========== WorkerManager, Process %d finished ===========" % os.getpid()
        result_queue.put((_conf.WORKER_FINISHED, et, et - st))
        
    
class Analyser():
    def __init__(self, queue_list, interval = _conf.ANALYSER_FRESH_INTERVAL):
        self.process_number = len(queue_list)
        self.in_queue_list = queue_list
        self.out_data = {}
        self.interval = interval
        
    def _draw_diagram(self):
        result = [(k, v) for k, v in self.out_data.iteritems()]
        result.sort()
        for pid, data in result:
            print '%10s :' % pid,
            for item in data :
                print item, 
            print
    
    def _is_not_finished(self):
        if not self.out_data: return True
        global stop
        if stop: return False
        for list_data in self.out_data.values():
            result, _start_time, _cost_time = list_data[-1]
            if result != _conf.WORKER_FINISHED:
                return True
            
        return False
    
    def _fetch_data(self):
        for k, v in self.in_queue_list.items():
            while True:
                try:
                    item = v.get_nowait()
                except:
                    break
                try:
                    self.out_data[k].append(item)
                except:
                    self.out_data[k] = [item]
    
    def do(self):
        while self._is_not_finished():
            self._fetch_data()
            time.sleep(self.interval)
            
        #self._draw_diagram()
        # TODO: 总结之前先保存数据
        self._summery()
        
    def _summery(self):
        request_num = 0
        total_time_all_processes = 0.0
        result = {}
        concurrency = len(self.out_data)
        costtime_list = []
        
        def print_sub_item(key, value):
            print "%25s| %-15s " % (("+ %-20s" % key), value)
            
        def calculate_costtime(ct_list = costtime_list):
            ct_list = costtime_list
            ct_list.sort() # 会修改传入的参数
            ct_len = len(ct_list)
            ct_result = {}
            ct_result['99%'] = "%.2f (ms)" % (ct_list[int(ct_len * 0.99)]*1000)
            ct_result['95%'] = "%.2f (ms)" % (ct_list[int(ct_len * 0.95)]*1000)
            ct_result['85%'] = "%.2f (ms)" % (ct_list[int(ct_len * 0.85)]*1000)
            ct_result['50%'] = "%.2f (ms)" % (ct_list[int(ct_len * 0.50)]*1000)
            ct_result['avg'] = "%.2f (ms)" % (sum(ct_list)/ct_len*1000)
            ct_result['min'] = "%.2f (ms)" % (ct_list[0]*1000)
            ct_result['max'] = "%.2f (ms)" % (ct_list[-1]*1000)
            return ct_result
        
        def dict_to_kvlist_and_sort(dict_obj):
            list_obj = list(dict_obj.iteritems())
            list_obj.sort()
            return list_obj
        
        def parse_result(result_dict = result, total = request_num):
            ret_dict = {}
            for k, v in result_dict.iteritems():
                ret_dict[k] = "%d (%.3f%%)" % (v, float(v)*100/total)
            return ret_dict
        
        start_time = 1 << 64
        end_time = 0
        for data_list in self.out_data.values():
            for res, st, ct in data_list:
                if res in [_conf.WORKER_FINISHED, _conf.WORKER_NOT_START]: continue
                
                request_num += 1
                try:
                    result[res] = result[res] + 1
                except KeyError:
                    result[res] = 1
                
                costtime_list.append(ct)
                
                total_time_all_processes += ct
                if st < start_time:
                    start_time = st
                if st + ct > end_time:
                    end_time =st + ct
                    
        min_rps = int(request_num / (end_time - start_time))
        max_rps = int(request_num / (total_time_all_processes / concurrency))
        print "%-25s| %-15s " % ('Request number', request_num)
        print "%-25s| %-15s " % ('Total time ', end_time-start_time)
        print "%-25s| %-15s " % ('Requests per sec', "%d~%d" % (min_rps, max_rps))
        print "%-25s| %-15s " % ('COSTTIME ', '--------------')
        for k, v in dict_to_kvlist_and_sort(calculate_costtime(costtime_list)):
            print_sub_item(k, v)
        print "%-25s| %-15s " % ('RESULT ', '--------------')
        for k, v in dict_to_kvlist_and_sort(parse_result(result, request_num)):
            print_sub_item(k, v)
        
def usage():
    print '''Simple Benchmark Tool
    
Usage: ./benchmark.py [OPTIONS]
Parameters:
    -h            test host.
    -c            concurrency, the number of connections at the same time.
    -r            the number of requests each connection performs.
    -t            timeout.
    -u            server user.
    -p            server password
'''

def main():
    import sys
    import getopt
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h:c:r:t:u:p:a')
        opts, args = getopt.getopt(sys.argv[1:], 'h:c:r:t')
    except getopt.GetoptError, e:
        usage()
        print '>>>> ERROR: %s' % str(e)
        sys.exit(2)
        
    print opts
    for o, v in opts:
        if o in ('-h', ):       _conf.DEFAULT_HOST = v
        elif o in ('-c', ):     _conf.DEFAULT_CONCURRENCY = int(v)
        elif o in ('-r', ):     _conf.DEFAULT_REQUEST_NUMBER = int(v)
        elif o in ('-t', ):     _conf.DEFAULT_TIMEOUT = int(v)
        elif o in ('-u', ):     _conf.KUAIPAN_USER = v
        elif o in ('-p', ):     _conf.KUAIPAN_PASS = v
        
        
    from worker.cdnmanagerwork import (
                                     CDNManagerWorker
    )
    
    test = CDNManagerWorker()
    mgr = WorkerManager(test, _conf.DEFAULT_CONCURRENCY, _conf.DEFAULT_REQUEST_NUMBER)
    ql = mgr.start_benchmark()
    anr = Analyser(ql)
    anr.do()


if __name__ == '__main__':
    main()