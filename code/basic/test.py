#!/usr/bin/python
# -*- coding: UTF-8 -*

import os.path
import re


def sql_from_file():
    f = '/home/hdp-ads-dw/stark_PC_SHOW_FLOW_REPORT_TASK_shbt-prod/zip/task/show/bool/ba_yd_media_analysis_channel_deal_mode.sql'
    if not os.path.exists(f):
        raise ('参数错误:[SQL FILE {_file} NOT EXISTS.]'.format(_file=f))
    with open(f, 'r', encoding='utf8') as f_handler:
        str_hql = re.sub(r"(\r\n|\n)*;$", "", f_handler.read().rstrip().format(day='2021-12-19'))
    return str_hql


def run(account, profile='test'):
    f(account)
    f(profile)


def f(var):
    print(var)


if __name__ == '__main__':

    for letter in 'Python':     # 第一个实例
        if letter == 'h':
            continue
        print ('当前字母 :', letter)

    var = 10                    # 第二个实例
    while var > 0:
        var = var -1
        if var == 5:
            continue
        print ('当前变量值 :', var)
    print ("Good bye!")