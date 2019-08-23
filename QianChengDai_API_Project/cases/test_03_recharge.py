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
do_excel = HandleExcel(os.path.join(EXCEL_PATH, "QianChengDai_interface_cases.xlsx"), "recharge")

# 获取Excel中充值接口的所有测试用例数据
cases = do_excel.get_all_case()


@ddt
class TestRecharge(unittest.TestCase):
    """
    测试充值接口，需要对用户可用余额、流水信息进行验证
    """
    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()   # 将发送请求对象定义为类属性，是为了能在测试结束后关闭session会话，释放资源
        cls.do_sql = HandleSql()  # 建立数据库连接
        log_operate.debug("*******************《充值》接口开始执行测试******************")

    @classmethod
    def tearDownClass(cls):
        cls.do_request.session_close()    # 调用关闭session会话方法，释放资源
        cls.do_sql.close()  # 关闭数据库连接
        log_operate.debug("*******************《充值》接口测试执行完成******************")

    @data(*cases)  # 将cases里的数据一条条传给下面方法
    def test_register(self, case):
        """
        测试充值接口
        :param case:
        :return:
        """
        interface_url = case["url"]  # 接口名称
        interface_method = case["method"]   # 接口请求方法
        interface_data = HandleContext.recharge_api_parameterization(case["data"])   # 接口请求参数 --使用参数化方法参数化
        interface_expect_result = json.loads(case["expected"])   # 期望结果  将取到的字符串期望结果数据转为字典类型
        check_sql_result = {}  # 用来存放数据校验结果

        log_operate.debug(f"=========================={case['title']}用例开始执行===============================")

        # 发送请求前对用户的可用余额、流水记录数量进行查询
        if case["check_sql"]:  # 如果Excel中有校验sql语句则进行校验
            check_sql = json.loads(case["check_sql"])  # sql校验语句
            # 发送请求前，先去数据库中查询用户账号的可用额度以及流水记录数量，以便于后续校验
            search_amount_result = self.do_sql.execute_sql(check_sql["LeaveAmount"],
                                                           args=(json.loads(interface_data)["mobilephone"],))  # 返回字典类型数据
            if search_amount_result:
                # search_result["LeaveAmount"]为decimal类型，需要转换为float类型,并保留2位小数
                before_leave_amount = round(float(search_amount_result["LeaveAmount"]), 2)
                check_sql_result["before_leave_amount"] = before_leave_amount
                log_operate.debug(f"发送充值请求前，用户的可用余额为{before_leave_amount}")

            # 流水记录数量
            search_result = self.do_sql.execute_sql("select Id from member where mobilephone=%s",
                                                    args=(json.loads(interface_data)["mobilephone"],))

            search_financelog_count = self.do_sql.execute_sql(check_sql["financelog_count"],
                                                              args=(search_result["Id"], search_result["Id"]))
            if search_financelog_count:
                before_financelog_count = search_financelog_count["financelog_count"]
                check_sql_result['before_financelog_count'] = before_financelog_count
                log_operate.debug(f"发送充值请求前，用户所有流水记录数量为：[{before_financelog_count}]")
            else:
                check_sql_result['before_financelog_count'] = 0

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
                for key, value in check_sql.items():  # 针对所有的sql语句进行查询
                    if key == "LeaveAmount":
                        # 查询用户可用余额
                        search_result = self.do_sql.execute_sql(value,
                                                                args=(json.loads(interface_data)["mobilephone"],))
                        if search_result:  # 此处是为了处理所传投资人ID不存在或错误的情况
                            after_leave_amount = round(float(search_result["LeaveAmount"]), 2)
                            check_sql_result["after_leave_amount"] = after_leave_amount
                            log_operate.debug(f"发送充值请求后，用户的可用余额为{after_leave_amount}")
                            try:
                                # 对投资后用户账户前后可用余额的变化值与实际请求参数中投资金额断言
                                # 此处是为了判断在投资成功的时候，用户可用余额的变化情况
                                self.assertEqual(round((after_leave_amount - before_leave_amount), 2),float(json.loads(interface_data)["amount"]))
                                log_operate.info(f'发送充值请求后，账号可用余额正常增加，金额为:'
                                                 f'{after_leave_amount - before_leave_amount}')
                                check_sql_result["increase_amount"] = round((after_leave_amount - before_leave_amount), 2)
                            except AssertionError:
                                try:
                                    # 此处是为了判断在投资失败的时候，用户可用余额的变化情况
                                    self.assertEqual(round((after_leave_amount - before_leave_amount), 2), 0.00)
                                    check_sql_result["increase_amount"] = round(after_leave_amount - before_leave_amount, 2)
                                    log_operate.info(f"发送充值请求后，账号可用余额未增加,剩余可用金额为:{after_leave_amount}")
                                except AssertionError:
                                    check_sql_result["increase_amount"] = round(after_leave_amount - before_leave_amount, 2)
                                    log_operate.error(f'发送充值请求后，账号可用余额增加金额不正确，增加金额为'
                                                      f'{after_leave_amount - before_leave_amount}')
                        else:
                            log_operate.error(f"充值的投资人mobile[{json.loads(interface_data)['mobilephone']}]错误，未查到该用户的记录")

                    if key == "financelog":
                        # 查询充值流水
                        # 先查询用户ID
                        search_result = self.do_sql.execute_sql("select Id from member where mobilephone=%s", args=(json.loads(interface_data)["mobilephone"],))
                        if search_result:  # 如果该用户存在则继续查询
                            # 查询发送请求后的流水记录数量
                            search_financelog_count = self.do_sql.execute_sql(check_sql["financelog_count"],
                                                                              args=(search_result["Id"], search_result["Id"]))
                            if search_financelog_count:  # 如果该用户有流水记录则继续
                                after_financelog_count = search_financelog_count["financelog_count"]
                                check_sql_result['after_financelog_count'] = after_financelog_count
                                if after_financelog_count - before_financelog_count == 1:
                                    # 如果有生成新的流水则在查询投资流水详细信息
                                    finance_log = self.do_sql.execute_sql(value,
                                                                          args=(
                                                                          json.loads(interface_data)["memberId"],))
                                    check_sql_result['financelog_info'] = finance_log
                                    log_operate.debug(f"投资流水为：{finance_log}")
                                else:
                                    log_operate.debug("没有生成新的流水信息")
                            else:
                                check_sql_result['after_financelog_count'] = 0
                                log_operate.debug(f"用户{json.loads(interface_data)['mobilephone']}还没有流水记录哦")
                        else:
                            log_operate.debug(f"用户{json.loads(interface_data)['mobilephone']}不存在哦")
            # 断言成功，将结果写入Excel文件中
            if len(check_sql_result):
                do_excel.write_data_in_excel(case["case_id"] + 1, res.text, "PASS", json.dumps(check_sql_result))
            else:
                do_excel.write_data_in_excel(case["case_id"] + 1, res.text, "PASS")

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
