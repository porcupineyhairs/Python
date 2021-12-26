from flask import Blueprint

api_dingtalk_program_vacation_blueprint = Blueprint('api_dingtalk_program_vacation_blueprint', __name__)


@api_dingtalk_program_vacation_blueprint.route('/api/dingtalk/program/vacation/get', methods=['POST'])
def get_user_vacation():
	# data = request.get_json(force=True)
	# auth_code = data['authCode']
	# auth_user = DdUser(current_app.root_path)
	# result = auth_user.get_dd_info_authcode(auth_code)
	# return jsonify(result)
	pass
