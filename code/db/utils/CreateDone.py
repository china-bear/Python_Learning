# -*- coding: UTF-8 -*-

# ===============================================================================
# 创建Done标记
# ===============================================================================
import getopt
import logging
import sys

from utils.UDone import UDone

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    group = None
    project = None
    job = None
    done = None
    date = None

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help", "group=", "project=", "job=", "done=", "date="])
            for name, value in opts:
                logging.info('{_name}={_value}'.format(_name=name, _value=value))
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

            if not date:
                import datetime
                today = datetime.date.today()
                oneday = datetime.timedelta(days=1)
                yesterday = today - oneday
                date = str(yesterday)

            logging.info('传入Task参数:[group={_group},project={_project},job={_job},done={_done},date={_date}]'.format(
                _group=group,
                _project=project,
                _job=job,
                _done=done,
                _date=date,
            ))
        except getopt.error as msg:
            raise Usage(msg)

        UDone.create(group, project, job, "{_done}_{_date}".format(_done=done, _date=date))

    except Usage as err:
        logging.error(err.msg)
        return 1


if __name__ == '__main__':
    sys.exit(main())
