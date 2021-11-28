#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import os
import multiprocessing


def sing(num):
    print("唱歌进程id", os.getpid(), "唱歌进程父id", os.getppid())  # 进程的编号, 父进程的编号
    for m in range(num):
        print("...唱歌...")
        time.sleep(1)


def dance(count):
    print("跳舞进程id", os.getpid(), "跳舞进程父id", os.getppid())  # 进程的编号, 父进程的编号
    for j in range(count):
        print("...跳舞...")
        time.sleep(1)


def work():
    for k in range(3):
        print("...工作中...")


if __name__ == '__main__':
    # 主进程(由操作系统创建)
    work()
    print("主进程id", os.getpid())  # 进程的编号
    # 创建子进程(由主进程创建并执行)
    sing_process = multiprocessing.Process(target=sing, args=(3,))  # args：使用元祖方式给指定任务传参， 元祖值一定和函数参数顺序保持一致

    # 创建子进程()
    dance_process = multiprocessing.Process(target=dance, kwargs={"count": 2}) # kwargs：使用字典方式给指定任务传参，字典中的key一定要和函数参数名称保持一致

    sing_process.start()
    dance_process.start()
