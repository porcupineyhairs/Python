from flask import Blueprint
from urls.api.dingtalk import api_dingtalk_blueprint
from urls.api.test import api_test_blueprint

api_root_blueprint = Blueprint('api_root_blueprint', __name__)


api_root_blueprint.register_blueprint(api_dingtalk_blueprint, url_prefix='/dingtalk')
api_root_blueprint.register_blueprint(api_test_blueprint, url_prefix='/test')


@api_root_blueprint.route('/', methods=['GET'])
def index():
	return '<title>Flask</title><body><h1>Welcome Api Root Url!</body>'
