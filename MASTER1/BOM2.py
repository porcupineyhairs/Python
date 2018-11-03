
import sqlite3
import time
STR = []


# def SelectSqlite3(sqlcmd):
# 	GetBack = []
# 	conn = sqlite3.connect("./DB.db")
# 	cur = conn.cursor()
# 	cur.execute(sqlcmd)
# 	conn.commit()
# 	res = cur.fetchall()
# 	# 关闭连接
# 	cur.close()
# 	conn.close()
# 	if len(res) == 0:
# 		GetBack = None
# 	for List in res:
# 		GetBack.append(list(List))
# 	return GetBack


def Main():
	Str0 = (r"SELECT TR009, TR017, TR200 FROM COPTR WHERE 1=1 "
			r"AND RTRIM(TR001) = '10710101' AND RTRIM(TR002) = '保友 TW绿 标配' "
			r"AND RTRIM(TR004) = '24000017' AND RTRIM(TR009) = '3010304004' ")
	# get = SelectSqlite3(Str0)

	get = None

	if get is not None:
		print(get[0][0])
		print(get[0][1])
		get = get[0][2]
		kk = get.split(' ')
		ss = []
		for k in kk:
			if k != '':
				ss.append(k)
		print(ss)
		del ss[0]
		del ss[0]
		print(ss)
	else:
		print(get)
