import json
from Module import MsSql
import requests
from Module import AES16


def WebClient():
	aes16 = AES16()
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
	# pda_JH.MainWork(get_json)
	print(json.dumps(get_json))
	

def DbTime():
	info = {'Mode': 'Sort'}
	r = requests.post("http://192.168.1.60:8099/Client/GetTime", data=json.dumps(info))
	print(r.json())
	
	
def sqltest():
	conn = ['40.73.246.171', 'sa', 'DGlsdnkj168', 'test']
	mssql = MsSql()
	get = mssql.Sqlwork(conn, 'select * from test0')
	
	print(get)
	

def Perm():
	from Module import Permission
	userPerm = Permission.UserPermission()
	# __get = userPerm.getUserPermission(userId='000068')
	# print(__get)
	# userPerm.setUserPermission(userId='000068', permList=['码垛线_订单类别编码管理', '玖友_查询物料需求量'])
	

def _Json():
	detail = [['99', True],
	          ['97', False],
	          ['95', True]]
	title = ['first', 'second']
	dict = None
	
	if detail is not None and title is not None:
		dict = []
		if len(title) == len(detail[0]):
			for rowIndex in range(len(detail)):
				for colIndex in range(len(title)):
					dictTmp = {title[colIndex]: detail[rowIndex][colIndex]}
					dict.append(dictTmp)
	
	print(json.dumps(dict))
	

if __name__ == '__main__':
	WebClient()
	# JHXA()
	# MD()
	# DbTime()
	# sqltest()
	# Perm()
	# _Json()
