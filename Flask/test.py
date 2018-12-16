import requests
import json


def WebClient():
	info = {'Mode': 'Insert'}
	r = requests.post("http://192.168.1.60:8099/Client/MaDuo/GetInfo", data=json.dumps(info))
	print(r.json())
	
	
def MD():
	from Module.MaDuoSystem.MD_GetInfo import GetInfo as MDGetInfo
	getinfo = MDGetInfo()
	getinfo.MainWork()


if __name__ == '__main__':
	WebClient()
	# MD()
