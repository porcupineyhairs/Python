from flask import current_app, Blueprint, request, jsonify
from views.api.dingtalk.UserHandler import DdUser

api_dingtalk_program_user_blueprint = Blueprint('api_dingtalk_program_user_blueprint', __name__)


@api_dingtalk_program_user_blueprint.route('/authUser/<string:method>', methods=['POST'])
def get_auth_user(method):
	data = request.get_json(force=True)
	result = {}
	if method == 'get':
		auth_code = data['authCode']
		dd_user = DdUser(current_app.root_path)
		result = dd_user.get_dd_user_info_by_authcode(auth_code)
		# print(result)
	return jsonify(result)


@api_dingtalk_program_user_blueprint.route('/reSyncUser/<string:method>', methods=['POST'])
def re_sync_user(method):
	data = request.get_json(force=True)
	dd_user = DdUser(current_app.root_path)
	result = {}
	job_number = data['jobnumber']
	if method == 'get':
		result = dd_user.get_user_info(job_number)
	if method == 'del':
		result = dd_user.set_dd_del_info_by_user_code(job_number)
	if method == 'new':
		result = dd_user.set_dd_new_info_by_user_code(job_number)
	if method == 'update':
		result = dd_user.set_dd_update_info_by_user_code(job_number)
	# print(result)
	return jsonify(result)
