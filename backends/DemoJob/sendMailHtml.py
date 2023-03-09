"""
@Time ： 2023/3/9 22:20
@Auth ： Song
@File ：sendMailHtml.py
"""

'''
1，根据请求参数data获取对应的构建状态，项目名称，用例总数，成功用例数，失败用例数，跳过用例数以及邮件内容
2，拼接html邮件模板，并返回html值；
3，具体html格式内容暂不了解，后续编写前端代码时再补充详细解析；
'''


# 邮件模板
def sendHtml(data):
	executionState = str(data['executionState'])
	projectName = str(data['plan_name'])
	caseTotal = str(data['case_total'])
	caseSuccess = str(data['success_case'])
	caseFail = str(data['fail_case'])
	caseSkip = str(data['skip_case'])
	contentEmailHtml = str(data['Recombination'])
	html = '''<html>
				<body>
				<div style="margin-left: 2%>
					<div style="font-size: 24px;color: #4cae4c; margin-top: 20px;">
					构建状态: ''' + executionState + '''
				</div>
			<hr>
			<div>
			<p style="color:#6C9AD9">详细地址：<a href="">点击跳转查看详细报告</a></p>
			<p style="color:#3C763D">项目名称：''' + projectName + '''</p>
			<p style="color:#31708F">用例总数：''' + caseTotal + '''</p>
			<p style="color:#8A6D3B">通过用例数：''' + caseSuccess + '''</p>
			<p style="color:#A94442">失败用例数：''' + caseFail + '''</p>
			<p style="color:#999999">跳过用例数：''' + caseSkip + '''</p>
			</div>
			<hr>
			<div style="width: 70%>
			<table class="table table-hover>
				<tr>
					<th>#id</th>
					<th>用例名称</th>
					<th>接口地址</th>
					<th>用例结果</th>
				</tr>
				''' + contentEmailHtml + '''
			</table>
			<div>
			</div>
			<hr>
			<div>
			<address>
			<strong>Demo-Test</strong><br>
			Song<br>
			<abbr title="Phone">P:</abbr>123567890
			<a href="mailto:#">123@111.com</a>
			</address>
			</div>
			</body>
			<style>
			.table{
				width: 100%
			}
			.table td{
				text-align: center;
				padding: 1px;
				color: #7A8DA5;
			}
			.table th{
				color: #5196AE;
				font-size: 18px
			}
			.table th, td{
				border: 1px solid black;
			}
			</style>
			</html>
					
	'''
	return html
