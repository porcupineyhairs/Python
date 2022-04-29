from flask import current_app, Blueprint, send_file, render_template
from werkzeug.utils import safe_join 
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
	downloadPath = safe_join(current_app.root_path,'/downloadFile/files/',url)
	if os.path.exists(downloadPath):
		return send_file(downloadPath, as_attachment=True)
	else:
		return 'File "{}" Dose Not Exists!'.format(url)
