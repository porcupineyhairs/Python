"""ServerManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from app.views import LoginView, ProgramView, IndexView

from ServerManage.global_setting import global_setting

global_setting = global_setting(None)
root_url = global_setting.get('root_url2')


urlpatterns = [
	path('', RedirectView.as_view(url=root_url)),
	path(root_url + '', RedirectView.as_view(url='index')),
	path(root_url + 'index/', IndexView.index),
	path(root_url + 'login/', LoginView.login),
	path(root_url + 'logout/', LoginView.logout),
	path(root_url + 'user_show/<int:kid>/', LoginView.user_show),
	
	path(root_url + 'program_add/', ProgramView.program_add),
	path(root_url + 'program_show/', ProgramView.program_show),
	path(root_url + 'program_status/<int:kid>/', ProgramView.program_status),
	path(root_url + 'program_update/<int:kid>/', ProgramView.program_update),
	path(root_url + 'program_delete/<int:kid>/', ProgramView.program_delete),
	path(root_url + 'program_set/<int:kid>/<str:set_type>/', ProgramView.program_set_type),
	
]
