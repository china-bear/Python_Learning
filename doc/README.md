## Python MYSQL环境 
1. 安装Anaconda2(默认安装 python2.7)
Anaconda2-2019.07-Windows-x86_64.exe

2. 安装 python 3.7

    开始菜单 --> 启动 Anaconda Prompt (Anaconda2) --> conda create -n python3.7 python=3.7

3. 安装  MySQL client library

- To activate python3.7 environment:
    - conda activate python3.7 (python3.7 环境)
    
    - pip install mysql-connector-python
    - pip install mysqlclient
    - pip install PyMySQL

- deactivate an active environment: 
    - conda deactivate  (返回到 python2.7 环境)



## __init__.py的设计原则

> _init__.py 标识该目录是一个python包(package), 它可以是一个空文件, 在__init__.py中声明的所有类型和变量, 就是其代表的模块的类型和变量, 
> 在Python工程里, 当python检测到一个目录下存在__init__.py文件时, python就会把目录当成一个包(package). package跟C＋＋的命名空间和Java的Package的概念很像, 都是为了科学地组织化工程, 管理命名空间
> 在利用__init__.py时, 应该遵循如下几个原则:

1. 不要污染现有的命名空间. 模块一个目的, 是为了避免命名冲突, 如果你在种用__init__.py时违背这个原则, 是反其道而为之, 就没有必要使用模块了. 

2. 利用__init__.py对外提供类型、变量和接口, 对用户隐藏各个子模块的实现. 一个模块的实现可能非常复杂, 你需要用很多个文件, 甚至很多子模块来实现, 但用户可能只需要知道一个类型和接口. 就像我们的arithmetic例子中, 用户只需要知道四则运算有add、sub、mul、dev四个接口, 却并不需要知道它们是怎么实现的, 也不想去了解arithmetic中是如何组织各个子模块的. 由于各个子模块的实现有可能非常复杂, 而对外提供的类型和接口有可能非常的简单, 我们就可以通过这个方式来对用户隐藏实现, 同时提供非常方便的使用. 

3. 只在__init__.py中导入有必要的内容, 不要做没必要的运算. 像我们的例子, import arithmetic语句会执行__ini__.py中的所有代码. 如果我们在__init__.py中做太多事情, 每次import都会有额外的运算, 会造成没有必要的开销. 一句话, __init__.py只是为了达到B中所表述的目的, 其它事情就不要做啦. 

## python模块导入顺序

1. 系统包 > 同目录 > sys.path
2. 当导入包时: _init_会先执行
3. 当导入一个模块时: 模块的顶层变量会被执行, 包括全局变量, 类以及函数的声明(类对象, 函数对象将被创建, 不会被调用), 因此在编写模块时一定要注意消除副作用(函数的调用)
4. sys.modules: 是存放已载入模块的地方, 模块一经载入python 会把这个模块加入 sys.modules 中供下次载入使用, 这样可以加速模块的引入起到缓存的作用
```python
import sys
import os
# 动态获取所有已加载模块目录和路径
def get_module_dir(name):
    path = getattr(sys.modules[name], '__file__', None)
    if not path:
        raise AttributeError('module %s has not attribute __file__'%name)
    return os.path.dirname(os.path.abspath(path))
```


## Python  _, __ 和 __xx__的区别

1. "_" 单下划线
> Python中是不存在真正的私有的 成员 或者 方法的, 但是为了实现类似于c++中的私有 成员 或者 方法, 于是就在类的成员 或者 方法或者属性前加一个"_", 意味着该方法或者属性就不应该被调用,
>  这个只是出于某种君子约定, 我们一般不去调用, 实际上这个方法是能被调用

```python
class A(object):
    _age = 100

    def _test(self):
        print("这个函数不应该通过_test调用，而应该通过test调用")

    def test(self):
        return self._test()
a = A()
a._test()  # 这个函数不应该通过_test调用，而应该通过test调用
a.test()   # 这个函数不应该通过_test调用，而应该通过test调用
print(a._age)
```

