"""
自定义异常处理类
"""


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
    except:
        print('异常处理代码')
        MyException()
