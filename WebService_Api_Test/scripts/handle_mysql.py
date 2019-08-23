# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 14:58
# @Author  : lyx
# @File    : handle_mysql.py
# @Project : WebService_Api_Test
# 从模块为处理连接数据库、查询数据库操作

import pymysql
import random


class HandleMySql:
    """
    数据库连接、查询操作封装类
    """
    def __init__(self):
        self.connect = pymysql.connect(host="120.24.235.105",
                                       port=3306,
                                       user="python",
                                       password="python666",
                                       db="sms_db_95",
                                       cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connect.cursor()

    def execute_sql(self, sql, args=None, is_more=False):
        """
        执行sql语句，返回查询结果
        :param sql:
        :param args:
        :param is_more:
        :return:
        """
        self.cursor.execute(sql, args=args)
        self.connect.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        """
        关闭游标、关闭连接
        :return:
        """
        self.cursor.close()
        self.connect.close()

    @staticmethod
    def make_mobile():
        """
        动态生成11位手机号码
        :return:
        """
        last_three_num = "495"  # 将号码最后三位数字固定，有助于查询数据库（分表分库）
        first_two_num = ["1590", "1730", "1891", "1331"]  # 将号码开始两位数字固定为这几种
        first = random.choice(first_two_num)
        middle = ''.join(random.sample('0123456789', 4))
        mobile = first + middle + last_three_num
        return mobile

    def is_registed_mobile(self, mobile):
        """
        判断号码是否已发送过验证码，没有则肯定没注册（因用户信息表中号码是加密保存的）
        :return:
        """
        sql = "select * from sms_db_95.t_mvcode_info_4 where Fmobile_no=%s"
        result = self.execute_sql(sql, args=(mobile,))
        if result:
            return True
        else:
            return False

    def make_not_registed_mobile(self):
        """
        生成一个未注册的手机号码
        :return:
        """
        while True:
            mobile = self.make_mobile()
            if not self.is_registed_mobile(mobile):
                break
        return mobile


if __name__ == '__main__':
    do = HandleMySql()
    sql = "select * from t_mvcode_info_3 limit 3"
    result = do.execute_sql(sql, is_more=True)
    do.close()
    print(result)
