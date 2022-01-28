# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.db.models import Q, F
from django.core.paginator import Paginator
import os
import uuid
from project.global_setting import global_setting


global_setting = global_setting(None)
root_url = global_setting.get('root_url')


def pag_not_found(request, exception):
	# 全局404处理函数
	response = render(request, 'a_base_404.html', locals())
	response.status_code = 404
	return response


def page_error(request):
	# 全局500处理函数
	response = render(request, 'a_base_500.html', locals())
	response.status_code = 500
	return response
