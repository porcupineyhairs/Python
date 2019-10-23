import WebTest


def SetRoute(app=None, hostInfo=None):
	if app is not None:
		# 页面报错的信息 403, 404, 500
		WebTest.Error(app=app, hostInfo=hostInfo)
		
		# 网页端服务请求
		WebTest.Route(app=app, hostInfo=hostInfo)
