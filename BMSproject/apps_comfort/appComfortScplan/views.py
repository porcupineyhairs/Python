# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
import os
import uuid

from project.global_setting import global_setting


global_setting = global_setting(None)
root_url = global_setting.get('root_url')

