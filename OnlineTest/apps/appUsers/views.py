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
from appUsers.models import PermissionBase, UserTypePermission, PermissionUser
from user_agents import parse
import pandas as pd
from project.views import global_setting
from appBase.function import BaseFunction
from appUsers.function import UserPermission
import datetime
import json

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
		user = request.user

		# 返回主页资料
		self_index = user.self_index
		if self_index != '':
			return render(request, self_index, locals())
		else:
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


# 锁屏
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


# 用户信息
class UserProfileView(View):
	def get(self, request):
		return render(request, 'a_normal_profile.html', locals())

	def post(self, request):
		return render(request, 'a_normal_profile.html', locals())


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


# 用户管理
class UserManagerView(View):
	def get(self, request):
		return render(request, 'b_users.html', locals())

	def post(self, request):
		opt = request.POST.get('opt', '')
		username = request.POST.get('username', '')
		info = {
			'mobile': username,
			'nick_name': request.POST.get('nick_name', ''),
			'email': request.POST.get('email', ''),
			'address': request.POST.get('address', ''),
			'birthday': '2022-01-01' if request.POST.get('birthday', '') == '' else request.POST.get('birthday', ''),
			'gender': request.POST.get('gender', ''),
			'dept_id': request.POST.get('dept_id', ''),
			'group_id': request.POST.get('group_id', ''),
			'type_id': request.POST.get('type_id', ''),
			'is_dingtalk': True if request.POST.get('is_dingtalk', '') == 'checked' else False,
			'dingtalkid': request.POST.get('dingtalkid', ''),
			'is_wechat': True if request.POST.get('is_wechat', '') == 'checked' else False,
			'wechatid': request.POST.get('wechatid', ''),
			'client_no': request.POST.get('client_no', ''),
			'erp_no': request.POST.get('erp_no', ''),
			'hr_no': request.POST.get('hr_no', ''),
		}

		if opt == 'get':
			users = User.objects.all().values('username', 'nick_name', 'email', 'address', 'birthday', 'image', 'gender',
			                                  'client_no', 'erp_no', 'hr_no', 'dept_id', 'dept__dept_name',
			                                  'group_id', 'group__group_name', 'type_id', 'type__type_name',
			                                  'is_dingtalk', 'dingtalkid', 'is_wechat', 'wechatid')
			depts = Department.objects.all().values('dept_id', 'dept_name')
			groups = UserGroup.objects.all().values('group_id', 'group_name')
			types = UserType.objects.all().values('type_id', 'type_name')
			return JsonResponse({'users': {'rows': list(users)}, 'depts': list(depts), 'groups': list(groups),
			                     'types': list(types), 'status': 'ok'})

		elif opt == 'check':
			users = User.objects.filter(username=username).values('username')
			if len(list(users)) > 0:
				return JsonResponse({'status': 'fail'})
			else:
				return JsonResponse({'status': 'ok'})

		elif opt == 'put':
			try:
				User.objects.filter(username=username).update(modiuser=request.user.username, modidate=timezone.now(), **info)
				return JsonResponse({'status': 'ok'})
			except:
				return JsonResponse({'status': 'fail'})

		elif opt == 'post':
			try:
				User.objects.create_user(username=username, password='comfort', createuser=request.user.username, **info)
				return JsonResponse({'status': 'ok'})
			except:
				return JsonResponse({'status': 'fail'})

		elif opt == 'delete':
			try:
				user = User.objects.get(Q(username=username))
				if not user.is_superuser:
					User.objects.filter(username=username).delete()
				return JsonResponse({'status': 'ok'})
			except:
				return JsonResponse({'status': 'fail'})


# 部门管理
class DepartmentView(View):
	def get(self, request):
		return render(request, 'b_department.html', locals())

	def post(self, request):
		opt = request.POST.get('opt', '')
		dept_id = request.POST.get('dept_id', None)
		dept_name = request.POST.get('dept_name', '')
		dept_manager_user = request.POST.get('dept_manager_user', '')
		remark = request.POST.get('remark', '')

		# 获取
		if opt == 'get':
			dept = Department.objects.all().values()
			return JsonResponse({'rows': list(dept), 'status': 'ok'})

		# 检验
		elif opt == 'check':
			dept = Department.objects.filter(Q(dept_name=dept_name) & ~Q(dept_id=dept_id)).values()
			if len(list(dept)) > 0:
				return JsonResponse({'status': 'fail'})
			else:
				return JsonResponse({'status': 'ok'})

		# 修改
		elif opt == 'put':
			try:
				Department.objects.filter(dept_id=int(dept_id)).update(dept_name=dept_name, remark=remark,
				                                                       modiuser=request.user.username, modidate=timezone.now())
				return JsonResponse({'status': 'ok'})
			except:
				return JsonResponse({'status': 'fail'})

		# 创建
		elif opt == 'post':
			try:
				Department.objects.create(dept_name=dept_name, createuser=request.user.username)
				return JsonResponse({'status': 'ok'})
			except:
				return JsonResponse({'status': 'fail'})

		# 删除
		elif opt == 'delete':
			return JsonResponse({})

		else:
			return JsonResponse({})


