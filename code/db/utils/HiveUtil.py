# -*- coding: UTF-8 -*-

# ===============================================================================
# Hive工具类
# ===============================================================================
import time
import logging

from pyhive import hive
from config.cfg import cfg_hive_dict


class HiveUtil(object):
    def __init__(self, account='hdp-ads-dw'):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        if account not in cfg_hive_dict.keys():
            raise ('字典KEY错误:[cfg_hive_dict {_account} KEY NOT EXISTS.]'.format(_account=account))

        self.account = account

        try:
            self.conn = hive.Connection(**cfg_hive_dict[account])
            self.cursor = self.conn.cursor()
            logging.info('[HiveUtil] 成功连接 HiveServer2...')
        except BaseException as ex:
            logging.error('Connect to HiveServer2 failed [{_error_}]'.format(_error_=ex))
            raise ex

    # ===========================================================================
    # 执行查询s
    # ===========================================================================
    def execute(self, str_hql):
        start = time.time()
        self.cursor.execute(str_hql)
        end = time.time()

        logging.info('[hql] {_floatElapseTime} {_str_hql}'.format(
            _floatElapseTime=(end - start),
            _str_hql=str_hql
        ))

        for hiveLog in self.cursor.fetch_logs():
            print(hiveLog)

    # ===========================================================================
    # 取字段信息
    # ===========================================================================
    def get_schema(self):
        schema = self.cursor.description

        return [
            fieldSchema[0].split('.')[1] if fieldSchema[0].split('.').__len__() == 2 else fieldSchema[0].split('.')[
                0] for fieldSchema in schema]

    # ===========================================================================
    # 取全部数据
    # ===========================================================================
    def fetch_all(self, str_hql):
        try:
            self.execute(str_hql)
            schemas = self.get_schema()
            return [dict(zip(schemas, line)) for line in self.cursor.fetchall()], schemas
        except BaseException as e:
            logging.exception(e)
            logging.error('Execute sql failed [{_error_}]'.format(_error_=e))
            logging.error('[sql] {_str_hql}'.format(_str_hql=str_hql))
            return False

    # ===========================================================================
    # 取单条数据
    # ===========================================================================
    def fetch_one(self, str_hql):
        self.execute(str_hql)
        schemas = self.get_schema()
        return [dict(zip(schemas, line)) for line in self.cursor.fetchOne()]

    # ===========================================================================
    # 取多条数据
    # ===========================================================================
    def fetch_many(self, size):
        schemas = self.get_schema()
        return [dict(zip(schemas, line)) for line in self.cursor.fetchmany(size)]


if __name__ == '__main__':
    pass
