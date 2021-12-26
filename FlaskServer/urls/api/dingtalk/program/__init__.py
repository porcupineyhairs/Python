from flask import Blueprint
from urls.api.dingtalk.program.user import api_dingtalk_program_user_blueprint
from urls.api.dingtalk.program.permission import api_dingtalk_program_permission_blueprint
from urls.api.dingtalk.program.vacation import api_dingtalk_program_vacation_blueprint

api_dingtalk_program_buleprint = Blueprint('api_dingtalk_program', __name__)

api_dingtalk_program_buleprint.register_blueprint(api_dingtalk_program_user_blueprint, url_prefix='/user')
api_dingtalk_program_buleprint.register_blueprint(api_dingtalk_program_permission_blueprint, url_prefix='/permission')
api_dingtalk_program_buleprint.register_blueprint(api_dingtalk_program_vacation_blueprint, url_prefix='/vacation')


@api_dingtalk_program_buleprint.route('/', methods=['GET'])
@api_dingtalk_program_buleprint.route('', methods=['GET'])
def program_welcome():
	return 'Dingtalk Program Welcome!'
