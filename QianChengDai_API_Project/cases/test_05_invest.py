# -*- coding: utf-8 -*-
# @Time    : 2019/8/9 11:30
# @Author  : lyx
# @File    : test_03_invest.py
# @Project : QianChengDai_API_Project

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
do_excel = HandleExcel(os.path.join(EXCEL_PATH, "QianChengDai_interface_cases.xlsx"), "invest")

cases = do_excel.get_all_case()


@ddt
class InvestTest(unittest.TestCase):
    """
    测试投资接口---使用的标id依赖于管理人加标、审核接口后的标id
    接口之间存在依赖关系的，应做到接口测试之间的独立性，在单个接口测试中完所要依赖接口的数据
    """
    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()   # 将发送请求对象定义为类属性，是为了能在测试结束后关闭session会话，释放资源
        cls.do_sql = HandleSql()    # 建立数据库连接
        log_operate.debug("*******************《投资》接口测试开始测试******************")

    @classmethod
    def tearDownClass(cls):
        cls.do_request.session_close()    # 调用关闭session会话方法，释放资源
        cls.do_sql.close()     # 关闭数据库连接
        log_operate.debug("*******************《投资》接口测试执行完成******************")

    @data(*cases)
    def test_invest(self, case):
        """
        测试投资接口，需要对数据库中用户可用余额、投资记录、流水记录信息进行验证
        :param case:
        :return:
        """
        interface_url = case["url"]  # 接口名称
        interface_method = case["method"]   # 接口请求方法
        interface_data = HandleContext.invest_api_parameterization(case["data"])   # 接口请求参数 --使用参数化方法参数化
        interface_expect_result = json.loads(case["expected"])  # 期望结果  使用loads()方法将取到的字符串期望结果数据转为字典类型
        check_sql_result = {}  # 用来存放数据校验结果
        log_operate.debug(f"=========================={case['title']}用例开始执行===============================")

        if case["check_sql"] and "LeaveAmount" in case["check_sql"]:  # 如果Excel中有校验sql语句则进行校验
            check_sql = json.loads(case["check_sql"])  # sql校验语句
            # 发送请求前，先去数据库中查询用户账号的可用额度以及用户所有正常状态下的投资记录和流水记录数量，以便于后续校验
            search_amount_result = self.do_sql.execute_sql(check_sql["LeaveAmount"],
                                                          args=(json.loads(interface_data)["memberId"],))  # 返回字典类型数据
            if search_amount_result:
                # search_result["LeaveAmount"]为decimal类型，需要转换为float类型,并保留2位小数
                before_leave_amount = round(float(search_amount_result["LeaveAmount"]), 2)
                check_sql_result["before_leave_amount"] = before_leave_amount
                log_operate.debug(f"发送投资请求前，用户的可用余额为{before_leave_amount}")

            # 投资记录数量
            search_recode_count = self.do_sql.execute_sql(check_sql["invest_recode_count"], args=(json.loads(interface_data)["memberId"],))
            if search_recode_count:
                before_invest_recode_count = search_recode_count["invest_recode_count"]
                log_operate.debug(f"发送投资请求前，用户所有正常状态下的投资记录个数为：[{before_invest_recode_count}]")

            # 流水记录数量
            search_financelog_count = self.do_sql.execute_sql(check_sql["financelog_count"],
                                                          args=(json.loads(interface_data)["memberId"], json.loads(interface_data)["memberId"]))
            if search_financelog_count:
                before_financelog_count = search_financelog_count["financelog_count"]
                log_operate.debug(f"发送投资请求前，用户所有流水记录数量为：[{before_financelog_count}]")

        # 发送投资请求
        res = self.do_request.send_request(interface_url, interface_method, data=interface_data)
        log_operate.info(f"请求响应结果：{res}{res.text}")

        # 在管理人加标成功后，查询数据库保存该标的id，以便后续使用
        # 按照加标接口返回结果中的msg判断是否为加标成功
        if "加标成功" in res.text:
            search_result = self.do_sql.execute_sql(case['check_sql'],
                                                    args=(json.loads(interface_data)["memberId"],))
            if search_result:
                # 如果第一个参数是实例对象，那么会为这个实例对象创建一个实例属性，第二个参数为属性名，第三个参数是属性值
                # 如果第一个参数是类，则会创建一个类属性
                # 这里动态创建HandleContex类属性，这样在handle_context.py文件的HandleContext类中就可以实时的获取到loan_id
                setattr(HandleContext, "loan_id", search_result['Id'])

        # 对响应结果进行断言，使用响应结果中的status和code字段进行断言
        # 此处有另一种可能出错的地方，接口返回结果不一定是json格式，如果响应码不是200，则可能是一个html页面，
        # 这时候进行loads()转换就会报错-----可以使用assertIn断言方法
        # response_status = json.loads(res.text)["status"]
        # response_code = json.loads(res.text)["code"]

        try:
            # self.assertEqual(interface_expect_result["status"], response_status)
            # self.assertEqual(interface_expect_result["code"], response_code)
            # 使用assertIn比使用assertEqual更合适，因为接口返回结果可能是html，而非json
            self.assertIn(interface_expect_result["code"], res.text)
            log_operate.info(f"断言成功：期望status[{interface_expect_result['status']}],"
                             f"code[{interface_expect_result['code']}] 实际响应结果[res.text]")

            # 此处为对数据校验代码
            # 投资请求后，sql查询相应数据库结果
            if case["check_sql"] and "LeaveAmount" in case["check_sql"]:
                for key, value in check_sql.items():  # 针对所有的sql语句进行查询
                    if key == "LeaveAmount":
                        # 查询用户可用余额
                        search_result = self.do_sql.execute_sql(value,
                                                                args=(json.loads(interface_data)["memberId"],))
                        if search_result:  # 此处是为了处理所传投资人ID不存在或错误的情况
                            after_leave_amount = round(float(search_result["LeaveAmount"]),2)
                            check_sql_result["after_leave_amount"] = after_leave_amount
                            log_operate.debug(f"发送投资请求后，用户的可用余额为{after_leave_amount}")
                            try:
                                # 对投资后用户账户前后可用余额的变化值与实际请求参数中投资金额断言
                                # 此处是为了判断在投资成功的时候，用户可用余额的变化情况
                                self.assertEqual((before_leave_amount - after_leave_amount),
                                                 json.loads(interface_data)["amount"])
                                check_sql_result["decrease_amount"] = round(before_leave_amount - after_leave_amount, 2)
                                log_operate.info(f'发送投资请求后，账号可用余额正常减少，金额为:'
                                                 f'{before_leave_amount - after_leave_amount}')
                            except AssertionError:
                                try:
                                    # 此处是为了判断在投资失败的时候，用户可用余额的变化情况
                                    self.assertEqual((before_leave_amount - after_leave_amount),0)
                                    check_sql_result["decrease_amount"] = round(before_leave_amount - after_leave_amount, 2)
                                    log_operate.info(f"发送投资请求后，账号可用余额未减少,剩余可用金额为:{after_leave_amount}")
                                except AssertionError:
                                    check_sql_result["decrease_amount"] = round(before_leave_amount - after_leave_amount, 2)
                                    log_operate.error(f'发送投资请求后，账号可用余额减少金额不正确，减少金额为'
                                                  f'{(before_leave_amount - after_leave_amount)}')
                        else:
                            log_operate.error(f"投资人id[{json.loads(interface_data)['memberId']}]错误，未查到该用户的记录")

                    if key == "invest_recode":
                        # 查询投资记录
                        # 查询发送请求后的投资记录数量
                        search_recode_count = self.do_sql.execute_sql(check_sql["invest_recode_count"], args=(json.loads(interface_data)["memberId"],))
                        after_invest_recode_count = search_recode_count["invest_recode_count"]
                        if after_invest_recode_count - before_invest_recode_count == 1:
                            # 如果有生成新的投资记录则在查询投资记录详细信息
                            invest_recode = self.do_sql.execute_sql(value,
                                                                    args=(json.loads(interface_data)["memberId"],
                                                                          json.loads(interface_data)["loanId"]))
                            # 将返回的字典中的decimal类型和datetime数据都转为字符串类型，否则在转为json写入Excel时候会报错
                            invest_recode["Amount"] = float(invest_recode["Amount"])
                            invest_recode["CreateTime"] = invest_recode["CreateTime"].strftime("yyyy-MM-dd HH:mm:ss")
                            check_sql_result["new_invest_recode"] = invest_recode
                            log_operate.debug(f"生成的投资记录为：{invest_recode}")
                        else:
                            check_sql_result["new_invest_recode"] = None
                            log_operate.debug(f"没有生成新的投资记录信息")

                    if key == "financelog":
                        # 查询投资流水
                        # 查询发送请求后的流水记录数量
                        search_financelog_count = self.do_sql.execute_sql(check_sql["financelog_count"],
                                                                      args=(json.loads(interface_data)["memberId"],
                                                                            json.loads(interface_data)["memberId"]))
                        after_financelog_count = search_financelog_count["financelog_count"]
                        if after_financelog_count - before_financelog_count == 1:
                            # 如果有生成新的流水则在查询投资流水详细信息
                            finance_log = self.do_sql.execute_sql(value, args=(json.loads(interface_data)["memberId"],))
                            # 将返回的字典中的decimal类型和datetime数据都转为字符串类型，否则在转为json写入Excel时候会报错
                            finance_log["Amount"] = float(finance_log["Amount"])
                            finance_log["IncomeMemberMoney"] = float(finance_log["IncomeMemberMoney"])
                            finance_log["PayMemberMoney"] = float(finance_log["PayMemberMoney"])
                            finance_log["CreateTime"] = finance_log["CreateTime"].strftime("yyyy-MM-dd HH:mm:ss")
                            check_sql_result["new_financelog"] =finance_log
                            log_operate.debug(f"投资流水为：{finance_log}")
                        else:
                            check_sql_result["new_financelog"] = None
                            log_operate.debug("没有生成新的流水信息")
                    if key == "Loan_status":
                        # 查询标状态
                        loan_status = self.do_sql.execute_sql(value, args=(json.loads(interface_data)["loanId"],))
                        if loan_status:
                            log_operate.info(f"该用户投资的标[id:{json.loads(interface_data)['loanId']}]的状态为：{loan_status} "
                                             f"参考：1:审核中 2:二审(初 审中) 3:三审(复审中) 4: 竞标中 5:核保审批 6:平台 终审 "
                                             f"7:还款中 8:审核不通 过 9:流 标 10:还 款 完 成 11：申请流标")
                        else:
                            log_operate.info(f"该用户投资的标[id:{json.loads(interface_data)['loanId']}]的不存在")
                    if key == "Loan_status_Amount":
                        # 用户所投的标的状态和标的额度
                        loan_status_amount = self.do_sql.execute_sql(value,
                                                                     args=(json.loads(interface_data)["loanId"],))
                        if loan_status_amount:
                            log_operate.info(f"该用户投资的标[id:{json.loads(interface_data)['loanId']}]的状态为：[{loan_status_amount['Status']}] "
                                                     f"参考：1:审核中 2:二审(初 审中) 3:三审(复审中) 4: 竞标中 5:核保审批 6:平台 终审 "
                                                     f"7:还款中 8:审核不通 过 9:流 标 10:还 款 完 成 11：申请流标")
                            log_operate.info(f"用户投资的标[id:{json.loads(interface_data)['loanId']}]的状态与可投金额为：[{loan_status_amount['Amount']}]")
                    if key == "Loan_Amount_invested":
                        # 用户所投的标的已经投资的额度
                        loan_amount = self.do_sql.execute_sql("select Amount from loan where id=%s",
                                                              args=(json.loads(interface_data)["loanId"],))
                        loan_amount_invested = self.do_sql.execute_sql(value,
                                                                       args=(json.loads(interface_data)["loanId"],))
                        if loan_amount:
                            if loan_amount_invested:
                                log_operate.info(f"用户投资的标[id:{json.loads(interface_data)['loanId']}]的已投资金额为：{loan_amount_invested}")
                                log_operate.info(
                                    f"该标[id:{json.loads(interface_data)['loanId']}]剩余的可投金额为：{loan_amount['Amount'] - loan_amount_invested['invested_amount']}")
                            else:
                                log_operate.info("用户投资的标的还没有被投资")
                                log_operate.info(
                                    f"该标[id:{json.loads(interface_data)['loanId']}]剩余的可投金额为：{loan_amount['Amount']}")
            if len(check_sql_result):
                do_excel.write_data_in_excel(case["case_id"] + 1, res.text, "PASS", json.dumps(check_sql_result))
            else:
                do_excel.write_data_in_excel(case["case_id"] + 1, res.text, "PASS")
        except AssertionError as e:
            log_operate.error(f"断言失败：期望status[{interface_expect_result['status']}],"
                              f"code[{interface_expect_result['code']}]  "
                              f"实际响应结果[res.text]")
            do_excel.write_data_in_excel(case["case_id"] + 1, res.text, "FAIL")
            raise e

        log_operate.debug(f"=============================={case['title']}用例执行结束================================")


if __name__ == '__main__':
    unittest.main()
