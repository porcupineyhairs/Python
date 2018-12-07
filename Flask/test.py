import Module
from Module.ModuleDictionary import DataBase_Dict
from Module.SelfModule import MsSql
from Module.MaDuoSystem.MD_GetInfo import GetInfo
import requests
import json


def Main():
	mssql = MsSql()
	conn = DataBase_Dict['ROBOT_TEST']
	sqlstr = "UPDATE SCHEDULE SET SC038 = 'y' WHERE SC001 = '{0}'"
	li = ['2212-DY001261-0001', '2212-DY001262-0001', '2212-DY001262-0004']
	for i in li:
		sqlstr1 = sqlstr.format(i)
		mssql.Sqlwork(DataBase=conn, SqlStr=sqlstr1)
	print(1)


def WebClient():
	info = {'Mode': 'Insert'}
	r = requests.post("http://192.168.7.252:8099/Client/MaDuo/GetInfo", data=json.dumps(info))
	print(r.json())


def MaxSize(__Item):
	Vol = []
	for i in range(len(__Item)):
		Num = __Item[i].split('*')
		Size = int(Num[0]) * int(Num[1]) * int(Num[2])
		Vol.append(Size)
	print(__Item[Vol.index(max(Vol))])


if __name__ == '__main__':
	# MaxSize(['540*240*180', '540*240*160', '540*210*180'])
	MD = GetInfo()
	MD.MainWork()
