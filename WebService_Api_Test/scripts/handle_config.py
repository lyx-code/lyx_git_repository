# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 15:18
# @Author  : lyx
# @File    : handle_config.py
# @Project : WebService_Api_Test
# 此模块为处理配置文件读写

from configparser import ConfigParser


class HandleConfig:
    """
    读写配置文件操作的封装类
    """
    def __init__(self, filename):
        self.filename = filename
        self.conf = ConfigParser()
        self.conf.read(self.filename, encoding="utf-8")

    def get_data(self, section, option):
        """
        读取指定区域、选项的数据，读取结果为字符串
        :param section:
        :param option:
        :return:
        """
        try:
            data = self.conf.get(section=section, option=option)
            return data
        except Exception:
            return "输入的区域名或选项名错误"

    def get_int_data(self, section, option):
        """
        读取指定区域、选项的数据，读取结果为整型
        :param section:
        :param option:
        :return:
        """
        try:
            data = self.conf.getint(section=section, option=option)
            return data
        except ValueError:
            return "读取的数据为非整型"
        except Exception:
            return "输入的区域名或选项名错误"

    def get_float_data(self, section, option):
        """
        读取指定区域、选项的数据，读取结果为浮点型
        :param section:
        :param option:
        :return:
        """
        try:
            data = self.conf.getfloat(section=section, option=option)
            return data
        except ValueError:
            return "读取的数据为非浮点型"
        except Exception:
            return "输入的区域名或选项名错误"

    def get_eval_data(self, section, option):
        """
        读取指定区域、选项的数据，读取结果为使用eval()方法后的数据，可读取字典、列表等数据类型
        :param section:
        :param option:
        :return:
        """
        try:
            data = eval(self.conf.get(section=section, option=option))
            return data
        except Exception:
            return "输入的区域名或选项名错误 或 所取数据格式有误"

    def get_bool_data(self, section, option):
        """
        读取指定区域、选项的数据，读取结果为bool类型
        :param section:
        :param option:
        :return:
        """
        try:
            data = self.conf.getboolean(section=section, option=option)
            return data
        except Exception:
            return "输入的区域名或选项名错误"

    @staticmethod
    def write_config(filename, data):
        """
        写入配置文件数据
        :param filename: 要写入配置数据的配置文件
        :param data: 要为嵌套字典的字典格式数据
        :return:
        """
        # 进行写入配置文件，最好使用新文件
        conf = ConfigParser()
        # 判断参数data是否为嵌套字典的字典
        if isinstance(data, dict):
            for item in data.values():
                if not isinstance(item, dict):
                    return "数据不是嵌套字典的字典"
            for key in data:
                conf[key] = data[key]

            with open(filename, mode="w", encoding="utf-8") as file:
                conf.write(file)


if __name__ == '__main__':
    do = HandleConfig(r"D:\PythonLearning\WebService_Api_Test\configs\test.ini")
    data = {
        "first": {"name": "lyx"},
        "second": {"class": "python_20"}
    }
    # do.write_config(r"D:\PythonLearning\WebService_Api_Test\configs\test.ini", data)
    print(do.get_data("first", "name"))
    print(do.get_int_data("first", "name"))
