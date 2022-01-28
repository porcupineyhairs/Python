from flask import current_app, Blueprint, request, jsonify
from views.api.dingtalk.ComfortErpHandler import CreateMoctg

api_dingtalk_program_comforterp_blueprint = Blueprint('api_dingtalk_program_comforterp_blueprint', __name__)


@api_dingtalk_program_comforterp_blueprint.route('/<string:method>', methods=['POST'])
def get(method):
	create = CreateMoctg()
	if method == 'get':
		return create.get()
