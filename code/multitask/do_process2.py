#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import multiprocessing


def work():
    for k in range(10):
        print("...工作中...")
        time.sleep(0.2)


if __name__ == '__main__':
    # 创建子进程(由主进程创建并执行)
    work_process = multiprocessing.Process(target=work)
    # 为了保证子进程能正常运行，默认主进程会等所有的子进程执行完成后再销毁， 设置守护主进程的目的就是主进程退出了进程就销毁，不让主进程再等待子进程去执行
    # work_process.daemon = True  # 设置守护主进程，主进程结束子进程会自动销毁，不再执行子进程代码
    work_process.start()

    # 让主进程等待 1 秒
    time.sleep(1)
    print("主进程执行完成了.")
