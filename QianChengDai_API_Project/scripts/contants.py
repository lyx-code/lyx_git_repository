# -*- coding utf-8 -*-
"""

"""
import os
# from scripts.handle_config import conf_operate

# 动态获取文件所在目录的绝对路径，有利于拓展与维护

# 当前文件的绝对路径
one_path = os.path.abspath(__file__)
# 一层层来获取项目根目录所在的绝对路径
two_path = os.path.dirname(one_path)  # dirname()会返回当前目录上一级目录的绝对路径
BASE_PATH = os.path.dirname(two_path)  # 使用大写字母保存项目根目录的绝对路径，有助于一目了然

# 测试类所在路径
CASE_PATH = os.path.join(BASE_PATH, "cases")

# 测试报告文件所在路径
REPORT_PATH = os.path.join(BASE_PATH, "reports")

# excel文件所在的绝对路径
EXCEL_PATH = os.path.join(BASE_PATH, 'datas')
# excel_name = conf_operate.get_config_data('excel file path', 'case_data_file')  # 从配置文件中读取文件名称
# EXCEL_FILE_PATH = os.path.join(excel_dir, "QianChengDai_interface_cases.xlsx")

# 配置文件的绝对路径
CONFIG_PATH = os.path.join(BASE_PATH, 'configs')
# CONFIG_FILE_PATH = os.path.join(config_dir, 'qcd_config_file.ini')

# 日志文件所在的绝对路径
LOG_PATH = os.path.join(BASE_PATH, 'logs')
# LOG_FILE_PATH = os.path.join(log_dir, "lyx_logging_file.log")

# 记录问题：此文件中如果导入配置文件操作对象进行读取配置文件，那么当别的模块中也导入了配置文件对象，再导入该模块时就会发生无法导入的情况
