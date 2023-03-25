"""
@Time ： 2023/3/25 22:24
@Auth ： Song
@File ：baseCode.py
"""


class GetReasonCode:
	'''
	返回响应状态&响应码&响应内容
	'''

	def __init__(self):
		self.data = {}

	def getSuccess(self):
		self.data['status'] = "success"
		self.data['code'] = 200
		self.data['error'] = 0
		self.data['data'] = {}
		return self.data

	def getFail(self):
		self.data['error'] = 1
		self.data['status'] = "success"
		self.data['code'] = 201
		return self.data

	def getError(self):
		self.data['error'] = 1
		self.data['status'] = "fail"
		self.data['msg'] = "异常"
		self.data['code'] = 500
		return self.data
