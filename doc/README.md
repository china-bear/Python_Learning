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

> _init__.py的原始使命是声明一个模块, 所以它可以是一个空文件, 在__init__.py中声明的所有类型和变量, 就是其代表的模块的类型和变量, 
> 在Python工程里, 当python检测到一个目录下存在__init__.py文件时, python就会把它当成一个模块(module). Module跟C＋＋的命名空间和Java的Package的概念很像, 都是为了科学地组织化工程, 管理命名空间
> 在利用__init__.py时, 应该遵循如下几个原则:

1. 不要污染现有的命名空间. 模块一个目的, 是为了避免命名冲突, 如果你在种用__init__.py时违背这个原则, 是反其道而为之, 就没有必要使用模块了. 

2. 利用__init__.py对外提供类型、变量和接口, 对用户隐藏各个子模块的实现. 一个模块的实现可能非常复杂, 你需要用很多个文件, 甚至很多子模块来实现, 但用户可能只需要知道一个类型和接口. 就像我们的arithmetic例子中, 用户只需要知道四则运算有add、sub、mul、dev四个接口, 却并不需要知道它们是怎么实现的, 也不想去了解arithmetic中是如何组织各个子模块的. 由于各个子模块的实现有可能非常复杂, 而对外提供的类型和接口有可能非常的简单, 我们就可以通过这个方式来对用户隐藏实现, 同时提供非常方便的使用. 

3. 只在__init__.py中导入有必要的内容, 不要做没必要的运算. 像我们的例子, import arithmetic语句会执行__ini__.py中的所有代码. 如果我们在__init__.py中做太多事情, 每次import都会有额外的运算, 会造成没有必要的开销. 一句话, __init__.py只是为了达到B中所表述的目的, 其它事情就不要做啦. 

