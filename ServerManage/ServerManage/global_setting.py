def global_setting(request):
	setting = {
		'NORMAL_TITLE': '服务管理系统',
		'ICP_NO': '粤ICP备2021161430号-1',
		'root_url': '/manage',  # 用于html引用
		'root_url2': 'manage/',  # 用于urls.py
		
	}
	return setting
