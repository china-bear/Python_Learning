# -*- coding: UTF-8 -*-
# /usr/local/bin/python2.7 /opt/mba-report/mba-report/PRouteAzkaban.py --job=ba_zs_overall_analysis_all --date=2018-10-17 --debug=1 --period=day
import random
import time

from utils.MysqlUtil import MysqlUtil
from utils.HiveUtil import HiveUtil


# python3.8  common_run_python_task.py  --account=hdp_ads_dw --package=task.show.overall  --module=ba_zs_overall_analysis_bl_search --day=2022-02-22 --profile=dev
def run(account, package, module, day, profile='test'):
    task = AnalysisTask(account, package, module, day, profile)
    return task.exec_task()


class AnalysisTask:
    def __init__(self, account, package, module, day, profile):
        self.table = 'ba_zs_overall_analysis'
        self.dimension = 'bl'
        self.business_line_code = 'BL_001'

        self.account = account
        self.package = package
        self.module = module
        self.day = day
        self.profile = profile

    def exec_task(self):
        time.sleep(random.randint(1, 10))

        list_dict_data = self.__get_data()
        if not list_dict_data:
            raise Exception("__getData Error")

        dict_sql = self.__get_sql(list_dict_data)

        if not self.__clean_data():
            raise Exception("__cleanData Error")

        if not self.__write_data(dict_sql):
            raise Exception("__write Error")

        return True

    # ===========================================================================
    # 取数据
    # ===========================================================================
    def __get_data(self):
        ins_mysql = MysqlUtil(profile=self.profile)

        list_dict_data = ins_mysql.fetch_all("""
SELECT date
  ,dimension
  ,'BL_001' AS business_line_code
  ,'搜索' AS business_line_name
  ,terminal_code
  ,terminal_name
  ,ad_pv
  ,ad_cost AS internal_cost
FROM ba_search_traffic_analysis 
WHERE date = '{_day}' 
  AND dimension = 'terminal';
        """.format(_day=self.day))

        return list_dict_data

    # ===========================================================================
    # 生成Sql格式
    # ===========================================================================
    def __get_sql(self, list_dict_data):
        ins_sql = """
INSERT INTO `mba_app`.`{_table}` (
  date,
  dimension,
  business_line_code,
  business_line_name,
  terminal_code,
  terminal_name,
  ad_pv,
  internal_cost
) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """.format(_table=self.table, )

        ins_sql_data = []
        for i in list_dict_data:
            ins_sql_data.append((
                self.day,
                self.dimension,
                i['business_line_code'],
                i['business_line_name'],
                i['terminal_code'],
                i['terminal_name'],
                i['ad_pv'],
                i['internal_cost'],
            ))

        return {'sql': ins_sql, 'data': ins_sql_data}

    # ===========================================================================
    # 清理旧数据
    # ===========================================================================
    def __clean_data(self):
        del_sql = """
delete from {_table} where date='{_day}' and dimension = '{_dimension}' and business_line_code in ('{_business_line_code}')
        """.format(
            _table=self.table,
            _dimension=self.dimension,
            _day=self.day,
            _business_line_code=self.business_line_code,
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


if __name__ == 'main':
    pass
