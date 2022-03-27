# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from django.db.models import Q, F
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import django.utils.timezone as timezone
from appUsers.models import User, UserType, UserGroup, Department
from appUsers.models import PermissionBase, PermissionGroupTitle, PermissionGroupDetail, PermissionUser
from user_agents import parse
from project.views import global_setting
from appBase.function import BaseFunction
import datetime

root_url = global_setting.get('root_url')


# 邮箱和用户名都可以登录，免密登录等
# 基与ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
	def authenticate(self, request, mobile=None, password=None,
	                 dingtalkid=None, wechatid=None,
	                 types='password', **kwargs):
		if types == 'password':
			try:
				# 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
				# 其他用户只能用手机号码登录
				user = User.objects.get(Q(username=mobile))
				
				# django的后台中密码加密：所以不能password==password
				# UserProfile继承的AbstractUser中有def check_password(self, raw_password):
				if user.check_password(password):
					return user
			except Exception as e:
				print(e)
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
		user_extend = request.session.get('user_extend', {})

		# 重新获取权限
		# pm = [
		# 	{
		# 		'id': 1,
		# 		'title': '系统设置',
		# 		'image': '',
		# 		'has_child': True,
		# 		'child': [
		# 			{
		# 				'id': 1,
		# 				'title': '添加用户',
		# 				'image': '',
		# 				'has_child': False,
		# 				'url': '/user/register/'
		# 			},
		# 			{
		# 				'id': 2,
		# 				'title': '查看部门信息',
		# 				'image': '',
		# 				'has_child': False,
		# 				'url': '/system/department/list/'
		# 			},
		# 		]
		# 	},
		# ]
		# user_extend.update({'permission': pm})

		# 保存session，取出，请到中间件中取出
		request.session['user_extend'] = user_extend

		# 返回主页资料
		return render(request, 'a_normal_index.html', locals())


# 登录
class LoginView(View):
	def get(self, request):
		return render(request, 'a_normal_login.html')
	
	def post(self, request):
		mobile = request.POST.get('mobile')
		password = request.POST.get('password')
		user = authenticate(mobile=mobile, password=password, types='password')
		if user is not None:
			# 登录
			login(request, user)
			BaseFunction.UserInfoOpt.set_init_user_extend_info(request)

			# 进入主页
			return HttpResponseRedirect(root_url + '/index/')
		else:
			err_msg = '账号或密码错误'
			return render(request, 'a_normal_login.html', locals())


# 退出
class LogoutView(View):
	def get(self, request):
		request.session.clear()
		logout(request)
		return HttpResponseRedirect(root_url + '/login/')


class UserLockScreenView(View):
	def get(self, request):
		BaseFunction.UserInfoOpt.set_user_extend_info(request, 'lockscreen', True)
		return render(request, 'a_normal_lockscreen.html', locals())

	def post(self, request):
		user = request.user
		password = request.POST.get('password', '')
		if user.check_password(password):
			BaseFunction.UserInfoOpt.set_user_extend_info(request, 'lockscreen', False)
			return HttpResponseRedirect(root_url + '/index/')
		else:
			err_msg = '密码错误！'
			return render(request, 'a_normal_lockscreen.html', locals())


class UserProfileView(View):
	def get(self, request):
		return render(request, 'a_normal_profile.html', locals())

	def post(self, request):
		return render(request, 'a_normal_profile.html', locals())


# 用户管理
class UserManagerView(View):
	def get(self, request):
		pass
	
	def post(self, request):
		pass


# 用户注册
class UserRegisterView(View):
	def get(self, request):
		now_year = datetime.datetime.now().year
		now_month = datetime.datetime.now().month
		now_day = datetime.datetime.now().day
		birthday_year = range(1890, 2099)
		birthday_month = range(1, 13)
		birthday_day = range(1, 32)
		user_type = UserType.objects.all()
		user_group = UserGroup.objects.all()
		dept = Department.objects.all()
		return render(request, 'a_normal_register.html', locals())
	
	def post(self, request):
		mobile = request.POST.get('mobile', '')
		nick_name = request.POST.get('nick_name', '')
		email = request.POST.get('email', '')
		address = request.POST.get('address', '')
		passwd = request.POST.get('passwd', '')
		passwd_check = request.POST.get('passwd_check', '')
		dept_select = request.POST.get('dept_select', '')
		user_type_select = request.POST.get('user_type_select', '')
		user_group_select = request.POST.get('user_group_select', '')
		gender_select = request.POST.get('gender_select', '')
		print(request.POST)
		messages.success(request, '保存成功')
		return render(request, 'a_normal_register.html', locals())


# 用户修改密码
class UserPasswordView(View):
	def get(self, request):
		return render(request, 'a_normal_reset_password.html', locals())

	def post(self, request):
		user = request.user
		old_pwd = request.POST.get('old_passwd', '')
		new_pwd = request.POST.get('new_passwd', '')
		new_pwd_check = request.POST.get('new_passwd_check', '')
		# print(old_pwd, new_pwd, new_pwd_check)
		msg = ''
		old_passwd = old_pwd

		if new_pwd == '':
			msg = '新密码不能为空'
		else:
			if new_pwd == new_pwd_check:
				if user.check_password(old_pwd):
					user.set_password(new_pwd)
					user.save()
					old_passwd = ''
					# 因修改了密码，需要将当前用户的登录全部退出
					update_session_auth_hash(request, user)
					return HttpResponseRedirect(root_url + '/logout/')
				else:
					old_passwd = ''
					msg = '原密码错误，保存失败'
			else:
				msg = '新密码不一致，请重新输入'

		return render(request, 'a_normal_reset_password.html', locals())


class DepartmentView(View):
	def get(self, request):
		page_name = '部门信息'

		dept = Department.objects.all()
		return render(request, 'b_department.html', locals())

	def post(self, request):
		opt = request.POST.get('opt', '')
		dept_id = request.POST.get('dept_id', None)
		dept_name = request.POST.get('dept_name', '')
		dept_manager_user = request.POST.get('dept_manager_user', '')

		# 获取
		if opt == 'get':
			if dept_id is None:
				dept = Department.objects.all().values()
				return JsonResponse({'rows': list(dept), 'status': 'ok'})
			elif dept_id is not None:
				dept = Department.objects.filter(dept_id=dept_id).values()
				return JsonResponse({'rows': list(dept), 'status': 'ok'})

		# 检验
		if opt == 'check':
			dept = Department.objects.filter(Q(dept_name=dept_name) & ~Q(dept_id=dept_id)).values()
			if len(list(dept)) > 0:
				return JsonResponse({'status': 'fail'})
			else:
				return JsonResponse({'status': 'ok'})

		# 修改
		elif opt == 'put':
			try:
				Department.objects.filter(dept_id=int(dept_id)).update(dept_name=dept_name, modiuser=request.user.username)
				return JsonResponse({'status': 'ok'})
			except:
				return JsonResponse({'status': 'not ok'})

		# 创建
		elif opt == 'post':
			try:
				Department.objects.create(dept_name=dept_name, createuser=request.user.username)
				return JsonResponse({'status': 'ok'})
			except:
				return JsonResponse({'status': 'not ok'})

		# 删除
		elif opt == 'delete':
			return JsonResponse({})
		else:
			return JsonResponse({})
