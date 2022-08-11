# -*- coding: UTF-8 -*-
import sys
import os
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
    day = None
    profile = None
    period = None

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help", "account=", "package=", "module=", "day=", "profile=", "period="])
            for name, value in opts:
                if name == '--account':
                    account = value
                if name == '--package':
                    package = value
                if name == '--module':
                    module = value
                if name == '--day':
                    day = value
                if name == '--profile':
                    profile = value
                if name == '--period':
                    period = value
        except getopt.error as msg:
            raise Usage(msg)

        logging.info('传入Task参数:[account={_account}, package={_package}, module={_module}, day={_day}, profile={_profile}, period={_period}]'
                     .format(_account=account, _package=package, _module=module, _day=day, _profile=profile, _period=period))

        if not account:
            raise Usage('参数错误:[account={_account}]'.format(_account=account))

        if not package:
            raise Usage('参数错误:[package={_package}]'.format(_package=package))

        if not module:
            raise Usage('参数错误:[module={_module}]'.format(_module=module))

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
        ## python3.8  common_run_python_task.py  --account=hdp_ads_dw --package=task.show.overall  --module=ba_zs_overall_analysis_bl_search --day=2022-02-22 --profile=dev
        # ==================================================
        basedir = os.getcwd()
        logging.info(f'Current root directory: {basedir}')

        bin_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(bin_dir)
        logging.info(f'Current working directory: {bin_dir}')

        fun = None

        if day.__len__() == 10:
            day = UTime.stamp2time(UTime.time2stamp(day, "%Y-%m-%d"), "%Y-%m-%d")
        elif day.__len__() == 13:
            day = UTime.stamp2time(UTime.time2stamp(day, "%Y-%m-%d %H"), "%Y-%m-%d %H")

        logging.info('运行Task参数:[account={_account}, package={_package}, module={_module}, day={_day}, profile={_profile}, '
                     'period={_period}]'.format(_account=account, _package=package, _module=module, _day=day,
                                                _profile=profile, _period=period))
        try:
            fun = importlib.import_module(package + '.' + module)
        except ModuleNotFoundError as ex:
            logging.error(ex.msg)
            raise ModuleNotFoundError("Can not found Module:[module={_module}]".format(_module=module))
        else:
            time.sleep(random.randint(1, 60))
            UDone.delete('ad', 'mba', 'dw', "{_done}_{_day}".format(_done=module, _day=day, ))
            status = fun.run(account=account, package=package, module=module, day=day, profile=profile)

        if status:
            if profile == 'prod':
                UDone.create('ad', 'mba', 'dw', "{_done}_{_day}".format(
                    _done=module,
                    _day=day,
                ))
            else:
                UDone.create('ad', 'mba', 'dw', "{_done}_{_profile}_{_day}".format(
                    _done=module,
                    _profile=profile,
                    _day=day,
                ))

            return 0
        else:
            raise RuntimeError("{_done}_{_day} {_profile} create done failed!".format(_done=module, _profile=profile, _day=day, ))
    except BaseException as err:
        title = '[{_module}][{_day}][{_profile}]'.format(
            _module=module,
            _day=day,
            _profile=profile,
        )

        app_content = """
        任务名称：{_module} 
        执行时间：{_day} 
        执行模式：{_profile} 
        执行主机：{_hostname}
        执行结果：失败！
        """.format(
            _module=module,
            _day=day,
            _profile=profile,
            _hostname=socket.gethostname(),
        )

        content = """
        任务名称：{_module} <br>
        执行时间：{_day} <br>
        执行模式：{_profile} <br>
        执行主机：{_hostname} <br>
        异常信息：{_error} <br>
        执行结果：失败！
        """.format(
            _module=module,
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
