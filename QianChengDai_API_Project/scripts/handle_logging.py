# -*- coding: utf-8 -*-
# @Time    : 2019/7/25 15:27
# @Author  : lyx
# @File    : sh_lyx_0731_python_logging_handle_class.py
# @Project : Django_Project

# 将对日志文件的操作进行封装
import logging
import os

from scripts.handle_config import conf_operate
from scripts.contants import LOG_PATH

# 日志文件
LOG_FILE_PATH = os.path.join(LOG_PATH, "lyx_logging_file.log")


class HandleLogging:

    def __init__(self):
        logger_name = conf_operate.get_config_data("log file", "logger_name")  # 日志收集器名称
        # log_file = conf_operate.get_config_data("log file", "log_file_path")   # 日志文件名称
        log_format = conf_operate.get_config_data("log file", "log_format")    # 日志输出格式

        # 1.定义日志收集器
        self.my_logger = logging.getLogger(logger_name)

        # 2. 定义日志收集器的日志等级
        # 日志等级有： NOTSET（0）、DEBUG（10）、INFO（20）、WARNING（30）、ERROR（40）、CRITICAL（50）
        self.my_logger.setLevel(logging.DEBUG)
        # 第二种方法，使用字符串指定等级
        # self.my_logger.setLevel("DEBUG")

        # 3. 定义日志输出的渠道
        # 控制台渠道
        console_handle = logging.StreamHandler()
        # 文件渠道
        file_handle = logging.FileHandler(LOG_FILE_PATH, mode="a", encoding="utf-8")

        # 4. 指定输出到渠道的日志等级
        console_handle.setLevel(logging.ERROR)
        file_handle.setLevel(logging.DEBUG)

        # 5. 定义日志输出格式
        # %(asctime)s 表示时间；%(levelname)s 表示日志等级； %(module)s 表示当前模块名称；%(lineno)d 表示代码行号 ；%(message)s 表示日志信息
        # log_formatter = logging.Formatter("%(asctime)s : %(levelname)s  %(module)s :%(lineno)d  - %(message)s")
        log_formatter = logging.Formatter(log_format)

        console_handle.setFormatter(log_formatter)
        file_handle.setFormatter(log_formatter)
        
        # 6. 对接日志收集器与输出渠道
        self.my_logger.addHandler(console_handle)
        self.my_logger.addHandler(file_handle)

    def get_logger(self):
        """
        获取日志收集器
        :return:
        """
        return self.my_logger


log_operate = HandleLogging().get_logger()

if __name__ == '__main__':
    first_log = HandleLogging()
    my_logger = first_log.get_logger()
    my_logger.debug("这是我测试的debug级别日志")
    my_logger.info("这是我测试的info级别日志")
    my_logger.warning("这是我测试的warning级别日志")
    my_logger.error("这是我测试的error级别日志")
    my_logger.critical("这是我测试的critical级别日志")


