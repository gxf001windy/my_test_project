#-*- coding:utf-8 -*-
import configparser, os, time, logging, random, csv, re
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC

class Config():
    """将配置统一提取到config文件中配置"""
    def __init__(self):
        """根据工程目录获取config文件路径"""
        # 获取项目目录
        projectPath = os.path.abspath('..')

        # config文件目录
        configPath = projectPath + "/" + "config"

        # config.ini文件
        configFile = configPath + "/" + "config.ini"

        conf = configparser.ConfigParser()
        conf.read(configFile)

        # 获取config.ini文件配置
        # self.logDir = os.path.join(projectPath, conf.get('base', 'logDir'))  # 日志输出路径
        # self.screenDir = os.path.join(projectPath, conf.get('base', 'screenDir'))  # 截图输出路径
        # self.reportDir = os.path.join(projectPath, conf.get('base', 'reportDir'))  # 测试报告输出路径
        # self.csvDir = os.path.join(projectPath, conf.get('base', 'csvDir'))  # csv配置文件路径
        # self.testDir = os.path.join(projectPath, conf.get('base', 'testDir'))  # 测试用例文件路径
        # self.sendMsg = conf.get('base', 'sentMsg') # 消息推送开关=1推送
        self.logDir = os.path.join(projectPath, "log")  # 日志输出路径
        self.screenDir = os.path.join(projectPath, 'screen')  # 截图输出路径
        self.reportDir = os.path.join(projectPath, 'report')  # 测试报告输出路径
        self.csvDir = os.path.join(projectPath, 'csv')  # csv配置文件路径
        self.testDir = os.path.join(projectPath, 'src/TestCase')  # 测试用例文件路径
        self.sendMsg = '1'  # 消息推送开关=1推送

        # self.putreport = conf.get('sec_report', 'put_report')
        self.putreport = 'test*.py'

class Log():
    """日志模块，在log路径下生成log文件，以小时分割。同时控制台也会打印"""

    def __init__(self):
        configBase = Config()
        self.logName = configBase.logDir + '/' + time.strftime('%Y-%m-%d-%H') + '.log'

    def printConsole(self, level, message):
        # 创建一个log
        logger = logging.getLogger(__name__)

        # 设置日志记录级别
        logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.logName, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给log添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        # 记录一条日志
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        time.sleep(1)
        fh.close()

    def debug(self, message):
        self.printConsole('debug', message)

    def info(self, message):
        self.printConsole('info', message)

    def warning(self, message):
        self.printConsole('warning', message)

    def error(self, message):
        self.printConsole('error', message)

