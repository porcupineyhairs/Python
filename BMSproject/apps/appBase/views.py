# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse, StreamingHttpResponse
from django.utils.encoding import escape_uri_path
from django.views.generic.base import View
from django.db.models import Q, F
from django.core.paginator import Paginator
import os
import pandas as pd
import uuid
from appBase.function import BaseFunction
from project.views import global_setting


root_url = global_setting.get('root_url')


class FileDownloadView(View):
	def get(self, request):
		url_parm = BaseFunction.UrlParmOpt.get_url_parm_get(request)
		file_path = url_parm.get('file_path')
		file_name = url_parm.get('file_name')
		file_ext = os.path.splitext(f'static/temp_file/download/{file_path}')[-1]
		file = open(f'static/temp_file/download/{file_path}', 'rb')
		if not os.path.isfile(f'static/temp_file/download/{file_path}'):  # 判断下载文件是否存在
			return HttpResponse("Sorry but Not Found the File")
		else:
			response = StreamingHttpResponse(file)
			response['Content-Type'] = 'application/octet-stream'
			response['Content-Disposition'] = "attachment;filename*=UTF-8''{0}".format(escape_uri_path(file_name + file_ext))
			return response

	def post(self, request):
		opt = request.POST.get('opt', '')
		data = request.POST.get('data', '')
		file_name = request.POST.get('file_name', '')
		if opt != '':
			rtn_dict = {}
			if opt == 'export':
				uuid_name = str(uuid.uuid1()) + '.xlsx'
				df = pd.read_json(data)
				df.to_excel('static/temp_file/download/' + uuid_name, index=None, encoding='utf-8')
				rtn_dict.update({'status': 'ok', 'msg': '',
				                 'url': root_url + f'/download/temp/file/?file_path={uuid_name}&file_name={file_name}'})
			return JsonResponse(rtn_dict)
		else:
			return JsonResponse({'status': 'err', 'msg': '参数错误'})


def pag_not_found(request, exception):
	# 全局404处理函数
	response = render(request, 'a_base_404.html', locals())
	response.status_code = 404
	return response


def page_error(request):
	# 全局500处理函数
	response = render(request, 'a_base_500.html', locals())
	response.status_code = 500
	return response
