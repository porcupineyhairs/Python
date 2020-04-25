import os
from flask import current_app, Blueprint, make_response, send_from_directory


urlClient = Blueprint('Client', __name__)


@urlClient.route('/', methods=['GET'])
def mainIndex():
	return 'Client'


# 下载文件，联友外挂的更新下载
@urlClient.route("/WG/Download/<path:filename>", methods=['GET'])
def WG_DownloadFile(filename):
	directory = current_app.root_path + '/downloadFile/LyWg/'  # 文件目录
	# 判断所需文件是否存在
	if os.path.exists(directory + filename):
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".\
			format(filename.encode().decode('latin-1'))
		return response
	else:
		return None

