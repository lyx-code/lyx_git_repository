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
from scripts.handle_sql import HandleSql

# 创建Excel文件操作对象
do_excel = HandleExcel(os.path.join(EXCEL_PATH, "QianChengDai_interface_cases.xlsx"), "add")

# 获取Excel中加标接口的所有测试用例数据
cases = do_excel.get_all_case()


@ddt
class Test(unittest.TestCase):
    """
    测试充值接口，需要对用户可用余额、流水信息进行验证
    """
    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()   # 将发送请求对象定义为类属性，是为了能在测试结束后关闭session会话，释放资源
        cls.do_sql = HandleSql()  # 建立数据库连接
        log_operate.debug("*******************《加标》接口开始执行测试******************")

    @classmethod
    def tearDownClass(cls):
        cls.do_request.session_close()    # 调用关闭session会话方法，释放资源
        cls.do_sql.close()  # 关闭数据库连接
        log_operate.debug("*******************《加标》接口测试执行完成******************")

    @data(*cases)  # 将cases里的数据一条条传给下面方法
    def test_register(self, case):
        """
        测试AddLoan加标接口
        :param case:
        :return:
        """
        interface_url = case["url"]  # 接口名称
        interface_method = case["method"]   # 接口请求方法
        interface_data = HandleContext.add_loan_api_parameterization(case["data"])   # 接口请求参数 --使用参数化方法参数化
        interface_expect_result = json.loads(case["expected"])   # 期望结果  将取到的字符串期望结果数据转为字典类型
        check_sql_result = {}  # 用来存放数据校验结果

        log_operate.debug(f"=========================={case['title']}用例开始执行===============================")

        # 发送请求前对用户的可用余额、流水记录数量进行查询
        if case["check_sql"]:  # 如果Excel中有校验sql语句则进行校验
            check_sql = json.loads(case["check_sql"])  # sql校验语句
            # 发送请求前，先去数据库中查询该借款人用户是否存在
            search_result = self.do_sql.execute_sql("select Id from member where Id=%s",
                                                    args=(json.loads(interface_data)['memberId'],))
            if search_result:
                # 如果借款人ID存在，则去数据库中查询该借款人用户下的标的数量，以便于后续校验
                search_result = self.do_sql.execute_sql(check_sql['loan_count'],
                                                        args=(json.loads(interface_data)["memberId"],))  # 返回字典类型数据
                if search_result:
                    # search_result["LeaveAmount"]为decimal类型，需要转换为float类型,并保留2位小数
                    before_loan_count = search_result["loan_count"]
                else:
                    before_loan_count = 0
                check_sql_result["before_loan_count"] = before_loan_count
                log_operate.debug(f"发送加标请求前，借款人[id:{json.loads(interface_data)['memberId']}]用户的名下的标数量为{before_loan_count}")

        # 发送请求
        res = self.do_request.send_request(interface_url, interface_method, data=interface_data)
        log_operate.info(f"请求响应结果：{res}{res.text}")

        # 对响应结果进行断言,使用响应结果中的status和code来进行断言
        response_status = json.loads(res.text)["status"]
        response_code = json.loads(res.text)["code"]

        try:
            self.assertEqual(interface_expect_result["status"], response_status)
            self.assertEqual(interface_expect_result["code"], response_code)
            # 另一种断言方法，使用成员运算符的断言
            # self.assertIn(case["excepted"], res.text)
            log_operate.info(f"断言成功：期望status[{interface_expect_result['status']}],"
                             f"code[{interface_expect_result['code']}] 实际结果status[{response_status}],"
                             f"code[{response_code}]")

            # 此处为对数据校验代码
            # 充值请求后，sql查询相应数据库结果
            if case["check_sql"]:
                # 查询借款人用户名下的标数量
                search_result = self.do_sql.execute_sql(check_sql['loan_count'],
                                                        args=(json.loads(interface_data)["memberId"],))
                if search_result['loan_count']:
                    after_loan_count = search_result["loan_count"]
                    check_sql_result["after_loan_count"] = after_loan_count
                    log_operate.debug(
                        f"发送加标请求后，借款人[id:{json.loads(interface_data)['memberId']}]用户的名下的标数量为{after_loan_count}")
                    try:
                        # 此处是为了判断在数据库中是否加标成功
                        self.assertEqual((after_loan_count - before_loan_count), 1)
                        loan_info = self.do_sql.execute_sql(check_sql['loan_info'], args=(json.loads(interface_data)['memberId'], json.loads(interface_data)['title']))
                        check_sql_result["new_loan_info"] = {"id": loan_info['Id'], "title": loan_info['Title'], "memberid": loan_info['MemberID'], "amount": float(loan_info['Amount'])}
                        log_operate.info(
                            f"发送加标请求后，数据库中对应标记录生成成功，信息为{loan_info}")
                    except AssertionError:
                        check_sql_result["new_loan_info"] = None
                        log_operate.error("发送加标请求后，数据库中未生成对应标记录")
                else:
                    check_sql_result["new_loan_info"] = None
                    log_operate.error("发送加标请求后，数据库中未生成对应标记录")
            # 断言成功，将结果（包括数据校验结果）写入Excel文件中
            do_excel.write_data_in_excel(case["case_id"] + 1, res.text, "PASS", json.dumps(check_sql_result))
        except AssertionError as e:
            log_operate.error(f"断言失败：期望status[{interface_expect_result['status']}],"
                              f"code[{interface_expect_result['code']}]  "
                              f"实际结果status[{response_status}],code[{response_code}]")
            # 断言失败，将结果写入Excel文件中
            do_excel.write_data_in_excel(case["case_id"] + 1, res.text, "FAIL")
            # 手动抛出异常，unittest框架才能统计用例失败数量
            raise e
        log_operate.debug(f"=============================={case['title']}用例执行结束================================")


if __name__ == '__main__':
    unittest.main()