class Method():
    """公共模块方法"""
    def __init__(self, driver):
        self.driver = driver
        self.putlog = Log()

    def getScreens(self, errorInfo = None):
        """截图模块"""
        configBase = Config()
        putlog = Log()
        fileName = str(errorInfo)+'_' + time.strftime('%Y-%m-%d-%H-%M-%S')+'.jpg'
        filePath = configBase.screenDir + '\\' + fileName

        getscreen =self.driver.get_screenshot_as_file(filePath)
        if getscreen ==True:
            putlog.info('截图成功，文件名称：%s' % fileName)
        else:
            putlog.info('截图失败，IO异常')

    def elementExist(self, by, element):
        """判断元素是否存在，超过隐性等待时间不中断程序，继续执行"""
        putlog = Log()
        try:
            self.driver.find_element(by, element)
        except:
            putlog.error('元素不存在：%s' % element)
            self.getScreens()
            return False
        else:
            putlog.info('元素存在：%s' % element)
            return True

    def elementIsNeedExist(self, by, element, stuta):
        """校验是否需要元素存在。超过隐性等待时间不中断程序，继续执行
        stuta =1：元素应该显示，stuta =2：元素应该隐藏，状态值只能是str类型"""
        putlog = Log()
        if stuta == '1':
            try:
                self.driver.find_element(by, element)
            except:
                putlog.error('没有找到元素，元素隐藏：%s' % element)
                self.getScreens()
            else:
                putlog.info('元素存在，没有隐藏：%s' % element)
        elif stuta == '2':
            try:
                self.driver.find_element(by, element)
            except:
                putlog.info('没有找到元素，元素隐藏：%s' % element)
            else:
                putlog.info('元素存在，没有隐藏：%s' % element)
                self.getScreens()
        else:
            putlog.error('stuta状态赋值异常，只能是1或2')

    def element_is_visible(self, element, timeout):
        """判断元素是否可见（非隐藏）且长宽高都不为0
        element = self.driver.find_element()"""
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of(element))
            return True
        except TimeoutException:
            return False

    def element_is_not_visible(self, element, timeout):
        """一直等待元素消失"""
        try:
            ui.WebDriverWait(self.driver, timeout).until_not(EC.visibility_of(element))
            return True
        except TimeoutException:
            return False

    def element_is_present(self, element, timeout):
        """判断元素是否被加到了dom树里，并不代表该元素一定可见
        element = (by.xxx,xxx)"""
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(element))
            return True
        except TimeoutException:
            return False

    def element_is_incloud_text(self, by, element, text, timeout):
        """判断元素中text是否包含了预期的字符串"""
        try:
            # ui.WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element(element, text))
            ui.WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element((by, element), text))
            return True
        except TimeoutException as e:
            print(e)
            return False

    def element_is_incloud_value(self, by, element, value, timeout,):
        """判断元素value是否包含了预期的字符串，若是当前元素无该Value则会一直等待超时时间"""
        try:
            # ui.WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element_value(*element, value))
            ui.WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element_value((by, element), value))
            return True
        except TimeoutException:
            return False

    def element_is_clickable(self, by, element, timeout):
        """判断元素是否可点击"""
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, element)))
            return True
        except TimeoutException:
            return False

    def click_element(self, indentifyBy, locatorString, name):
        """点击元素"""
        self.flag = False
        try:
            if indentifyBy == 'id':
                self.driver.find_element_by_id(locatorString).click()
                self.flag = True
            elif indentifyBy == 'xpath':
                self.driver.find_element_by_xpath(locatorString).click()
                self.flag = True
            elif indentifyBy == 'name':
                self.driver.find_element_by_name(locatorString).click()
                self.flag = True
            elif indentifyBy == 'class_name':
                self.driver.find_element_by_class_name(locatorString).click()
                self.flag = True
            elif indentifyBy == 'link_text':
                self.driver.find_element_by_link_text(locatorString).click()
                self.flag = True
        except NoSuchElementException as msg:
            self.putlog.error('点击操作元素所在位置不可见：%s（%s）：%s' % (name, locatorString, msg))
            self.flag = False
        except ElementNotInteractableException as msg:
            self.putlog.error('元素：%s（%s）不可交互：%s' % (name, locatorString, msg))
            self.flag = False
        else:
            self.putlog.info('点击元素：%s（%s）：%s' % (name, locatorString, self.flag))
            time.sleep(1)

    def write_element(self, indentifyBy, locatorString, input):
        """输入元素"""
        self.flag = False
        try:
            if indentifyBy == 'id':
                self.driver.find_element_by_id(locatorString).clear()
                self.driver.find_element_by_id(locatorString).send_keys(input)
                self.flag = True
            elif indentifyBy == 'xpath':
                self.driver.find_element_by_xpath(locatorString).clear()
                self.driver.find_element_by_xpath(locatorString).send_keys(input)
                self.flag = True
            elif indentifyBy == 'name':
                self.driver.find_element_by_name(locatorString).clear()
                self.driver.find_element_by_name(locatorString).send_keys(input)
                self.flag = True
            elif indentifyBy == 'class_name':
                self.driver.find_element_by_class_name(locatorString).clear()
                self.driver.find_element_by_class_name(locatorString).send_keys(input)
                self.flag = True
            elif indentifyBy == 'link_text':
                self.driver.find_element_by_link_text(locatorString).clear()
                self.driver.find_element_by_link_text(locatorString).send_keys(input)
                self.flag = True
        except NoSuchElementException as msg:
            self.putlog.error('输入元素所在位置未找到：%s（%s）：%s' % (input, locatorString, msg))
            self.flag = False
        except ElementNotInteractableException as msg:
            self.putlog.error('元素：%s（%s）不可交互：%s' % (input, locatorString, msg))
            self.flag = False
        else:
            self.putlog.info('输入元素：%s（%s）：%s' % (input, locatorString, self.flag))
            time.sleep(1)

    def select_element(self, indentifyBy, locatorString, value):
        """选择元素"""
        self.flag = False
        try:
            if indentifyBy == 'id':
                self.driver.find_element_by_id(locatorString).select_by_value(value)
                self.flag = True
            elif indentifyBy == 'xpath':
                self.driver.find_element_by_xpath(locatorString).select_by_value(value)
                self.flag = True
            elif indentifyBy == 'name':
                self.driver.find_element_by_name(locatorString).select_by_value(value)
                self.flag = True
            elif indentifyBy == 'class_name':
                self.driver.find_element_by_class_name(locatorString).select_by_value(value)
                self.flag = True
            elif indentifyBy == 'link_text':
                self.driver.find_element_by_link_text(locatorString).select_by_value(value)
                self.flag = True
        except NoSuchElementException as msg:
            self.putlog.error('选择元素所在位置不可见：%s（%s）：%s' % (value, locatorString, msg))
            self.flag = False
        except ElementNotInteractableException as msg:
            self.putlog.error('元素：%s（%s）不可交互：%s' % (value, locatorString, msg))
            self.flag = False
        else:
            self.putlog.info('选择元素：%s（%s）：%s' % (value, locatorString, self.flag))
            time.sleep(1)

    def scrollIntoView(self, by, element):
        """不在可视范围内拖动滚动条至元素"""
        toElement = self.driver.find_element(by, element)
        self.driver.execute_script('arguments[0].scrollIntoView()', toElement)
        toElement.click()

    def isInput(self, element, value):
        """value从配置csv文件中获取，配置为空时不执行输入。value有中文时转码输入"""
        if value ==None:
            pass
        elif value =='':
            pass
        else:
            if value.isdigit() == True:
                self.driver.find_element_by_xpath(element).clear()
                self.driver.find_element_by_xpath(element).send_keys(value)
                self.putlog.info('输入：%s' % value)
            else:
                value = value.decode('gb2312')
                self.driver.find_element_by_xpath(element).clear()
                self.driver.find_element_by_xpath(element).send_keys(value)
                self.putlog.info('输入：%s' % value)

