#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback

"""
Python3 内置异常的类层级结构: https://docs.python.org/zh-cn/3/library/exceptions.html
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- EncodingWarning
           +-- ResourceWarning
"""

for arg in sys.argv[1:]:
    try:
        f = open(arg, 'r')
    except OSError:
        print('cannot open', arg)
    except BaseException as err:
        print("Unexpected err")
    else:
        print('没有引发异常, 必须要执行的代码块')
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()
    finally:
        print('不论 try 语句是否触发异常, 都会执行的代码块')

"""
内容介绍了几种比较复杂的触发异常情景：
1. 如果执行 try 子句期间触发了某个异常，则某个 except 子句应处理该异常。如果该异常没有 except 子句处理，在 finally 子句执行后会被重新触发。
2. except 或 else 子句执行期间也会触发异常。 同样，该异常会在 finally 子句执行之后被重新触发。
3. 如果 finally 子句中包含 break、continue 或 return 等语句，异常将不会被重新引发。
4. 如果执行 try 语句时遇到 break,、continue 或 return 语句，则 finally 子句在执行 break、continue 或 return 语句之前执行。
5. 如果 finally 子句中包含 return 语句，则返回值来自 finally 子句的某个 return 语句的返回值，而不是来自 try 子句的 return 语句的返回值。
"""

# 自定义异常类及其用法
class BusinessError(Exception):
    # 自定义异常类型的初始化
    def __init__(self, msg):
        self.msg = msg
        # 返回异常类对象的说明信息

    def __str__(self):
        return "{} 打印出来".format(repr(self.msg))


try:
    raise BusinessError("业务出现异常了")
except BusinessError as ex:
    print("错误是{}".format(ex))

# raise

# 获取异常的详细信息



#  异常链


https://bbs.huaweicloud.com/blogs/detail/289764
https://docs.python.org/zh-cn/3/library/exceptions.html
https://docs.python.org/zh-cn/3/tutorial/errors.html
https://docs.python.org/zh-cn/3/library/exceptions.html#bltin-exceptions
