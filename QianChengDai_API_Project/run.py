# -*- coding utf-8 -*-
"""

"""
import unittest
import os
from datetime import datetime
from libs.HTMLTestRunnerNew import HTMLTestRunner

from scripts.contants import CASE_PATH, REPORT_PATH, CONFIG_PATH
# case_dir是测试数据文件（excel文件）所在目录的绝对路径
# report_dir是报告文件所在目录的绝对路径
from scripts.handle_account import HandleAccount


is_need_make_account = False  # 是否需要注册管理人、投资人、借款人三个账号标识
# 如果需要重新注册这三个账号，则修改is_need_make_account为True，默认为false,不注册
# 还可以通过判断account.ini配置文件是否存在来决定是否要注册这三个账号
account_file_path = os.path.join(CONFIG_PATH, "account.ini")
# if is_need_make_account:
if not os.path.exists(account_file_path):
    do_register_account = HandleAccount()
    do_register_account.write_mobile_in_config(do_register_account.register_manager_investor_borrower_mobile())
    do_register_account.close()


# 以下为测试套件内容
one_suite = unittest.defaultTestLoader.discover(CASE_PATH, "test_*.py")
report_file = REPORT_PATH + "\\" + "case_report_" + datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + ".html"
with open(report_file, mode="wb") as file:
    one_runner = HTMLTestRunner(stream=file,
                                    verbosity=2,
                                    title="lyx_前程贷接口测试报告",
                                    description="前程贷接口测试",
                                    tester="lyx")
    one_runner.run(one_suite)
