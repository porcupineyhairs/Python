from django.shortcuts import render, render_to_response

# Create your views here.

from django.http import HttpResponse
import GlobalVar



def index(request):
	# return HttpResponse("Hello, world. You're at the polls index66866.")
	GetBack0 = '<link rel="shortcut icon" href="{{ url_for("static", filename="favicon.ico") }}">'
	GetBack1 = '<form test><select name="cars"><option value="volvo">Volvo</option><option value="saab">Saab</option><option value="fiat" selected="selected">Fiat</option><option value="audi">Audi</option></select></form>'
	GetBack2 = '<select>  <option value ="volvo">Volvo</option>  <option value ="saab">Saab</option><option value="opel">Opel</option><option value="audi">Audi</option></select>'
	GetBack3 = '<button type="button">Click Me!</button>'
	return HttpResponse(GetBack1 + GetBack2 + GetBack3 + GetBack0)


def table(request):
	file = open(GlobalVar.BASE_DIR + '/1.html').read()
	return HttpResponse(file)


def index2(request):
	# return render(request, GlobalVar.BASE_DIR + '/root/index.html')
	return render_to_response('index.html')


def add(request):
	num1 = request.GET['num1']
	num2 = request.GET['num2']
	sum = int(num1) + int(num2)
	return render(request, GlobalVar.BASE_DIR + '/root/index.html', {'sum': sum})
