# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 17:08
# @Author  : lyx
# @File    : handle_context.py
# @Project : WebService_Api_Test
# 此模块为处理请求参数的参数化

import re
import random
from scripts.handle_mysql import HandleMySql


class HandleContext:
    """
    处理请求参数的参数化封装类
    """
    not_registed_mobile_pattern = r"\${not_registed_mobile}"   # 未注册手机号模式
    exited_mobile_pattern = r"\${exited_mobile}"               # 已获取验证码的号码模式
    verify_code_pattern = r"\${verify_code}"                   # 验证码模式
    not_registed_user_id_pattern = r"\${user_id}"                           # user_id模式
    registed_user_id_pattern = r"\${registed_user_id}"
    uid_pattern = r"\${uid}"                                   # 用户uid模式
    true_name_pattern = r"\${true_name}"                       # 真实姓名模式
    cre_id_pattern = r"\${cre_id}"
    cre_id = ["511823198401103576", "511823198401103218", "511823198401109871", "511823198401109150", "511823198401101378",
              "511823198401103891", "511823198401106574", "511823198401109353", "511823198401108350", "511823198401103939",
              "511823198401101159", "511823198401108553", "511823198401102055", "511823198401105096", "511823198401106013",
              "511823198401106339", "511823198401108430", "511823198401107518", "511823198401105571", "511823198401101618",
              "51182319840110689X", "511823198401107155"]

    @classmethod
    def not_registed_mobile_replace(cls, data):
        """
        未注册的手机号参数化
        :param data:
        :return:
        """
        if re.search(cls.not_registed_mobile_pattern, data):
            do_sql = HandleMySql()
            mobile = do_sql.make_not_registed_mobile()
            data = re.sub(cls.not_registed_mobile_pattern, mobile, data)
            do_sql.close()
        return data

    @classmethod
    def exited_mobile_replace(cls, data):
        """
        已获取验证码的手机号参数化
        :param data:
        :return:
        """
        if re.search(cls.exited_mobile_pattern, data):
            data = re.sub(cls.exited_mobile_pattern, cls.mobile, data)
        return data

    @classmethod
    def verify_code_replace(cls, data):
        """
        验证码参数化
        :param data:
        :return:
        """
        if re.search(cls.verify_code_pattern, data):
            data = re.sub(cls.verify_code_pattern, cls.verify_code, data)
        return data

    @classmethod
    def not_registed_user_id_replace(cls, data):
        """
        user_id(姓名）参数化---未注册过的用户名
        :param data:
        :return:
        """
        if re.search(cls.not_registed_user_id_pattern, data):
            user_id = "lyx_test" + str(random.randint(1, 10000))
            data = re.sub(cls.not_registed_user_id_pattern, user_id, data)
        return data

    @classmethod
    def registed_user_id_replace(cls, data):
        if re.search(cls.registed_user_id_pattern, data):
            data = re.sub(cls.registed_user_id_pattern, cls.user_id, data)
        return data

    @classmethod
    def uid_replace(cls, data):
        """
        用户uid参数化
        :param data:
        :return:
        """
        if re.search(cls.uid_pattern, data):
            data = re.sub(cls.uid_pattern, str(cls.uid), data)
        return data

    @classmethod
    def cre_id_replace(cls, data):
        """
        身份证号参数化
        :param data:
        :return:
        """
        if re.search(cls.cre_id_pattern, data):
            cre_id = random.choice(cls.cre_id)
            data = re.sub(cls.cre_id_pattern, cre_id , data)
        return data

    @classmethod
    def register_api_parametrization(cls, data):
        """
        注册接口参数的参数化
        :param data:
        :return:
        """
        data = cls.not_registed_mobile_replace(data)
        data = cls.exited_mobile_replace(data)
        data = cls.verify_code_replace(data)
        data = cls.not_registed_user_id_replace(data)
        data = cls.registed_user_id_replace(data)
        return data

    @classmethod
    def verify_user_auth_api_parametrization(cls, data):
        """
        实名认证接口参数的参数化
        :param data:
        :return:
        """
        data = cls.not_registed_mobile_replace(data)
        data = cls.verify_code_replace(data)
        data = cls.exited_mobile_replace(data)
        data = cls.not_registed_user_id_replace(data)
        data = cls.uid_replace(data)
        data = cls.cre_id_replace(data)
        return data


