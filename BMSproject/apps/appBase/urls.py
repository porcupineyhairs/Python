from django.urls import path
from django.views.generic import RedirectView

from project.global_setting import global_setting

global_setting = global_setting(None)
root_url = global_setting.get('root_url2')


urlpatterns = [
]
