from flask import Blueprint
from .program import api_dingtalk_program_buleprint

api_dingtalk_blueprint = Blueprint('api_dingtalk_blueprint', __name__)

api_dingtalk_blueprint.register_blueprint(api_dingtalk_program_buleprint, url_prefix='/program')
