#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading


def sing(num):
    for m in range(num):
        print("...唱歌...")
        time.sleep(1)


def dance(count):
    for j in range(count):
        print("...跳舞...")
        time.sleep(1)


def work():
    for k in range(10):
        print("...工作中...")



if __name__ == '__main__':
    # 主进程(由操作系统创建)
    work()

    # 创建线程(由主进程创建并运行)
    sing_thread = threading.Thread(target=sing, args=(3,))  # args：使用元祖方式给指定任务传参， 元祖值一定和函数参数顺序保持一致

    # 创建线程(由主进程创建并运行)
    dance_thread = threading.Thread(target=dance, kwargs={"count": 2}) # kwargs：使用字典方式给指定任务传参，字典中的key一定要和函数参数名称保持一致

    sing_thread.start()
    dance_thread.start()