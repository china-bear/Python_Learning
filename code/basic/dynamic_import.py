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


# sys.path 列出 Python 模块查找的目录列表
print(sys.path)

# sys.meta_path 存放的是所有的查找器
print(sys.meta_path)

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
