"""BMSproject URL Configuration

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
from django.urls import path, re_path
from django.views.generic import RedirectView

from app.views import index, zhuce, denglu, exitd, appdept, appproduct, apppversion, appmeans, appmatter, appproject
from app.views import showuser, upuser, showdept, updetp, showproduct, upproduct, banben, fileupload
from app.views import showmeans, wenjiandd, meanswj, showmiaoshu, showproject, upproject, showmatter, jshowmatter
from app.views import upmatter, fenpeimatter, jshowuser, jshowdept, jshowproduct, qshowmatter, qupmatter, xmindex, cpindex, kfindex

from app.views import gerenxinxi, jshowproject, kshowmatter, wenjianxiazai, filexiazai2, tzsucess, goajax, xiangmu, deptselect

from app.views import projectselect, jueseselect, souname

from app.global_setting import global_setting

global_setting = global_setting(None)
root_url = global_setting.get('root_url2')


urlpatterns = [
	path('', RedirectView.as_view(url=root_url)),
	# path('/', RedirectView.as_view(url=root_url)),
	path(root_url + '', RedirectView.as_view(url='index')),
	path(root_url + 'admin/', admin.site.urls),
	path(root_url + 'index/', index),
	path(root_url + 'zhuce/', zhuce),
	path(root_url + 'denglu/', denglu),
	path(root_url + 'exitd/', exitd),
	path(root_url + 'appdept/', appdept),
	path(root_url + 'appproduct/', appproduct),
	path(root_url + 'apppversion/', apppversion),
	path(root_url + 'appmeans/', appmeans),
	path(root_url + 'appmatter/', appmatter),
	path(root_url + 'appproject/', appproject),
	
	path(root_url + 'showuser/', showuser),
	path(root_url + 'upuser/<int:uid>/', upuser),
	path(root_url + 'showdept/', showdept),
	path(root_url + 'updept/<int:deptdid>/', updetp),
	path(root_url + 'showproduct/', showproduct),
	path(root_url + 'upproduct/<int:pid>/', upproduct),
	path(root_url + 'banben/', banben),
	path(root_url + 'fileupload/', fileupload),
	path(root_url + 'showmeans/', showmeans),
	path(root_url + 'wenjiandd/', wenjiandd),
	path(root_url + 'meanswj/', meanswj),
	path(root_url + 'showmiaoshu/<int:mid>/', showmiaoshu),
	path(root_url + 'showproject/', showproject),
	path(root_url + 'upproject/<int:pid>/', upproject),
	path(root_url + 'showmatter/', showmatter),
	path(root_url + 'upmatter/<int:mid>/', upmatter),
	path(root_url + 'fenpeimatter/<int:mid>/', fenpeimatter),
	path(root_url + 'jshowuser/', jshowuser),
	path(root_url + 'jshowdept/', jshowdept),
	path(root_url + 'jshowproduct/', jshowproduct),
	path(root_url + 'qshowmatter/', qshowmatter),
	path(root_url + 'qupmatter/<int:mid>/', qupmatter),
	path(root_url + 'jshowmatter/', jshowmatter),
	path(root_url + 'xmindex/', xmindex),
	path(root_url + 'cpindex/', cpindex),
	path(root_url + 'kfindex/', kfindex),
	path(root_url + 'gerenxinxi/<int:uid>/', gerenxinxi),
	path(root_url + 'jshowproject/', jshowproject),
	path(root_url + 'kshowmatter/', kshowmatter),
	path(root_url + 'wenjianxiazai/', wenjianxiazai),
	path(root_url + 'filexiazai2/<str:filename>/', filexiazai2),
	path(root_url + 'tzsucess/', tzsucess),
	path(root_url + 'goajax/<str:username>/', goajax),
	path(root_url + 'xiangmu/', xiangmu),
	path(root_url + 'deptselect/<int:deptid>/', deptselect),
	path(root_url + 'projectselect/<int:projectid>/', projectselect),
	path(root_url + 'jueseselect/<str:juese>/', jueseselect),
	path(root_url + 'souname/', souname),
]
