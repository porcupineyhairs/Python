from flask import Blueprint, request, jsonify
from views.api.dingtalk.PermissionHandler import Permission

api_dingtalk_program_permission_blueprint = Blueprint('api_dingtalk_program_permission_blueprint', __name__)


@api_dingtalk_program_permission_blueprint.route('/<string:method>', methods=['POST'])
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
