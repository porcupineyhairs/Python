from django.urls import path
from django.views.generic import RedirectView
from appDingtalk.views import DingTalkAutoLoginMainView

urlpatterns = [
	path('login/autologin/main/', DingTalkAutoLoginMainView.as_view()),
	
]
