name = 2


def f1():
    print(name)


def f2():
    name = 100
    print(name)


f1()
f2()

print(name)
