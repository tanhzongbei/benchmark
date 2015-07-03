#coding:utf8 
#__author__ = 'xiaobei'
#__time__= '7/2/15'

import sys
reload(sys)
sys.path.append('../')

import functools
from baseworker import Worker
import config as _conf
from kputils.urltools import curl
import ujson
import random
import time

def db_executor_retry(func):
    """retry once when lost connection error raise."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            res = func(self, *args, **kwargs)
            if not res:
                res = func(self, *args, **kwargs)
        except Exception as e:
            raise

        return res

    return wrapper

QUERY_URL = 'http://speedup-xlmc.xunlei.com/cdnmanager/querycdn'

gcid = [
'0063EEC589F2EC8A2056AFDCE4950FF1D7F8916D',
'0064C56A71445A4F1EFF43CD6949BCE65C4CFA34',
'0068012B73E8AE260C4895007490B7E99A4EF13D',
'00693FA4B148A5D417B6E93110C197BCD4950EAC',
'006A22935E199A859365DD5CDF0C74E95792E513',
'006CF8EE26711BDA812FBF417CE7D6AF419E3710',
'006DCD6C71AFE90A2622E36E87DACB15443AC9ED',
'006E9BA5B24DA4CE014B5BF93437B5E449543343',
'006E9D3A3ED0D49854962114070CE89B0628EAE8',
'006EDEC337C7435EDC08BE81D7CE4E5ACB1CDC61',
'007041ECEC2AC911D8BFE671792C18C7B88C2B28',
'0072C452361F6B6F1DA019C62A123BF8E767825A',
'0079150B6942C12977D91391F945DDCB3FE30381',
'007948C73B3411E1B68E19FA2974D6A853C2A508',
'007AC0657C0A6BCB2E2836674A2ABE50AD1432FE',
'007B38B2A0026C7AC54F59054780080D18487ED7',
'007BE0C8CA4A3B02F32A67AE70A7B03FBF648158',
'007D092B79646054392E1097DAC85DEED9804763',
'007D68235F657E20CE64EEC769674AF9F9E888FE',
'007D8F3E3880DC8E138A8EA34E0D2E698523F66C',
'007EFA0B7263472FA5627308F47EDFE11DD0DED2',
'007FC2B95A55CDEA3B27E143CB1073B8DA7F9E5E',
'007FEBD896491A24160752C1B37CF88F1EDDE23F',
'00808242388E1D063251C04FC89DF0DEDF8152B2',
'008118872F5AF3717A19F94690B3D50C21F2B9B8',
'0083967825A82025897F7B75D485C0BED049A8C5',
'0087B7A011F4E748EA50265229D0D8EFF0285D64',
]

class CDNManagerWorker(Worker):
    def __init__(self):
        self.result = False, 0, _conf.WORKER_UNHANDLE_ERROR

    def _do_work(self, timeout = 3):
        start_time = time.time()
        post = {'gcid' : gcid[random.randint(0,26)], 'peer_capability' : 1}
        code, res = curl.openurl(QUERY_URL, ujson.dumps(post), {'Content-Type': 'application/json'})
        cost_time = time.time() - start_time
        if code != 298 or not res:
            self.result = 'UnhandleError : cdnmanager querycdn %s' ,  start_time, cost_time

        self.result = 'ok', start_time, cost_time

if __name__ == '__main__':
    t = CDNManagerWorker()
    t._do_work()