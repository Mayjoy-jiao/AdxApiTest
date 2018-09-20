# -*- coding: utf-8 -*-
import unittest
import paramunittest
import readConfig as readConfig
import os
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp

import requests
import json


adx_xls = common.get_xls("adx.xlsx", "adx")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
proDir = readConfig.proDir
info = {}


@paramunittest.parametrized(*adx_xls)
class Adx(unittest.TestCase):
    def setParameters(self, case_name, method, header, url, data, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param header:
        :param url:
        :param data
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.header = str(header)
        self.url = str(url)
        self.data = str(data)
        self.result = str(result)
        self.code = int(code)
        self.msg = int(msg)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")

    def testAdx(self):
        """
        test body
        :return:
        """
        # set url
        url = 'http://adx73:4400/api/v1/adx/1'
        print("第一步：设置url  "+self.url)

        # set headers
        header = localReadConfig.get_headers("header")
        header = {"header": str(header)}
        print(header)
        configHttp.set_headers(header)
        print("第二步：设置header等")

        # set params
        json_path = os.path.join(readConfig.proDir, "testFile","json","zmm.json")
        json = configHttp.load_json(json_path)
        print("第三步：设置发送请求的参数")

        self.return_json = requests.request("POST", url, json = json)
        print(self.return_json.json())
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查结果")

    def tearDown(self):
        """

        :return:
        """
        info = self.info
        if info['statusCode'] == 0:
            pass
        else:
            pass
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)


        if self.result == '0':
            self.assertEqual(self.info["statusCode"], self.code)
            self.assertEqual(self.info['ads'][0]['adType'],self.msg)

        if self.result == '1':
            self.assertEqual(self.info['statusCode'], self.code)
            self.assertEqual(self.info['ads'][0]['adType'], self.msg)
