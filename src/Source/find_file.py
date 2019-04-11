import os

# 定义文件目录
result_dir = 'D:\\testpro\\report'

lists = os.listdir(result_dir)

# 重新按时间对目录下的文件进行排序
lists.sort(key=lambda fn: os.path.getmtime(result_dir+'\\'+fn))
print(('最新的文件为：' + lists[-1]))
file = os.path.join(result_dir, lists[-1])
print(file)

# 首先定义测试报告的目录resul_dir，os。；os.listdir()可以获取目录下的所有文件及文件夹。
# 利用sort()方法对目录下的文件及文件夹按时间重新排序。List[-1]取到的就是最新生成的文件或文件夹