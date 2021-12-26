from flask import current_app, Blueprint, request, jsonify

api_dingtalk_program_permission_blueprint = Blueprint('api_dingtalk_program_permission_blueprint', __name__)


@api_dingtalk_program_permission_blueprint.route('/<string:method>', methods=['POST'])
def user_permission(method):
	data = request.get_json(force=True)
	result = {}
	dd_user_id = data['dd_user_id']
	if method == 'get':
		if dd_user_id in ['01180666186637615720', ]:
			permission = [
				{
					'title': '用户信息',
					'subs': [
						{'title': '当前用户信息', 'page': '/page/user/authUser/authUser'},
						{'title': '重置钉钉信息', 'page': '/page/user/reSyncUserInfo/reSyncUserInfo'}
					]
				},
				{
					'title': '联友ERP系统',
					'subs': [
						{'title': '生成生产入库单', 'page': '/page/user/authUser/authUser'},
						{'title': '重置钉钉信息2', 'page': '/page/user/reSyncUserInfo/reSyncUserInfo'}
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
					]
				},
				# {
				# 	'title': 'API2',
				# 	'page': '/page/API/get-network-type/get-network-type'
				# }
			]
		elif dd_user_id in ['16166501188994528', '16314931505867353', ]:
			permission = [
				{
					'title': '用户信息',
					'subs': [
						{'title': '当前用户信息', 'page': '/page/user/authUser/authUser'},
						{'title': '重置钉钉信息', 'page': '/page/user/reSyncUserInfo/reSyncUserInfo'}
					]
				},
			]
		else:
			permission = [
				{
					'title': '用户信息',
					'subs': [
						{'title': '当前用户信息', 'page': '/page/user/authUser/authUser'},
					]
				},
			]
		result = {'userId': dd_user_id, 'permission': permission}
	if method == 'del':
		result = None
	if method == 'new':
		result = None
	if method == 'update':
		result = None
	# print(result)
	return jsonify(result)
