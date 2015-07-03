#coding:utf-8
#author:leanse

import json
import time
import random
from urllib import quote

from baseworker import Worker
from utils.urltool import openUrlCurl as _curl
from config import SEARCH_PROXY_ADDR
from config import MAX_USERID
from config import DEFAULT_TIMEOUT


class SearchWorker(Worker):
    def __init__(self, words):
        self.words = words
        self.search_addr = SEARCH_PROXY_ADDR
    
    def before_run(self):
        r = random.randint(0, len(self.words) - 1)
        word = self.words[r]
        userId = random.randint(1, MAX_USERID)
        
        query = {"userId": userId, "keywords":[word]}
        self.params = {"query" : query,
                       "start" : 0,
                       "rows" : 20 }
        
    def _do_work(self, query, start, rows):
        q = "?userId=%d" % (int(query['userId'])) + "&keywords=%s" %  (quote(','.join(query['keywords']).encode('utf-8'))) 
        url = self.search_addr + q + "&start=%d&rows=%d" % (int(start), int(rows))
        
        start = time.time()
        try:
            _, hr = _curl(url, timeout = DEFAULT_TIMEOUT)
            hr = json.loads(hr)
            if hr['result'] != "ok":
                self.result = "failed", start, time.time() - start
            else:
                self.result = "ok", start, time.time() - start
        except Exception, e:
            self.result = "UnhandleError : %s" % (str(e)), start, time.time() - start
            
        
        
        