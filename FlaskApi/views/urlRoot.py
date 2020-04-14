from flask import current_app, Blueprint, request, jsonify
from modules.Log import flaskLog


urlRoot = Blueprint('', __name__)


# 收藏图标
@urlRoot.route('/favicon.ico', methods=['GET'])
def get_favicon_ico():
	return current_app.send_static_file('img/favicon.ico')


# 主页
@urlRoot.route('/', methods=['PUT', 'GET', 'POST', 'DELETE', 'PATCH', 'OPTIONS', 'LOCK', 'UNLOCK'])
def webRootIndex():
	rtnDict = {'method': request.method}
	flaskLog(request=request, rtnDict=rtnDict)
	return jsonify(rtnDict)
