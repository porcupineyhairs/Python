from ScheduleHelper import *
from SqlHelper import MsSqlHelper
from BaseHelper import Logger
import sys


loggerTest = Logger(sys.path[0] + '/Log/debug.log')
sql99 = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')



def main():
	sqlStr = r"Select top 20 TD001+'-'+TD002+TD003 FROM COPTD " \
	         r"INNER JOIN WG_DB..SC_PLAN ON SC001 = RTRIM(TD001)+'-'+RTRIM(TD002)+'-'+RTRIM(TD003) " \
	         r"INNER JOIN INVMB ON MB001 = TD004 AND MB025 = 'M' " \
	         r"WHERE SC003 >= '20210101' " \
	         r"AND NOT EXISTS (SELECT 1 FROM MOCTB_Group WHERE TA026 = TD001 AND TA027 = TD002 AND TA028 = TD003) "

	sqlStr2 = "EXEC P_SetMOCTBGroup '{0}' "

	get = sql99.sqlWork(sqlStr)

	if get is not None:
		for tmp in get:
			dd = tmp[0]
			print(dd)
			# sql99.sqlWork(sqlStr2.format(dd))


if __name__ == '__main__':
	print('test')
	# work = INVMBBoxSize()
	# work = GetBomList()
	# work = AutoErpPlanHelper()
	# # work.test()
	# work.work()
	
	# print('AA'.ljust(10, ' '))
	main()
