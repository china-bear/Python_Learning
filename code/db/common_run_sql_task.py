# -*- coding: UTF-8 -*-
import sys
import os
import traceback
import time
import socket
import random
import getopt
import logging

from utils.Hive2Mysql import Hive2Mysql
from utils.UOdin import UOdin
from utils.UDone import UDone
from utils.UTime import UTime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    account = None
    package = None
    sql = None
    db = None
    table = None
    dimension = None
    day = None
    profile = None
    period = None

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help", "account=", "package=", "sql=", "db=", "table=", "dimension=", "day=", "profile=", "period="])
            for name, value in opts:
                if name == '--account':
                    account = value
                if name == '--package':
                    package = value
                if name == '--sql':
                    sql = value
                if name == '--db':
                    db = value
                if name == '--table':
                    table = value
                if name == '--dimension':
                    dimension = value
                if name == '--day':
                    day = value
                if name == '--profile':
                    profile = value
                if name == '--period':
                    period = value
        except getopt.error as msg:
            raise Usage(msg)

        logging.info('传入Task参数:[account={_account}, package={_package}, sql={_sql}, db={_db}, '
                     'table={_table}, dimension={_dimension} , day={_day}, profile={_profile}, period={_period}]'
                     .format(_account=account, _package=package, _sql=sql, _db=db,
                             _table=table, _dimension=dimension, _day=day, _profile=profile, _period=period))

        if not account:
            raise Usage('参数错误:[account={_account}]'.format(_account=account))

        if not package:
            raise Usage('参数错误:[package={_package}]'.format(_package=package))

        if not sql:
            raise Usage('参数错误:[sql={_sql}]'.format(_sql=sql))

        if not db:
            raise Usage('参数错误:[db={_db}]'.format(_db=db))

        if not table:
            raise Usage('参数错误:[table={_table}]'.format(_table=table))

        if not dimension:
            raise Usage('参数错误:[dimension={_dimension}]'.format(_dimension=dimension))

        if not profile:
            raise Usage('参数错误:[profile={_profile}]'.format(_profile=profile))

        if not day:
            import datetime
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            day = str(yesterday)
        else:
            if period == 'night':
                day = UTime.get_date_before_time(day, 1, format_type='%Y-%m-%d')

    except Usage as err:
        logging.error(err.msg)
        return 100

    try:
        # ==================================================
        # 启动调度任务
        # ==================================================

        basedir = os.getcwd()
        logging.info(f'Current root directory: {basedir}')

        bin_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(bin_dir)
        logging.info(f'Current working directory: {bin_dir}')

        status = None

        if day.__len__() == 10:
            day = UTime.stamp2time(UTime.time2stamp(day, "%Y-%m-%d"), "%Y-%m-%d")
        elif day.__len__() == 13:
            day = UTime.stamp2time(UTime.time2stamp(day, "%Y-%m-%d %H"), "%Y-%m-%d %H")

        logging.info('运行Task参数:[account={_account}, package={_package}, sql={_sql}, db={_db},'
                     'table={_table}, dimension={_dimension}, day={_day}, profile={_profile}, period={_period}]'
                     .format(_account=account, _package=package, _sql=sql, _db=db,
                             _table=table, _dimension=dimension, _day=day, _profile=profile, _period=period))

        try:
            time.sleep(random.randint(1, 60))
            hive2mysql = Hive2Mysql(account, package, sql, db, table, dimension, day, profile=profile)
            if profile == 'prod':
                UDone.delete('ad', 'mba', 'dw', "{_done}_{_day}".format(_done=sql, _day=day, ))
            else:
                UDone.delete('ad', 'mba', 'dw', "{_done}_{_profile}_{_day}".format(_done=sql, _profile=profile, _day=day, ))

            status = hive2mysql.run()
        except:
            logging.error(traceback.format_exc())

        if status:
            if profile == 'prod':
                UDone.create('ad', 'mba', 'dw', "{_done}_{_day}".format(
                    _done=sql,
                    _day=day,
                ))
            else:
                UDone.create('ad', 'mba', 'dw', "{_done}_{_profile}_{_day}".format(
                    _done=sql,
                    _profile=profile,
                    _day=day,
                ))

            return 0
        else:
            raise RuntimeError(f'{sql}_{profile}_{day} create done failed!')
    except Exception as err:
        logging.error(err)
        title = '[{_sql}][{_day}][{_profile}]'.format(
            _sql=sql,
            _day=day,
            _profile=profile,
        )

        app_content = """
        任务名称：{_sql} 
        执行时间：{_day} 
        执行模式：{_profile} 
        执行主机：{_hostname}
        执行结果：失败！
        """.format(
            _sql=sql,
            _day=day,
            _profile=profile,
            _hostname=socket.gethostname(),
        )

        content = """
        任务名称：{_sql} <br>
        执行时间：{_day} <br>
        执行模式：{_profile} <br>
        执行主机：{_hostname} <br>
        异常信息：{_error} <br>
        执行结果：失败！
        """.format(
            _sql=sql,
            _day=day,
            _profile=profile,
            _hostname=socket.gethostname(),
            _error=err,
        )

        # UOdin.send('mba_ba_task_alarm', title, app_content, content)
        logging.exception(err)
        return 1


if __name__ == '__main__':
    sys.exit(main())
