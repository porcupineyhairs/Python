from flask import Blueprint
from urls.api.dingtalk import api_dingtalk_blueprint

api_root_blueprint = Blueprint('api_root_blueprint', __name__)


api_root_blueprint.register_blueprint(api_dingtalk_blueprint, url_prefix='/dingtalk')
