import json

from user_agents import parse
import pandas as pd


class BaseFunction:
	class UrlParmOpt:
		@staticmethod
		def get_url_parm_get(request):
			parm = {}
			for k, v in request.GET.items():
				parm.update({k: v})
			return parm

		@staticmethod
		def get_url_parm_post(request):
			parm = {}
			for k, v in request.POST.items():
				parm.update({k: v})
			return parm

	class UserInfoOpt:
		@staticmethod
		def set_init_user_extend_info(request):
			# 添加额外信息
			user_extend = request.session.get('user_extend', {})
			ua_string = request.META.get('HTTP_USER_AGENT', '')
			ua = parse(ua_string)
			# 记录浏览器的类型(DingTalk/Wechat/Other)，设备类型(iOS/Android)
			if ua_string.count('DingTalk'):
				user_extend.update({'browser_type': 'DingTalk'})
				user_extend.update({'browser_type_name': '钉钉登录'})
			elif ua_string.count('MicroMessenger'):
				user_extend.update({'browser_type': 'WeChat'})
				user_extend.update({'browser_type_name': '微信登录'})
			else:
				user_extend.update({'browser_type': ua.browser.family})
				user_extend.update({'browser_type_name': '浏览器登录'})

			# print(ua)
			if ua.os.family in ['iOS']:
				user_extend.update({'device_type': 'iOS'})
			elif ua.os.family in ['Android']:
				user_extend.update({'device_type': 'Android'})
			elif ua.os.family in ['PC', 'Mac OS X']:
				user_extend.update({'device_type': 'PC'})
			else:
				user_extend.update({'device_type': 'Other'})

			user_extend.update({'lockscreen': False})

			# 获取权限
			pm = [
				{
					'id': 1,
					'title': '系统设置',
					'image': '',
					'has_child': True,
					'child': [
						{
							'id': 1,
							'title': '用户管理',
							'image': '',
							'has_child': False,
							'url': '/user/register/'
						},
						{
							'id': 2,
							'title': '部门管理',
							'image': '',
							'has_child': False,
							'url': '/manage/department/'
						},
					]
				},
				{
					'id': 2,
					'title': '测试',
					'image': '',
					'has_child': True,
					'child': [
						{
							'id': 1,
							'title': '测试1',
							'image': '',
							'has_child': False,
							'url': '/test/test1/'
						},
						{
							'id': 2,
							'title': '测试2',
							'image': '',
							'has_child': False,
							'url': '/test/test2/'
						},
					]
				},
			]
			user_extend.update({'permission': pm})
			# print(user_extend)

			request.session['user_extend'] = user_extend

		@staticmethod
		def set_user_extend_info(request, key, value):
			user_extend = request.session.get('user_extend', {})
			user_extend.update({key: value})
			request.session['user_extend'] = user_extend

	class DataFrameOpt:
		@staticmethod
		def dataframe_2_dict(df):
			rtn_dict = {}
			jsons = df.to_json(orient='records')
			rows = json.loads(jsons)
			total = len(rows)
			rtn_dict.update({'total': total, 'rows': rows})
			return rows
