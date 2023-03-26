"""
@Time ： 2023/3/26 22:00
@Auth ： Song
@File ：DemoPublicInterface.py
"""
import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from Code.TesterYellow.backends.DatabaseTools import connectionDB
from Code.TesterYellow.backends.DemoJob.DemoJboContentSqlXML import get_sql
from Code.TesterYellow.backends.DemoService.baseCode import GetReasonCode
from Code.TesterYellow.backends.models import DemoTestPublicInterface, DemoTestHeaders

logger = logging.getLogger('log')
'''
1，@csrf_exempt  # 允许跨域访问
2，@api_view(['POST'])：指定接口支持POST请求
3，JsonResponse：用来将任意序列对象dumps转换成json字符串，然后将json字符串封装成Response对象返回给浏览器，并且Content-Type默认 application/json
'''

@csrf_exempt
@api_view(['POST'])
def addPublicInterface(request):  # 新增公共接口管理
	data = json.loads(request.body)
	try:
		# 创建测试公共接口，参数包含url，method，数据类型，数据请求头，数据内容，数据值
		DemoPubIn = DemoTestPublicInterface.objects.create(url=data['url'], method=data['method'],
														   request_data_type=data['request_data_type'],
														   request_header_param=data['request_header_param'],
														   request_data_content=data['request_data_content'],
														   request_value=data['request_value'])
		# 创建测试请求头，包含请求头以及请求id
		DemoHeader = DemoTestHeaders.objects.create(headersName=data['headersName'], tpi_id=DemoPubIn.request_id)
		# 保存数据
		DemoHeader.save()
		DemoPubIn.save()
		# 返回创建成功
		response = GetReasonCode().getSuccess()
		return JsonResponse(response)
	except EOFError as e:
		logger.error(e)
		response = GetReasonCode().getError()
		return JsonResponse(response)

# SQL xml文件名
path = "DemoTestCaseActionSQL.xml"


@csrf_exempt  # 跨域访问
@api_view(['POST'])
def queryPublicInterface(request):  # 查询公共接口管理
	try:
		sql = get_sql("Case", "pubInter", "queryPubInter", sql_name=path, file_name="DemoInterfaceManagementList")
		DemoPubInList = connectionDB().getMoreSql(sql)
		response = GetReasonCode().getSuccess()
		response['data'] = DemoPubInList
		return JsonResponse(response)
	except EOFError as e:
		logger.error(e)
		response = GetReasonCode().getError()
		return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
def runNerPublicInterface(request):  # 运行公共接口管理
	data = json.loads(request.body)
	try:
		# TODO 待实现
		# ExecutionCase().runReponsitoryPublicMethod(id=data['id'])
		response = GetReasonCode().getSuccess()
		return JsonResponse(response)
	except EOFError as e:
		logger.error(e)


@csrf_exempt
@api_view(['POST'])
def delPublicInterface(request):  # 删除公共接口管理
	data = json.loads(request.body)
	try:
		DemoTestPublicInterface.objects.get(request_id=data['id']).delete()
		DemoTestHeaders.objects.get(tpi_id=data['id']).delete()
		response = GetReasonCode().getSuccess()
		return response
	except EOFError as e:
		logger.error(e)