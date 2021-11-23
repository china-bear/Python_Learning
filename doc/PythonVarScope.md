# Python 变量作用域
> Python 只有模块(module）、类(class）以及函数(def、lambda）才会引入新的作用域, 其它的代码块(如 if/elif/else/、try/except、for/while等）是不会引入新的作用域的，也就是说这些语句内定义的变量，外部也可以访问

## Python 4种 作用域  

* L (Local） 局部作用域
* E (Enclosing） 闭包函数外的函数中
* G (Global） 全局作用域
* B (Built-in） 内建作用域
* L –> E –> G –>B 的规则查找，即: 在局部找不到，便会去局部外的局部找(例如闭包), 再找不到就会去全局找，再者去内建中找



## 全局变量和局部变量

*  定义在函数内部的变量拥有一个局部作用域, 局部变量只能在其被声明的函数内部访问
*  定义在函数外的拥有全局作用域, 全局变量可以在整个程序范围内访问, 默认情况下局部是无法修改全局变量的：
*  调用函数时，所有在函数内声明的变量名称都将被加入到作用域中

```python
name = "Mr.Bear"

def f1():
  print(name)

def f2():
  name = "Mike"

f1()
f2()
```

```python
total = 0 # 这是一个全局变量

def sum( arg1, arg2 ):
    #返回2个参数的和."
    total = arg1 + arg2 # total在这里是局部变量.
    print ("函数内是局部变量 : ", total)
    return total
 
#调用sum函数
sum( 10, 20 )
print ("函数外是全局变量 : ", total)
```

## 局部修改全局变量的两种办法

* 增加global、nonlocal关键字
```python
num = 1
def fun1():
    global num  # 需要使用 global 关键字声明
    print(num) 
    num = 123
    print(num)
fun1()
print(num)

def outer():
    i = 10
    def inner():
        nonlocal i   # i nonlocal关键字声明
        i = 100
        print(i)
    inner()
    print(i)
outer()

```

* 对于可变对象，如list、dict等，使用内置函数

```python
b = [1]
def local():
    b.append(2)
local()
print(b)
```

