import requests
import json


def WebClient():
	info = {'Mode': 'Insert'}
	r = requests.post("http://192.168.1.60:8099/Client/PDA/JH_LYXA", data=json.dumps(info))
	print(r.json())
	
	
def MD():
	from Module.MaDuoSystem.MD_GetInfo import GetInfo as MDGetInfo
	getinfo = MDGetInfo()
	getinfo.MainWork()
	
	
def JHXA():
	from Module.PDA.JH_LYXA import PDA_JH_Handle
	pda_JH = PDA_JH_Handle()
	pda_JH.MainWork('JH201812250956060001')
	
	
def sql():
	from Module import MsSql
	from Module import DataBase_Dict
	mssql = MsSql()
	Conn = DataBase_Dict['ROBOT_TEST']
	sqlstr0 = r"UPDATE BoxSizeCode SET Valid = 'N' "
	sqlstr1 = r"SELECT BoxSize, BoxCode, BoxSet FROM T123"
	sqlstr2 = r"SELECT BoxSize, BoxCode, BoxSet FROM BoxSizeCode WHERE BoxSize = '{0}' "
	sqlstr3 = r"UPDATE BoxSizeCode SET BoxCode = '{1}', BoxSet = '{2}', Valid = 'Y' WHERE BoxSize = '{0}' "
	sqlstr4 = (r"INSERT INTO BoxSizeCode (BoxSize, BoxCode, BoxSet, Valid) "
	           r"VALUES ('{0}', '{1}', '{2}', 'Y')")
	mssql.Sqlwork(DataBase=Conn, SqlStr=sqlstr0)
	get = mssql.Sqlwork(DataBase=Conn, SqlStr=sqlstr1)
	if get[0] != 'None':
		print(len(get))
		for item in get:
			print(item[0])
			get2 = mssql.Sqlwork(DataBase=Conn, SqlStr=sqlstr2.format(item[0]))
			if get2[0] != 'None':
				print('update', item[0])
				mssql.Sqlwork(DataBase=Conn, SqlStr=sqlstr3.format(item[0], item[1], item[2]))
			else:
				print('insert', item[0])
				mssql.Sqlwork(DataBase=Conn, SqlStr=sqlstr4.format(item[0], item[1], item[2]))


if __name__ == '__main__':
	# WebClient()
	# MD()
	# sql()
	JHXA()
