#-*- coding:utf-8 -*-
import unittest
import time, platform
from Source import public_method
from Source.HTMLTestRunner import HTMLTestRunner
from shutil import copyfile
# from smtplib import SMTP

if __name__ == '__main__':
    config = public_method.Config()
    testunit = unittest.TestSuite()
    """生成HTML测试报告"""
    dotest = config.putreport  # 获取配置文件中需要
    dataname = dotest.split(',')
    now = time.strftime('%Y-%m-%d-%H-%M-%S')
    print(config.reportDir)
    filename = config.reportDir + '/' + now + 'report.html'

    # 定义报告存放路径
    fp = open(filename, 'wb')
    for i in dataname:
        print(i)
        # 定义测试报告
        discover = unittest.defaultTestLoader.discover(config.testDir, pattern=i)
        if i == 'test*.py':
            runner = HTMLTestRunner(stream=fp, title='百度Debug-测试报告', description='用例执行情况')
            runner.run(discover)
        else:
            runner = HTMLTestRunner(stream=fp, title='%s测试报告' % i, description='用例情况')
            runner.run(discover)
    print('==========Done==========')
    fp.close()

    """在服务器中将HTML报告复制到wwwroot目录下指定文件夹中，
    火星路径地址的HTML报告从该目录文件进行获取，若无该文件则会提示404错误"""
    platformMsg = platform.platform()
    targetPath = "c://XXXXXxx"
    if 'Server' in platformMsg:
        copyfile(filename, targetPath)

    """windowsServer平台发送推送消息，否则不发送"""
    if config.sendMsg == '1':
        if 'Server' in platformMsg:
            html_file = open(filename, 'r', encoding='utf-8')
            connet = html_file.read()
            # 读取HTML里面的文档并将需要的结果部分进行截取
            needConnet = connet.split('<td>Total</td>')[-1].split('<td>&nbsp;</td>')[0]
            # 在截取后文档中，删除多余前缀<td>
            needResu1 = needConnet.replace('<td>', '')
            # 在截取后文档中，删除多余后缀</td>
            needResu2 = needResu1.replace('</td>', '')
            # 将最后结果转换为列表
            needResu = needResu2.split()

            # 测试报告地址
            report_url = config.reportDir + '\\' + now + 'report.html'
            msg_text = "【XXX】自动化执行结果：\n测试报告地址：%s\n总执行用例数：%s，执行通过用例数：%s，执行发现错误数：%s"\
                       % (report_url, needResu[0], needResu[1], needResu[3])
        else:
            pass
