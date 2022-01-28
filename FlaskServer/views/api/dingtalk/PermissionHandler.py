

class Permission:
	def __init__(self):
		pass

	def __del__(self):
		pass
	
	def get_user_perm(self, dd_user_id):
		permission = []
		
		if dd_user_id in ['01180666186637615720', ]:
			permission = [
				{
					'title': '用户信息',
					'subs': [
						{'title': '重置钉钉信息', 'page': '/page/user/reSyncUserInfo/reSyncUserInfo'}
					]
				},
				{
					'title': '联友ERP系统',
					'subs': [
						{'title': '生成生产入库单', 'page': '/page/erp-comfort/moci05-scan/index'},
					]
				},
				{
					'title': 'API',
					'subs': [
						{'title': '下拉刷新', 'page': '/page/API/pull-down-refresh/pull-down-refresh'},
						{'title': '加载提示', 'page': '/page/API/loading/loading'},
						{'title': '操作菜单', 'page': '/page/API/action-sheet/action-sheet'},
						{'title': '获取当前位置', 'page': '/page/API/get-location/get-location'},
						{'title': '使用原生地图查看位置', 'page': '/page/API/open-location/open-location'},
						{'title': '页面跳转', 'page': '/page/component/navigator/navigator'},
						{'title': '扫码', 'page': '/page/API/scan-code/scan-code'},
						{'title': '网络信息', 'page': '/page/API/get-network-type/get-network-type'},
						{'title': 'button', 'page': '/page/component/button/button'},
						{'title': 'input', 'page': '/page/component/input/input'},
						{'title': 'text', 'page': '/page/component/text/text'},
						{'title': 'image', 'page': '/page/component/image/image'},
						{'title': 'label', 'page': '/page/component/label/label'},
						{'title': 'form', 'page': '/page/component/form/form'},
					]
				},
				# {
				# 	'title': 'API2',
				# 	'page': '/page/API/get-network-type/get-network-type'
				# }
			]
		# 高靖,陈伟琪,吴杰正
		elif dd_user_id in ['16314931505867353', '16300237192192520', 'manager4235']:
			permission = [
				{
					'title': '用户信息',
					'subs': [
						{'title': '重置钉钉信息', 'page': '/page/user/reSyncUserInfo/reSyncUserInfo'}
					]
				},
			]
		# 谭月高,冯国涛
		elif dd_user_id in ['16143230369067864', '16166501188994528']:
			permission = [
				{
					'title': '联友ERP系统',
					'subs': [
						{'title': '生成生产入库单', 'page': '/page/user/authUser/authUser'},
					]
				},
			]
		self.__add_basic_perm(permission)
		return permission

	def __add_basic_perm(self, perm_list):
		if len(perm_list) > 0:
			flag1 = False
			for index1 in range(len(perm_list)):
				if perm_list[index1]['title'] == '用户信息':
					flag1 = True
					perm_list[index1]['subs'].insert(0, {'title': '当前用户信息', 'page': '/page/user/authUser/authUser'})
				else:
					pass
			if not flag1:
				perm_list.insert(0, {
					'title': '用户信息',
					'subs': [{'title': '当前用户信息', 'page': '/page/user/authUser/authUser'}, ]
				})
		else:
			perm_list.insert(0, {
				'title': '用户信息',
				'subs': [{'title': '当前用户信息', 'page': '/page/user/authUser/authUser'}, ]
			})
