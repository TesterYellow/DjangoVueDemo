"""
@Time ： 2023/3/15 22:36
@Auth ： Song
@File ：AsynchronousTaskExecution.py
"""
import json
import time
import logging

# from rest_framework import serializers
from django.core import serializers

from Code.TesterYellow.backends.models import DemoResponseContentReport, DemoTestRequestTestCase, DemoTestRequest, \
	DemoTestHeaders

'''
任务执行器&邮件触发器
1，
'''


class DemoTask():

	def __init__(self):
		self.logger = logging.getLogger('log')

	def waitForPlan(self, id):
		'''
		执行测试计划进行更改状态至---等待执行
		:param id:
		:return:
		'''
		try:
			# 首先根据id查询到测试计划数据，然后将执行状态更新为2[等待执行]，更新时间更新为当前时间
			DemoResponseContentReport.objects.filter(plan_id=id).update(execution_state=2, update_time=time.strftime(
				"%Y-%m-%d %H:%M:%S", time.localtime()))
		except Exception as e:
			self.logger.error(e)

	def testRunningPlan(self, id):
		'''
		更新执行状态至 执行中
		:param id:
		:return:
		'''
		try:  # 首先根据id查询到测试计划数据，然后将执行状态更新为4[执行中]，更新时间更新为当前时间
			DemoResponseContentReport.objects.filter(plan_id=id).update(execution_state=4,
																		update_time=time.strftime("%Y-%m-%d %H:%M:%S",
																								  time.localtime()))
		except Exception as e:
			self.logger.error(e)

	def errorTestPlan(self, id):
		'''
		执行测试计划进行更新状态至 等待执行
		:param id:
		:return:
		'''
		try:
			# 首先根据id查询到测试计划数据，然后将执行状态更新为5[等待执行]，更新时间更新为当前时间
			DemoResponseContentReport.objects.filter(plan_id=id).update(execution_state=5,
																		update_time=time.strftime("%Y-%m-%d %H:%M:%S",
																								  time.localtime()))
		except Exception as e:
			self.logger.error(e)

	def sendEmail(self, id):
		'''
		测试完成后发送测试报告邮件
		:param id:
		:return:
		'''
		data = {}
		# 根据测试计划id获取执行结果
		result = DemoResponseContentReport.objects.get(plan_id=id)
		# 如果执行结果的执行状态为5【等待执行】，则状态为执行失败
		if str(result.execution_state) == "5":
			data['executionState'] = "执行失败，请联系管理员!!!"
		else:
			data['executionState'] = "success"
		# 获取执行结果内的参数，执行计划名称，成功用例条数，失败用例调试，跳过用例条数，总条数
		data['plan_name'] = result.plan_name
		store_test_case = eval(result.store_test_case)
		data['success_case'] = result.success_case
		data['fail_case'] = result.fail_case
		data['skip_case'] = result.skip_case
		data['case_total'] = result.case_total
		recombination = ""
		for i in range(len(store_test_case)):
			caseId = store_test_case[i]
			TCResult = DemoTestRequestTestCase.objects.get(case_id=caseId)
			case_name = TCResult.case_name
			request_code = TCResult.request_code
			case_request_id = TCResult.case_request_id
			TRList = DemoTestRequest.objects.get(request_id=case_request_id)
			request_address = TRList.request_address
			if request_code == "success":
				send_message = "<tr><td>" + str(caseId) + "</td><td>" + str(case_name) + "</td><td>" + str(
					request_address) + "</td><td style='color:#4CAE4C>" + "成功" + "</td></tr>"
			else:
				send_message = "<tr><td>" + str(caseId) + "</td><td>" + str(case_name) + "</td><td>" + str(
					request_address) + "</td><td style='color:red>" + "失败" + "</td></tr>"
			# 循环添加执行情况
			recombination = recombination + send_message
		data['recombination'] = recombination
		# 返回组装成功后的参数值
		return data

	def startPlan(self, plan_id):
		'''
		启动任务
		:param plan_id:
		:return:
		'''
		from django_celery_beat.models import CrontabSchedule, PeriodicTask
		import json

		time = DemoResponseContentReport.objects.filter(plan_id=plan_id).get()
		scheduleList = eval(time.timing_task)
		periodic_task_name = time.plan_name
		schedule, _ = CrontabSchedule.objects.get_or_create(
			minute=scheduleList[0],
			hour=scheduleList[1],
			day_of_week=scheduleList[2],
			day_of_month=scheduleList[3],
			month_of_year=scheduleList[4],
			timezone="Asia/Shanghai"
		)
		periodic_task = PeriodicTask.obejcts.create(
			crontab=schedule,
			name=periodic_task_name,
			task='demo.tasks.ExecuteTestPlanAsynchronously',
			args=json.dumps([plan_id])

		)
		periodic_task.enabled = True
		schedule.save()
		periodic_task.save()

	def stop(self, plan_id):
		'''
		停止任务
		:param plan_id:
		:return:
		'''
		try:
			from django_celery_beat.models import CrontabSchedule, PeriodicTask
			import json, datetime
			time = DemoResponseContentReport.objects.filter(plan_id=plan_id).get()
			periodic_task = PeriodicTask.objects.filter(name=time.plan_name).get()
			periodic_task.enabled = True
			periodic_task.save()
		except EOFError as e:
			self.logger.error(e)

	def delete(self, plan_id):
		'''
		删除任务
		:param plan_id:
		:return:
		'''
		try:
			self.stop(plan_id)
			from django_celery_beat.models import CrontabSchedule, PeriodicTask
			time = DemoResponseContentReport.objects.filter(plan_id=plan_id).get()
			periodic_task = PeriodicTask.objects.filter(name=time.plan_name).get()
			CrontabSchedule.objects.filter(id=periodic_task.crontab_id).delete()
			PeriodicTask.objects.filter(id=periodic_task.id).delete()
		except EOFError as e:
			self.logger.error(e)

	def startPublicInter(self):
		try:
			mmhth = DemoTestHeaders.objects.all()
			data = json.loads(serializers.serialize("json", mmhth))
			if data == [] or data == "":
				self.logger.info("没有可执行的头部信息")
			else:
				for i in range(len(data)):
					pass
					# TODO 此行代码依赖类以及方法暂未编写
					# ExecutionCase().runRepositoryPublicMethod(id=int(data[i]['fields']['tpi_id']))
					self.logger.info("-----头部信息更新完成-----")
		except EOFError as e:
			self.logger.error(e)
