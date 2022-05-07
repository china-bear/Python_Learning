# -*- coding: UTF-8 -*-
# ===============================================================================
# Mysql 工具类
# ===============================================================================

import logging
import time
import MySQLdb
from config.cfg import cfg_mysql_dict

# ===========================================================================
# 将warning记录到异常
# ===========================================================================


class MysqlUtil(object):
    def __init__(self, profile='test'):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.profile = profile
        self.conRes = {}
        self.connect()

    def connect(self):
        try:
            conn = MySQLdb.connect(**cfg_mysql_dict[self.profile])
            self.conRes['conn'] = conn
            self.conRes['cursor'] = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        except BaseException as err:
            logging.error('Profile {_profile} Connect to mysql server failed [{_error_}]'.format(_profile=self.profile, _error_=err))
            raise

    # ===========================================================================
    # 执行
    #
    # execute("""INSERT INTO animals (name, species) VALUES ("Harry","Hamster")""")
    # execute("INSERT INTO animals (name, species) VALUES (%s, %s)",(name, species))
    # ===========================================================================
    def execute(self, str_sql, args=None):
        # self.connect(self.host, self.port, self.username, self.password, self.database)
        try:
            start = time.time()
            self.conRes['cursor'].execute(str_sql, args)
            self.conRes['conn'].commit()
            end = time.time()
            logging.info('[sql] {_floatElapseTime} {_strSql}'.format(
                _floatElapseTime=(end - start),
                _strSql=str_sql
            ))
            return True
        except BaseException as e:
            logging.exception(e)
            logging.error('Execute sql failed [{_error_}]'.format(_error_=e))
            logging.error('[sql] {_strSql}'.format(_strSql=str_sql))
            self.conRes['conn'].rollback()
            return False

    # ===========================================================================
    # 批量执行
    #
    # executemany("INSERT INTO animals (name, species) VALUES (%s,%s)", [('Rollo', 'Rat'),('Dudley', 'Dolphin')]
    # ===========================================================================
    def execute_many(self, str_sql, args=None):
        # self.connect(self.host, self.port, self.username, self.password, self.database)
        try:
            # start = time.time()
            self.conRes['cursor'].executemany(str_sql, args)
            self.conRes['conn'].commit()
            # end = time.time()
            # logging.info('[sql] {_floatElapseTime} {_strSql}'.format(
            #     _floatElapseTime=(end - start),
            #     _strSql=str_sql
            # ))
            return True
        except BaseException as e:
            logging.exception(e)
            logging.error('Execute sql failed [{_error_}]'.format(_error_=e.message))
            logging.error('[sql] {_strSql}'.format(_strSql=str_sql))
            self.conRes['conn'].rollback()
            return False

    # ===========================================================================
    # 执行
    #
    # execute("""INSERT INTO animals (name, species) VALUES ("Harry","Hamster")""")
    # execute("INSERT INTO animals (name, species) VALUES (%s, %s)",(name, species))
    # ===========================================================================
    def execute_many_sqls(self, str_sqls, args=None):
        # self.connect(self.host, self.port, self.username, self.password, self.database)
        try:
            self.conRes['conn'].autocommit(False)
            for str_sql in str_sqls:
                start = time.time()
                self.conRes['cursor'].execute(str_sql, args)
                end = time.time()
                logging.info('[sql] {_floatElapseTime} {_strSql}'.format(
                    _floatElapseTime=(end - start),
                    _strSql=str_sql
                ))
            self.conRes['conn'].commit()
            return True
        except BaseException as e:
            logging.exception(e)
            logging.error('Execute sql failed [{_error_}]'.format(_error_=e))
            logging.error('[sql] {_strSql}'.format(_strSql=str_sql))
            self.conRes['conn'].rollback()
            return False

    # ===========================================================================
    # 查询返回全部记录
    # ===========================================================================
    def fetch_all(self, str_sql):
        try:
            start = time.time()
            self.conRes['cursor'].execute(str_sql)
            end = time.time()
            logging.info('[sql] {_floatElapseTime} {_strSql}'.format(
                _floatElapseTime=(end - start),
                _strSql=str_sql
            ))
            return self.conRes['cursor'].fetchall()
        except BaseException as e:
            logging.exception(e)
            logging.error('Execute sql failed [{_error_}]'.format(_error_=e.message))
            logging.error('[sql] {_strSql}'.format(_strSql=str_sql))
            return False

    def close(self):
        self.conRes['cursor'].close()
        self.conRes['conn'].close()


if __name__ == '__main__':
    pass
