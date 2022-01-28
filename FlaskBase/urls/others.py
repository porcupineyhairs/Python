from flask import Blueprint, current_app, redirect, make_response, send_from_directory
from modules import *

other_blueprint = Blueprint('other_blueprint', __name__)


# 主页重定向
@other_blueprint.route('/', methods=['GET'])
@other_blueprint.route('/local/file', methods=['GET'])
@other_blueprint.route('/local/file/download', methods=['GET'])
def root():
	return redirect('/flask/local/file/download/index')


# 下载文件，外挂程序的更新下载
@other_blueprint.route("/local/file/download/WgFile/<filename>", methods=['GET'])
def DownloadFile2(filename):
	if timeCompare():
		directory = current_app.root_path + '/WgFile/'  # 文件目录
		# 判断所需文件是否存在
		if os.path.exists(directory + filename):
			response = make_response(send_from_directory(directory, filename, as_attachment=True, conditional=True))
			response.headers["Content-Disposition"] = "attachment; filename={}".\
				format(filename.encode().decode('latin-1'))
			return response
		else:
			return r"Doesn't exist file! "
	else:
		return None


# 下载文件
@other_blueprint.route("/local/file/download/downloadFile/<filename>", methods=['GET'])
def DownloadFile3(filename):
	if timeCompare():
		directory = current_app.root_path + '/DownLoadFile/'  # 文件目录
		# 判断所需文件是否存在
		if os.path.exists(directory + filename):
			response = make_response(send_from_directory(directory, filename, as_attachment=True, conditional=True))
			response.headers["Content-Disposition"] = "attachment; filename={}".\
				format(filename.encode().decode('latin-1'))
			return response
		else:
			return r"Doesn't exist file! "
	else:
		return None


# 文件下载索引页面
@other_blueprint.route('/local/file/download/index', methods=['GET'])
def fileDownload():
	html = '<title>文件列表</title><h1>可下载文件</h1><br><br><h3>{0}</h3>'
	htmltmp = '<a href="/flask/local/file/download/downloadFile/{0}">{0}</a><br>'
	ll = ''
	file = open(current_app.root_path + '/DownLoadFile/DownLoadList.txt', mode='r', encoding='GBK')
	lists = file.readlines()

	for tmp in lists:
		if len(tmp) > 2:
			if tmp[0:2] == '--':
				pass
			else:
				ll += htmltmp.format(tmp)
		else:
			pass
	return html.format(ll)
