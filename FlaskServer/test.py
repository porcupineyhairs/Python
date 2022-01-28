import datetime
import requests
import json

timestamp = int(datetime.datetime.now().timestamp() * 2000000) + 12345123450
time_now = datetime.datetime.now()

headers = {'content-type': 'application/json'}
data = {'data_str': str(timestamp), 'data_name': ''}
rtn = False
try:
	r = requests.post('https://harvey-tools.top/flask/others/function/status/get', data=json.dumps(data), headers=headers)

	data2 = r.json()
	data_status = data2.get('data_status', '')
	print(data_status)
	timestamp2 = data_status.split('|')[0]
	timestamp2 = (int(timestamp2) - 5123450) / 2000000.000000
	times = datetime.datetime.fromtimestamp(timestamp2)
	print(times, time_now)
	if times >= time_now:
		if (times - time_now).seconds < 30:
			rtn = True
except:
	pass
finally:
	# return rtn
	print(rtn)
