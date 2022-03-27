from SqlHelper import MsSqlHelperBasic

mssql = MsSqlHelperBasic(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')


# 删除领料数量为0的INVLA, MOCTE(5401, 5406)
def cleanLlZero():
	sqlStr1 = r"SELECT LA006, RTRIM(LA007), LA008, LA004, LA001, LA009, LA010, " \
	          r"CAST(LA011 AS FLOAT), LA024 " \
	          r"FROM INVLA " \
	          r"WHERE 1=1 " \
	          r"AND LA004 BETWEEN '20210601' AND '20211231' " \
	          r"AND LA011 = 0 " \
	          r"AND LA006 IN ('5401', '5406') " \
	          r"ORDER BY LA004, LA006, RTRIM(LA007), LA008 "
	
	sqlStr2 = r"DELETE FROM MOCTE WHERE TE001 = '{0}' AND TE002 = '{1}' AND TE003 = '{2}' " \
	          r"DELETE FROM INVLA WHERE LA006 = '{0}' AND LA007 = '{1}' AND LA008 = '{2}' "

	sqlStr3 = r"SELECT TC001, TC002, TC003 FROM MOCTC  " \
			  r"WHERE NOT EXISTS ( " \
			  r"	SELECT 1 FROM MOCTE WHERE TE001 = TC001 AND TE002 = TC002 ) " \
			  r"AND TC009 = 'Y' " \
			  r"ORDER BY TC003"

	sqlStr4 = r"DELETE FROM MOCTD WHERE TD001 = '{0}' AND TD002 = '{1}' " \
			  r"DELETE FROM MOCTC WHERE TC001 = '{0}' AND TC002 = '{1}' "
	
	dt1 = mssql.sqlWork(sqlStr1)
	
	if dt1 is not None:
		print('领料数量为0的库存交易共有' + str(len(dt1)) + '笔')
		index = 1
		for dt1Tmp in dt1:
			print(index, dt1Tmp)
			mssql.sqlWork(sqlStr2.format(dt1Tmp[0], dt1Tmp[1], dt1Tmp[2]))
			index += 1

	dt2 = mssql.sqlWork(sqlStr3)

	if dt2 is not None:
		print('单身为空的领料单共有' + str(len(dt2)) + '笔')
		index = 1
		for dt2Tmp in dt2:
			print(index, dt2Tmp)
			mssql.sqlWork(sqlStr4.format(dt2Tmp[0], dt2Tmp[1]))
			index += 1


if __name__ == '__main__':
	cleanLlZero()
