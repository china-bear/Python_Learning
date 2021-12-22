
# Concurrency

*Concurrent programming* means that you have two or more sub-programs running simultaneously.
This potentially allows you to use all your processors at once.
This sounds like an enticing idea, but there are good reasons to be very cautious with it.

### Why is Concurrency a bad idea?

* Starting multiple Python processes instead is really easy (e.g. from a batch script).
* Coordinating parallel sub-programs is very difficult to debug (look up the words *"race condition"* and *"heisenbug"*).
* Python has a strange thing called the **GIL (Global Interpreter Lock)**. That means, Python can really only execute one command at a time.
* There are great existing solutions for the most typical applications.

### Alternatives

* if you want to read/write data, use a database
* if you want to scrape web pages, use the `scrapy` framework.
* if you want to build a web server, use `Flask` or `Django`.
* if you want to do number crunching, use `Spark`, `Pytorch` or `Tensorflow`

### When could concurrency be a good idea?

I can think of one reason:

You are writing a computer game for fun and would like many sprites to move at the same time
**AND** you are looking for difficult problems to solve.

There are two noteworthy approaches to concurrency in Python: **threads** and **coroutines**.


### 多任务概念
多任务是指在同一时间内执行多个任务， 多任务的表现形式
1. 并发
在一段时间内交替去执行多个任务， 例如：对于单核cpu处理多任务，操作系统轮流让各个任务交替执行

2. 并行
在一段时间内真正同时一起执行多个任务呢，例如：对于多核cpu 处理任务

### 进程的概念
进程是资源分配的最小单位， 它是操作系统进行资源分配和调度运行的基本单位，通俗理解 就是一个正在运行的程序就是一个进程，一个程序最少有一个进程

### 线程的概念
进程是资源分配的最小单位， 一旦创建一个进程就会分配一定的资源， 线程是程序执行的最小单位，实际上进程只负责分配资源，而利用这些资源
执行程序的是线程，也就是说进程是线程的容器，一个进程中至少有一个线程来负责执行程序，同时线程本身不拥有系统资源，只需要一点在运行中
必不可少的资源，但线程与同属一个进程的其它线程共享进程所有的全部资源

### 进程 与 线程的对比
1. 关系对比
> 线程是依附在进程里面的， 没有进程就没有线程
> 一个进程默认提供一个线程，进程能创建多个线程


2. 区别对比
> 创建进程的资源开销要比创建线程的资源开销大
> 进程是操作系统资源分配的基本单位，线程是CPU调度的基本单位
> 线程不能够独立执行，必须依附存在的进程中

3. 优缺点对比
> 进程的优缺点
a.优点： 可以用多核
b.缺点： 资源开销大

> 线程的优缺点
a. 优点：资源开销小
b. 缺点：不能使用多核   ？？？

