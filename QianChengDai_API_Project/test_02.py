# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 16:49
# @Author  : lyx
# @File    : test_02.py
# @Project : QianChengDai_API_Project

var = 'hhh'


class Test:
    def test_1(self):
        global var
        var = 'test'
        print(var)


if __name__ == '__main__':
    print(var)
    test = Test()
    test.test_1()
    print(var)
