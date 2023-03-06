"""
@Time ： 2023/2/28 22:54
@Auth ： Song
@File ：testDatabase.py
"""
import logging

import pymysql

from Code.TesterYellow.backends.models import DemoTestDatabase

'''
本章笔记
1，logger = logging.getLogger("log") 创建日志对象 【详细介绍：https://blog.csdn.net/liming89/article/details/109609557】
2，引入models中定义的数据库表，获取数据库连接信息；
3，与connectionDB.py区别：可以根据数据库中查询到的连接信息查询指定数据库内容；
4，pymysql：python操作mysql数据库的第三方工具库
'''

logger = logging.getLogger("log")


def getSql(id, sql):
	try:
		# 根据数据库id查询指定数据库信息，并返回数据对象
		database = DemoTestDatabase.objects.filter(id=id)
		host = database.values("host")[0]["host"]
		username = database.values("username")[0]["username"]
		password = database.values("password")[0]["password"]
		port = database.values("port")[0]["port"]
		connect = pymysql.Connect(host=str(host), user=str(username), passwd=str(password), port=int(port),
								  charset="utf8")
		# 获取游标
		cursor = connect.cursor()
		cursor.execute(sql)
		rawData = cursor.fetchall()
		# 获取表的字段名称
		col_names = [desc[0] for desc in cursor.description]
		result = []
		for row in rawData:
			objectDict = {}
			# 遍历每一行数据并放到objectDict中
			for index, value in enumerate(row):
				objectDict[col_names[index]] = value
			result.append(objectDict)
		return result
	except Exception as e:
		logger.error(e)
	finally:
		cursor.close()
		connect.close()

















