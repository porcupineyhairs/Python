from flask import current_app, Blueprint, request, render_template, redirect


urlRoot = Blueprint('', __name__)


# 收藏图标
@urlRoot.route('/favicon.ico', methods=['GET'])
def get_favicon_ico():
	return current_app.send_static_file('img/favicon.ico')


# 主页
@urlRoot.route('/', methods=['GET'])
def webIp():
	return render_template('urlRoot/index.html')
