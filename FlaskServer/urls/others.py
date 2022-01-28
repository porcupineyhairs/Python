from flask import Blueprint, request, jsonify
import base64
import datetime

others_root_blueprint = Blueprint('others_root_blueprint', __name__)


@others_root_blueprint.route('/', methods=['GET'])
def index():
	return '<title>Flask</title><body><h1>Welcome Others Root Url!</body>'


@others_root_blueprint.route('/function/status/get', methods=['POST'])
def comfort_function_status():
	time_now = datetime.datetime.now()
	timestamp_now = int(time_now.timestamp() * 2000000) + 5123450
	status = '1234567890' + '|false'

	rtn_data = {'time': time_now, 'data_status': str(status)}
	try:
		data = request.get_json(force=True)
		timestamp = data.get('data_str', '')
		# data_name = data.get('data_name', '')
		if timestamp != '':
			timestamp = (int(timestamp) - 12345123450) / 2000000.0000000
			# print(timestamp)
			times = datetime.datetime.fromtimestamp(timestamp)
			secode = (time_now - times).seconds
			if time_now > times:
				if secode <= 120:
					rtn_data.update({'data_status': str(timestamp_now) + '|true'})
	except:
		pass
	finally:
		return jsonify(rtn_data)
