from flask import current_app, Blueprint, send_file, render_template
import os


urlDownload = Blueprint('download', __name__)


@urlDownload.route('/', methods=['GET'])
def downloadIndex():
	return 'download'


@urlDownload.route('/<string:url>', methods=['GET'])
def downloadFile(url):
	return render_template('urlDownload/download.html', url=url)


@urlDownload.route('/file/<path:url>', methods=['GET'])
def downloadFileWork(url):
	downloadPath = current_app.root_path + '/downloadFile/files/'
	if os.path.exists(downloadPath + url):
		return send_file(downloadPath + str(url), as_attachment=True)
	else:
		return 'File "{}" Dose Not Exists!'.format(url)
