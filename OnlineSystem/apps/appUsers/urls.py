from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from appUsers.views import LoginView, LogoutView, IndexView, UserProfileView, UserRegisterView, UserPasswordView, \
	UserLockScreenView, DepartmentView, UserTypeView, UserManagerView, PermissionBaseView

urlpatterns = [
	path('login/', LoginView.as_view()),
	path('logout/', LogoutView.as_view()),
	path('index/', IndexView.as_view()),
	path('user/profile/', UserProfileView.as_view()),
	path('user/password/', UserPasswordView.as_view()),
	path('user/register/', UserRegisterView.as_view()),
	path('user/lockscreen/', UserLockScreenView.as_view()),

	path('manage/departments/', DepartmentView.as_view()),
	path('manage/usertypes/', UserTypeView.as_view()),
	path('manage/users/', UserManagerView.as_view()),
	path('manage/permission-base/', PermissionBaseView.as_view()),
	# path('manage/permission-group/', DepartmentView.as_view()),
	# path('manage/permission-user/', DepartmentView.as_view()),

]
