#coding:utf8
# Author: Ilcwd@2011/09/05

## 测试mysql 存储过程
MYSQL_HOST = '192.168.10.200'
MYSQL_PORT = 3306
MYSQL_USER = 'python'
MYSQL_PASSWORD = 'python'
MYSQL_DB = 'docsvr0'
MYSQL_TABLE = 'xfile_0'

MYSQL_BU_PROCEDURE = 'find_parents'
MYSQL_TD_PROCEDURE = 'find_fileids'

FILE_ID_PATH = './fileid'
TOP_DOWN_TEST_CASES = './testcases'

## 测试mysql 存储过程 

DEFAULT_HOST = '192.168.10.200'
DEFAULT_FUNCTION = 'user'
DEFAULT_REQUEST_NUMBER = 500
DEFAULT_CONCURRENCY = 4
DEFAULT_TIMEOUT = 8


CONSUMER_KEY = '79a7578ce6cf4a6fa27dbf30c6324df4'
CONSUMER_SECRET = 'c7ed87c12e784e48983e3bcdc6889dad'

#CONSUMER_KEY = '6ea5e82a238b494ba1c47b8b9ddfad90'
#CONSUMER_SECRET = '2fccd17475b54c21bf6c64e564685ee6'


KUAIPAN_USER = 'ma3@126.com'
KUAIPAN_PASS = '123456'


WORKER_TIMEOUT = -1
WORKER_UNHANDLE_ERROR = -2
WORKER_NOT_START = -3
WORKER_FINISHED = -4

ANALYSER_FRESH_INTERVAL = 1

# 测试solr的更新速度
SOLR_UPDATE_URL = "http://127.0.0.1:10000/solr/core/update/json"
SOLR_BATCH_UPDATE_COUNT = 1
SOLR_ORGIN_FILE_PATH = "/home/fore/Downloads/apache-solr-3.5.0/core-server/exampledocs/solr_meter_docs_tab"

#搜索代理服务器
SEARCH_PROXY_ADDR = "http://localhost:11111/"
MAX_USERID  = 10000

# loginsvr
LOGINSVR_URI = "http://114.112.66.65"
LOGINSVR_REGISTER_URI = "/loginsvr/register"
LOGINSVR_LOGIN_URI = "/loginsvr/login"
LOGINSVR_GETUSERINFO_URI = "/loginsvr/getUserInfoById"
LOGINSVR_QUERYSIDINFO_URI = "/loginsvr/querySidInfo"

DOCSVR_REGISTER_URL = "http://192.168.10.201/xsvr/adminRegisterEmail"
DOCSVR_LOGIN_URL = "http://192.168.10.201/xsvr/login"

SUPER_USERNAME = "test@kingsoft.com"
SUPER_PWD = "123456"

