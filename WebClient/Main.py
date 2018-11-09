import requests
import json


def WebClient():
	info = {'Mode': 'Insert'}
	r = requests.post("http://192.168.7.252/Client/MaDuo/GetInfo", data=json.dumps(info))
	print(r.json())


if __name__ == '__main__':
	WebClient()
