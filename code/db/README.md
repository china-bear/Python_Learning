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
. https://github.com/PyMySQL/mysqlclient

* install  
https://opensourcedbms.com/dbms/installing-mysql-5-7-on-centosredhatfedora/
https://segmentfault.com/a/1190000003049498

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

## python 3.6 mysqlclient 环境安装

1. 安装mysql8.0 客户端
yum list installed | grep mysql

yum -y remove mysql-community-release.noarch  mysql56u.x86_64 mysql56u-common.x86_64 mysqlclient16.x86_64
wget https://dev.mysql.com/get/mysql80-community-release-el6-4.noarch.rpm
rpm -ivh mysql80-community-release-el6-4.noarch.rpm
yum install -y mysql-community-client
yum install -y mysql-community-devel  
yum install -y mysql-community-shared
yum install -y mysql-community-libs-compat

或 安装mysql5.7 客户端
wget http://dev.mysql.com/get/mysql57-community-release-el6-7.noarch.rpm
rpm -ivh mysql57-community-release-el6-7.noarch.rpm
yum install -y mysql-community-client
yum install -y mysql-community-devel  
yum install -y mysql-community-shared
yum install -y mysql-community-libs-compat

或 如果安装包与本机冲突 强制安装，先官网下载RPM 包
rpm -ivh mysql-community-*.rpm  --force --nodeps

成功后 查看mysql  信息
> mysql_config --version
> mysql_config --libs


2. 安装Python mysqlclient
yum -y remove python34u.x86_64 python34u-devel.x86_64  python34u-libs.x86_64  python34u-pip.noarch python34u-setuptools.noarch

wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
sh Anaconda3-2020.07-Linux-x86_64.sh
vi  /home/hdp-ads-dw/.bashrc
> added by Anaconda3 installer  

export PATH="/usr/local/anaconda3/bin:$PATH"

/usr/local/anaconda3/bin/python3.8 /usr/local/anaconda3/bin/pip3 uninstall mysqlclient
/usr/local/anaconda3/bin/python3.8 /usr/local/anaconda3/bin/pip3 install mysqlclient
/usr/local/anaconda3/bin/python3.8 /usr/local/anaconda3/bin/pip3 install thrift
/usr/local/anaconda3/bin/python3.8 /usr/local/anaconda3/bin/pip3 install pyhive
/usr/local/anaconda3/bin/python3.8 /usr/local/anaconda3/bin/pip3 install emoji

> HiveServer1 需要增加下面模块

/usr/local/anaconda3/bin/python3.8 /usr/local/anaconda3/bin/pip3 install sasl
/usr/local/anaconda3/bin/python3.8 /usr/local/anaconda3/bin/pip3 install thrift_sasl

3.其它
> 验证安装包的位置 与  Python版本对应
import site; site.getsitepackages()
> how to get itThe resulting search path is accessible in the Python variable sys.path, which is obetained from a module named sys
> make sure your module be found First way is make sure your module in any path of above three.

import sys
sys.path

> Another way is put the module in the path you choice and then modify sys.path.

sys.path.append(r"/path")
Find the path where your module locate

> Find the path where your module locate

import module
module.__file__

4. centos换pip源  https://zhuanlan.zhihu.com/p/109939711
> 添加修改下面任何文件一个, pip 配置文件的优先级, 如果 pip 配置文件有很多个，则按照如下顺序读取配置：
> 读取站点范围（site-wide）的配置，这里指全局配置。
> 读取每个用户目录的配置。
> 读取特定于虚拟环境的配置。

/etc/pip.conf  ~/.config/pip/pip.conf ~/.pip/pip.conf

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
> 清华源  pypi 镜像每 5 分钟同步一次

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
> 阿里源

pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
> 腾讯源

pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple
> 豆瓣源

pip config set global.index-url http://pypi.douban.com/simple/