import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

# 发送邮件服务器
smtpserver = 'smtp.sina.com'

# 发送邮箱用户/密码
user = '464723183@qq.com'
password = '123456'

# 发送邮箱
sender = '464723183@qq.com'

# 接收邮箱
receiver = 'gxf483860@qq.com'

# 发送邮件主题
subject = 'Python send email test'

# 发送的附件
sendfile = open('D:\\testpro\\reprot\\log.txt', 'rb').read()

att = MIMEText(sendfile, 'base64', 'utf-8')
att['Content-Type'] = 'application/octet-stream'
att['Content-Disposition'] = 'attachment;filename= "log.txt"'

msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = subject
msgRoot.attach(att)


# 编写HTML类型的邮件正文
msg = MIMEText('<html><h1>你好！</h1></html>', 'html', 'utf-8')  # MIMEText()用于定义邮件正文，参数为HTML格式的文本
msg['Subject'] = Header(subject, 'utf-8')  # Header()方法用来定义邮件标题

# 连接发送邮件
smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(user, password)
# smtp.sendmail(sender, receiver, msg.as_string())
smtp.sendmail(sender, receiver, msgRoot.as_string())
smtp.quit()

