from flask import Flask, request
import logging
import os
import time
import json
from config import AppConfig
from urls import root_blueprint
from urls.api import api_root_blueprint
from urls.web import web_root_blueprint
from urls.others import others_root_blueprint


def make_dir(make_dir_path):
	path = make_dir_path.strip()
	if not os.path.exists(path):
		os.makedirs(path)
	return path


def json_loads(json_str):
	try:
		rtn = json.loads(json_str)
		return rtn
	except:
		return json_str


app = Flask(__name__, static_folder='../static', template_folder='../templates')

# 设置全局logger的最低等级，避免二级logger等级设置不成功
logging.root.setLevel(logging.NOTSET)

log_dir_name = 'logs'
log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
log_file_folder = '/'.join(app.root_path.split(os.sep)[0:-1]) + os.sep + log_dir_name
make_dir(log_file_folder)
log_file_str = log_file_folder + os.sep + log_file_name
log_handler = logging.FileHandler(log_file_str, mode='a', encoding='UTF-8')
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))


app.config.from_object(AppConfig)
app.logger.addHandler(log_handler)


app.register_blueprint(root_blueprint, url_prefix='/flask')
app.register_blueprint(api_root_blueprint, url_prefix='/flask/api')
app.register_blueprint(web_root_blueprint, url_prefix='/flask/web')
app.register_blueprint(others_root_blueprint, url_prefix='/flask/others')


@app.route('/favicon.ico', methods=['GET'])
def get_favicon_ico():
	return app.send_static_file('image/favicon.ico')


@app.before_request
def before_request():
	pass


@app.after_request
def after_request(response):
	url = request.url.replace('://', '').split('/', 1)[1]
	url_type = url.split('/', 1)[0]
	methods = request.method
	if url_type in ['api', 'others']:
		request_data = request.data.decode("utf-8")
		response_data = response.data.decode("utf-8")
		status_code = response.status_code
		log_str = {
			'url': url,
			'methods': methods,
			'status': status_code,
			'request_data': json_loads(request_data),
			'response_data': json_loads(response_data),
		}
		if status_code == 200:
			app.logger.info(log_str)
		elif status_code == 404:
			app.logger.error(log_str)
		else:
			app.logger.warning(log_str)
	return response
