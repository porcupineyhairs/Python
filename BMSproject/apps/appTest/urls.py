from django.urls import path
from django.views.generic import RedirectView
from appTest.views import TestView, TestView1, TestView2, PostTestView

urlpatterns = [
	path('test/<int:no>/', TestView.as_view()),
	path('test/test1/', TestView1.as_view()),
	path('test/test2/', TestView2.as_view()),

	path('test/post/test/', PostTestView.as_view()),
	
]
