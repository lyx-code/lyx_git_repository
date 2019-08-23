# -*- coding: utf-8 -*-
# @Time    : 2019/8/16 17:25
# @Author  : lyx
# @File    : handle_excel_use_pandas.py
# @Project : QianChengDai_API_Project
import pandas


class HandleExcelUsePandas:
    '''
    使用pandas读写excel文件
    '''
    def __init__(self, filename, sheetname):
        self.filename = filename
        self.sheetname = sheetname
        self.df = pandas.read_excel(self.filename, self.sheetname)

    def get_all_case(self):
        '''
        读取所有excel文件数据，返回嵌套字典的列表
        :return:
        '''
        case_list = []
        for r_index in self.df.index:
            case_list.append(self.df.iloc[r_index].to_dict())
        return case_list

    def get_one_case(self, row):
        """
        获取一行测试数据
        :return:
        """
        return self.get_all_case()[row-1]

    def write_in_excel(self, row, actual, result):
        """
        往excel文件中写入
        :param actual:
        :param result:
        :return:
        """
        self.df["actual"][row-1] = actual
        self.df["result"][row-1] = result

        with pandas.ExcelWriter(self.filename) as writer:
            self.df.to_excel(writer, sheet_name="test", index=False)


if __name__ == '__main__':
    filename = "test_excel_new.xlsx"
    sheetname = "test"
    do = HandleExcelUsePandas(filename, sheetname)
    print("所有用例数据：", do.get_all_case())

    print("单条用例数据：", do.get_one_case(2))

    actual = "{actual}"
    result = "{result}"
    do.write_in_excel(3, actual, result)
