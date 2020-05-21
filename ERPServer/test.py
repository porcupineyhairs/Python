from ScheduleHelper import *
from SqlHelper import MsSqlHelper
from BaseHelper import Logger
import sys
import os


loggerTest = Logger(sys.path[0] + '/Log/test.log')
sql198 = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='ROBOT_TEST')
sql99 = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')


# def boxSize():
# 	sqlStr198Select = "SELECT SC001 FROM ROBOT_TEST.dbo.SCHEDULE " \
# 	                  "WHERE SC003 > CONVERT(VARCHAR(8), DATEADD(DAY, -7, GETDATE()), 112) AND SC039 = 'N' " \
# 	                  "ORDER BY SC003, SC001 "
# 	sqlStr99Select = "SELECT TOP 1 RTRIM(TA026)+'-'+RTRIM(TA027)+'-'+RTRIM(TA028) AS DD, ISNULL(MBU01, '') MBU01 " \
# 	                 "FROM COMFORT.dbo.MOCTA " \
# 	                 "LEFT JOIN COMFORT.dbo.MOCTB ON TA001 = TB001 AND TA002 = TB002 " \
# 	                 "LEFT JOIN COMFORT.dbo.INVMB ON MB001 = TB003 " \
# 	                 "WHERE 1=1 " \
# 	                 "AND MBU02 IS NOT NULL " \
# 	                 "AND (MB002 LIKE '%纸箱%' OR MB002 LIKE '%彩盒%' OR MB002 LIKE '%天地盖%') " \
# 	                 "AND RTRIM(TA026)+'-'+RTRIM(TA027)+'-'+RTRIM(TA028) = '{0}' " \
# 	                 "ORDER BY RTRIM(TA026)+'-'+RTRIM(TA027)+'-'+RTRIM(TA028), MBU02 DESC "
# 	sqlStr198Update = "UPDATE ROBOT_TEST.dbo.SCHEDULE SET SC040 = '{1}' WHERE SC001 = '{0}' "
#
# 	get = sql198.sqlWork(sqlStr198Select)
# 	if all([get]):
# 		for getTmp in get:
# 			get2 = sql99.sqlWork(sqlStr99Select.format(getTmp[0]))
# 			if all([get2]):
# 				print(sqlStr198Update.format(getTmp[0], get2[0][1]))
# 				sql198.sqlWork(sqlStr198Update.format(getTmp[0], get2[0][1]))


if __name__ == '__main__':
	print('test')
	# boxSize()
	bom = GetBomList()
	bom.work()
