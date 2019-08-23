# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 18:00
# @Author  : lyx
# @File    : handle_context.py
# @Project : QianChengDai_API_Project
"""
该模块用来处理测试数据的参数化
"""
import re
import os
from scripts.handle_sql import HandleSql
from scripts.handle_config import HandleConfig
from scripts.contants import CONFIG_PATH

# config_file = config_dir + "\\" + "mobile.ini"   # 这种拼接路径方法容易忘掉中间加上\
mobile_config_file = os.path.join(CONFIG_PATH, "account.ini")  # 要保存管理人、投资人、借款人三个账号的配置文件
do_conf = HandleConfig(mobile_config_file)


class HandleContext:
    """
    处理测试数据参数化
    """
    # 将excel中data(参数)中的要匹配的模式都定义为类属性
    not_register_mobile_patten = r"\${not_register_mobile}"  # 未注册的号码 模式字符串
    investor_mobile_patten = r"\${investor_mobile}"          # 投资人号码 模式字符串
    investor_pwd_patten = r"\${investor_pwd}"        # 投资人账号密码 模式字符串
    investor_id_patten = r"\${investor_ID}"    # 投资人id 模式字符串
    ing_loanid_patten = r"\${ing_loan_ID}"     # 竞标中状态的标id 模式字符串
    not_ready_loanid_patten = r"\${not_ready_loan_ID}"  # 不在竞标中状态的标id 模式字符串
    already_loanid_patten = r"\${already_loan_ID}"      # 已满标状态的标id 模式字符串
    manager_mobile_pattern = r"\${manager_mobile}"    # 管理人号码 模式字符串
    manager_pwd_pattern = r"\${manager_pwd}"          # 管理人账号密码模式字符串
    borrower_id_pattern = r"\${borrower_id}"          # 借款人ID 模式字符串
    loan_id_pattern = r"\${loan_id}"          # 标id 模式字符串

    @classmethod
    def not_register_mobile_replace(cls, data):
        """
        替换未注册号码的参数化方法---所有需要替换未注册号码的接口都可以调用该方法，实现重用
        :param data:  原始数据
        :return:
        """
        # 先判断原始字符串中是否能匹配到
        if re.search(cls.not_register_mobile_patten, data):
            # 如果能匹配到，则创建HandleSql对象、使用sub()方法替换
            # 在此处创建HandleSql对象，原因是：如果原始字符串中匹配不到则不需要创建mysql连接，只有需要替换时才创建连接，可以提高性能
            do_sql = HandleSql()
            data = re.sub(cls.not_register_mobile_patten, do_sql.make_not_registered_mobile(), data)
            do_sql.close()  # 一定要记住关闭连接
        return data

    @classmethod
    def investor_mobile_replace(cls, data):
        """
        替换投资人号码的参数化方法，投资人号码有单独模块handle_account.py注册后保存至配置文件中，号码直接从配置文件中取就可以
        :param data: 原始数据
        :return:
        """
        # 先判断原始字符串中是否能匹配到
        if re.search(cls.investor_mobile_patten, data):
            # 如果能匹配到，则使用sub()方法替换
            # 从配置文件中取出投资人号码 进行替换
            investor_mobile1 = do_conf.get_config_data("investor", "mobilephone")
            data = re.sub(cls.investor_mobile_patten, investor_mobile1, data)
        return data

    @classmethod
    def investor_pwd_replace(cls, data):
        """
        替换投资人账号密码的参数化方法---密码从配置文件中取出
        :param data:
        :return:
        """
        # 先判断原始字符串中是否能匹配到
        if re.search(cls.investor_pwd_patten, data):
            # 如果能匹配到，则使用sub()方法替换
            # 从配置文件中取出投资人账号密码 进行替换
            investor_pwd = do_conf.get_config_data("investor", "pwd")
            data = re.sub(cls.investor_pwd_patten, investor_pwd, data)
        return data

    @classmethod
    def investor_id_replace(cls, data):
        """
        投资人id参数化方法 ---id从配置文件中获取
        :param data:
        :return:
        """
        # 先判断原始字符串中是否能匹配到
        if re.search(cls.investor_id_patten, data):
            # 如果能匹配到，则使用sub()方法替换
            # 从配置文件中取出投资人账号密码 进行替换
            investor_id = do_conf.get_config_data("investor", "id")
            data = re.sub(cls.investor_id_patten, investor_id, data)
        return data

    @classmethod
    def manager_mobile_replace(cls, data):
        """
        管理人号码参数化
        :param data:
        :return:
        """
        if re.search(cls.manager_mobile_pattern, data):
            data = re.sub(cls.manager_mobile_pattern, do_conf.get_config_data("manager", "mobilephone"), data)
        return data

    @classmethod
    def manager_pwd_replace(cls, data):
        """
        管理人账号密码参数化
        :param data:
        :return:
        """
        if re.search(cls.manager_pwd_pattern, data):
            data = re.sub(cls.manager_pwd_pattern, do_conf.get_config_data("manager", "pwd"), data)
        return data

    @classmethod
    def borrower_id_replace(cls, data):
        """
        借款人ID参数化
        :param data:
        :return:
        """
        if re.search(cls.borrower_id_pattern, data):
            data = re.sub(cls.borrower_id_pattern, do_conf.get_config_data("borrower", "id"), data)
        return data

    # @classmethod
    # def ing_loanid_replace(cls, data):
    #     """
    #     竞标中状态的标id参数化
    #     :param data:
    #     :return:
    #     """
    #     if re.search(cls.ing_loanid_patten, data):
    #         sql = "select Id, Amount from loan where Status = 4 order by Id desc limit 1;"
    #         do_sql = HandleSql()
    #         # 要替换的新字符串必须为字符串类型
    #         data = re.sub(cls.ing_loanid_patten, str(do_sql.execute_sql(sql)['Id']), data)
    #         do_sql.close()
    #     return data

    @classmethod
    def not_ready_loanid_replace(cls, data):
        """
        非竞标中状态(不包括满标状态)的标id参数化
        :param data:
        :return:
        """
        if re.search(cls.not_ready_loanid_patten, data):
            sql = "select Id from loan where Status not in (4, 7) order by Id desc limit 1;"
            do_sql = HandleSql()
            data = re.sub(cls.not_ready_loanid_patten, str(do_sql.execute_sql(sql)['Id']), data)
            do_sql.close()
        return data

    @classmethod
    def loan_id_replace(cls, data):
        if re.search(cls.loan_id_pattern, data):
            # getattr 获取属性值
            loan_id = str(getattr(HandleContext, "loan_id"))
            data = re.sub(cls.loan_id_pattern, loan_id, data)
        return data

    @classmethod
    def already_loanid_replace(cls, data):
        """
        已满标状态的标id参数化
        :param data:
        :return:
        """
        if re.search(cls.already_loanid_patten, data):
            sql = "select Id from loan where Status = 7 order by Id desc limit 1;"
            do_sql = HandleSql()
            data = re.sub(cls.already_loanid_patten, str(do_sql.execute_sql(sql)['Id']), data)
            do_sql.close()
        return data

    @classmethod
    def register_api_parameterization(cls, data):
        """
        注册接口参数的参数化
        :param data:
        :return:
        """
        # 一一调用注册接口参数中所有的模式替换方法（如果参数中有多个模式匹配，则可全部替换完成）
        data = cls.not_register_mobile_replace(data)
        data = cls.investor_mobile_replace(data)
        # 将参数化后的参数返回
        return data

    @classmethod
    def login_api_parameterization(cls, data):
        """
        登录接口参数的参数化
        :param data: 原始参数
        :return:
        """
        data = cls.not_register_mobile_replace(data)
        data = cls.investor_mobile_replace(data)
        data = cls.investor_pwd_replace(data)
        return data

    @classmethod
    def invest_api_parameterization(cls, data):
        """
        投资接口参数的参数化
        :param data:
        :return:
        """
        data = cls.manager_mobile_replace(data)
        data = cls.manager_pwd_replace(data)
        data = cls.borrower_id_replace(data)
        data = cls.loan_id_replace(data)
        data = cls.investor_mobile_replace(data)
        data = cls.investor_pwd_replace(data)
        data = cls.investor_id_replace(data)
        # data = cls.ing_loanid_replace(data)
        data = cls.not_ready_loanid_replace(data)
        data = cls.already_loanid_replace(data)
        return data

    @classmethod
    def recharge_api_parameterization(cls, data):
        """
        充值接口参数的参数化
        :param data:
        :return:
        """
        data = cls.investor_mobile_replace(data)
        data = cls.investor_pwd_replace(data)
        data = cls.not_register_mobile_replace(data)
        return data

    @classmethod
    def add_loan_api_parameterization(cls, data):
        """
        加标接口参数的参数化
        :param data:
        :return:
        """
        data = cls.manager_mobile_replace(data)
        data = cls.manager_pwd_replace(data)
        data = cls.borrower_id_replace(data)
        return data


if __name__ == '__main__':
    src_str = '{"mobilephone":"${not_register_mobile}","test": "${investor_mobile}", "pwd":"123123", "regname":"lyx_test_借款人"}'
    # src_str1 = '{"mobilephone":"${investor_mobile}", "pwd":"${investor_pwd}"}'
    result = HandleContext.register_api_parameterization(src_str)
    # data = HandleContext.login_api_parameterization(src_str1)
    pass