# 用户类型管理
class UserTypeView(View):
	def get(self, request):
		return render(request, 'b_usertype.html', locals())

	def post(self, request):
		opt = request.POST.get('opt', '')
		type_id = request.POST.get('type_id', None)
		type_name = request.POST.get('type_name', '')
		permission = request.POST.get('permission', [])
		remark = request.POST.get('remark', '')
		# 获取
		if opt == 'get':
			usertype = list(UserType.objects.all().values())
			for index in range(len(usertype)):
				usertype_item = usertype.pop(0)
				permission = list(UserTypePermission.objects.filter(Q(type_id=usertype_item['type_id']) &
				                                                    Q(perm__valid=1) )
				                  .order_by('perm__show_index')
				                  .values('perm_id', 'perm__parent', 'perm__name', 'run', 'print', 'edit', 'export', 'delete', 'new', 'lock'))
				usertype_item.update({'permission': permission})
				usertype.append(usertype_item)
			return JsonResponse({'rows': usertype, 'status': 'ok'})

		# 检验
		elif opt == 'check':
			usertype = UserType.objects.filter(Q(type_name=type_name) & ~Q(type_id=type_id)).values()
			if len(list(usertype)) > 0:
				return JsonResponse({'status': 'fail'})
			else:
				return JsonResponse({'status': 'ok'})

		# 修改
		elif opt == 'put':
			try:
				UserType.objects.filter(type_id=int(type_id)).update(type_name=type_name, remark=remark,
				                                                     modiuser=request.user.username, modidate=timezone.now())
				print(permission)
				permission = json.loads(permission)
				for item in permission:
					perm_id = item.pop('perm_id')

					UserTypePermission.objects.filter(perm_id=int(perm_id), type_id=int(type_id)).update(**item, modiuser=request.user.username, modidate=timezone.now())
				return JsonResponse({'status': 'ok'})
			except Exception as e:
				print(e)
				return JsonResponse({'status': 'fail'})

		# 创建
		elif opt == 'post':
			try:
				type_new = UserType.objects.create(type_name=type_name, remark=remark, createuser=request.user.username)
				return JsonResponse({'status': 'ok'})
			except:
				return JsonResponse({'status': 'fail'})

		# 删除
		elif opt == 'delete':
			return JsonResponse({})

		else:
			return JsonResponse({})


# 基础权限管理
class PermissionBaseView(View):
	def get(self, request):
		return render(request, 'b_permission_base.html', locals())

	def post(self, request):
		opt = request.POST.get('opt', '')
		id = request.POST.get('id', '')
		info = {
			'name': request.POST.get('name', ''),
			'parent': request.POST.get('parent', ''),
			'parent_name': request.POST.get('parent_name', ''),
			'url': request.POST.get('url', ''),
			'valid': request.POST.get('valid', ''),
			'show_index': request.POST.get('show_index', ''),
			'image': request.POST.get('image', ''),
			'remark': request.POST.get('remark', ''),
		}

		# 获取
		if opt == 'get':
			perm_base = list(PermissionBase.objects.all().order_by('show_index').values())
			return JsonResponse({'rows': perm_base, 'status': 'ok'})

		elif opt == 'put':
			try:
				PermissionBase.objects.filter(id=int(id)).update(**info, modiuser=request.user.username, modidate=timezone.now())
				if info['parent'] == '0':
					PermissionBase.objects.filter(parent=int(id)).update(valid=info['valid'], modiuser=request.user.username,
					                                                 modidate=timezone.now())
				return JsonResponse({'status': 'ok'})
			except Exception as e:
				print(e)
				return JsonResponse({'status': 'fail'})

		elif opt == 'post':
			try:
				perm_new = PermissionBase.objects.create(**info, createuser=request.user.username, createdate=timezone.now())
				perm_new_id = perm_new.id
				types = list(UserType.objects.all().values())
				for types_item in types:
					type_id = types_item['type_id']
					UserTypePermission.objects.create(type_id=type_id, perm_id=perm_new_id, createuser=request.user.username, createdate=timezone.now())

				return JsonResponse({'status': 'ok'})
			except Exception as e:
				print(e)
				return JsonResponse({'status': 'fail'})
