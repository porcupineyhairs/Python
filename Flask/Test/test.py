import json
from Module import MsSql
import requests
from Module import EncryptDict


def WebClient():
	aes16 = EncryptDict()
	info = {'Mode': 'Insert'}
	r = requests.post("http://192.168.0.197:8099/Client/MaDuo/GetInfo", data=aes16.Encrypt(info))
	print(r)
	
	
def MD():
	from Module.MaDuoSystem.MD_GetInfo import GetInfo as MDGetInfo
	getinfo = MDGetInfo()
	getinfo.MainWork()
	
	
def JHXA():
	from Module.PDA.JH_LYXA import PDA_JH_Handle, PDA_JH_GetInfo
	# pda_JH = PDA_JH_GetInfo()
	# get_json = {'Uid': '001114', 'Mode': 'Complete', 'Parameter': 'JH201812281329460001', 'Data': '', 'RowCount': '4'}
	# pda_JH.MainWork(get_json)
	# print(json.dumps(get_json))
	
	jh_handel = PDA_JH_Handle()
	get = jh_handel.MainWork('JH201905201049460001')
	print(get)

def DbTime():
	info = {'Mode': 'Sort'}
	r = requests.post("http://192.168.1.60:8099/Client/GetTime", data=json.dumps(info))
	print(r.json())
	
	
def sqltest():
	conn = ['40.73.246.171', 'sa', 'DGlsdnkj168', 'WG_DB']
	mssql = MsSql()
	sqlstrLs_T = r" INSERT INTO LY_MaterialList_T (CreateDate, Status) VALUES ('{0}', 'Process')"
	get = mssql.Sqlwork(conn, sqlstrLs_T.format('20190101'))
	
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
	# WebClient()
	# JHXA()
	MD()
	# DbTime()
	# sqltest()
	# Perm()
	# _Json()
