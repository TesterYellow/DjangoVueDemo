"""
@Time ： 2023/2/28 22:57
@Auth ： Song
@File ：models.py
"""

# 项目模块
from django.db import models


# 运行环境表
class DemoTestOperatingEnvironment(models.Model):
	oe_id = models.AutoField(primary_key=True, null=False, db_index=True)  # id
	oe_text = models.TextField(default="")  # 环境内容
	create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
	update_time = models.DateTimeField(auto_now=True)  # 修改时间
	remark = models.CharField(max_length=60, default='')  # 备注


# 项目表
class DemoTestProject(models.Model):
	pj_id = models.AutoField(primary_key=True, null=False, db_index=True)  # 项目id
	pj_name = models.TextField()  # 项目名称
	pj_img = models.TextField(default='')  # 项目图片地址
	pj_running_address = models.TextField(default='')  # 项目运行地址
	configure_address = models.TextField(default='')  # 微服务运行地址1
	other_configure = models.TextField(default='')  # 微服务运行地址2
	create_time = models.DateTimeField(auto_now_add=True)  # 当前数据的创建时间
	update_time = models.DateTimeField(auto_now=True)  # 当前数据的修改时间
	remark = models.CharField(max_length=60, default='')  # 备注说明


# 分组表
class DemoTestGrouping(models.Model):
	group_id = models.AutoField(primary_key=True, null=False, db_index=True)  # 分组id
	group_name = models.TextField()  # 分组名称
	group_pj_id = models.TextField()  # 关联项目id
	create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
	update_time = models.DateTimeField(auto_now=True)  # 修改时间
	remark = models.CharField(max_length=60, default='')  # 备注说明


# 接口表
class DemoTestRequest(models.Model):
	request_id = models.AutoField(primary_key=True, null=False, db_index=True)  # 接口id
	request_name = models.TextField()  # 接口名称
	request_group_id = models.TextField()  # 分组id
	request_address = models.TextField()  # 接口地址
	request_mode = models.TextField(0)  # 请求接口方式
	create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
	update_time = models.DateTimeField(auto_now=True)  # 修改时间
	remark = models.CharField(max_length=60, default='')  # 备注说明


# 测试用例表
class DemoRequestTestCase(models.Model):
	case_id = models.AutoField(primary_key=True, null=False, db_index=True)  # 用例id
	case_name = models.TextField()  # 用例名称
	case_request_id = models.TextField()  # 关联接口id
	request_header_param = models.TextField(default='')  # header 请求头信息
	headerData = models.TextField(default='')  # header动态取值内容
	request_data_content = models.TextField(default='')  # 请求参数
	request_other_type = models.TextField(default='')  # 是否使用关联接口
	request_relation_content = models.TextField(default='')  # 关联接口内容 1：存入接口地址，入参数据和提取数据字段
	request_response = models.TextField(default='')  # 响应结果
	request_code = models.TextField(default='')  # 断言结果
	request_result = models.TextField(default='')  # 入参动态 断言内容
	request_result_Assertion_content = models.TextField(default='')  # 结果断言内容
	create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
	update_time = models.DateTimeField(auto_now=True)  # 修改时间
	other_case_id = models.TextField(default='')  # 关联其他用例id
	other_case_id_conclusion_value = models.TextField(default='')  # 关联其他取值
	data_type = models.TextField(default='')  # 接口请求类型： json|type
	sql_content = models.TextField(default="")  # 前后置接口内容
	remark = models.CharField(max_length=60, default='')  # 备注说明


# 存储公共接口表
class DemoTestPublicInterface(models.Model):
	request_id = models.AutoField(primary_key=True, null=False, db_index=True)
	url = models.TextField()  # 请求接口的地址
	method = models.CharField(max_length=10)  # 接口请求方式：post get
	request_data_type = models.TextField(default='')  # 接口请求类型
	request_header_param = models.TextField(default='')  # 请求头
	request_data_content = models.TextField(default='')  # 请求参数
	request_value = models.TextField(default='')  # 接口动态取值
	create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
	update_time = models.DateTimeField(auto_now=True)  # 修改时间爱你
	remark = models.CharField(max_length=60, default='')  # 备注说明


# 计划和结果报表主表
class DemoResponseContentReport(models.Model):
	plan_id = models.AutoField(primary_key=True, null=False, db_index=True, max_length=200)
	plan_name = models.TextField(default='')  # 计划名称
	store_test_case = models.TextField(default='')  # 存入的测试用例
	execution_state = models.TextField(default='')  # 执行状态
	execution_progress = models.TextField(default='')  # 执行进度
	success_case = models.TextField(default='')  # 成功用例
	fail_case = models.TextField(default='')  # 失败用例
	skip_case = models.TextField(default='')  # 跳过用例
	case_total = models.TextField(default='')  # 执行用例总数
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	timing_open_close = models.TextField(default='')  # 是否开启定时任务
	timing_task = models.TextField(default='')  # 定时任务
	remark = models.CharField(max_length=60, default='')


# 响应结果表
class DemoResponseReportResult(models.Model):
	id = models.AutoField(primary_key=True, null=True, db_index=True)
	plan_id = models.AutoField(primary_key=True, null=False, db_index=True, max_length=200)
	plan_name = models.TextField(default='')  # 计划名称
	success_case = models.TextField(default='')  # 成功用例
	fail_case = models.TextField(default='')  # 失败用例
	skip_case = models.TextField(default='')  # 跳过用例
	case_total = models.TextField(default='')  # 执行用例总数
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	timing_open_close = models.TextField(default='')  # 是否开启定时任务
	remark = models.CharField(max_length=60, default='')


# 链接测试数据库
class DemoTestDatabase(models.Model):
	id = models.AutoField(primary_key=True, null=False, db_index=True)
	host = models.CharField(max_length=60)
	username = models.CharField(max_length=60)
	password = models.CharField(max_length=60)
	port = models.CharField(max_length=60)
	remark = models.CharField(max_length=60, default='')


# 测试邮箱
class DemoTestEmail(models.Model):
	id = models.AutoField(primary_key=True, null=False)
	host = models.TextField(default='')  # SMTP服务器
	port = models.TextField(default='')  # 端口号
	user = models.TextField(default='')  # 用户名
	password = models.TextField(default='')  # 密码
	sender = models.TextField(default='')  # 发件人
	receivers = models.TextField(default='')  # 收件人
	remark = models.TextField(default='')  # 备注


# 用户表
class DemoUser(models.Model):
	user_type_choices = ((1, "一级权限"), (2, "二级权限"), (3, "三级权限"))
	user_id = models.AutoField(primary_key=True, null=False, db_index=True)
	user_name = models.CharField(max_length=60, db_index=True)  # 用户名
	user_account = models.CharField(max_length=60)  # 用户登录账号
	user_password = models.CharField(max_length=60)  # 密码
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	user_type = models.IntegerField(choices=user_type_choices, default=1)  # 用户类型，默认1
	remark = models.CharField(max_length=60, default='')
	token = models.CharField(max_length=60, null=True)


class DemoTestHeads(models.Model):
	id = models.AutoField(primary_key=True, null=False)
	tpi_id = models.TextField(default='') # 关联公共接口id
	headerName = models.TextField() # 头部名称
	headerValues = models.TextField() # 头部值
