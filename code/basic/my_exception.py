"""
自定义异常处理类
"""
import os


class MyException(Exception):
    def __init__(self):
        import traceback  # 打印或检索栈回溯
        import logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s [line:%(lineno)d] [%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        # 写入日志
        logging.error(traceback.format_exc())


class B(Exception):
    pass


class C(B):
    pass


class D(C):
    pass


if __name__ == '__main__':

    print(os.getcwd())  # 执行时脚本时 所在的目录
    print(os.path.realpath(__file__))  # will first resolve any symbolic links in the path, and then return the absolute path.
    print(os.path.dirname(__file__))  # python执行文件 相对路径

    absolute_path = os.path.abspath(__file__)  # returns the absolute path, but does NOT resolve symlinks in its argument.
    print("Full path: " + absolute_path)
    print("Directory Path: " + os.path.dirname(absolute_path))

    # os.path.abspath returns the absolute path, but does NOT resolve symlinks in its argument
    os.path.abspath('./')
    os.path.abspath('./Python_Learning/../basic')

    # os.path.realpath will resolve symlinks AND return an absolute path from a relative path
    os.path.realpath('./')
    os.path.realpath('./Python_Learning/../')

    # NEITHER abspath or realpath will resolve or remove ~.
    os.path.abspath('~/basic')
    os.path.realpath('~/basic')

    # And the returned path will be invalid
    os.path.exists(os.path.abspath('~/basic'))

    os.path.exists(os.path.realpath('~/basic'))


    # Use realpath + expanduser to resolve ~
    os.path.realpath(os.path.expanduser('~/Python_Learning/../basic'))


    for cls in [B, C, D]:
        try:
            raise cls()
        except D:
            print("D")
        except C:
            print("C")
        except B:
            print("B")

    try:
        int('abc')
    except: # If you don't have a specific exception you're expecting, at least except Exception, which is the base type for all "Regular" exceptions.
        print('异常处理代码')
        MyException()