class randomInput():
    def random_Letter(self):
        letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z']
        letter_lenth = random.randint(3, 5)
        name = ''
        for i in range(letter_lenth):
            name += random.choice(letter_list)
        return name

    def random_Digit(self):
        digit_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        digit_lenth = random.randint(3, 5)
        digit = ''
        for i in range(digit_lenth):
            digit += random.choice(digit_list)
        return digit

    def random_All(self):
        all_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        all_lenth = random.randint(3, 5)
        all = ''
        for i in range(all_lenth):
            all += random.choice(all_list)
        return all

    def random_Ip(self):
        ip_list = [ '1', '2', '3', '4', '5', '6', '7', '8', '9']
        ip_lenth = random.randint(2, 2)
        times = 4
        ip = ''
        for i in range(times):
            for j in range(ip_lenth):
                ip += random.choice(ip_list)
            if i != 3:
                ip += '.'
        return ip

class checkStrType():
    """判断是否含有汉字"""
    def is_include_Chinese(self, text):
        zhPattern = re.compile('[\u4e00 - \u9fa5]+')
        match = zhPattern.search(text)
        if match:
            return True
        else:
            return False

class writeDataToCsv():
    """将在自动化代码中生成或捕获的数据写入/读取于CSV文件，便于后续查找和获取"""

    def readCsv(self, filename):
        """读取csv文件，以字典形式返回"""
        config = Config()
        csvPath = config.csvDir + '/' + filename
        with open(csvPath, 'r') as csvFile:
            read = csv.DictReader(csvFile)
            for row in read:
                data = row
        csvFile.close()
        return data

