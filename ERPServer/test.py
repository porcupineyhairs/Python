from ScheduleHelper import *
from SqlHelper import MsSqlHelper
from BaseHelper import Logger
import sys


loggerTest = Logger(sys.path[0] + '/Log/debug.log')
sql99 = MsSqlHelper(host='192.168.0.99', user='sa', passwd='comfortgroup2016{', database='COMFORT')


if __name__ == '__main__':
	print('test')
	# work = INVMBBoxSize()
	# work = GetBomList()
	# work = AutoErpPlanHelper()
	# # work.test()
	# work.work()
	
	print('AA'.ljust(10, ' '))
