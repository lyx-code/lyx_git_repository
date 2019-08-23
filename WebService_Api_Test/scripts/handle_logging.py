# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 16:09
# @Author  : lyx
# @File    : handle_logging.py
# @Project : WebService_Api_Test
# 此模块为处理日志输出
import os
import logging
from scripts.content_os import LOG_FILE_PATH
log_dir = os.path.join(LOG_FILE_PATH, "webservice_api.log")


class HandleLog:
    """
    处理日志输出封装类
    """
    def __init__(self):
        pass
        self.logger = logging.getLogger("api_test_logger")
        self.logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        file = logging.FileHandler(log_dir, mode="a", encoding="utf-8")

        console.setLevel(logging.ERROR)
        file.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s : %(levelname)s  %(module)s :%(lineno)d  - %(message)s")
        console.setFormatter(formatter)
        file.setFormatter(formatter)

        self.logger.addHandler(console)
        self.logger.addHandler(file)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    test = "eheheheheheh"
    do = HandleLog().get_logger()
    do.debug(test)
    do.error(test)

