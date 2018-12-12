import requests
import json


def WebClient(url, data):
	r = requests.post(url, data=data)
	print(r.json())


if __name__ == '__main__':
	# WebClient()
	WebClient(url='http://192.168.7.180:8099/Client/MaDuo/GetInfo', data=json.dumps({'Mode': 'Insert'}))
