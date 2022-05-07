# -*- coding: UTF-8 -*-

# ===============================================================================
# 时间类
# ===============================================================================
import calendar
import time

import datetime

import math


class UTime(object):

    # ===========================================================================
    # 微秒
    # ===========================================================================
    @staticmethod
    def microtime(bool_return_float=True):
        if bool_return_float:
            return time.time()
        else:
            # 分别返回整数和小数
            return "%f %d" % math.modf(time.time())

    # ===========================================================================
    # 日期转时间戳
    # ===========================================================================
    @staticmethod
    def time2stamp(time_str, format_type='%Y-%m-%d %H:%M:%S'):
        return time.mktime(time.strptime(time_str, format_type))

    # ===========================================================================
    # 时间戳转日期 stamp为整型
    # ===========================================================================
    @staticmethod
    def stamp2time(stamp, format_type='%Y-%m-%d %H:%M:%S'):
        return time.strftime(format_type, time.localtime(stamp))

    # ===========================================================================
    # 根据日期范围取列表 格式20121212
    # ===========================================================================
    @staticmethod
    def date_range_list(max_time, min_time):
        max_time_stamp = UTime.time2stamp(max_time, '%Y%m%d')
        min_time_stamp = UTime.time2stamp(min_time, '%Y%m%d')
        date_list = []
        while min_time_stamp <= max_time_stamp:
            date_list.append(UTime.stamp2time(min_time_stamp, '%Y%m%d'))
            min_time_stamp += 86400
        return date_list

    # ===========================================================================
    # 昨天日期
    # ===========================================================================
    @staticmethod
    def get_yesterday_date(format_type='%Y%m%d'):
        return UTime.stamp2time(time.time() - 24 * 60 * 60, format_type)

    # ===========================================================================
    # 获取之前日期
    # ===========================================================================
    @staticmethod
    def get_date_before(day_nums, format_type='%Y-%m-%d'):
        return UTime.stamp2time(time.time() - day_nums * 24 * 60 * 60, format_type)

    # ===========================================================================
    # 获取之前日期
    # ===========================================================================
    @staticmethod
    def get_date_before_time(time_str, day_nums, format_type='%Y-%m-%d'):
        stamp = UTime.time2stamp(time_str, format_type)
        return UTime.stamp2time(stamp - day_nums * 24 * 60 * 60, format_type)

    # ===========================================================================
    # 获取之后日期
    # ===========================================================================
    @staticmethod
    def get_date_after_time(time_str, day_nums, format_type='%Y-%m-%d'):
        stamp = UTime.time2stamp(time_str, format_type)
        return UTime.stamp2time(stamp + day_nums * 24 * 60 * 60, format_type)

    # ===========================================================================
    # 今天日期 %Y-%m-%d %H:%M:%S
    # ===========================================================================
    @staticmethod
    def get_today_date(format_type='%Y-%m-%d %H:%M:%S'):
        return UTime.stamp2time(time.time(), format_type)

    # ===========================================================================
    # 今年第一天 %Y-%m-%d
    # ===========================================================================
    @staticmethod
    def get_first_day_of_year(time_str, format_type='%Y-%m-%d'):
        t = datetime.datetime.strptime(time_str, format_type)
        return datetime.datetime(year=t.year, month=1, day=1).strftime("%Y-%m-%d")

    # ===========================================================================
    # 今年最后一天 %Y-%m-%d
    # ===========================================================================
    @staticmethod
    def get_last_day_of_year(time_str, format_type='%Y-%m-%d'):
        t = datetime.datetime.strptime(time_str, format_type)
        return datetime.datetime(year=t.year, month=12, day=31).strftime("%Y-%m-%d")

    @staticmethod
    def add_months(dt, months):
        month = dt.month - 1 + months
        year = dt.year + month / 12
        month = month % 12 + 1
        day = min(dt.day, calendar.monthrange(year, month)[1])
        return dt.replace(year=year, month=month, day=day)

    @staticmethod
    def get_between_month(begin_date):
        date_list = []
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m")
            date_list.append(date_str)
            begin_date = UTime.add_months(begin_date, 1)
        return date_list

    @staticmethod
    def get_between_quarter(begin_date):
        # 加上每季度的起始日期、结束日期
        quarter = None
        tempvalue = datetime.datetime.strptime(begin_date, "%Y-%m-%d").strftime("%Y-%m").split("-")
        year = tempvalue[0]
        month = tempvalue[1]
        if month in ['01', '02', '03']:
            quarter = ('%s-01-01' % year, '%s-03-31' % year)
        elif month in ['04', '05', '06']:
            quarter = ('%s-04-01' % year, '%s-06-30' % year)
        elif month in ['07', '08', '09']:
            quarter = ('%s-07-01' % year, '%s-09-30' % year)
        elif month in ['10', '11', '12']:
            quarter = ('%s-10-01' % year, '%s-12-31' % year)

        return quarter

    @staticmethod
    def get_days(day1, day2):
        s_day = datetime.date(int(day1.split('-')[0]), int(day1.split('-')[1]), int(day1.split('-')[2]))
        e_day = datetime.date(int(day2.split('-')[0]), int(day2.split('-')[1]), int(day2.split('-')[2]))

        return (e_day - s_day).days + 1

    @staticmethod
    def get_days_list(day1, day2):
        days = []

        s_day = datetime.date(int(day1.split('-')[0]), int(day1.split('-')[1]), int(day1.split('-')[2]))
        e_day = datetime.date(int(day2.split('-')[0]), int(day2.split('-')[1]), int(day2.split('-')[2]))

        day = s_day

        while day <= e_day:
            days.append(day)
            day = day + datetime.timedelta(days=1)

        return days


if __name__ == '__main__':
    for i in range(2, 16):
        print('更新行业信息【{_dt}】'.format(_dt=UTime.get_date_before(day_nums=i, format_type='%Y-%m-%d')))
