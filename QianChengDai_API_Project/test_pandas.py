# -*- coding: utf-8 -*-
# @Time    : 2019/8/16 11:48
# @Author  : lyx
# @File    : test_pandas.py
# @Project : QianChengDai_API_Project

import pandas

# 读取excel文件
# 返回一个DataFrame对象，多维数据结构
df = pandas.read_excel(r"D:\PythonLearning\QianChengDai_API_Project\datas\QianChengDai_interface_cases.xlsx", sheet_name="login")
# print(df)

# 读取一列数据
# df["title"]   返回一个Series对象，记录title这列的数据
data = df["title"]
# print(data)
# print(df.title)
# print(df.case_id)

# Series对象能转化为任何序列类型和dict字典类型
data_list = list(data)   # 转为列表
# excel文件中的表头title、case_id等是DataFrame对象的属性
data_list_02 = list(df.title)
data_tuple = tuple(data)  # 转为元组
data_dict = dict(data)    # 转为字典

# 读取某一个单元格数据
# 不包括表头，指定列名和行索引
# print(df.title[0])  # title列,不包括表头的第一个单元格

# 读取多列数据
# print(df[["case_id", "title"]])


# 按行读取数据
# 读取一行数据
# 不包含表头，第一个索引值为0
# 获取第一行数据（除表头），可以将其转换为列表、元组、字典
row_data = df.iloc[0]
# print(row_data.to_dict())
# print(list(row_data))
# print(dict(row_data))
# print(tuple(row_data))

# 读取某一个单元格数据
# 不包含表头，指定行索引和列索引（或者列名）
# print(df.iloc[0][1])  # 指定行索引和列索引
# print(df.iloc[0]["title"])   # 指定行索引和列名

# 读取多行数据
# print(df.iloc[0:4])  # 读取第一行到第四行数据
# data_all = df.iloc[0:]
# print(data_all)    # 读取所有行数据


# iloc方法
# iloc使用数字索引来读取行和列
# 也可以使用iloc方法读取某一列
# print(df.iloc[:, 1])
# print(df.iloc[:, -1])

# 读取多列
# print(df.iloc[:, 0:3])

# 读取多行多列
# print(df.iloc[0:4, 0:3])     # 这样是指定读取前4行、前3列的数据
# print(df.iloc[[0, 4], [1, 2]])  # 读取指定行号（第一行0和第五行4）、列号的数据

# 读取所有数据
# 读取到的数据为嵌套列表的列表类型，此方法不推荐
# print(df.values)

# 嵌套字典的列表
all_data_dict_list = []
for r_index in df.index:
    all_data_dict_list.append(df.iloc[r_index].to_dict())
# print(all_data_dict_list)


# 写入数据
df["result"][0] = 1000
# print(df)
with pandas.ExcelWriter(r"test_excel_new.xlsx") as writer:
    df.to_excel(writer, sheet_name="new", index=False)


# 读取csv文件
csvframe = pandas.read_csv("data.log")
new_csvframe = csvframe.loc[csvframe["Success"] == 0]
result_csvframe = new_csvframe["TestTime"]
avg_result = round(sum(result_csvframe)/len(result_csvframe), 2)
print("TestTime最小值为：{}\nTestTime最大值为：{}\nTestTime平均值为：{}".
      format(min(result_csvframe), max(result_csvframe), avg_result))
pass



