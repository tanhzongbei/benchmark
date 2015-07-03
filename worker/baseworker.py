#coding: utf8
# Author: Ilcwd@20110919


import time
import config as _conf

class Worker():
    params = {}
    def __init__(self):
        self.params = {}
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR
    
    def set_params(self, **kw):
        self.params = kw
        
    def _do_work(self, **kw):
        raise NotImplementedError
    
    def before_run(self):
        pass
    
    def run(self):
        self.before_run()
        self._do_work(**self.params)
        
    def after_run(self):
        pass
        
    def get_result(self):
        ''' @return: <result, start time, cost time>
        '''
        return self.result
    
if __name__ == '__main__':
    pass