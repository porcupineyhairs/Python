from django.urls import path
from django.views.generic import RedirectView
from appTest.views import TestView

urlpatterns = [
	path('<int:no>', TestView.as_view()),
	
]
