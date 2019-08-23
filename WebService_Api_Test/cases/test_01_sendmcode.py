# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 11:41
# @Author  : lyx
# @File    : test_01_sendmcode.py
# @Project : WebService_Api_Test
import unittest
import json
import os
from libs.ddt import ddt, data
from scripts.handle_excel import HandleExcel
from scripts.handle_config import HandleConfig
from scripts.handle_logging import HandleLog
from scripts.handle_context import HandleContext
from scripts.content_os import EXCEL_FILE_PATH, CONFIG_FILE_PATH, LOG_FILE_PATH
from scripts.handle_webservice_request import HandleWebserviceRequest

excel_dir = os.path.join(EXCEL_FILE_PATH, "webservice_api_test_cases.xlsx")
do_excel = HandleExcel(excel_dir, "sendmcode")
cases = do_excel.get_all_case()

conf_dir = os.path.join(CONFIG_FILE_PATH, "api_config.ini")
do_conf = HandleConfig(conf_dir)

do_log = HandleLog().get_logger()
do_context = HandleContext()


@ddt
class TestSendMCode(unittest.TestCase):
    """
    测试发送短信验证码接口
    """
    @classmethod
    def setUpClass(cls):
        url = do_conf.get_data("interface url", "sendmcode_api_url")
        # cls.client = Client(url)  # 创建Client对象
        cls.do_request = HandleWebserviceRequest(url)
        do_log.debug("{:=^50s}".format("发送短信验证码接口-测试用例开始执行"))

    @classmethod
    def tearDownClass(cls):
        do_log.debug("{:=^50s}".format("发送短信验证码接口-测试用例执行结束"))

    @data(*cases)
    def test_send_m_code(self, case):
        """
        测试接口方法
        :param params:  接口参数
        :return:
        """
        # 发送请求
        # 此处如果请求不成功则会抛出异常，所以要对异常进行捕获处理
        # webservice接口中一个url下会有多个接口，要通过请求名称来区分要请求的接口
        do_log.debug("{:*^50s}".format(case['title']))
        param = json.loads(do_context.not_registed_mobile_replace(case['params']))
        do_log.debug(f"请求参数为：【{param}】")
        res = self.do_request.send_request(param, case['interface_name'])
        do_log.info(f"请求返回结果为：【{res}】")
        # try:
        #     do_log.debug(f"请求参数为：【{param}】")
        #     res = self.client.service.sendMCode(param)
        #     # 如果没有抛异常，则对接口返回结果进行处理，通过debug可查看返回结果
        #     # 可将res转换为json格式，有利于后面对返回结果进行断言
        #     res = json.dumps(dict(res), ensure_ascii=False)
        #     do_log.info(f"请求返回结果为：【{res}】")
        # except Exception as e:
        #     # 通过debug可查看出发生异常时，需要的异常信息在e.fault中，对此转换为json做为接口返回结果
        #     res = json.dumps(dict(e.fault), ensure_ascii=False)
        #     do_log.info(f"请求返回结果为：【{res}】")

        # 对结果进行断言
        # expect_result = '{"retCode": "0", "retInfo": "ok"}'
        try:
            self.assertEqual(case["expected"], res)
            # print(f"结果为成功,实际接口返回结果为{res}")
            do_excel.write_in_excel(case["case_id"], actual=res, result="Pass")
            do_log.info(f"断言成功，期望结果：【{case['expected']}】，实际结果：【{res}】")
        except Exception as e:
            # print(f"结果为失败, 实际接口返回结果为{res}")
            do_excel.write_in_excel(case["case_id"], actual=res, result="Fail")
            do_log.error(f"断言失败，期望结果：【{case['expected']}】，实际结果：【{res}】")
            raise e


if __name__ == '__main__':
    unittest.main()
