# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 15:38
# @Author  : lyx
# @File    : handle_config.py
# @Project : QianChengDai_API_Project

# 该模块为对配置文件相关操作的封装
import os
from configparser import ConfigParser

from scripts.contants import CONFIG_PATH


# 将对配置文件的读写相关操作封装到类中
class HandleConfig:

    def __init__(self, filename):
        self.filename = filename
        # 创建配置解析器对象
        self.config = ConfigParser()
        # 指定读取的配置文件
        self.config.read(self.filename, encoding="utf-8")

    def get_config_data(self, section, option):
        """
        读取指定区域名、选项名的配置数据，当区域名、选项名有误时返回错误提示信息
        :param section:  区域名
        :param option:  选项名
        :return:
        """
        # 使用方括号[]和get方法读取到的配置数据都是字符串类型

        # 方法一：
        # try:
        #     data = self.config[section][option]   # 当区域名或选项名不存在时会抛KeyError异常
        #     return data
        # except KeyError as e:
        #     return "输入的区域名或选项名错误"
        # 方法二：
        try:
            data = self.config.get(section, option)  # 当区域名不存在时报NoSectionError错误，当选项名不存在时报NoOptionError错误
            return data
        except Exception:
            return "输入的区域名或选项名错误"

    def get_int_config_data(self, section, option):
        """
        读取出int型数据
        :param section:
        :param option:
        :return:
        """
        try:
            data = self.config.getint(section, option)  # 当读取到的数据不是int样式的数据时，会报ValueError
            return data
        except ValueError:
            return "读取的数据为非整型"
        except Exception:  # 用来捕获区域名或选项名错误的异常
            return "输入的区域名或选项名错误"

    def get_float_config_data(self, section, option):
        """
        读取出float型数据
        :param section:
        :param option:
        :return:
        """
        try:
            data = self.config.getfloat(section, option)  # 当读取到的数据不是float样式的数据时，会报ValueError
            return data
        except ValueError:
            return "读取的数据为非浮点型"
        except Exception:  # 用来捕获区域名或选项名错误的异常
            return "输入的区域名或选项名错误"

    def get_bool_config_data(self, section, option):
        """
        读取出bool型数据
        1、yes、on、true、True --> 会读取为True
        0、no、off、false、False  -->  会读取为False
        :param section:
        :param option:
        :return:
        """
        try:
            data = self.config.getboolean(section, option)  # 当读取到的数据不是bool样式的数据时，会报ValueError
            return data
        except ValueError:
            return "读取的数据为非浮点型"
        except Exception:  # 用来捕获区域名或选项名错误的异常
            return "输入的区域名或选项名错误"

    def get_eval_config_data(self, section, option):
        """
        读取出一些python内置数据类型，如列表、元组、字典
        :param section:
        :param option:
        :return:
        """
        try:
            data = eval(self.config.get(section, option))  # 当get取出的数据不是python内置数据类型样式时、所给区域名、选项名不存在时都会报错
            return data
        except Exception:
            return "输入的区域名或选项名错误 或 所取数据格式有误"

    @staticmethod
    def write_config_data(config_data, filename):
        """
        将所给数据写入配置文件中
        写入时，尽量不要与读取操作使用同一个解析器对象，容易出现操作失误而导致覆盖掉原有的配置数据，尽量写入到新的文件中
        :param config_data:
        :param filename:
        :return:
        """
        # 创建配置解析器对象
        config = ConfigParser()

        # 因config数据格式类似与嵌套字典的字典，所以使用字典给配置文件传数据
        # 判断对给数据是否为嵌套字典的字典
        if isinstance(config_data, dict):
            for value in config_data.values():
                if not isinstance(value, dict):
                    return "所给数据格式不是嵌套字典的字典"

            for key in config_data:
                config[key] = config_data[key]  # 将解析器对象看作为一个空字典

            # 将数据保存到配置文件中
            with open(filename, mode="w", encoding="utf-8") as file:
                config.write(file)


conf_file_name = os.path.join(CONFIG_PATH, "qcd_config_file.ini")
conf_operate = HandleConfig(conf_file_name)

if __name__ == '__main__':
    # data1 = {
    #     "file path":  {"report file": "test_report_result.html", "log file": "test_log_file"},
    #     "msg": {"success_result": "PASS", "fail_result": "FAIL"},
    #     "int": {"one": 12},
    #     "float": {"two": 12.3},
    #     "bool": {"three": "yes"}
    #
    # }
    # data2 = {
    #     "file path":  {"report file": "test_report_result.html", "log file": "test_log_file"},
    #     "msg": "test2"
    # }
    # test_conf = HandleConfig(CONFIG_FILE_PATH)
    # 测试写入
    # result = test_conf.write_config_data(data1, "test.ini")
    # print(result)

    # 测试读取
    # result = test_conf.get_config_data("msg", "success_result")
    # print(result)
    # result = test_conf.get_config_data("msg1", "success_result")
    # print(result)
    # result = test_conf.get_config_data("msg", "success_result2")
    # print(result)

    # result = test_conf.get_int_config_data("msg", "success_result")
    # print(result)
    # result = test_conf.get_int_config_data("int", "one")
    # print(result)
    # result = test_conf.get_int_config_data("float", "two")
    # print(result)
    # result = test_conf.get_int_config_data("int", "one1")
    # print(result)

    # result = test_conf.get_float_config_data("msg", "success_result")
    # print(result)
    # result = test_conf.get_float_config_data("int", "one")
    # print(result)
    # result = test_conf.get_float_config_data("float", "two")
    # print(result)
    # result = test_conf.get_float_config_data("int", "one1")
    # print(result)
    test = HandleConfig(r"D:\PythonLearning\QianChengDai_API_Project\configs\mobile.ini")
    result = test.get_config_data("investor", "mobilephone")
    pass

