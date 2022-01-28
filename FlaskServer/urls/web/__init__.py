from flask import Blueprint
from urls.web.comfort import web_comfort_blueprint
from urls.web.dingtalk import web_dingtalk_blueprint

web_root_blueprint = Blueprint('web_root_blueprint', __name__)


web_root_blueprint.register_blueprint(web_comfort_blueprint, url_prefix='/comfort')
web_root_blueprint.register_blueprint(web_dingtalk_blueprint, url_prefix='/dingtalk')


@web_root_blueprint.route('/', methods=['GET'])
def index():
	return '<title>Flask</title><body><h1>Welcome Web Root Url!</body>'
