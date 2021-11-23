#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 内置模块
import os
import sys
import importlib

# 第三方模块
import json
import urllib.request as urllib2


# 本地模块
# from foo import bar

# Python dynamic import - how to import * from module name from variable?
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch15s04.html
# https://segmentfault.com/a/1190000018032094 【Python Package Import 之痛】
# Python动态导入模块  方式一: __import__  built-in function
def importName(module_name, class_name):
    """ Import a named object from a module in the context of this function.
    """
    try:
        module = __import__(module_name, globals(), locals(), [class_name])
    except ImportError:
        print(ImportError.msg)
        return None
    return vars(module)[class_name]


# 一个模块被另一个程序第一次引入时, 其主程序将运行, 如果想在模块被引入时, 模块中的程序块不执行，我们可以用__name__ 属性来使该程序块仅在该模块自身运行时执行
# 每个模块都有一个__name__属性，当其值是'__main__'时，表明该模块自身在运行, 否则是被引入
if __name__ == '__main__':
    print('程序自身在运行')
else:
    print('我来自另一模块')

# sys.path 列出 Python 模块查找的目录列表, 一个模块只会被导入一次, 不管执行了多少次 import
print(sys.path)

# sys.meta_path 存放的是所有的查找器
print(sys.meta_path)

# 模块文件的路径名: 以相对路径执行__file__是相对路径, 以绝对路径执行__file__是绝对路径
print(__file__)

# 为了保证__file__每次都能准确得到模块的正确位置,最好再取一次绝对路径os.path.abspath(__file__)
print(os.path.abspath(__file__))

# 内置的函数dir()用来查询一个类或者对象所有属性, 以一个字符串列表的形式返回
dir()

# help()函数帮助了解模块、类型、对象、方法、属性的详细信息
help()

print('------------------------------------------------')

f = importName("package.extensions.cat", 'Cat')

f.eat()
f.play()

print('------------------------------------------------')

try:
    f = importlib.import_module('package.extensions.cat')

    f.run()
    print(f.age)
    f.eat()
    f.Cat.play()
except ModuleNotFoundError as e:
    print(e.msg)
else:
    print(f.age)
print('------------------------------------------------')


# 动态获取所有已加载模块目录和路径
def get_module_dir(name):
    path = getattr(sys.modules[name], '__file__', None)
    if not path:
        raise AttributeError('module %s has not attribute __file__' % name)
    return os.path.dirname(os.path.abspath(path))


for ext in 'spam', 'eggs':
    HandlerClass = importName("package.extensions." + ext, "Handler")
    handler = HandlerClass()
    handler.handleSomething()

moduleName = 'json'
className = 'dumps'

print(importName(moduleName, className))
d = dict(name='Bob', age=20, score=88)
data = importName(moduleName, className)(d)
print('JSON Data is a str:', data)

# Python动态导入模块  方式二: importlib built-in function
print('---------------------------------------------------------------')
j = importlib.import_module('json').dumps(d)
print('JSON Data is a str:', data)


def add_func():
    print("add func")


class Animal(object):
    @staticmethod
    def run():
        print('Animal is running...')


for ext in 'spam', 'eggs':
    HandlerClass = importlib.import_module("package.extensions." + ext)
    print(HandlerClass)
    handler = HandlerClass.Handler()
    handler.handleSomething()

# 使用反射判断是否有对应类、方法, 无则设置
f = importlib.import_module('package.subpackage1.foo')
if hasattr(f, "say"):
    print("yes")
    c = getattr(f, "say")
else:  # 没有则设置
    setattr(f, "add_func", add_func)
    setattr(f, "Animal", Animal)

f.add_func()
f.Animal.run()


# my_importer.py
# 查找器
class UrlMetaFinder(importlib.abc.MetaPathFinder):
    def __init__(self, baseurl):
        self._baseurl = baseurl

    def find_module(self, fullname, path=None):
        if path is None:
            baseurl = self._baseurl
        else:
            # 不是原定义的url就直接返回不存在
            if not path.startswith(self._baseurl):
                return None
            baseurl = path

        try:
            loader = UrlMetaLoader(baseurl)
            return loader
        except Exception:
            return None


# 加载器
class UrlMetaLoader(importlib.abc.SourceLoader):
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get_code(self, fullname):
        f = urllib2.urlopen(self.get_filename(fullname))
        return f.read()

    def get_data(self):
        pass

    def get_filename(self, fullname):
        return self.baseurl + fullname + '.py'


# 注册自定义的查找器（UrlMetaFinder）
def install_meta(address):
    finder = UrlMetaFinder(address)
    sys.meta_path.append(finder)
