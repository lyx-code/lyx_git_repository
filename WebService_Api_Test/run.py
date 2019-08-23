# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 17:46
# @Author  : lyx
# @File    : run.py
# @Project : WebService_Api_Test

import unittest
import os
from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.content_os import REPORTS_FILE_PATH, CASE_CLASS_PATH

reports_file = os.path.join(REPORTS_FILE_PATH, "webservice_api_test_report.html")
with open(reports_file, mode="wb") as file:
    one_suite = unittest.defaultTestLoader.discover(CASE_CLASS_PATH, pattern='test_*.py')
    one_runner = HTMLTestRunner(file,
                                verbosity=2,
                                title="webservice项目接口测试报告",
                                description="发送短信验证码接口、注册接口、实名认证接口",
                                tester="lyx")
    one_runner.run(one_suite)


