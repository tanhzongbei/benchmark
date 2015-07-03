#coding:utf8
# Author: Ilcwd@2011/12/17

import MySQLdb as m
import commands
import config as _conf

db = m.connect(host=_conf.MYSQL_HOST,
               port=_conf.MYSQL_PORT,
               user=_conf.MYSQL_USER,
               passwd=_conf.MYSQL_PASSWORD,
               db=_conf.MYSQL_DB)

cur = db.cursor()


def crawl_fileid():
    print 'INFO: crawl_fileid :', 
    SQL = "SELECT fileId FROM `%s`;" % _conf.MYSQL_TABLE    
    
    cur.execute(SQL)
    
    f = open(_conf.FILE_ID_PATH, 'w')
    
    for item in cur.fetchall():
        f.write(str(item[0])+'\n')
    
    f.close()
    
    print commands.getoutput('wc -l %s' % _conf.FILE_ID_PATH)
    print cur.fetchall()
    while cur.nextset():
        print cur.fetchall()
    
    
def create_bu_procedure():
    print 'INFO: create_procedure :', 
    SQL =  '''

DROP PROCEDURE IF EXISTS `%s` ;
CREATE PROCEDURE `%s`(
 in fid bigint(20)
)
begin
declare p bigint(20) ;
declare c int;
set @p=fid, @c=100;
/*select @c, @p;*/
while @p <> 0 and @c<>0 do
  select parent into @p from %s where fileid = @p;
  set @c = @c-1;
  select @p;
end while;
end ;


''' % (_conf.MYSQL_BU_PROCEDURE, _conf.MYSQL_BU_PROCEDURE,  _conf.MYSQL_TABLE)
    #print SQL
    print cur.execute(SQL)
    
    print cur.fetchall()
    while cur.nextset():
        print cur.fetchall()
    
    
def create_td_procedure():
    print 'INFO: create_procedure :', 
    SQL =  '''
DROP PROCEDURE IF EXISTS `%s`;
create procedure `%s` (
    in pcount int,
    in hparent bigint(20),
    in md5slice varchar(4096)
)
begin
    declare prtid bigint(20);
    declare idx int;

    set @prtid=hparent, @idx=1;

    while (@idx < pcount*16) and (@prtid is not NULL) do
        select fileid into @prtid from `%s`
        where fnamesha=unhex(concat(lpad(hex(@prtid), 16, 0), substring(md5slice, @idx, 16)));
        set @idx=@idx+16;        

        select @prtid;
    end while;
end ;
'''  % (_conf.MYSQL_TD_PROCEDURE, _conf.MYSQL_TD_PROCEDURE,  _conf.MYSQL_TABLE)
    #print SQL
    print cur.execute(SQL)
    
    print cur.fetchall()
    while cur.nextset():
        print cur.fetchall()


def procSql(fileId):
    parents = []
    cur.callproc(_conf.MYSQL_PROCEDURE, (int(fileId), ))
    #print fileId
    res = cur.fetchall()
    if res:
        parents.append(res[0][0])
        while cur.nextset():
            res = cur.fetchall()
            if res:
                parents.append(res[0][0])
            
    return parents


def main():
    create_bu_procedure()
    create_td_procedure()
    #crawl_fileid()

if __name__ == '__main__':
    main()