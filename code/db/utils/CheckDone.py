# -*- coding: UTF-8 -*-

# ===============================================================================
# 检查Hive表是否有数据
# ===============================================================================
import getopt
import logging
import socket
import sys
import time

from utils.UDone import UDone
from utils.UOdin import UOdin
from utils.UTime import UTime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class CheckDoneException(Exception):
    def __init__(self, msg):
        self.msg = msg


class CheckDone(object):
    def __init__(self, _host, _group, _project, _job, _done, _date):
        self.host = _host
        self.group = _group
        self.project = _project
        self.job = _job
        self.done = _done
        self.date = _date

    def check(self):
        counter = 1
        status = '1'

        while status != '0' and counter <= 5:
            status = UDone.check(self.host, self.group, self.project, self.job, self.done, self.date)

            if status != '0':
                counter = counter + 1
                time.sleep(60)

        if status != '0':
            raise CheckDoneException('Check done is not exists.')


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    host = None
    group = None
    project = None
    job = None
    done = None
    date = None
    period = None
    deadline = "00:00:00"

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help", "host=", "group=", "project=", "job=", "done=", "date=", "period=", "deadline="])
            for name, value in opts:
                logging.info('{_name}={_value}'.format(_name=name, _value=value))
                if name == '--host':
                    host = value
                if name == '--group':
                    group = value
                if name == '--project':
                    project = value
                if name == '--job':
                    job = value
                if name == '--done':
                    done = value
                if name == '--date':
                    date = value
                if name == '--period':
                    period = value
                if name == '--deadline':
                    deadline = value
        except getopt.error as msg:
            raise Usage(msg)

        if not date:
            import datetime
            today = datetime.date.today()
            oneday = datetime.timedelta(days=1)
            yesterday = today - oneday
            date = str(yesterday)

        if date.__len__() == 13:
            date = UTime.stamp2time(UTime.time2stamp(date, "%Y-%m-%d %H"), "%Y-%m-%d-%H")
        else:
            if period == 'night':
                date = UTime.get_date_before_time(date, 1, format_type='%Y-%m-%d')

        logging.info('传入Task参数:[host={_host},group={_group},project={_project},job={_job},done={_done},date={_date},period={_period},deadline={_deadline}]'.format(
            _host=host,
            _group=group,
            _project=project,
            _job=job,
            _done=done,
            _date=date,
            _period=period,
            _deadline=deadline,
        ))

        chd = CheckDone(host, group, project, job, done, date)

        chd.check()

    except Usage as err:
        logging.error(err.msg)
        return 1

    except CheckDoneException:
        if time.strftime('%H:%M:%S') >= deadline:
            title = '[checkdone][{_date}][{_done}]'.format(
                _date=date,
                _done=done,
            )

            app_content = """
执行时间：{_date} 
执行主机：{_hostname}
检查参数：[host={_host},group={_group},project={_project},job={_job},done={_done},date={_date},period={_period},deadline={_deadline}]
执行结果：检查失败！
            """.format(
                _done=done,
                _date=date,
                _hostname=socket.gethostname(),
                _host=host,
                _group=group,
                _project=project,
                _job=job,
                _period=period,
                _deadline=deadline,
            )

            content = """
执行时间：{_date} <br>
执行主机：{_hostname} <br>
检查参数：[host={_host},group={_group},project={_project},job={_job},done={_done},date={_date},period={_period},deadline={_deadline}] <br>
执行结果：检查失败！
            """.format(
                _done=done,
                _date=date,
                _hostname=socket.gethostname(),
                _host=host,
                _group=group,
                _project=project,
                _job=job,
                _period=period,
                _deadline=deadline,
            )

            UOdin.send('mba_check_done_alarm', title, app_content, content)
        else:
            print('当前时间[{_date_}] < [{_deadline_}]，暂时不发送报警信息！'.format(
                _date_=time.strftime('%H:%M:%S'),
                _deadline_=deadline,
            ))

        return 1


if __name__ == '__main__':
    sys.exit(main())
