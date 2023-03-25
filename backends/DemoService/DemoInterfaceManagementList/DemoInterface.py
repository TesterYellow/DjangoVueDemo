"""
@Time ： 2023/3/25 22:17
@Auth ： Song
@File ：DemoInterface.py
"""
import json
import logging
import math
import re

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from rest_framework.decorators import api_view

from Code.TesterYellow.backends.DemoService.baseCode import GetReasonCode
from Code.TesterYellow.backends.models import DemoTestRequest, DemoTestRequestTestCase

logger = logging.getLogger("log")

'''
文件笔记：
1，@csrf_exempt  # 允许跨域访问
2，@api_view(['POST'])：指定接口支持POST请求
3，eval(json.loads(request.body)['data'])：获取接口请求参数
4，JsonResponse：用来将任意序列对象dumps转换成json字符串，然后将json字符串封装成Response对象返回给浏览器，并且Content-Type默认 application/json
5，db.models.Q : 对 对象的复杂查询，Q对象(django.db.models.Q)可以对关键字参数进行封装，从而更好地应用多个查询；
	可以组合使用 &（and）,|（or），~（not）操作符，当一个操作符是用于两个Q的对象,它产生一个新的Q对象。
6，serializers.serialize("json", groupList): 将QuerySet对象转换为json字符串格式返回
'''
@csrf_exempt  # 允许跨域访问
@api_view(['POST'])
def addInterface(request):  # 新增接口方法
	data = eval(json.loads(request.body)['data'])
	try:
		logger.info(data)
		# 如果请求参数中这些参数都不为空，则执行数据存储操作，保存接口数据到数据库并返回成功响应
		if (data['request_mode'] != "" and data['request_name'] != "" and data['request_address'] != "" and data[
			'request_group_id']):
			interface = DemoTestRequest(request_name=data['request_name'], reqeust_mode=data['request_mode'],
										remark=data['remark'], request_group_id=data['request_group_id'],
										request_address=data['request_address'])
			interface.save()
			response = GetReasonCode().getSuccess()
			return JsonResponse(response)
		else:
			response = GetReasonCode().getFail()
			response['msg'] = "缺少参数"
			return JsonResponse(response)
	except EOFError as e:
		logger.error(e)
		response = GetReasonCode().getError()
		return JsonResponse(response)


@csrf_exempt  # 允许跨域访问
@api_view(['POST'])
def getInterface(request):  # 获取查询表
	data = eval(json.loads(request.body)['data'])
	pageSize = data['pageSize']
	pageNum = data['pageNum']
	try:
		# 根据request_group_id查询DemoTestRequest表中数据，并根据更新时间排序
		groupList = DemoTestRequest.objects.filter(request_group_id=data['request_group_id']).order_by('-update_time')
		groupList = groupList.filter(
			Q(request_name__icontains=data['request_name']) & Q(request_address__icontains=data['request_address']) & Q(
				request_mode__icontains=data['request_mode']))
		groupSizeList = groupList[:pageSize * pageNum]  # 查询数据
		groupCount = groupList.count()  # 查询总数
		countNum = math.ceil(groupCount / pageSize)  # 总页数
		data = json.loads(serializers.serialize("json", groupSizeList))[
			   pageSize * pageNum - pageSize:pageSize * pageNum]
		for i in range(len(data)):
			createTime = data[i]['fields']['create_time']
			update_time = data[i]['fields']['update_time']
			# 正则表达式，
			data[i]['fields']['create_time'] = re.split('[TZ.]', createTime)[0] + " " + re.split('[TZ.]', createTime)[1]
			data[i]['fields']['update_time'] = re.split('[TZ.]', update_time)[0] + " " + re.split('[TZ.]', update_time)[
				1]
		response = GetReasonCode().getSuccess()
		response['data'] = data
		response['countNum'] = countNum  # 总页数
		response['groupCount'] = groupCount  # 总数据量
		response['pageNum'] = pageNum  # 当前页码
		response['pageSize'] = pageSize  # 当前一页多少个数据

		return JsonResponse(response)
	except EOFError as e:
		logger.error(e)
		response = GetReasonCode().getError()
		return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
def updateInterface(request):  # 修改接口信息
	data = eval(json.loads(request.body)['data'])
	try:
		logger.info(data)
		if data['interfaceid'] != "" and data['request_name'] != "" and data['request_address'] != "" and data[
			'request_mode'] != "":
			# 获取指定request_id的数据信息，并将请求参数中的值 更新到数据库
			interface = DemoTestRequest.objects.get(request_id=data['interfaceid'])
			interface.request_name = data['request_name']
			interface.request_address = data['request_address']
			interface.request_mode = data['request_mode']
			interface.remark = data['remark']
			interface.save()
			response = GetReasonCode().getSuccess()
			return JsonResponse(response)
		else:
			response = GetReasonCode().getFail()
			response['msg'] = "缺少参数，或参数为空"
			return JsonResponse(response)
	except EOFError as e:
		logger.error(e)
		response = GetReasonCode().getError()
		return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
def deleteInterface(request):  # 删除接口信息
	data = eval(json.loads(request.body)['data'])
	try:
		if data['id'] != "":
			# 查询指定case_request_id，并判断查询值的长度
			demoRequest = DemoTestRequestTestCase.objects.filter(case_request_id=data['id'])
			if len(demoRequest) > 0:
				response = GetReasonCode().getFail()
				response['msg'] = "当前接口中还存在接口用例无法删除"
				return JsonResponse(response)
			if len(demoRequest) == 0:
				DemoTestRequest.objects.filter(request_id=data['id']).delete()
				response = GetReasonCode().getSuccess()
				response['msg'] = "删除成功"
				return JsonResponse(response)
		else:
			response = GetReasonCode().getFail()
			response['msg'] = "缺少参数，或参数为空"
			return JsonResponse(response)
	except EOFError as e:
		logger.error(e)
		response = GetReasonCode().getError()
		return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
def getRequest(request):  # 获取单个接口列表数据
	data = eval(json.loads(request.body)["data"])
	try:
		groupList = DemoTestRequest.objects.filter(request_id=data['request_id'])
		data = json.loads(serializers.serialize("json", groupList))
		response = GetReasonCode().getSuccess()
		response['data'] = data
		return JsonResponse(response)
	except EOFError as e:
		logger.error(e)
		response = GetReasonCode().getError()
		return JsonResponse(response)
