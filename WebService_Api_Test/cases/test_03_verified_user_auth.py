# -*- coding: utf-8 -*-
# @Time    : 2019/8/20 14:59
# @Author  : lyx
# @File    : test_03_verified_user_auth.py
# @Project : WebService_Api_Test
import unittest
import os
import json
from libs.ddt import ddt, data
from scripts.content_os import CONFIG_FILE_PATH, EXCEL_FILE_PATH
from scripts.handle_config import HandleConfig
from scripts.handle_excel import HandleExcel
from scripts.handle_context import HandleContext
from scripts.handle_mysql import HandleMySql
from scripts.handle_logging import HandleLog
from scripts.handle_webservice_request import HandleWebserviceRequest
# 日志收集器
do_log = HandleLog().get_logger()
# 参数化操作对象
do_context = HandleContext()

# 配置文件操作对象
do_conf = HandleConfig(os.path.join(CONFIG_FILE_PATH, "api_config.ini"))
# excel文件操作对象
do_excel = HandleExcel(os.path.join(EXCEL_FILE_PATH, "webservice_api_test_cases.xlsx"), "verifeduserauth")
cases = do_excel.get_all_case()


@ddt
class TestUserAuth(unittest.TestCase):
    """
    测试实名认证接口封装类
    """
    @classmethod
    def setUpClass(cls):
        do_log.debug("{:=^50s}".format("实名认证接口测试用例开始执行"))
        sendcode_url = do_conf.get_data("interface url", "sendmcode_api_url")
        regist_url = do_conf.get_data("interface url", "register_api_url")
        userauth_url = do_conf.get_data("interface url", "userauth_api_url")

        cls.do_request_sendcode = HandleWebserviceRequest(sendcode_url)
        cls.do_request_regist = HandleWebserviceRequest(regist_url)
        cls.do_request_verify = HandleWebserviceRequest(userauth_url)
        # cls.sendcode_client = Client(sendcode_url)
        # cls.regist_client = Client(regist_url)
        # cls.userauth_client = Client(userauth_url)
        # 创建MySQL对象
        cls.do_sql = HandleMySql()
        pass

    @classmethod
    def tearDownClass(cls):
        cls.do_sql.close()  # 关闭MySQL游标、连接
        do_log.debug("{:=^50s}".format("实名认证接口测试用例执行结束"))
        pass

    @data(*cases)
    def test_verify_user_auth(self, case):
        """
        测试实名认证接口方法
        :param case:
        :return:
        """
        do_log.debug("{:*^50s}".format(case['title']))
        # 参数的参数化
        param = json.loads(do_context.verify_user_auth_api_parametrization(case['params']))
        do_log.debug(f"请求参数为：【{param}】")
        if case['interface_name'] == "sendMCode":
            res = self.do_request_sendcode.send_request(param, case['interface_name'])
        elif case['interface_name'] == 'userRegister':
            res = self.do_request_regist.send_request(param, case['interface_name'])
        elif case['interface_name'] == 'verifyUserAuth':
            res = self.do_request_verify.send_request(param, case['interface_name'])
        else:
            res = "接口名称不正确"
        do_log.debug(f"请求响应结果为:【{res}】")

        # try:
        #     # 根据参数中的键值判断要调用哪个接口
        #     if "uid" in param:
        #         # 请求实名认证接口
        #         res = self.userauth_client.service.verifyUserAuth(param)
        #     elif "verify_code" in param:
        #         # 请求注册接口
        #         res = self.regist_client.service.userRegister(param)
        #     else:
        #         # 请求发送验证码接口
        #         res = self.sendcode_client.service.sendMCode(param)
        #     res = json.dumps(dict(res), ensure_ascii=False)
        #     do_log.debug(f"请求响应结果为：【{res}】")
        # except Exception as e:
        #     # 在调用发送短信验证码接口时，如果失败则会抛异常，此处为捕获异常并处理结果
        #     res = json.dumps(dict(e.fault), ensure_ascii=False)
        #     do_log.debug(f"请求响应结果为：【{res}】")

        try:
            # 断言结果
            self.assertEqual(case['expected'], res)
            if case['interface_name'] == "sendMCode":
                # 如果为发送短信验证码接口，则需到数据库中查询验证码并保存
                HandleContext.mobile = param['mobile']
                # 因已经将号码的后三位固定为495，所以库名后缀为95，表名后缀为4
                sql = "select Fverify_code from sms_db_95.t_mvcode_info_4 where Fmobile_no=%s"
                # 将查询出来的验证码动态生成为HandleContext类的类属性，以便注册接口参数化使用
                HandleContext.verify_code = self.do_sql.execute_sql(sql, args=(HandleContext.mobile,))['Fverify_code']
                do_log.debug(f"动态生成的手机号码：【{HandleContext.mobile}】，获取的验证码为：【{HandleContext.verify_code}】")
            elif case['interface_name'] == 'userRegister':
                # 如果为注册接口，则需到数据库中查询用户id并保存
                # 查询出用户注册后的uid---取最新的数据
                sql = "select Fuid from user_db.t_user_info order by Fuid desc limit 1"
                result = self.do_sql.execute_sql(sql)
                HandleContext.uid = result['Fuid']
                do_log.debug(f"注册成功用户的uid为：【{HandleContext.uid}】")
            # 数据校验
            result_dict = {}   # 用于存放数据校验结果
            if case['check_sql']:
                check_result = self.do_sql.execute_sql(case['check_sql'], args=(param['uid'], param['true_name']))
                if check_result:
                    # 影响数据表的行数
                    result_dict['effect_line_num'] = check_result['num']
            if result_dict:
                do_excel.write_in_excel(row=case['case_id'], actual=res, result="Pass", check_result=json.dumps(result_dict))
            else:
                do_excel.write_in_excel(row=case['case_id'], actual=res, result="Pass")
            do_log.debug(f"断言成功，期望结果【{case['expected']}】，实际结果【{res}】")
        except Exception as e:
            do_excel.write_in_excel(row=case['case_id'], actual=res, result="Fail")
            do_log.debug(f"断言失败，期望结果【{case['expected']}】，实际结果【{res}】")
            raise e


if __name__ == '__main__':
    unittest.main()
