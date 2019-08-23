# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 10:30
# @Author  : lyx
# @File    : handle_account.py
# @Project : QianChengDai_API_Project

"""
此模块用来初始时注册管理人、投资人、借款人三个账号，并保存至配置文件中
"""
import json
import os
from scripts.handle_sql import HandleSql
from scripts.handle_request import HandleRequest
from scripts.contants import CONFIG_PATH
from scripts.handle_config import HandleConfig
from scripts.handle_logging import log_operate

conf_operate = HandleConfig(os.path.join(CONFIG_PATH, "account.ini"))
account_file_name = os.path.join(CONFIG_PATH, "account.ini")    # 保存三个账号信息的配置文件名


class HandleAccount:
    """
    该封装类是用来注册管理人、投资人、借款人三个账号，并将其保存至配置文件中的
    """
    def __init__(self):
        self.do_sql = HandleSql()
        self.do_request = HandleRequest()


    def register_member_mobile(self, regname=None):
        """
        注册号码
        :param regname: 昵称  可为空
        :return:
        """
        while True:
            # 调用方法生成未注册过的号码
            mobile = self.do_sql.make_not_registered_mobile()

            # 制造请求参数
            pwd = "abc" + mobile
            data = {"mobilephone": mobile, "pwd": pwd, "regname": regname}

            # 调接口进行注册
            register_api = "/member/register"
            response = self.do_request.send_request(register_api, method="post", data=data)

            # 判断是否注册成功  根据响应结果中的code判断   注册成功则将号码\密码返回，否则继续注册
            # 还需要对实际是否注册成功进行判断，先从数据库中查询新注册的用户信息，如果查询接口不为空则表示注册成功
            sql = "select id from member where mobilephone=%s"
            res = self.do_sql.execute_sql(sql, args=(mobile,))
            if json.loads(response.text)["code"] == "10001" and res:
                # 注册成功则去数据库中查询用户id
                member_id = res['id']
                log_operate.debug(f"生成的未注册账号信息：mobilephone : {mobile}, pwd : {pwd}, id : {member_id}")
                return mobile, pwd, member_id

    def register_manager_investor_borrower_mobile(self):
        """
        注册管理人、投资人、借款人三个账号
        :return:
        """
        member_dict = {"manager": {"regname": "manager", "id": 0, "mobilephone": "", "pwd": ""},
                       "investor": {"regname": "investor", "id": 0, "mobilephone": "", "pwd": ""},
                       "borrower": {"regname": "borrower", "id": 0, "mobilephone": "", "pwd": ""}}
        for value in member_dict.values():
            mobile, pwd, member_id = self.register_member_mobile(value["regname"])
            value["mobilephone"] = mobile
            value["pwd"] = pwd
            value["id"] = member_id
        log_operate.debug(f"新注册的管理人、投资人、借款人三个账号信息为 {member_dict}")
        return member_dict

    @staticmethod
    def write_mobile_in_config(data):
        """
        将data写入配置文件中，data为嵌套字典的字典
        :param data:
        :return:
        """
        conf_operate.write_config_data(data, account_file_name)
        log_operate.info("新注册的管理人、投资人、借款人三个账号写入配置文件成功")

    def close(self):
        """
        关闭session会话、数据库连接，释放资源
        :return:
        """
        self.do_request.session_close()
        self.do_sql.close()


if __name__ == '__main__':
    do = HandleAccount()
    do.write_mobile_in_config(do.register_manager_investor_borrower_mobile())
    do.close()


