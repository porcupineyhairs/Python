from SqlHelper import MsSqlHelper

mssql = MsSqlHelper(host='172.16.210.239', user='sa', passwd='comfortsjl2013{', database='Comfortseating')


# 清除ERP系统日志
def cleanLog():
	index = 1
	sqlstr1 = r"SELECT TOP 2000 TB001, TB002, RTRIM(TB003), RTRIM(TB004), CONVERT(VARCHAR(50), TB006, 21), RTRIM(TB007) FROM ADMTB " \
			  r"WHERE 1=1 " \
			  r"AND TB003 LIKE 'MOC%' " \
			  r"ORDER BY TB006 "
	
	sqlstr2 = r"DELETE FROM ADMTB WHERE TB001 = '{0}' AND TB002 = '{1}' AND TB003 = '{2}' AND TB004 = '{3}' " \
	          r"AND TB006 = '{4}' AND TB007 = '{5}'"

	flag = True

	while flag:
		dt1 = mssql.sqlWork(sqlstr1)

		if dt1 is None:
			flag = False
		else:
			for dt1Tmp in dt1:
				print(index, dt1Tmp)
				mssql.sqlWork(sqlstr2.format(dt1Tmp[0], dt1Tmp[1], dt1Tmp[2], dt1Tmp[3], dt1Tmp[4], dt1Tmp[5]))

				index += 1

			

if __name__ == '__main__':
	cleanLog()
