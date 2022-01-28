import datetime
import urllib.request
import json
import os
import requests


def make_dir(make_dir_path):
	path = make_dir_path.strip()
	if not os.path.exists(path):
		os.makedirs(path)
	return path


def json_loads(json_str):
	try:
		rtn = json.loads(json_str)
		return rtn
	except:
		return json_str


def getNetworkTime():
	intime = str(urllib.request.urlopen("http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp").read().decode())
	one = intime[:intime.rfind('"')]
	times = datetime.datetime.fromtimestamp(int(one[one.rfind('"')+1:-3]))
	return times


def timeCompare():
	netWorkTime = getNetworkTime()
	localTime = datetime.datetime.now()
	stopTime = datetime.datetime.strptime('2022-10-31', '%Y-%m-%d').date()
	return True if netWorkTime.date() < stopTime and localTime.date() < stopTime else False


def getStatus():
	timestamp = int(datetime.datetime.now().timestamp() * 2000000) + 12345123450
	time_now = datetime.datetime.now()

	headers = {'content-type': 'application/json'}
	data = {'data_str': str(timestamp), 'data_name': ''}
	rtn = False
	try:
		r = requests.post('https://harvey-tools.top/flask/others/function/status/get', data=json.dumps(data),
		                  headers=headers)
		data2 = r.json()
		data_status = data2.get('data_status', '')
		print(data_status)
		timestamp2 = data_status.split('|')[0]
		timestamp2 = (int(timestamp2) - 5123450) / 2000000.000000
		times = datetime.datetime.fromtimestamp(timestamp2)
		print(times)
		if times >= time_now:
			if (times - time_now).seconds < 30:
				rtn = True
	except:
		pass
	finally:
		# print(rtn)
		return rtn
