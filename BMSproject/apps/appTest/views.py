# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from appBase.models import AppConfig
from django.db.models import Q, F
from django.core.paginator import Paginator
from project.views import global_setting


root_url = global_setting.get('root_url')


class TestView(View):
	def get(self, request, no):
		return render(request, 'a_test_demo.html', locals())
