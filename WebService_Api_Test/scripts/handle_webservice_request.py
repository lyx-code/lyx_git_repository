# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 17:31
# @Author  : lyx
# @File    : handle_webservice_request.py
# @Project : WebService_Api_Test

# 该模块用于处理对webservice接口发送请求
from suds.client import Client
import json


class HandleWebserviceRequest:
    """
    对webservice接口发送请求操作封装类
    """
    def __init__(self, url):
        self.url = url
        # 创建Client对象
        self.client = Client(self.url)

    def send_request(self, param, interface_name):
        if interface_name == 'sendMCode':
            # 发送短信验证码接口
            try:
                res = self.client.service.sendMCode(param)
                res = json.dumps(dict(res), ensure_ascii=False)
            except Exception as e:
                res = json.dumps(dict(e.fault), ensure_ascii=False)
        elif interface_name == 'userRegister':
            # 注册接口
            res = self.client.service.userRegister(param)
            res = json.dumps(dict(res), ensure_ascii=False)
        elif interface_name == 'verifyUserAuth':
            # 实名认证接口
            res = self.client.service.verifyUserAuth(param)
            res = json.dumps(dict(res), ensure_ascii=False)
            pass
        else:
            return "所传接口名称暂不支持！"
        return res


if __name__ == '__main__':
    url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    interface_name = 'sendMCode'
    param = {"client_ip":"192.168.1.1", "tmpl_id":"1", "mobile":"17301230000"}
    do = HandleWebserviceRequest(url)
    res = do.send_request(param, interface_name)
    pass


