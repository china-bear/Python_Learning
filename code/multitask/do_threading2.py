#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading


def work():
    for k in range(10):
        print("...工作中...")
        time.sleep(0.2)


if __name__ == '__main__':
    sub_thread = threading.Thread(target=work)

    # 主线程默认等待所有的子线程执行结束再结束，
    # 主线程结束不想等待子线程结束才结束，可以设置子线程守护主线程
    # 设置守护主线程有二种方式：
    # 1. threading.Thread(target=work, daemon=True)
    # 2. 线程对象.setDaemon(True)
    sub_thread.setDaemon(True)
    sub_thread.start()

    # 让主进程等待 1 秒 后结束
    time.sleep(1)
    print("主进程执行完成了.")

