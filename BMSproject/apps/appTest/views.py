# Create your views here.
import json
import os.path

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from appBase.models import AppConfig
from django.db.models import Q, F
from django.core.paginator import Paginator
from appBase.function import BaseFunction
from project.views import global_setting
from project.settings import STATICFILES_DIRS as static_dir
import pandas as pd


root_url = global_setting.get('root_url')


class TestView(View):
	def get(self, request, no):
		shoucang3_disabled = 'disabled'
		return render(request, 'a_test_demo.html', locals())

	def post(self, request, no):
		print(request.POST)
		if 'select' in request.POST.get("button"):
			msg = 'select'
			shoucang3_disabled = ''
			data = [
				{
					'a': 1,
					'b': 2,
				},
				{
					'a': 3,
					'b': 4,
				}
			]
		if 'output' in request.POST.get('button'):
			data = request.POST.get('data')
			print(data)
			msg3 = 'output'
			shoucang3_disabled = 'disabled'
		return render(request, 'a_test_demo.html', locals())


class TestView1(View):
	def get(self, request):
		return render(request, 'a_normal_index2.html', locals())


class TestView2(View):
	def get(self, request):
		datalist = [[93, 93, 0, 100.0], [20, 23, 26, 29]]
		return render(request, 'a_test_table.html', locals())


class PostTestView(View):
	def get(self, request):
		file = os.path.join(static_dir, 'temp_file', 'upload', 'aaaa.xlsx')
		df = pd.read_excel(open(file))
		return JsonResponse(df)

	def post(self, request):
		# print(static_dir[0])
		file = os.path.join(static_dir[0], 'temp_file/upload/aaaa.xlsx')
		# print(file)
		df = pd.read_excel(file)
		rtn = BaseFunction.DataFrameOpt.dataframe_2_dict(df)
		return JsonResponse(rtn, safe=False)

	def options(self, request, *args, **kwargs):
		# print(static_dir[0])
		file = os.path.join(static_dir[0], 'temp_file/upload/aaaa.xlsx')
		# print(file)
		df = pd.read_excel(file)
		rtn = BaseFunction.DataFrameOpt.dataframe_2_dict(df)

		return JsonResponse(rtn, safe=False)
