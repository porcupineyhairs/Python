from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from project.global_setting import global_setting

global_setting = global_setting(None)
root_url = global_setting.get('root_url2')


urlpatterns = [
	path('', RedirectView.as_view(url=root_url)),
	path(root_url + 'admin/', admin.site.urls),
	path(root_url + '', RedirectView.as_view(url='index')),
	
	# 引用App的url配置
	path(root_url, include('appBase.urls')),
	path(root_url, include('appUsers.urls')),
	path(root_url, include('appComfortSc.urls')),
	path(root_url, include('appComfortCw.urls')),
	path(root_url, include('appComfortHr.urls')),
	path(root_url, include('appTest.urls')),
	path(root_url, include('appDingtalk.urls')),
]

# 全局404页面配置
handler404 = 'appBase.views.pag_not_found'
# 全局500页面配置
handler500 = 'appBase.views.page_error'
