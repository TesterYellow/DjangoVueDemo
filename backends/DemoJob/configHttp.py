"""
@Time ： 2023/3/13 22:19
@Auth ： Song
@File ：configHttp.py
"""
# 文件内容，配置http请求
'''
1,requests:python用于做接口请求的第三方库；
2，urllib3.disable_warnings()：关闭ssl警告
3，logging：日志工具库 【初始化类，使用self.logger.error() 方法打印错误日志】
4，requests.get(),requests.post() 分别用于做get和post请求；
	1，参数包含 url，请求头，请求参数，超时时间，是否认证【设置为False】，cookies

疑问：
1,url,headers,params,cookies 等参数都未定义，具体参数值从何而来待后续确认？
'''
import requests
import urllib3
import logging


class ConfigHttp:
	urllib3.disable_warnings()

	def __init__(self):
		# 设置超时时间
		self.timeout = 7000
		self.logger = logging.getLogger('log')

	def json_get(self):
		'''
		定义get方法
		:return:
		'''
		try:
			response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(self.timeout),
									verify=False, cookies=self.cookies)
			# 返回响应类
			return response
		# 捕获超时异常并打印错误日志
		except TimeoutError as e:
			self.logger.error("Time Out!", e)
			return None

	def json_post(self):
		'''
		定义post方法
		:return:
		'''
		try:
			response = requests.post(self.url, headers=self.headers, params=self.params, timeout=float(self.timeout),
									 verify=False, cookies=self.cookies)
			return response
		except TimeoutError as e:
			self.logger.error("Time Out!", e)
			return None

	def data_get(self):
		'''
		定义get方法
		:return:
		'''
		try:
			response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(self.timeout),
									verify=False)
			return response
		except TimeoutError as e:
			self.logger.error("Time Oue!", e)
			return None

	def data_post(self):
		'''
		定义post方法
		:return:
		'''
		try:
			response = requests.post(self.url, headers=self.headers, params=self.params, timeout=float(self.timeout),
									 verify=False, cookies=self.cookies)
			return response
		except TimeoutError as e:
			self.logger.error("Time Out!", e)
			return None

