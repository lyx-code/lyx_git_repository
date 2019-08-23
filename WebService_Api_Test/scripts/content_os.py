# -*- coding: utf-8 -*-
# @Time    : 2019/8/20 10:24
# @Author  : lyx
# @File    : content_os.py
# @Project : WebService_Api_Test
# 此模块为动态获取各文件、日志等的目录

import os

# 项目根目录
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# excel文件所在目录
EXCEL_FILE_PATH = os.path.join(BASE_PATH, "datas")

# 配置文件所在目录
CONFIG_FILE_PATH = os.path.join(BASE_PATH, "configs")

# 日志文件所在目录
LOG_FILE_PATH = os.path.join(BASE_PATH, "logs")

# 报告文件所在目录
REPORTS_FILE_PATH = os.path.join(BASE_PATH, "reports")

# 封装的测试类所在目录
CASE_CLASS_PATH = os.path.join(BASE_PATH, "cases")

pass
