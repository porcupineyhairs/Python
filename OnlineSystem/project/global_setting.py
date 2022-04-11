def global_setting(request):
	setting = {
		# 基本配置信息
		'system_name': '管理系统',
		'system_author': 'Harvey',
		'icp_no': '粤ICP备2021161430号-1',
		'host_url': 'harvey-tools.top',
		'root_url': '/online',  # 用于html引用
		'root_url2': 'online/',  # 用于urls.py
		
	}
	return setting
