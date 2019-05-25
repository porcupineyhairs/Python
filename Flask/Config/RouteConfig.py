import MessionHandeler
import WebHandeler
import Test


def SetRoute(app=None, hostInfo=None):
	if app is not None:
		# 页面报错的信息 403, 404, 500
		WebHandeler.Error(app=app, hostInfo=hostInfo)
		
		# 客户端服务请求
		MessionHandeler.Route(app=app, hostInfo=hostInfo)
		
		# 网页端服务请求
		WebHandeler.Route(app=app, hostInfo=hostInfo)
		
		# 测试
		Test.Route(app=app, hostInfo=hostInfo)
