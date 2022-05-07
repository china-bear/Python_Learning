#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import logging

# 通过下面的方式进行简单配置输出方式与日志级别, 只有日志级别大于等于ERROR的日志才会输出
#logging.basicConfig(filename='logger.log', level=logging.INFO)

# 默认情况下，logging模块将日志打印到屏幕上(stdout)，日志级别为WARNING(即只有日志级别高于WARNING的日志信息才会输出)
print(logging.getLogger(__name__))

logging.debug('debug message')
logging.info('info message')
logging.warning('warn message')
logging.error('error message')
logging.critical('critical message')

# https://www.jianshu.com/p/feb86c06c4f4
# create logger
logger_name = "example"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

# create file handler
log_path = "./log.log"
fh = logging.FileHandler(log_path)
fh.setLevel(logging.WARN)

# create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)

# print log info
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')