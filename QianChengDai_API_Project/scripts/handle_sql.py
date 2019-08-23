# -*- coding utf-8 -*-
import random
import pymysql

from scripts.handle_config import conf_operate


class HandleSql:
    """
    封装sql查询操作
    """

    def __init__(self):
        db_conf = conf_operate.get_eval_config_data("DB Info", "db_conf")
        # 1.建立连接
        self.connect = pymysql.connect(**db_conf,
                                       charset="utf8",
                                       cursorclass=pymysql.cursors.DictCursor)

        # 2 建立游标
        self.cursor = self.connect.cursor()

    def execute_sql(self, sql, args=None, is_more=False):
        """
        执行sql语句，返回结果
        :param sql:
        :param is_more: 是否返回全部结果
        :param args  sql查询参数，需要为元组类型
        :return:
        """
        self.cursor.execute(sql, args=args)
        self.connect.commit()   # 提交之后才能实际执行sql语句
        if is_more:
            return self.cursor.fetchall()  # fetchall()返回所有结果行
        else:
            return self.cursor.fetchone()  # fetchone()返回一行结果

    @staticmethod
    def make_mobile():
        """
        动态生成手机号码，
        :return: 返回生成的号码
        """
        mobile_list = ['138', '139', '159', '189']
        # 从'0123456789'中随机取8次数字，获得一个列表，使用空字符拼接为后8位
        end_mobile = ''.join(random.sample('0123456789', 8))
        # 从three_num中随机选择一个元素作为前三位
        start_mobile = random.choice(mobile_list)
        mobile = start_mobile + end_mobile  # 拼接生成最终手机号码

        return mobile

    def is_registered_mobile(self, mobile):
        """
        判断号码是否已经注册过
        :param mobile:
        :return:
        """
        sql = "select * from member where mobilephone=%s"
        result = self.execute_sql(sql, args=(mobile,))  # 查询数据库  注意：args要传元祖类型
        if result:  # 如果查询结果不为空（即表示该号码已注册过）,返回True
            return True
        else:            # 如果查询结果为空，即表示该号码未注册，返回False
            return False

    def make_not_registered_mobile(self):
        """
        生成一个未注册过的号码，这个地方与动态生成号码分开是为了实现重用
        :return:
        """
        while True:
            mobile = self.make_mobile()  # 调用方法生成一个号码
            if not self.is_registered_mobile(mobile):  # 如果号码未注册，则跳出循环
                break
        return mobile

    def close(self):
        """
        最后一定要关闭游标和连接 ---先关闭游标，后关闭连接
        :return:
        """
        self.cursor.close()
        self.connect.close()


if __name__ == '__main__':
    sql_1 = "select * from member limit 4;"
    sql_2 = "select * from member where mobilephone='18922330012'"
    test_sql = HandleSql()
    print(test_sql.execute_sql(sql_1, is_more=True))
