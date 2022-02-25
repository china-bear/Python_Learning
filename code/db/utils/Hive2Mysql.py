# -*- coding: UTF-8 -*-

import os.path
import re
from utils.MysqlUtil import MysqlUtil
from utils.HiveUtil import HiveUtil


class Hive2Mysql:
    def __init__(self, account, package, sql, db, table, dimension, str_date, profile='test'):
        self.account = account
        self.package = package
        self.sql = sql
        self.db = db
        self.table = table
        self.dimension = dimension
        self.str_date = str_date
        self.profile = profile
        self.str_hql = self.sql_from_file()

    def run(self):
        # time.sleep(random.randint(1, 10))

        list_dict_data, schemas = self.__get_data()
        if not list_dict_data:
            raise Exception("__getData Error OR data empty")

        dict_sql = self.__get_sql(list_dict_data, schemas)

        if not self.__clean_data():
            raise Exception("__cleanData Error")

        if not self.__write_data(dict_sql):
            raise Exception("__write Error")

        return True

    # ===========================================================================
    # 取数据
    # ===========================================================================
    def __get_data(self):
        ins_hive = HiveUtil(account=self.account)
        str_hql = f'set mapred.job.name=Spark:[SHBT-{self.account}][{self.table}][{self.str_date}]'
        ins_hive.execute(str_hql)
        return ins_hive.fetch_all(self.str_hql)

    # ===========================================================================
    # 生成Sql格式
    # ===========================================================================
    def __get_sql(self, list_dict_data, schemas):
        list_columns = ['date', 'dimension'] + schemas
        columns = ', '.join(list_columns)
        values = '%s, ' * (len(list_columns) - 1) + '%s'
        ins_sql = f'insert into `{self.db}`.`{self.table}` ({columns}) VALUES ({values})'
        print(ins_sql)
        ins_sql_data = []
        for dict_line in list_dict_data:
            line = []
            for item in list_columns:
                if item == 'date':
                    line.append(self.str_date)
                elif item == 'dimension':
                    line.append(self.dimension)
                else:
                    line.append(dict_line[item])

            ins_sql_data.append(tuple(line))

        return {'sql': ins_sql, 'data': ins_sql_data}

    # ===========================================================================
    # 清理旧数据
    # ===========================================================================
    def __clean_data(self):
        del_sql = """
        delete from {_table} where date='{_date}' and dimension = '{_dimension}'
        """.format(
            _table=self.table,
            _dimension=self.dimension,
            _date=self.str_date,
        )
        ins_mysql = MysqlUtil(profile=self.profile)
        return ins_mysql.execute(del_sql)

    # ===========================================================================
    # 数据写入
    # ===========================================================================
    def __write_data(self, dict_sql):
        ins_mysql = MysqlUtil(profile=self.profile)
        count = len(dict_sql['data'])
        batch_size = count if count <= 1000 else 1000
        result = True
        for i in range(0, count, batch_size):
            if not ins_mysql.execute_many(dict_sql['sql'], dict_sql['data'][i:i + batch_size]):
                print("写入{_start}-{_end}条失败,开启逐条写入模式。".format(_start=i, _end=i + batch_size))
                for j in range(i, i + batch_size, 1):
                    if not ins_mysql.execute_many(dict_sql['sql'], dict_sql['data'][j:j + 1]):
                        print(str(dict_sql['data'][j:j + 1]))
                        # print(str(dict_sql['data'][j:j + 1]).decode("string_escape"))
                result = False
            else:
                print("写入{_start}-{_end}条成功".format(_start=i, _end=i + batch_size))
        return result

    def sql_from_file(self):
        f = './' + self.package.replace(r'.', r'/') + '/' + self.sql + '.sql'
        print('sql file: ' + os.getcwd() + f)
        if not os.path.exists(f):
            raise ('参数错误:[SQL FILE {_file} NOT EXISTS.]'.format(_file=f))
        with open(f, 'r', encoding='utf8') as f_handler:
            str_hql = re.sub(r"(\r\n|\n)*;$", "", f_handler.read().rstrip().format(day=self.str_date))
        return str_hql


if __name__ == 'main':
    pass
