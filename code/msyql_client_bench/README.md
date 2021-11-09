## There are currently a few options for using Python 3 with mysql
> 生产环境还是推荐mysqlclient, 也就是Python3版本的MySQLdb

1. mysql-connector-python
. Officially supported by Oracle
. Pure python
. A little slow
. Not compatible with MySQLdb

2. pymysql
. Pure python
. Faster than mysql-connector
. Almost completely compatible with MySQLdb, after calling pymysql.install_as_MySQLdb()

3. cymysql
. fork of pymysql with optional C speedups

4. mysqlclient
. Django's recommended library.
. Friendly fork of the original MySQLdb, hopes to merge back some day
. The fastest implementation, as it is C based.
. The most compatible with MySQLdb, as it is a fork
. Debian and Ubuntu use it to provide both python-mysqldb andpython3-mysqldb packages.



[mysql客户端python下性能比较](https://cloud.tencent.com/developer/article/1399154)