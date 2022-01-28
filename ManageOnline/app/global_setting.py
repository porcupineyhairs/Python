def global_setting(request):
	setting = {
		'ICP_NO': '粤ICP备2021161430号',
		'root_url': '/django',  # 用于html引用
		'root_url2': 'django/',  # 用于urls.py
		
	}
	return setting
