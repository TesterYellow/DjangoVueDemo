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
