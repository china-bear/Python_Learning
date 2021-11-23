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


wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
tar -xzf Python-3.7.9.tgz
sudo ./configure prefix=/usr/local/python3
sudo mkdir /usr/local/python3
sudo make 
sudo make install
sudo ln -s /usr/local/python3/bin/python3 /usr/bin/python3
sudo ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
sudo pip3 install thrift -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
sudo pip3 install sasl -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
sudo pip3 install thrift-sasl -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
sudo pip3 install pyhive -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
sudo pip3 install mysqlclient
sudo pip3 install pymysql -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
sudo pip3 install sshtunnel -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
sudo pip3 install virtualenv -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
sudo pip3 install bpython -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
sudo ln -s /usr/local/python3/bin/virtualenv /usr/bin/virtualenv
sudo ln -s /usr/local/python3/bin/bpython /usr/bin/bpython
