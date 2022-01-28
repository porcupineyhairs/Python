# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from appBase.models import AppConfig
from django.db.models import Q, F
from django.core.paginator import Paginator
import dingtalk
import json
from project.views import global_setting


root_url = global_setting.get('root_url')


# 钉钉内部访问，免密登录
class DingTalkAutoLoginMainView(View):
	def get(self, request):
		ua_string = request.META.get('HTTP_USER_AGENT', '')
		if ua_string.count('DingTalk') > 0:
			user = request.user
			if user.is_authenticated:
				return render(request, 'a_normal_index.html', locals())
			else:
				dingtalk_config_json = AppConfig.objects.filter(apps='dingtalk', name='app', valid=1).all()[0].value
				dingtalk_config = json.loads(dingtalk_config_json)
				dingtalk_corpid = dingtalk_config['corp_id']
				return render(request, 'a_autologin_dingtalk.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/login/')
		
	def post(self, request):
		ua_string = request.META.get('HTTP_USER_AGENT', '')
		result = {'status': 'fail'}

		if ua_string.count('DingTalk') > 0:
			try:
				# print(request.body)
				body = json.loads(request.body)
				auth_code = body.get('auth_code')

				dingtalk_config_json = AppConfig.objects.filter(apps='dingtalk', name='app', valid=1).all()[0].value
				dingtalk_config = json.loads(dingtalk_config_json)
				dd_client = dingtalk.AppKeyClient(corp_id=dingtalk_config['corp_id'],
				                                  app_key=dingtalk_config['app_key'],
				                                  app_secret=dingtalk_config['app_secret'])

				info = dd_client.user.getuserinfo(auth_code)
				dingtalkid = info['userid']
				info2 = dd_client.user.get(dingtalkid)
				mobile = info2['mobile']
				# print(dingtalkid, mobile)

				user = authenticate(dingtalkid=dingtalkid, mobile=mobile, types='DingTalk')
				if user is not None:
					login(request, user)
					result.update({'status': 'ok'})
			except Exception as e:
				print(e)
				result.update({'status': 'error'})
			finally:
				return JsonResponse(result)
		else:
			return JsonResponse(result)
