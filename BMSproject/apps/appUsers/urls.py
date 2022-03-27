from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from appUsers.views import LoginView, LogoutView, IndexView, UserProfileView, UserRegisterView, UserPasswordView, \
	UserLockScreenView, DepartmentView

urlpatterns = [
	path('login/', LoginView.as_view()),
	path('logout/', LogoutView.as_view()),
	path('index/', IndexView.as_view()),
	path('user/profile/', UserProfileView.as_view()),
	path('user/password/', UserPasswordView.as_view()),
	path('user/register/', UserRegisterView.as_view()),
	path('user/lockscreen/', UserLockScreenView.as_view()),

	path('manage/department/', DepartmentView.as_view()),
	path('manage/permission/base/', DepartmentView.as_view()),
	path('manage/permission/group/', DepartmentView.as_view()),
	path('manage/permission/user/', DepartmentView.as_view()),

]
