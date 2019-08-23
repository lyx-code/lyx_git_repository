# -*- coding: utf-8 -*-
# @Time    : 2019/8/20 10:40
# @Author  : lyx
# @File    : test_02_register.py
# @Project : WebService_Api_Test
import os
import unittest
import json
from libs.ddt import ddt, data

from scripts.handle_excel import HandleExcel
from scripts.content_os import EXCEL_FILE_PATH, CONFIG_FILE_PATH
from scripts.handle_config import HandleConfig
from scripts.handle_context import HandleContext
from scripts.handle_mysql import HandleMySql
from scripts.handle_logging import HandleLog
from scripts.handle_webservice_request import HandleWebserviceRequest

do_log = HandleLog().get_logger()

do_context = HandleContext()

do_conf = HandleConfig(os.path.join(CONFIG_FILE_PATH, "api_config.ini"))

excel_dir = os.path.join(EXCEL_FILE_PATH, "webservice_api_test_cases.xlsx")
do_excel = HandleExcel(excel_dir, "register")
cases = do_excel.get_all_case()

@ddt
class TestRegister(unittest.TestCase):
    """
    测试注册接口封装类
    """
    @classmethod
    def setUpClass(cls):
        do_log.debug("{:=^50s}".format("注册接口测试用例开始执行"))
        sendcode_url = do_conf.get_data("interface url", "sendmcode_api_url")
        regist_url = do_conf.get_data("interface url", "register_api_url")
        # cls.client_sendcode = Client(sendcode_url)
        # cls.client_register = Client(regist_url)
        cls.do_request_sendcode = HandleWebserviceRequest(sendcode_url)
        cls.do_request_regist = HandleWebserviceRequest(regist_url)
        cls.do_sql = HandleMySql()
        pass

    @classmethod
    def tearDownClass(cls):
        cls.do_sql.close()
        do_log.debug("{:=^50s}".format("注册接口测试用例执行结束"))

    @data(*cases)
    def test_regiester(self, case):
        """

        :param case:
        :return:
        """
        do_log.debug("{:*^50s}".format(case['title']))
        param = json.loads(do_context.register_api_parametrization(case['params']))
        do_log.debug(f"请求参数为:【{param}】")
        if case['interface_name'] == "sendMCode":

            res = self.do_request_sendcode.send_request(param, case['interface_name'])
        elif case['interface_name'] == 'userRegister':
            res = self.do_request_regist.send_request(param, case['interface_name'])
        else:
            res = "接口名称不正确"
        do_log.debug(f"请求响应结果为:【{res}】")
        # try:
        #     if "verify_code" not in param:
        #         HandleContext.mobile = param['mobile']
        #         res = self.client_sendcode.service.sendMCode(param)
        #     else:
        #         res = self.client_register.service.userRegister(param)
        #     res = json.dumps(dict(res), ensure_ascii=False)
        #     do_log.debug(f"请求响应结果为:【{res}】")
        # except Exception as e:
        #     res = json.dumps(dict(e.fault), ensure_ascii=False)
        #     do_log.debug(f"请求响应结果为:【{res}】")

        try:
            # 对请求结果断言
            self.assertIn("ok", res)
            if case['interface_name'] == "sendMCode":
                HandleContext.mobile = param['mobile']
                sql = "select Fverify_code from sms_db_95.t_mvcode_info_4 where Fmobile_no=%s"
                # 将查询出来的验证码动态生成为HandleContext类的类属性，以便注册接口参数化使用
                HandleContext.verify_code = self.do_sql.execute_sql(sql, args=(HandleContext.mobile,))['Fverify_code']
                do_log.info(f"动态生成的号码【{HandleContext.mobile}】获取的验证码为【{HandleContext.verify_code}】")
            else:
                # 如果是注册成功，则将注册的用户名保存
                HandleContext.user_id = param['user_id']
            result_dict = {}   # 用来存放数据校验结果
            if case['check_sql']:
                # 如果有数据校验语句，则进行数据校验
                sql = do_context.register_api_parametrization(case['check_sql'])   # sql语句参数化
                check_result = self.do_sql.execute_sql(sql)
                if check_result:
                    result_dict["user_id"] = check_result['Fuser_id']
                    # 判断数据库中存储的密码和手机号长度，以判断是否加密保存
                    if len(check_result['Fpwd']) == 32:
                        result_dict['pwd_len'] = "ok"
                    else:
                        result_dict['pwd_len'] = "not enough"
                    if len(check_result['Fmobile']) == 24:
                        result_dict['mobile_len'] = "ok"
                    else:
                        result_dict['mobile_len'] = "not enough"
            # 将断言结果写入excel文件中
            if result_dict:
                do_excel.write_in_excel(row=case['case_id'], actual=res, result="Pass", check_result=json.dumps(result_dict))
            else:
                do_excel.write_in_excel(row=case['case_id'], actual=res, result="Pass")
            do_log.info(f"断言成功：期望结果为【{case['expected']}】，实际结果为【{res}】")
        except Exception as e:
            do_excel.write_in_excel(row=case['case_id'], actual=res, result="Fail")
            do_log.error(f"断言失败：期望结果为【{case['expected']}】，实际结果为【{res}】")
            raise e    # 断言失败要将异常抛出，这样unittest框架才能统计用例失败数量


if __name__ == '__main__':
    unittest.main()

