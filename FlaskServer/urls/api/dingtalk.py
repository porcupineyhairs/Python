from flask import current_app, Blueprint, request, jsonify
from views.api.dingtalk.ComfortErpHandler import CreateMoctg
from views.api.dingtalk.PermissionHandler import Permission
from views.api.dingtalk.UserHandler import DdUser


api_dingtalk_blueprint = Blueprint('api_dingtalk_buleprint', __name__)


@api_dingtalk_blueprint.route('/', methods=['GET'])
@api_dingtalk_blueprint.route('', methods=['GET'])
def program_welcome():
	return 'Dingtalk Welcome!'


@api_dingtalk_blueprint.route('/program/user/authUser/<string:method>', methods=['POST'])
def get_auth_user(method):
	data = request.get_json(force=True)
	result = {}
	if method == 'get':
		auth_code = data['authCode']
		dd_user = DdUser(current_app.root_path)
		result = dd_user.get_dd_user_info_by_authcode(auth_code)
		# print(result)
	return jsonify(result)


@api_dingtalk_blueprint.route('/program/user/reSyncUser/<string:method>', methods=['POST'])
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


@api_dingtalk_blueprint.route('/program/permission/<string:method>', methods=['POST'])
def user_permission(method):
	data = request.get_json(force=True)
	permission = Permission()
	result = {}
	dd_user_id = data['dd_user_id']
	if method == 'get':
		permission = permission.get_user_perm(dd_user_id)
		result = {'userId': dd_user_id, 'permission': permission}
	if method == 'del':
		result = None
	if method == 'new':
		result = None
	if method == 'update':
		result = None
	# print(result)
	return jsonify(result)


@api_dingtalk_blueprint.route('/program/comforterp/<string:method>', methods=['POST'])
def get(method):
	create = CreateMoctg()
	if method == 'get':
		return create.get()
	
	
@api_dingtalk_blueprint.route('/program/vacation/get', methods=['POST'])
def get_user_vacation():
	# data = request.get_json(force=True)
	# auth_code = data['authCode']
	# auth_user = DdUser(current_app.root_path)
	# result = auth_user.get_dd_info_authcode(auth_code)
	# return jsonify(result)
	pass
