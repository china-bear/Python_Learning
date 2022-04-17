# -*- coding: UTF-8 -*-
import sys
import os

import getopt
import logging

from utils.UTime import UTime
import os.path
from datetime import timedelta
from datetime import datetime
from utils.MysqlUtil import MysqlUtil

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    start_date = None
    end_date = None
    interval = None
    profile = None
    
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help", "start_date=", "end_date=", "interval=", "profile="])
            for name, value in opts:
                if name == '--start_date':
                    start_date = value
                if name == '--end_date':
                    end_date = value
                if name == '--interval':
                    interval = int(value)
                if name == '--profile':
                    profile = value
        except getopt.error as msg:
            raise Usage(msg)

        logging.info('传入Task参数:[start_date={_start_date}, end_date={_end_date}, interval={_interval}, profile={_profile}'
                     .format(_start_date=start_date, _end_date=end_date, _interval=interval, _profile=profile))

        if not start_date:
            raise Usage('参数错误:[start_date={_start_date}]'.format(_start_date=start_date))

        if not end_date:
            raise Usage('参数错误:[end_date={_end_date}]'.format(_end_date=end_date))

        if not interval:
            raise Usage('参数错误:[interval={_interval}]'.format(_interval=interval))

        if not profile:
            raise Usage('参数错误:[profile={_profile}]'.format(_profile=profile))

    except Usage as err:
        logging.error(err.msg)
        return 100

    try:
        # ==================================================
        # 执行sql任务
        # python3.8  common_run_task.py --start_date='2022-04-13' --end_date=2022-04-16 --interval=5 --profile=prod
        # ==================================================
        basedir = os.getcwd()
        logging.info(f'Current root directory: {basedir}')

        bin_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(bin_dir)
        logging.info(f'Current working directory: {bin_dir}')

        if start_date.__len__() == 10:
            start_date = UTime.stamp2time(UTime.time2stamp(start_date, "%Y-%m-%d"), "%Y-%m-%d")
        elif start_date.__len__() == 13:
            start_date = UTime.stamp2time(UTime.time2stamp(start_date, "%Y-%m-%d %H"), "%Y-%m-%d %H")

        if end_date.__len__() == 10:
            end_date = UTime.stamp2time(UTime.time2stamp(end_date, "%Y-%m-%d"), "%Y-%m-%d")
        elif end_date.__len__() == 13:
            start_date = UTime.stamp2time(UTime.time2stamp(end_date, "%Y-%m-%d %H"), "%Y-%m-%d %H")

        logging.info('运行Task参数:[start_date={_start_date}, end_date={_end_date}, interval={_interval}, '
                     'profile={_profile},'.format(_start_date=start_date, _end_date=end_date, _interval=interval, _profile=profile))

        mysql_conn = MysqlUtil(profile=profile)
        while start_date <= end_date:
            delta_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=interval + 1)).strftime("%Y-%m-%d")
            if delta_date > end_date:
                delta_date = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

            sql_str = """
update xxx 
set product_type_name='信息流'
where date>='{_start_date}' and date<'{_delta_date}' and `dimension` = 'space' 
 and business_type_name = '信息流';
                """.format(_start_date=start_date, _delta_date=delta_date,)

            mysql_conn.execute(sql_str)
            start_date = delta_date
        else:
            logging.info('执行结果：更新成功！')
            return 0
    except BaseException as err:
        logging.info('执行结果：更新失败！')
        logging.exception(err)
        return 1


if __name__ == '__main__':
    sys.exit(main())
