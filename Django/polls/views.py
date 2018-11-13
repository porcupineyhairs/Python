from django.shortcuts import render
import GlobalVar

# Create your views here.

from django.http import HttpResponse


def index(request):
	# return HttpResponse("Hello, world. You're at the polls index.66777")
	# return HttpResponse('<p><input name="username"></p>')
	return render(request, GlobalVar.BASE_DIR + '/1.html')


def table(request):
	file = open(GlobalVar.BASE_DIR + '/1.html').read()
	return HttpResponse(file)
