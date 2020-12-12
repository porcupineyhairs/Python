from SqlHelper import MsSqlHelper

mssql = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')


# 删除领料数量为0的INVLA, MOCTE(5401, 5406)
def cleanLlZero():
	sqlstr1 = r"SELECT LA006, RTRIM(LA007), LA008, LA001, LA009, LA010, " \
	          r"CAST(LA011 AS FLOAT), LA024 " \
	          r"FROM INVLA " \
	          r"WHERE 1=1 " \
	          r"AND LA004 BETWEEN '20200901' AND '20200931' " \
	          r"AND LA011 = 0 " \
	          r"AND LA006 IN ('5401', '5406') " \
	          r"ORDER BY LA004, LA006, RTRIM(LA007), LA008"
	
	sqlstr2 = r"DELETE FROM MOCTE WHERE TE001 = '{0}' AND TE002 = '{1}' AND TE003 = '{2}' " \
	          r"DELETE FROM INVLA WHERE LA006 = '{0}' AND LA007 = '{1}' AND LA008 = '{2}' "
	
	dt1 = mssql.sqlWork(sqlstr1)
	
	if dt1 is not None:
		print('共有' + str(len(dt1)) + '笔')
		index = 1
		for dt1Tmp in dt1:
			print(index, dt1Tmp)
			mssql.sqlWork(sqlstr2.format(dt1Tmp[0], dt1Tmp[1], dt1Tmp[2]))
			index += 1
		

# 订单已结束的工单，及其领料、生产入库、工单变更
def cleanGdFinished():
	sqlstr1 = r"SELECT TA001, RTRIM(TA002) TA002, TD001, TD002,TD003, TD016, TA011, TD004 " \
	          r"FROM MOCTA " \
	          r"INNER JOIN COPTD ON TD001 = TA026 AND TD002 = TA027 AND TD003 = TA028 " \
	          r"WHERE 1=1 " \
	          r"AND TD016 = 'Y' " \
	          r"AND TD013 BETWEEN '20140101' AND '20181231' " \
	          r"AND TA011 IN ('Y', 'y') " \
	          r"AND TA013 IN ('Y') " \
	          r"AND TA001 = '5101' " \
	          r"ORDER BY TA003, TD001, TD002, TD003"
	
	sqlstr2 = r"DELETE FROM MOCTE WHERE TE011 = '{0}' AND TE012 = '{1}' " \
	          r"DELETE FROM MOCTD WHERE TD003 = '{0}' AND TD004 = '{1}' " \
	          r"DELETE FROM MOCTG WHERE TG014 = '{0}' AND TG015 = '{1}' " \
	          r"DELETE FROM MOCTO WHERE TO001 = '{0}' AND TO002 = '{1}' " \
	          r"DELETE FROM MOCTP WHERE TP001 = '{0}' AND TP002 = '{1}' " \
	          r"DELETE FROM MOCTB WHERE TB001 = '{0}' AND TB002 = '{1}' " \
	          r"DELETE FROM MOCTA WHERE TA001 = '{0}' AND TA002 = '{1}' "
	
	dt1 = mssql.sqlWork(sqlstr1)
	
	if dt1 is not None:
		print('共有' + str(len(dt1)) + '笔')
		index = 1
		for dt1Tmp in dt1:
			print(index, dt1Tmp)
			mssql.sqlWork(sqlstr2.format(dt1Tmp[0], dt1Tmp[1]))
			index += 1


if __name__ == '__main__':
	cleanLlZero()
