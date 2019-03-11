import json
from Module import MsSql
import requests


def WebClient():
	info = {'Mode': 'Insert'}
	r = requests.post("http://192.168.0.197/Client/MaDuo/GetInfo", data=json.dumps(info))
	print(r.json())
	
	
def MD():
	from Module.MaDuoSystem.MD_GetInfo import GetInfo as MDGetInfo
	getinfo = MDGetInfo()
	getinfo.MainWork()
	
	
def JHXA():
	from Module.PDA.JH_LYXA import PDA_JH_Handle, PDA_JH_GetInfo
	pda_JH = PDA_JH_GetInfo()
	get_json = {'Uid': '001114', 'Mode': 'Complete', 'Parameter': 'JH201812281329460001', 'Data': '', 'RowCount': '4'}
	pda_JH.MainWork(get_json)
	

def DbTime():
	info = {'Mode': 'Sort'}
	r = requests.post("http://192.168.1.60:8099/Client/GetTime", data=json.dumps(info))
	print(r.json())
	
	
def sqltest():
	conn = ['40.73.246.171', 'sa', 'DGlsdnkj168', 'test']
	mssql = MsSql()
	get = mssql.Sqlwork(conn, 'select * from test0')
	
	print(get)
	



if __name__ == '__main__':
	# WebClient()
	# JHXA()
	MD()
	# DbTime()
	# sqltest()
