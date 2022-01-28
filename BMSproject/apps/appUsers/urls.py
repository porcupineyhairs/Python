from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from appUsers.views import LoginView, LogoutView, IndexView

urlpatterns = [
	path('login/', LoginView.as_view()),
	path('logout/', LogoutView.as_view()),
	path('index/', IndexView.as_view()),
]
