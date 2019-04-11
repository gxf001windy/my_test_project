#-*- coding:utf-8 -*-
import unittest
from selenium import webdriver
from Source.public_method import Method, randomInput
from Source.baidu_element import QianTai_Element
from Source import public_method
import time, inspect

class TestProjecName(unittest.TestCase):
    """Test项目名称简介"""
    put_log = public_method.Log()
    csv_io = randomInput()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.put_log.info("===============浏览器初始化完成===============")
        login_url = 'http://www.baidu.com'   # 输入需要登录的页面
        self.driver.get(login_url)
        time.sleep(1)

    def tearDown(self):
        self.put_log.info('===============清除数据，关闭浏览器===============')
        self.driver.quit()

    # @unittest.skip('暂时跳过该用例')
    def test_01_baiduDebug(self):
        element_qt = QianTai_Element()
        commond = Method(self.driver)
        commond.elementExist(*element_qt.search_input)
        # commond.elementIsNeedExist(*element_qt.search_input, '1')
        # try:
        # commond.element_is_incloud_value(*element_qt.search_button, '百度', 2)
        commond.element_is_clickable(*element_qt.search_button,  2)
        # except Exception as e:
        #     print(e)
        pass