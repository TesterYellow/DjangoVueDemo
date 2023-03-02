```python
"""
@Time ： 2023/2/27 22:34
@Auth ： Song
@File ：connectionDB.py
"""
import logging

from django.db import connection


# # 引入python打印日志的工具方法
# self.logger = logging.getself.Logger('log')


####################################
# getSql 与 getMoreSql的区别是：
# getMoreSql用于处理sql查询结果为多条时；
# 查看两个方法的代码结构，可重写为一个工具类
####################################
# def getSql(sql):
# 	try:
# 		# 获取游标
# 		cursor = connection.cursor()
# 		# 查询数据
# 		cursor.execute(sql)  # 执行sql
# 		connection.commit()
# 		# 判断查询数据长度为0时，打印日志并返回0
# 		if cursor.rowcount == 0:
# 			# 改写原有方法的变量引用方式
# 			self.logger.info(f"当前查询的SQL查询内容为空：{sql}")
# 			return 0
# 		else:
# 			# 获取sql查询出的所有数据，并返回查询到的第一条数据
# 			data = cursor.fetchall()
# 			for hrow in data:
# 				self.logger.info(f"当前SQL:{sql}，查询出的内容是:{hrow}")
# 				return hrow
# 	except Exception as e:
# 		# 打印异常信息
# 		self.logger.error(e)
# 	finally:
# 		# 关闭游标和数据库链接
# 		cursor.close()
# 		connection.close()
# 
# 
# def getMoreSql(sql):
# 	try:
# 		cursor = connection.cursor()
# 		cursor.execute(sql)
# 		rawData = cursor.fetchall()
# 		col_names = [desc[0] for desc in cursor.description]
# 		result = []
# 		for row in rawData:
# 			objDict = {}
# 			# enumerate(): 把每一行的数据遍历出来放到Dict中
# 			for index, value in enumerate(row):
# 				objDict[col_names[index]] = value
# 			result.append(objDict)
# 		return result
# 	except Exception as e:
# 		self.logger.error(e)
# 	finally:
# 		cursor.close()
# 		connection.close()

class ConnecitonDB:

	def __init__(self, sql):
		# 获取游标
		self.cursor = connection.cursor()
		self.sql = sql
		# 引入python打印日志的工具方法
		self.logger = logging.getLogger('log')

	def getSql(self):
		try:
			# 查询数据
			self.cursor.execute(self.sql)  # 执行sql
			connection.commit()
			# 判断查询数据长度为0时，打印日志并返回0
			if self.cursor.rowcount == 0:
				# 改写原有方法的变量引用方式
				self.logger.info(f"当前查询的SQL查询内容为空：{self.sql}")
				return 0
			else:
				# 获取sql查询出的所有数据，并返回查询到的第一条数据
				data = self.cursor.fetchall()
				for hrow in data:
					self.logger.info(f"当前SQL:{self.sql}，查询出的内容是:{hrow}")
					return hrow
		except Exception as e:
			# 打印异常信息
			self.logger.error(e)
		finally:
			# 关闭游标和数据库链接
			self.cursor.close()
			connection.close()

	def getMoreSql(self):
		try:
			self.cursor.execute(self.sql)
			rawData = self.cursor.fetchall()
			col_names = [desc[0] for desc in self.cursor.description]
			result = []
			for row in rawData:
				objDict = {}
				# enumerate(): 把每一行的数据遍历出来放到Dict中
				for index, value in enumerate(row):
					objDict[col_names[index]] = value
				result.append(objDict)
			return result
		except Exception as e:
			self.logger.error(e)
		finally:
			self.cursor.close()
			connection.close()

```