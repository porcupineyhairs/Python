# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.db.models import Q, F
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.core.paginator import Paginator

from project.views import global_setting
import datetime


urlpatterns = [
	# path(root_url + '', RedirectView.as_view(url='index')),
]
