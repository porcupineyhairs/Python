# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.db.models import Q, F
from django.contrib.auth.backends import ModelBackend
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from appUsers.models import User, UserGroup, PermissionBase, PermissionGroup, PermissionUser
from user_agents import parse
from project.views import global_setting

root_url = global_setting.get('root_url')


# 邮箱和用户名都可以登录，免密登录等
# 基与ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None,
	                 dingtalkid=None, wechatid=None, mobile=None,
	                 types='password', **kwargs):
		if types == 'password':
			try:
				# 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
				# 其他用户只能用手机号码登录
				user = User.objects.get(Q(mobile=username))
				
				# django的后台中密码加密：所以不能password==password
				# UserProfile继承的AbstractUser中有def check_password(self, raw_password):
				if user.check_password(password):
					return user
			except Exception as e:
				return None
		# 免密登录
		elif types == 'DingTalk':
			try:
				user = User.objects.get(Q(is_dingtalk=1) & Q(dingtalkid=dingtalkid) & Q(mobile=mobile))
				return user
			except:
				return None
		elif types == 'WeChat':
			try:
				user = User.objects.get(Q(is_wechat=1) & Q(wechatid=wechatid) & Q(mobile=mobile))
				return user
			except:
				return None
		else:
			return None
		
		
# 主页
class IndexView(View):
	def get(self, request):
		user = request.user
		ua_string = request.META.get('HTTP_USER_AGENT', '')
		ua = parse(ua_string)
		# 记录浏览器的类型(DingTalk/Wechat/Other)，设备类型(iOS/Android)
		if ua_string.count('DingTalk'):
			user.browser_type = 'DingTalk'
		elif ua_string.count('MicroMessenger'):
			user.browser_type = 'WeChat'
		else:
			user.browser_type = 'Other'
			
		# print(ua)
		if ua.os.family in ['iOS']:
			user.device_type = 'iOS'
		elif ua.os.family in ['Android']:
			user.device_type = 'Android'
		elif ua.os.family in ['PC', 'Mac OS X']:
			user.device_type = 'PC'
		else:
			user.device_type = 'Other'
		# 获取用户权限信息，并记录，可通过刷新到主页刷新用户权限
		
		user.permission = []
		
		# perm_list = PermissionUser.objects.raw((r"select appUsers_permissionuser.username, appUsers_permissionbase.id, appUsers_permissionbase.parent, "
		#                                        r"appUsers_permissionbase.name, appUsers_permissionbase.url, "
		#                                        r"appUsers_permissionuser.run, appUsers_permissionuser.new, appUsers_permissionuser.edit, "
		#                                        r"appUsers_permissionuser.`delete`, appUsers_permissionuser.`lock`, appUsers_permissionuser.print, "
		#                                        r"appUsers_permissionuser.output "
		#                                        r"from appUsers_permissionuser "
		#                                        r"inner join appUsers_permissionbase on appUsers_permissionuser.permissionid = appUsers_permissionbase.id  "
		#                                        r"where appUsers_permissionuser.username = '{username}'").format(username=user.username))
		# print(perm_list)
		# pm = perm_list[0]

		pm = [
			{
				'id': 1,
				'title': '系统管理1',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 11,
						'title': '成本异常报表(生产)导出',
						'image': '',
						'has_child': False,
						'url': '/test/11'
					},
					{
						'id': 12,
						'title': '系统参数1-2',
						'image': '',
						'has_child': False,
						'url': '/test/12'
					},
					{
						'id': 13,
						'title': '系统参数1-3',
						'image': '',
						'has_child': False,
						'url': '/test/13'
					},
				]
			},
			{
				'id': 2,
				'title': '系统管理2',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 21,
						'title': '系统参数2-1',
						'image': '',
						'has_child': False,
						'url': '/test/21'
					},
					{
						'id': 22,
						'title': '系统参数2-2',
						'image': '',
						'has_child': False,
						'url': '/test/22'
					},
				]
			},
			{
				'id': 3,
				'title': '系统管理3',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 31,
						'title': '系统参数3-1',
						'image': '',
						'has_child': False,
						'url': '/test/31'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
					{
						'id': 32,
						'title': '系统参数3-2',
						'image': '',
						'has_child': False,
						'url': '/test/32'
					},
				]
			},
			{
				'id': 4,
				'title': '系统管理4',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 41,
						'title': '系统参数4-1',
						'image': '',
						'has_child': False,
						'url': '/test/41'
					},
					{
						'id': 42,
						'title': '系统参数4-2',
						'image': '',
						'has_child': False,
						'url': '/test/42'
					},
				]
			},
			{
				'id': 5,
				'title': '系统管理5',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 51,
						'title': '系统参数5-1',
						'image': '',
						'has_child': False,
						'url': '/test/51'
					},
					{
						'id': 52,
						'title': '系统参数5-2',
						'image': '',
						'has_child': False,
						'url': '/test/52'
					},
				]
			},
			{
				'id': 6,
				'title': '系统管理6',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 61,
						'title': '系统参数6-1',
						'image': '',
						'has_child': False,
						'url': '/test/61'
					},
					{
						'id': 62,
						'title': '系统参数6-2',
						'image': '',
						'has_child': False,
						'url': '/test/62'
					},
				]
			},
			{
				'id': 7,
				'title': '系统管理7',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 71,
						'title': '系统参数7-1',
						'image': '',
						'has_child': False,
						'url': '/test/71'
					},
					{
						'id': 72,
						'title': '系统参数7-2',
						'image': '',
						'has_child': False,
						'url': '/test/72'
					},
				]
			},
			{
				'id': 8,
				'title': '系统管理8',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 81,
						'title': '系统参数8-1',
						'image': '',
						'has_child': False,
						'url': '/test/81'
					},
					{
						'id': 82,
						'title': '系统参数8-2',
						'image': '',
						'has_child': False,
						'url': '/test/82'
					},
				]
			},
			{
				'id': 9,
				'title': '系统管理9',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 91,
						'title': '系统参数9-1',
						'image': '',
						'has_child': False,
						'url': '/test/91'
					},
					{
						'id': 92,
						'title': '系统参数9-2',
						'image': '',
						'has_child': False,
						'url': '/test/92'
					},
				]
			},
			{
				'id': 10,
				'title': '系统管理10',
				'image': '',
				'has_child': True,
				'child': [
					{
						'id': 101,
						'title': '系统参数10-1',
						'image': '',
						'has_child': False,
						'url': '/test/101'
					},
					{
						'id': 102,
						'title': '系统参数10-2',
						'image': '',
						'has_child': False,
						'url': '/test/102'
					},
				]
			},
		]
		user.permission = pm
		# print('perm', user.permission)
		
		# 返回主页资料
		return render(request, 'a_normal_index.html', locals())


# 登录
class LoginView(View):
	def get(self, request):
		return render(request, 'a_normal_login.html')
	
	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password, types='password')
		if user is not None:
			login(request, user)

			# 单一用户登录
			# session_key = request.session.session_key
			# # 删除非当前用户session_key的记录
			# for session in Session.objects.filter(~Q(session_key=session_key), expire_date__gte=timezone.now()):
			# 	data = session.get_decoded()
			# 	if data.get('_auth_user_id', None) == str(request.user.id):
			# 		session.delete()

			return HttpResponseRedirect(root_url + '/index/')
		else:
			msg = '账号或密码错误'
			return render(request, 'a_normal_login.html', locals())


# 退出
class LogoutView(View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect(root_url + '/login/')
	
	
# 用户管理
class UserManagerView(View):
	def get(self, request):
		pass
	
	def post(self, request):
		pass


# 用户注册
class RegisterView(View):
	def get(self, request):
		pass
	
	def post(self, request):
		pass
