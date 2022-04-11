from django.urls import path
from django.views.generic import RedirectView
from appTest.views import TestView, ChartTestView, TableTestView, IcoTestView, FormTestView, PostTestView, UiTestView

urlpatterns = [
	path('test/<int:no>/', TestView.as_view()),
	path('test/chart/', ChartTestView.as_view()),
	path('test/table/', TableTestView.as_view()),
	path('test/ico/', IcoTestView.as_view()),
	path('test/form/', FormTestView.as_view()),
	path('test/ui/', UiTestView.as_view()),

	path('test/post/test/', PostTestView.as_view()),
	
]
