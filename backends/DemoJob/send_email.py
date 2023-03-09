"""
@Time ： 2023/3/9 22:34
@Auth ： Song
@File ：send_email.py
"""

'''
1,DemoTestEmail.objects.get() 获取DemoTestEmail表中的数据;\
2,eval(email_list.receivers) eval() 用于执行一个字符串表达式，并返回表达式的值，这里返回一个receivers[收件人]的列表
3,sendMailHtml.sendHtml(data) 获取发送邮件的模板
4,MIMEText(): 通过smtp的MIMEText类发送 HTML格式的邮件；
'''

import logging
import smtplib
from email.mime.text import MIMEText

from Code.TesterYellow.backends.DemoJob import sendMailHtml
from Code.TesterYellow.backends.models import DemoTestEmail

logger = logging.getLogger('log')


# 邮件发送
def send_email(data):
	email_list = DemoTestEmail.objects.get()
	host = email_list.host  # SMTP服务器
	port = int(email_list.port)
	user = email_list.user  # 用户名
	password = email_list.password  # 邮箱授权密码
	sender = email_list.sender  # 发件人
	receivers = eval(email_list.receivers)  # 收件人
	subject = '自动化平台测试报告'  # 邮件主题
	content = sendMailHtml.sendHtml(data)
	# 内容:content，格式:html，编码:utf-8
	message = MIMEText(content + '\n Song:1234567890', _subtype='html', _charset="utf-8")
	# 以下两个方式都可以使用
	message['From'] = user
	message['From'] = "{}".format(user)
	message['To'] = ','.join(receivers)
	message['Subject'] = subject
	try:
		# 启用SSL发信，端口默认465
		smtpObj = smtplib.SMTP_SSL(host, port)
		# 登录验证邮箱，通过用户名和鉴权密码
		smtpObj.login(user, password)
		# 调用发送接口，传递发件人，收件人，邮件内容
		smtpObj.sendmail(sender, receivers, message.as_string())
		logger.info("邮件已成功发送")
	except smtplib.SMTPException as e:
		logger.error("邮件发送失败")
		logger.error(e)
