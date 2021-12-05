#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Animal(object):
    def run(self):
        print(self)
        print('Animal is running...')


class Dog(Animal):
    def run(self):
        print(self)
        print('Dog is running...')


class Cat(Animal):
    def run(self):
        print(self)
        print('Cat is running...')


def run_twice(animal):
    animal.run()
    animal.run()


a = Animal()
d = Dog()
c = Cat()

print(c.__dict__, '\n', c.__dir__(), '\n', c.__repr__())
print('a is Animal?', isinstance(a, Animal))
print('a is Dog?', isinstance(a, Dog))
print('a is Cat?', isinstance(a, Cat))
# 检测一个类是否是另一个类的子类
print(issubclass(Dog, Animal))


print('d is Animal?', isinstance(d, Animal))
print('d is Dog?', isinstance(d, Dog))
print('d is Cat?', isinstance(d, Cat))

run_twice(c)