2. “__” 双下划线
> 双下划线表示的是私有类型的变量 或者 方法, 不允许子类访问, 也不能被子类重写, 只允许类(self)自身内部访问

```python
class A(object):
    
    __age = 18
    
    def __test(self):
        print("I am test in A")

    def test(self):
        return self.__test()
    
    def getAge(self):
        return  self.__age



a = A()
a.test()
print(a.__age)
print(a.getAge())
class B(A):
    def __test(self):
        print("I am test in B")


b = B()
b.test()    # I am test in A
```

3. "__ xx __" 前后双下划线
> 方法被称为magic methods(魔术方法), 一般是系统定义名字,类似于__init__(), __del__() 一般是用于 Python调用
> __定义的私用属性，实际是变成： _类名__属性，  可以使用这张特殊的调用 私用属性变量

```python
class WrongMethod(object):
    def __init__(self, n):
        self.n = n

    def __add__(self, other):
        return self.n - other

    def __sub__(self, other):
        return self.n + other

    def __str__(self):
        return str(self.n)


num = WrongMethod(20)
print("num = ", num)    # num =  20
print("num + 10 = ", num + 10) # num + 10 =  10
print("num - 10 = ", num - 10) # num - 10 =  30

```

## Python中 *args 和 **kwargs的用法

1. " / "
> 特定形参可以标记为 仅限位置, 仅限位置时形参的顺序很重要, 且这些形参不能用关键字传递. 仅限位置形参应放在 / （正斜杠）前. / 用于在逻辑上分割仅限位置形参与其它形参.如果函数定义中没有 /, 则表示没有仅限位置形参.

2. " * "
> *args 表示任何多个无名参数, 运行传递任意数量的参数, 它本质是一个 tuple(位置参数positional argument)
```python
# 函数形参
def fun(name, *args, **kwargs):
  print(name)
  print(args)
  print(kwargs)
 
fun(1, 2, 3, 4, 5, a="1", b="2", c="3")

# 结果: 
# 1
# (2, 3, 4, 5)
# {a="1", b="2", c="3"}
```

3. " ** "
> **kwargs 表示关键字参数, 允许你使用没有事先定义的参数名, 它本质上是一个 dict(关键词参数keyword argument)
> 同时使用 *args 和 **kwargs 时, 必须 *args 参数列要在 **kwargs 之前, 可变位置参数*args是一个元组, 是不可修改

```python
# 函数实参
def fun(data1, data2, data3):
  print("data1: ", data1)
  print("data2: ", data2)
  print("data3: ", data3)
  
args = ("one", 2, 3)
fun(*args)

# data1:  one
# data2:  2
# data3:  3

kwargs = {"data3": "one", "data2": 2, "data1": 3}
fun(**kwargs)

# data1:  3
# data2:  2
# data3:  one
```

4. " 序列解包 "
> 什么是序列解包：这种方法并不限于列表和元组, 而是适用于任意序列类型(甚至包括字符串和字节序列), 只要赋值运算符左边的变量数目与序列中的元素数目相等, 都可以用这种方法将元素序列解包到另一组变量中

```python
a, b, c = 1, 2, 3
# a = 1
# b = 2
# c = 3

a, b, *c = 0, 1, 2, 3
# a = 0
# b = 1
# c = (2, 3)

a, *b, c = 0, 1, 2, 3
# a = 0
# b = (1, 2)
# c = 3

a, *b, c = a, b, *c = 0, 1
# a = 0
# b = 1
# c = ()

(a, b), (c, d) = (1, 2), (3, 4)
# a = 1
# b = 2
# c = 3
# d = 4
```

## Python logging

*[日志基础教程](https://docs.python.org/zh-cn/3.7/howto/logging.html)

* [Python 教程¶](https://docs.python.org/zh-cn/3.9/tutorial/index.html)
