"""
方法的分类
1. 对象方法
特征： a. 在类中定义的方法，含有self 参数
      b. 方法含有self的参数， 只能使用对象进行调用
      c. 会把调用这个方法的对象传梯进来

2. 类方法
特征：  a. 在类中定义的方法，方法前用@classmethod装饰
       b. 方法含有cls的参数， 不需要实类化对象，可以直接用类进行调用
       c. 会把调用这个方法的类传梯进来

3. 绑定类方法
      a. 在类中定义的方法没有任何参数
      b. 只能使用类进行调用， 对象不能调用
      c. 不会传剃类 或者 对象进来

4. 静态方法
特征：  a. 在类中定义的方法，方法前用staticmethod装饰
       b. 在类中定义的方法没有任何参数
       c. 可以使用类 或者 对象 进行调用
       d. 不会传剃 类 或者 对象 进来，方法可以有其它参数
"""


class demo:
    # 对象方法调用
    def fun1(self):
        print(self)
        print('Object Function')

    # 类方法
    @classmethod
    def fun2(cls):
        print(cls)
        print('Class function')

    # 绑定方法
    def fun3():
        print('bind class function')

    # 静态方法
    @staticmethod
    def fun4():
        print('static method function')


if __name__ == '__main__':
    # 对象方法调用
    obj = demo()
    obj.fun1()

    # 类方法调用
    demo.fun2()
    obj.fun2()  # 即使使用类对象调用，传剃进去 依然是 类对象

    # 绑定类方法调用
    demo.fun3()

    # 静态方法调用
    demo.fun4()
    obj.fun4()
