import dingtalk
from flask import Flask, request, jsonify, Response, current_app
import json

app = Flask(__name__)
basic_url = '/api/dingtalk/program'

app_key = "dings4y1o268lz7a1tui"
app_secret = "siZV69D95QZQaozl4wKrPF5cMp3eaS9xIfL04PH5QT2rQY-gHYd-ia915gnm3AnO"
corp_id = "1143998841"

# 新 access_token 获取方式
# client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)


@app.route(basic_url + '/welcome', methods=['GET'])
def welcome():
	return 'Welcome'


@app.route(basic_url + '/login', methods=['POST'])
def login():
	result = {'result': {'userId': '1', 'userName': '00'}}
	try:
		data = request.get_json(force=True)
		# print(data)
		auth_code = data['authCode']
		user_id = get_dd_user_id(auth_code=auth_code)
		# print(user_id)
		user_name, user_code = get_dd_user_info(user_id=user_id)
		# print(user_name)
		result = {'result': {'userId': user_id, 'userName': user_name, 'userCode': user_code}}
	except:
		# result = {'err': None}
		pass
	finally:
		return jsonify(result)


def get_dd_user_id(auth_code):
	client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)
	info = client.user.getuserinfo(auth_code)
	# print(info)
	return info['userid']


def get_dd_user_info(user_id):
	client = dingtalk.AppKeyClient(corp_id=corp_id, app_key=app_key, app_secret=app_secret)
	info = client.user.get(user_id)
	print(info)
	dd_user_name = info['name']
	dd_user_position = info['position']
	dd_user_code = info['jobnumber']
	dd_user_mobile = info['mobile']
	return dd_user_name, dd_user_code


if __name__ == '__main__':
	app.run(debug=True, port=8000, host='127.0.0.1', threaded=True)
	# get_dd_user_info('01180666186637615720')
