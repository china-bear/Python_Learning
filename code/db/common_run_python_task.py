# -*- coding: UTF-8 -*-
import sys
import time
import socket
import random
import getopt
import logging
import importlib

from utils.UDone import UDone
from utils.UOdin import UOdin
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
    module = None
    date = None
    profile = None
    period = None

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help", "account=", "package=", "module=", "date=", "profile=", "period="])
            for name, value in opts:
                if name == '--account':
                    account = value
                if name == '--package':
                    package = value
                if name == '--module':
                    module = value
                if name == '--date':
                    date = value
                if name == '--profile':
                    profile = value
                if name == '--period':
                    period = value
        except getopt.error as msg:
            raise Usage(msg)

        logging.info('传入Task参数:[account={_account}, package={_package}, module={_module}, date={_date}, profile={_profile}, period={_period}]'
                     .format(_account=account, _package=package, _module=module, _date=date, _profile=profile, _period=period))

        if not account:
            raise Usage('参数错误:[account={_account}]'.format(_account=account))

        if not package:
            raise Usage('参数错误:[package={_package}]'.format(_package=package))

        if not module:
            raise Usage('参数错误:[module={_module}]'.format(_module=module))

        if not profile:
            raise Usage('参数错误:[profile={_profile}]'.format(_profile=profile))

        if not date:
            import datetime
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            date = str(yesterday)
        else:
            if period == 'night':
                date = UTime.get_date_before_time(date, 1, format_type='%Y-%m-%d')

    except Usage as err:
        logging.error(err.msg)
        return 100

    try:
        # ==================================================
        # 启动调度任务
        # ==================================================
        fun = None

        if date.__len__() == 10:
            date = UTime.stamp2time(UTime.time2stamp(date, "%Y-%m-%d"), "%Y-%m-%d")
        elif date.__len__() == 13:
            date = UTime.stamp2time(UTime.time2stamp(date, "%Y-%m-%d %H"), "%Y-%m-%d %H")

        logging.info('运行Task参数:[account={_account}, package={_package}, module={_module}, date={_date}, profile={_profile}, '
                     'period={_period}]'.format(_account=account, _package=package, _module=module, _date=date,
                                                _profile=profile, _period=period))
        try:
            fun = importlib.import_module(package + '.' + module)
        except ModuleNotFoundError as ex:
            logging.error(ex.msg)
            raise ModuleNotFoundError("Can not found Module:[module={_module}]".format(_module=module))
        else:
            time.sleep(random.randint(1, 60))
            UDone.delete('ad', 'mba', 'dw', "{_done}_{_date}".format(_done=module, _date=date,))
            status = fun.run(date, account=account, profile=profile)

        if status:
            UDone.create('ad', 'mba', 'dw', "{_done}_{_date}".format(
                _done=module,
                _date=date,
            ))

            return 0
        else:
            raise RuntimeError("{_done}_{_date}  create done failed!".format(_done=module, _date=date,))
    except BaseException as err:
        title = '[{_module}][{_date}][{_profile}]'.format(
            _module=module,
            _date=date,
            _profile=profile,
        )

        app_content = """
        任务名称：{_module} 
        执行时间：{_date} 
        执行模式：{_profile} 
        执行主机：{_hostname}
        执行结果：失败！
        """.format(
            _module=module,
            _date=date,
            _profile=profile,
            _hostname=socket.gethostname(),
        )

        content = """
        任务名称：{_module} <br>
        执行时间：{_date} <br>
        执行模式：{_profile} <br>
        执行主机：{_hostname} <br>
        异常信息：{_error} <br>
        执行结果：失败！
        """.format(
            _module=module,
            _date=date,
            _profile=profile,
            _hostname=socket.gethostname(),
            _error=err,
        )

        UOdin.send('mba_ba_task_alarm', title, app_content, content)
        logging.exception(err)
        return 1


if __name__ == '__main__':
    sys.exit(main())
