"""
@Time ： 2023/3/28 22:29
@Auth ： Song
@File ：DemoImplementCase.py
"""
import logging

from Code.TesterYellow.backends.DemoJob import configHttp
from Code.TesterYellow.backends.models import DemoTestRequestTestCase, DemoResponseContentReport, \
	DemoResponseReportResult, DemoTestPublicInterface, DemoTestHeaders

logger = logging.getLogger("log")

'''
1，ExecutionCase:执行用例类，包含执行数据，异步任务执行，运行公共方法并存库 三个方法；
2，三个方法的流程，遍历方法接收到的参数，并查询数据库，根据对应的数据进行方法关联的操作；
3，关联调用的未实现的方法，待后续编写到对应文件后补充；
'''


class ExecutionCase(object):

	def singleeExecution(self, caseList):
		'''
		执行数据
		:param caseList:
		:return:
		'''
		try:
			for i in range(len(caseList)):
				case = DemoTestRequestTestCase.objects.filter(case_id=caseList[i])
				if not case:
					continue
				# TODO 获取数据库中的data，
				data = {}
				# data = ModelData().dataBaseHandle(case.values())[0]
				# 执行数据case，获得最后case的结果
				dictlsitall = {}
				# dictlsitall = method().JOBcheckCaseAll(data)
				sql_data = {
					"sqlTrueFlasetypeLast": data["sqlTrueFlasetypeLast"],
					"id": data['sqlChoiceLase'],
					"sql": data['SQLinputLast'],
					"SQLMomentum": data['SQLMomentum'],
					"sqlClusionValueLast": data['sqlClusionValueLast']
				}
				result = {}
				# result = method().AssertionResults(request_result=data['request_result'], result=dictlsitall['data'],
				# 								   resultlist=dictlsitall['result'], sqldata=sql_data)
				myCase = DemoTestRequestTestCase.objects.get(case_id=caseList[i])
				myCase.request_response = result['AssertionList']
				myCase.request_code = result['Assertion']
				myCase.request_result_Assertion_content = dictlsitall['data']
				myCase.save()
			return None
		except EOFError as e:
			logger.error(e)

	def singleeExectionMore(self, caseList, id):
		'''
		异步任务执行
		:param caseList:
		:param id:
		:return:
		'''
		try:
			Success = 0
			Fail = 0
			Skip = 0
			for i in range(len(caseList)):
				case = DemoTestRequestTestCase.objects.filter(case_id=caseList[i])
				if not case:
					continue
				# TODO 获取数据库中的data，
				data = {}
				# data = ModelData().dataBaseHandle(case.values())[0]
				# 执行数据case，获得最后case的结果
				dictlsitall = {}
				# dictlsitall = method().JOBcheckCaseAll(data)
				sql_data = {
					"sqlTrueFlasetypeLast": data["sqlTrueFlasetypeLast"],
					"id": data['sqlChoiceLase'],
					"sql": data['SQLinputLast'],
					"SQLMomentum": data['SQLMomentum'],
					"sqlClusionValueLast": data['sqlClusionValueLast']
				}
				result = {}
				# result = method().AssertionResults(request_result=data['request_result'], result=dictlsitall['data'],
				# 								   resultlist=dictlsitall['result'], sqldata=sql_data)
				myCase = DemoTestRequestTestCase.objects.get(case_id=caseList[i])
				myCase.request_response = result['AssertionList']
				myCase.request_code = result['Assertion']
				myCase.request_result_Assertion_content = dictlsitall['data']
				myCase.save()
				k = i + 1
				speedOfProgress = int((k / len(caseList)) * 1000) / 1000
				if k == len(caseList):
					speedOfProgress = 1
				execution_progress = str(speedOfProgress * 100) + "%"
				cr = DemoResponseContentReport.objects.get(plan_id=id)
				cr.execution_progress = execution_progress
				cr.save()
				caseSuccess = str(myCase.request_code)
				if caseSuccess == "success":
					Success += 1
				if caseSuccess == "skip":
					Skip += 1
				if caseSuccess == "fail":
					Fail += 1
				logger.info(f"执行结果:{caseSuccess}")
			mcr = DemoResponseContentReport.objects.get(plan_id=id)
			mcr.success_case = Success
			mcr.fail_case = Fail
			mcr.skip_case = Skip
			mcr.save()
			mrrr = DemoResponseReportResult(plan_id=mcr.plan_id, plan_name=mcr.plan_name, success_case=mcr.success_case,
											fail_case=mcr.fail_case, skip_case=mcr.skip_case, case_total=mcr.case_total,
											timing_open_close=mcr.timing_open_close)
			mrrr.save()
			return None
		except EOFError as e:
			logger.error(e)

	def runRepositoryPublicMethod(self, id):
		'''
		运行公共方法并存库
		:return:
		'''
		mmhPI = DemoTestPublicInterface.objects.get(request_id=id)
		url = mmhPI.url
		method = mmhPI.method
		request_data_type = mmhPI.request_data_type
		request_header_param = mmhPI.request_header_param
		if not request_header_param:
			request_header_param = {}
		else:
			request_header_param = eval(request_header_param)
		request_data_content = mmhPI.request_data_content
		request_value = eval(mmhPI.request_value)
		method_name = str(request_data_type) + str(method)
		if method_name == "DATAGET":
			Result = configHttp.ConfigHttp.data_get(self)
		if method_name == "DATAPOST":
			Result = configHttp.ConfigHttp.data_post(self)
		if method_name == "JSONGET":
			Result = configHttp.ConfigHttp.data_get(self)
		if method_name == "JSONPOST":
			Result = configHttp.ConfigHttp.data_post(self)
		valueList = {}
		for i in range(len(request_value)):
			key_name = request_value[i]['newKey']
			real_key_name = request_value[i]['realKey']
			num = request_value[i]['newValue']
			if not num:
				value = 1
			# TODO
			# value = jsondict().get_target_value(key_name, Result.json(), [])
			else:
				value = 2
			# value = jsondict().get_target_value(key_name, Result.json(), [])[num]
			valueList[real_key_name] = str(value)
		mmhHeader = DemoTestHeaders.objects.get(tpi_id=id)
		mmhHeader.headersValues = valueList
		mmhHeader.save()
		logger.info(f"更新完成当前头部信息:{mmhHeader.headersName}")
		return valueList
