"""
@Time ： 2023/3/13 22:34
@Auth ： Song
@File ：DemoJboContentSqlXML.py
"""

'''
1, 文件内容：读取sql xml配置
2，os.path.dirname(os.path.realpath(__file__))：获取当前文件所在的绝对路径
3，os.path.join(os.path.dirname(pro_path): 返回当前文件的目录信息
4，xml.etree.ElementTree：ElementTree 将整个XML文档表示为树
'''
import os
from xml.etree.ElementTree import ElementTree

pro_path = os.path.dirname(os.path.realpath(__file__))

database = {}  # 默认配置为空


def set_xml(sql_name, file_name):
	'''
	设置sql xml
	:param sql_name:
	:param file_name:
	:return: 解析SQL.xml中的内容
	'''
	proDir = os.path.join(os.path.dirname(pro_path), f"DemoService/{file_name}")
	# 判断先考虑最外层解析的database，在解析中层的table 最后解析最底层的ID标识
	if len(database) >= 0:  # 如果数据集合为空时
		sql_path = os.path.join(proDir, '%s') % (sql_name)  # 打开配置文件地址
		tree = ElementTree.parse(sql_path)  # 解析配置文件
		for db in tree.findall('database'):  # 全局解析XML中database属性
			db_name = db.get("name")  # 解析获得每一个database属性的table属性中的名称
			table = {}
			for tb in db.getchildren():  # 获得解析的database的子属性
				table_name = tb.get("name")  # 获得table子属性的标识名
				sql = {}
				for data in tb.getchildren():  # 获得table子属性的标识名
					sql_id = data.get("id")  # 获得id子属性的标识名
					sql[sql_id] = data.text  # 得到对应id属性的内容
				table[table_name] = sql  # 得到对应table属性的内容
			database[db_name] = table  # 得到对应的数据库中的内容


def get_xml_dict(database_name, table_name, sql_name, file_name):
	'''

	:param database_name: 获得SQL.xml的database名称
	:param table_name:  获得数据库名称对应的table的名称
	:param sql_name: 获得对应的SQLxml的名称
	:param file_name:
	:return: database_dict ： 返回sql的集合
	'''
	set_xml(sql_name, file_name)
	database_dict = database.get(database_name).get(table_name)
	return database_dict  # 获得当前database下table的所有SQL的集合


def get_sql(database_name, table_name, sql_id, sql_name, file_name):
	'''
	获得指定的SQL语句
	:param database_name:获得SQL.xml中的database名称
	:param table_name: 获得数据库名称对应的table名称
	:param sql_id:  SQL.xml文件的sql_index
	:param sql_name:  获得对应的SQLxml的名称
	:param file_name:
	:return:  sql
	'''
	db = get_xml_dict(database_name, table_name, sql_name, file_name)
	sql = db.get(sql_id)
	sql = sql.strip()  # 去除字符串的前后空格

	return sql
