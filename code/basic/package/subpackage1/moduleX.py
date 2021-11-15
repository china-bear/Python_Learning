# 不论是在 subpackage1/moduleX.py 还是 subpackage1/__init__.py 中，以下导入都是有效的:
# https://docs.python.org/zh-cn/3/reference/import.html
# 方式一： 相对路径导入使用前缀点号, 一个前缀点号表示相对导入从当前包开始, 两个或更多前缀点号表示对当前包的上级包的相对导入, 第一个点号之后的每个点号代表一级
from .moduleY import spam
from .moduleY import spam as ham
from . import moduleY
from ..subpackage1 import moduleY
from ..subpackage2.moduleZ import eggs
from ..moduleA import foo


# 方式二： 绝对路径导入可以使用 import <> 或 from <> import <> 语法, 但相对导入只能使用第二种形式

import code.basic.package.moduleA
from code.basic.package.moduleA import bar