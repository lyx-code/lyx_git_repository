# -*- coding: utf-8 -*-
# @Time    : 2019/8/1 14:15
# @Author  : lyx
# @File    : handle_request.py
# @Project : QianChengDai_API_Project
import requests
import json
from scripts.handle_logging import log_operate
from scripts.handle_config import conf_operate


# 接口域名路径
url_path = conf_operate.get_config_data('interface url path', 'url_path')


class HandleRequest:
    """
    封装处理请求类
    """

    def __init__(self):
        self.request_session = requests.Session()  # 创建Session会话对象，相当于JMeter中的Cookie管理器
        log_operate.debug("*" * 40)

    def send_request(self, url, method="post", data=None, is_json=False, **kwargs):
        """

        :param url:       模块/接口名称
        :param method:    请求方法，默认为post
        :param data:      请求参数
        :param is_json:   参数是否为json格式标志
        :param kwargs:    可变参数，可传请求头、cookie等
            headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None
        :return:
        """
    
        interface_url = url_path + url   # 拼接接口url
        log_operate.info("请求接口路径：  {}".format(interface_url))

        # 建议都将参数都作为字典传
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                log_operate.error(f"{data}参数不是json格式字符串")
                data = eval(data)  # 如果参数为字典类型字符串，则使用eval()方法转换为字典  ---此处适用于从Excel文件中取数据

        # 将传入的请求方法method转为大写之后进行判断
        if method.upper() == "GET":
            log_operate.info(f"发送请求--查询字符串形式：request = method:[{'GET'}] url:[{interface_url}] hearders:[{kwargs}] params:{data}")
            self.res = self.request_session.get(interface_url, params=data, **kwargs)
            log_operate.debug(f"response={self.res} {self.res.text}")
        elif method.upper() == "POST":
            # 判断是否要发送json格式参数
            if is_json:
                log_operate.info(f"发送请求--json形式：request = method:[{'POST'}]url:[{interface_url}] hearders:[{kwargs}] json:{data}")
                self.res = self.request_session.post(interface_url, json=data, **kwargs)
            else:
                log_operate.info(f"发送请求--form表单形式：request = method:[{'POST'}] url:[{interface_url}] hearders:[{kwargs}] data:{data}")
                self.res = self.request_session.post(interface_url, data=data, **kwargs)
            log_operate.debug(f"response={self.res} {self.res.text}")
            return self.res
        else:
            log_operate.error(f"传入请求方法 {method} 不支持，请检查后重试")
            return "传入请求方法不支持，请检查后重试"

    def session_close(self):
        """
        关闭会话---只是释放资源，仍可以发送请求
        :return:
        """
        self.request_session.close()


if __name__ == '__main__':
    # url_dir = "http://tj.lemonban.com/futureloan/mvc/api"
    login_url = "/member/login"
    withdraw_url = "/member/withdraw"
    login_data = '{"mobilephone": "18922330012","pwd": 123123}'

    withdraw_data = '{"mobilephone": "18922330012","amount": 100}'

    test_headers = {"User-Agent": "shengruhuakai--lyx"}

    test_data = '{"mobilephone": "18922330012","pwd": 123123}'
    one_session = HandleRequest()

    # 先登录
    res1 = one_session.send_request(url=login_url, data=login_data, headers=test_headers)
    # res1 = one_session.request_handle(login_url, "post", data=test_data, is_json=True)
    # print(f"登录请求：响应状态码{one_session.get_res_status_code()},响应头{one_session.get_res_header()},响应内容{one_session.get_res_content()}")
    print(
        f"登录请求：响应状态码{res1.status_code},响应头{res1.headers},响应内容{res1.text}")
    # 后取现
    res2 = one_session.send_request(withdraw_url, data=withdraw_data)
    # print(
    #     f"取现请求：响应状态码{one_session.get_res_status_code()},响应头{one_session.get_res_header()},响应内容{one_session.get_res_content()}")
    print(
        f"登录请求：响应状态码{res2.status_code},响应头{res2.headers},响应内容{res2.text}")
    pass

