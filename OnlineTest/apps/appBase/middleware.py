from django.shortcuts import render
import django.utils.timezone as timezone
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from user_agents import parse
from project import views
from appBase.models import AppLog
from appUsers.function import UserPermission


root_url = views.root_url


class MiddlewareApp(MiddlewareMixin):
	# 入口处理
	def process_request(self, request):
		# ua_string = request.META.get('HTTP_USER_AGENT', '')
		# print(ua_string)

		# 不检查用户是否登录的URL
		ingore_url = [
			root_url + '/login/',
			root_url + '/dingtalk/login/autologin/main/',
			root_url + '/wechat/login/autologin/main/',
		]

		# 已登陆用户都可访问的URL
		normal_url = [
			root_url + '/index/',
			root_url + '/user/profile/',
			root_url + '/user/lockscreen/',
			root_url + '/user/password/',
		]

		# 未登录用户可访问的URL(post)
		post_url = [

		]

		# 未登录用户跳转到登录界面
		if request.method == 'GET':
			user = request.user
			if request.path not in ingore_url:
				if not user.is_authenticated:
					return HttpResponseRedirect(root_url + '/login/')

		# 用户拓展信息写入用户信息，及记录操作日志
		if request.method in ['POST', 'GET'] and request.path not in ingore_url:
			user = request.user
			if user.is_authenticated:
				# 从session中获取共用数据，
				user_extend = request.session.get('user_extend', {})
				# print(user_extend)

				# 主页刷新权限，并保存至session中
				if request.path == root_url + '/index/':
					user_permission = UserPermission(request)
					perm = user_permission.get_perm()
					del user_permission
					user_extend.update({'permission': perm})
					request.session['user_extend'] = user_extend

				# 根据user_extend中资料，写入到request.user中
				for k in user_extend:
					exec(f'request.user.{k} = user_extend["{k}"]')

				if request.method == 'POST':
					opt = request.POST.get('opt', '')
					if opt in ['export', 'check']:
						pass
					else:
						# 记录日志
						AppLog.objects.create(username=request.user.username, nick_name=request.user.nick_name,
						                      user_type=request.user.type.type_name,
						                      browser_type=request.user.browser_type, device_type=request.user.device_type,
						                      urls=request.get_full_path(), methods=request.method,
						                      req=request.POST,
						                      createuser=request.user.username, createdate=timezone.now())
				if request.method == 'GET':
					# 记录日志
					AppLog.objects.create(username=request.user.username, nick_name=request.user.nick_name,
					                      user_type=request.user.type.type_name,
					                      browser_type=request.user.browser_type, device_type=request.user.device_type,
					                      urls=request.get_full_path(), methods=request.method, req=request.GET,
					                      createuser=request.user.username, createdate=timezone.now())

			elif request.path.startswith(root_url + '/test/post/'):
				pass

			else:
				return JsonResponse(request, {})

		# 用户锁定下，跳转到锁定界面
		if request.method in ['GET']:
			if (request.path not in ingore_url and request.path != root_url + '/user/lockscreen/'
					and request.path != root_url + '/logout/'):
				if request.user.lockscreen:
					return HttpResponseRedirect(root_url + '/user/lockscreen/')
