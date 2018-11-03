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
# 		GetBack.append('None')
# 	for List in res:
# 		GetBack.append(list(List))
# 	return GetBack




def mysql():
	import pymysql

	# 打开数据库连接
	db = pymysql.connect("localhost", "root", "Tiamohui", "COMFORT")

	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = db.cursor()

	Str0 = (r"SELECT DISTINCT "
			r"RTRIM(CB005), "  # 本阶品好
			r"RTRIM(MB002), "  # 品名
			r"RTRIM(MB003), "  # 规格
			r"RTRIM(CB004), "  # 序号
			r"RTRIM(INVMB.MB025), "  # 品号属性
			r"RTRIM(INVMB.MB109), "  # 核准状况
			r"RTRIM(MW001), "  # 工艺编码
			r"RTRIM(CB013), "
			r"RTRIM(CB014) "
			r"FROM BOMCB  "
			r"LEFT JOIN CMSMW ON MW001 = CB011 "
			r"LEFT JOIN INVMB ON CB005 = INVMB.MB001 "
			r"LEFT JOIN BOMCA ON CA003 = CB005 "
			r"LEFT JOIN INVMA ON INVMA.MA002 = INVMB.MB005 "
			r"LEFT JOIN PURMA ON PURMA.MA001 = INVMB.MB032 "
			r"WHERE CB001 = '" + str(000) + r"' "  # 上阶品号
			"AND (CB014 IS NULL OR CB014 = '' OR CB014 > '" + '20181021' + r"') "
			r"AND MB109 = 'Y' "
			r"ORDER BY RTRIM(CB004) ")

	# 使用 execute()  方法执行 SQL 查询
	cursor.execute(Str0)
	data = cursor.fetchall()
	db.close()
	print(data)


if __name__ == '__main__':
	mysql()
