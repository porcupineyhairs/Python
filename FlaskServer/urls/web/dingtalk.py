from flask import Blueprint, render_template, request, jsonify

web_dingtalk_blueprint = Blueprint('web_dingtalk_blueprint', __name__)


@web_dingtalk_blueprint.route('/test')
def test():
	header = request.headers
	user_agent = request.headers.get('User-Agent')
	print(user_agent)
	client_type = 'pc'
	if user_agent.count('AliApp'):
		if user_agent.count('iPhone'):
			client_type = 'ios-app'
		elif user_agent.count('Android'):
			client_type = 'android-app'
		else:
			client_type = 'mobile-app'
	elif user_agent.count('dingtalk-win'):
		client_type = 'win-app'
	elif user_agent.count('Mac'):
		client_type = 'mac-app'
	print(client_type)
	return render_template('scan_code.html')


@web_dingtalk_blueprint.route('/yida/get', methods=['POST', 'GET', 'PUT', 'DELETE'])
def get_data():
	data = request.data
	print('data: ', data)
	rtn_data = {
		'data': ['1', '2', '3', '4', '5']
	}
	return jsonify(rtn_data)


@web_dingtalk_blueprint.route('/yida/get2', methods=['POST', 'GET', 'PUT', 'DELETE'])
def get_data2():
	method = request.method
	data = request.data
	print('data: ', data)
	print(request)
	rtn_data = {
		'data': ['2', '2', '3', '4', '5']
	}
	return jsonify(rtn_data)
