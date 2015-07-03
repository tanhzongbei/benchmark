#coding: utf8
# Author: fulingting@kingsoft.com
#
'''
Created on Feb 13, 2012

@author: fore
'''

import json
import time

from baseworker import Worker
from utils.urltool import openUrlCurl
import config as _conf


class SorlWorker(Worker):
    def __init__(self):
        inFile = file(_conf.SOLR_ORGIN_FILE_PATH, 'r')
        line = inFile.readline()
        self.__all_lines = []
        self.__bu_count = _conf.SOLR_BATCH_UPDATE_COUNT #batch update count
        self.__crr_line_NO = 0
        while line != None and len(line) > 0:
            self.__all_lines.append(line)
            line = inFile.readline()
    
    # task ==> "add":{"doc": {"id" : "TestDoc1", "title" : "test1"}}
    def _do_work(self, post_data):
        start_time = time.time()

        try:          
#            print post_data  
            headers = {'Content-type' : 'application/json'}
            data = openUrlCurl(_conf.SOLR_UPDATE_URL, post_data, headers)            #print path,parents
#            print data
            cost_time = time.time() - start_time
            self.result = 'ok', start_time, cost_time
        except Exception, e:
            cost_time = time.time() - start_time
            self.result =  'UnhandleError : %s' % str(e), start_time, cost_time
            
    
    def before_run(self):
        c = 0
        post_data = "{"
        while c < self.__bu_count and self.__crr_line_NO < len(self.__all_lines):
            line = self.__all_lines[self.__crr_line_NO];
            fileid,parent,userid,fsize,fver,opver,shareid,ctime,mtime,ftype,fname,fsha,stor,chksum = line.split('\t')

            item = {'fileid' : fileid,
                    'parent' : parent,
                    'fsize'  : fsize,
                    'shareid' : shareid,
                    'ctime' : int(time.mktime(time.strptime(ctime, '%Y-%m-%d %H:%M:%S'))),
                    'mtime' : int(time.mktime(time.strptime(mtime, '%Y-%m-%d %H:%M:%S'))),
                    'ftype' : ftype,
                    'fname' : fname}
            
            doc ={'doc' : item}
            add = "\"add\":" +  json.dumps(doc, ensure_ascii = False)
            
            self.__crr_line_NO += 1
            c += 1
            
            if c < self.__bu_count:
                post_data = post_data + add + ','
            else:
                post_data = post_data + add
               
            
        
        post_data = post_data + "}"
        self.params = {'post_data' : post_data}