#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading


def task():
    time.sleep(1)
    # 获取当前线程的线程对象
    thread = threading.current_thread()
    print(thread)


if __name__ == '__main__':
    # 多线程执行是无序的， 是由CPU调度决定某个线程先执行
    for i in range(5):
        sub_thread = threading.Thread(target=task)
        sub_thread.start()
