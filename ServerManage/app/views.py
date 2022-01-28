import os
import uuid
import time
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login as login2, logout as logout2
from app.models import Program, OptionType, LoginLog, OptionLog

from django.core.paginator import Paginator
from ServerManage.global_setting import global_setting

root_url = global_setting(None).get('root_url')


class LoginView:
	# 登录
	@staticmethod
	def login(request):
		user = request.user
		if user.is_authenticated:
			return HttpResponseRedirect(root_url + '/index/')
		else:
			if request.POST:
				username = request.POST.get('username')
				password = request.POST.get('password')
				user = authenticate(username=username, password=password)
				if user is not None:
					login2(request, user)
					username = user.username
					# LoginLog.objects.create(username=username, log_type='login')
					return HttpResponseRedirect(root_url + '/index/')
				else:
					msg = '账号或密码错误'
					return render(request, 'a_login.html', locals())
			else:
				return render(request, 'a_login.html', locals())
	
	# 退出
	@staticmethod
	def logout(request):
		user = request.user
		username = user.username
		# LoginLog.objects.create(username=username, log_type='logout')
		logout2(request)
		return HttpResponseRedirect(root_url + '/login/')
	
	@staticmethod
	def user_show(request, uid):
		user = request.user
		if user.is_authenticated:
			return render(request, 'user_show.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/login/')


class IndexView:
	# 系统管理员主页
	@staticmethod
	def index(request):
		user = request.user
		if user.is_authenticated:
			program_list = Program.objects.all()
			return render(request, 'a_index.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/login/')


class ProgramView:
	@staticmethod
	def program_show(request):
		user = request.user
		if user.is_authenticated:
			return render(request, 'a_index.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/login/')
	
	@staticmethod
	def program_add(request):
		user = request.user
		if user.is_authenticated:
			if request.POST:
				progname = request.POST.get('progname')
				systemname = request.POST.get('systemname')
				remark = request.POST.get('remark')
				Program.objects.create(prog_name=progname, system_name=systemname, remark=remark)
				return HttpResponseRedirect(root_url + '/index/')
			else:
				return render(request, 'program_add.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/login/')
	
	@staticmethod
	def program_update(request, kid):
		user = request.user
		if user.is_authenticated:
			if request.POST:
				progname = request.POST.get('progname')
				systemname = request.POST.get('systemname')
				remark = request.POST.get('remark')
				Program.objects.filter(id=kid).update(prog_name=progname, system_name=systemname, remark=remark)
				
			program_list = Program.objects.filter(id=kid).all()[0]
			return render(request, 'program_update.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/login/')
	
	@staticmethod
	def program_delete(request, kid):
		user = request.user
		if user.is_authenticated:
			if request.POST:
				Program.objects.filter(id=kid).delete()
			return HttpResponseRedirect(root_url + '/index/')
		else:
			return HttpResponseRedirect(root_url + '/login/')
	
	@staticmethod
	def program_status(request, kid):
		user = request.user
		if user.is_authenticated:
			program_list = Program.objects.filter(id=kid).all()[0]
			prog_name = program_list.prog_name
			system_name = program_list.system_name
			remark = program_list.remark
			
			from app.function import ProgramStatusInfo
			program_status = ProgramStatusInfo()
			active, status, pid, enable = program_status.get_status(program_name=system_name)
			set_list = []
			if enable is True:
				set_list.append({'name': '关闭开机自启', 'set_type': 'disable'})
			else:
				set_list.append({'name': '打开开机自启', 'set_type': 'enable'})
				
			if active == 'Active':
				set_list.append({'name': '停止', 'set_type': 'stop'})
			else:
				set_list.append({'name': '运行', 'set_type': 'start'})
			
			return render(request, 'program_status.html', locals())
		else:
			return HttpResponseRedirect(root_url + '/login/')
	
	@staticmethod
	def program_set_type(request, kid, set_type):
		user = request.user
		if user.is_authenticated:
			program_list = Program.objects.filter(id=kid).all()[0]
			system_name = program_list.system_name
			
			from app.function import ProgramStatusInfo
			program_status = ProgramStatusInfo()
			
			if set_type == 'stop':
				program_status.set_stop(system_name)
			elif set_type == 'start':
				program_status.set_start(system_name)
			elif set_type == 'enable':
				program_status.set_enable(system_name)
			elif set_type == 'disable':
				program_status.set_disable(system_name)
			
			time.sleep(0.5)
			return HttpResponseRedirect(root_url + '/program_status/' + str(kid) + '/')
		else:
			return HttpResponseRedirect(root_url + '/login/')
