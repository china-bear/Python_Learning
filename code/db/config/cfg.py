# -*- coding: UTF-8 -*-
import MySQLdb
from pyhive import hive

# 测试环境
cfg_test = {'host': 'xxx', 'port': 4000, 'user': 'ad_stat', 'password': 'xxx', 'database': 'xxx', 'init_command': 'set names utf8', 'charset': 'utf8'}
# 开发环境
cfg_dev = {'host': 'xxx', 'port': 4000, 'user': 'ad_stat', 'password': 'xxx', 'database': 'xxx', 'init_command': 'set names utf8', 'charset': 'utf8'}
# 生产环境
cfg_prod = {'host': 'xxx', 'port': 4000, 'user': 'ad_stat', 'password': 'xxx', 'database': 'xxx', 'init_command': 'set names utf8', 'charset': 'utf8'}

# hive set
cfg_hive_set = {'mapreduce.job.queuename': 'root.bi', 'mapred.job.priority': 'VERY_HIGH', 'mapred.reduce.tasks': ' 1000', 'mapred.job.max.map.running': '1000',
                'mapred.job.max.reduce.running': '500', 'mapred.min.split.size': '104857600', 'mapred.max.split.size': '268435456', 'mapred.min.split.size.per.node': '134217728',
                'mapred.min.split.size.per.rack': '134217728', 'hive.exec.compress.output': 'true', 'mapreduce.output.fileoutputformat.compress': 'true',
                'mapred.output.compression.type': 'BLOCK', 'hive.groupby.skewindata': 'false', 'hive.auto.convert.join': 'false', 'hive.optimize.skewjoin': 'false'}

# hive hdp-ads-dw
cfg_dw = {'host': 'xxxx', 'port': 10000, 'scheme': 'hive2', 'username': 'hdp-xxx-dw', 'database': 'xx', 'auth': 'NOSASL', 'configuration': cfg_hive_set}
# hive hdp-ads-mba
cfg_mba = {'host': 'xxx', 'port': 10001, 'scheme': 'hive2', 'username': 'hdp-ads-xx', 'database': 'xx', 'auth': 'NOSASL', 'configuration': cfg_hive_set}

# mysql conf
cfg_mysql_dict = {'test': cfg_test, 'dev': cfg_dev, 'prod': cfg_prod}

# hive conf
cfg_hive_dict = {'hdp-ads-dw': cfg_dw, 'hdp-ads-mba': cfg_mba}

if __name__ == '__main__':

    for profile, conf in cfg_mysql_dict.items():
        try:
            conn = MySQLdb.connect(**conf)
        except BaseException as err:
            print('Profile {_profile} Connect to mysql server failed [{_error}]'.format(_profile=profile, _error=err))
        else:
            print('Profile {_profile} Connect to mysql server OK'.format(_profile=profile,))

    print('\n---------------------------------------------------------------\n')

    for account, conf in cfg_hive_dict.items():
        try:
            conn = hive.Connection(**conf)

        except BaseException as err:
            print('Account {_account} Connect to HiveServer2 failed [{_error}]'.format(_account=account, _error=err))
        else:
            print('Account {_account} Connect to HiveServer2 OK'.format(_account=account,))
