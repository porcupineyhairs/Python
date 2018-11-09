
import sqlite3
import time
from SelfModule import MsSql
from LIB.ModuleDictionary import DataBase_Dict
STR = []




def Main():
	Str0 = (r"SELECT TR009, TR017, TR200 FROM COPTR WHERE 1=1 "
			r"AND RTRIM(TR001) = '10710101' AND RTRIM(TR002) = '保友 TW黑 中性包装' "
			r"AND RTRIM(TR004) = '24004317' AND RTRIM(TR009) = '401020118' ")
	get = mssql.Sqlwork(DataBase=Conn, SqlStr=Str0)
	ll = []
	if get is not None:
		print(get[0][0])
		print(get[0][1])
		get = get[0][2]
		kk = get.split(' ')
		ss = []
		for k in kk:
			if k != '':
				ss.append(k)
		del ss[0]
		del ss[0]
		print(ss)
		for i in range(1, len(ss), 2):
			ll.append(ss[i])

		print(ll)
	else:
		print(get)


if __name__ == '__main__':
	mssql = MsSql()
	Conn = DataBase_Dict['COMFORT']
	Main()
