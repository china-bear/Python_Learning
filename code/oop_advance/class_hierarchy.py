#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 实现方式一
class Computer(object):
    def __init__(self, name, cpu):
        self.name = name
        self.cpu = cpu


class Laptop(Computer):
    def __init__(self, name, cpu, manufacturer):
        super(Laptop, self).__init__(name, cpu)
        self.manufacturer = manufacturer


class AutomatedTellerMachine(Computer):
    def __init__(self, name, cpu, bank):
        super(AutomatedTellerMachine, self).__init__(name, cpu)
        self.bank = bank


# 实现方式二
class Mobile(object):
    def __init__(self, name, cpu):
        self.name = name
        self.cpu = cpu


class CPU(object):
    def __init__(self, manufacturer, model):
        self.model = model
        self.manufacturer = manufacturer


if __name__ == "__main__":
    # 方式一测试
    macbook = Laptop('MyMacbook', 'Intel', 'Apple')
    atm = AutomatedTellerMachine('ATM01', 'AMD', 'WellFargo')

    print("{}, {} {}".format(macbook.name, macbook.cpu, macbook.manufacturer))
    print("{}, {} {}".format(atm.name, atm.cpu, atm.bank))

    # 方式二测试
    print('\n-----------------------------------------\n')
    intel_cpu = CPU('Intel', 'X86')
    my_mobile = Mobile('华为', intel_cpu)

    print("{}, {}, {}".format(my_mobile.name, my_mobile.cpu.model, my_mobile.cpu.manufacturer))
