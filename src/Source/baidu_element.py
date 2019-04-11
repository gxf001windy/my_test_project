#-*- coding:utf-8 -*-
"""
Created on 2019-04-01
@author:gxf
"""
from selenium.webdriver.common.by import By

class QianTai_Element():
    """
    前端界面元素
    """
    def __init__(self):
        self.search_input = (By.XPATH, '//*[@id="kw"]')
        self.search_button = (By.XPATH, '//*[@id="su"]')
