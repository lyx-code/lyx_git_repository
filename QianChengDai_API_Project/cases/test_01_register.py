# -*- coding utf-8 -*-
"""

"""
import unittest
import json
import os
from datetime import datetime
from libs.HTMLTestRunnerNew import HTMLTestRunner
from libs.ddt import ddt, data
from scripts.handle_excel import HandleExcel
from scripts.handle_request import HandleRequest
from scripts.handle_logging import log_operate
from scripts.contants import EXCEL_PATH
from scripts.handle_context import HandleContext

# 创建Excel文件操作对象
do_excel = HandleExcel(os.path.join(EXCEL_PATH, "QianChengDai_interface_cases.xlsx"), "register")


cases = do_excel.get_all_case()


@ddt
class RegisterTest(unittest.TestCase):
    """
    测试注册接口
    """
    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()   # 将发送请求对象定义为类属性，是为了能在测试结束后关闭session会话，释放资源
        log_operate.debug("*******************开始执行测试******************")

    @classmethod
    def tearDownClass(cls):
        cls.do_request.session_close()    # 调用关闭session会话方法，释放资源
        log_operate.debug("*******************测试执行完成******************")

    @data(*cases)
    def test_register(self, case):
        """
        测试注册接口
        :param case:
        :return:
        """
        interface_url = case["url"]  # 接口名称
        interface_method = case["method"]   # 接口请求方法
        interface_data = HandleContext.register_api_parameterization(case["data"])   # 接口请求参数 --使用参数化方法参数化
        interface_expect_result = eval(case["expected"])  # 期望结果  使用eval()方法将取到的字符串期望结果数据转为字典类型

        # 发送请求

        res = self.do_request.send_request(interface_url, interface_method, data=interface_data)
        log_operate.info(f"请求响应结果：{res}{res.text}")

        # 对响应结果进行断言
        response_status = json.loads(res.text)["status"]
        response_code = json.loads(res.text)["code"]

        try:
            self.assertEqual(interface_expect_result["status"], response_status)
            self.assertEqual(interface_expect_result["code"], response_code)
            log_operate.info(f"断言成功：期望status[{interface_expect_result['status']}],"
                             f"code[{interface_expect_result['code']}] 实际结果status[{response_status}],"
                             f"code[{response_code}]")
            do_excel.write_data_in_excel(case["case_id"]+1, res.text, "PASS")
        except AssertionError as e:
            log_operate.error(f"断言失败：期望status[{interface_expect_result['status']}],"
                              f"code[{interface_expect_result['code']}]  "
                              f"实际结果status[{response_status}],code[{response_code}]")
            do_excel.write_data_in_excel(case["case_id"] + 1, res.text, "FAIL")
            raise e


if __name__ == '__main__':
    one_suite = unittest.defaultTestLoader.discover("D:\PythonLearning\QianChengDai_API_Project\cases", "test_*.py")
    x = r"D:\PythonLearning\QianChengDai_API_Project\reports"
    report_file = x + "\case_report_" + datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + ".html"
    with open(report_file, mode="wb") as file:
        one_runner = HTMLTestRunner(stream=file,
                                    verbosity=2,
                                    title="lyx_0802_作业测试报告",
                                    description="前程贷注册接口测试",
                                    tester="lyx")
        one_runner.run(one_suite)
