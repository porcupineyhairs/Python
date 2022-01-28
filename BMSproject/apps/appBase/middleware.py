from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from user_agents import parse
from project import views


root_url = views.root_url


class MiddlewareApp(MiddlewareMixin):
	def process_request(self, request):
		ua_string = request.META.get('HTTP_USER_AGENT', '')
		# print(ua_string)
		ua = parse(ua_string)
		# print(ua.os.family)
		if request.method == 'GET':
			user = request.user
			ingore_url = [
				root_url + '/login/',
				root_url + '/dingtalk/login/autologin/main/',
				root_url + '/wechat/login/autologin/main/',
				]
			if request.path in ingore_url:
				pass
			else:
				if user.is_authenticated:
					pass
				else:
					return HttpResponseRedirect(root_url + '/login/')
		else:
			pass
