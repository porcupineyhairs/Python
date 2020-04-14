from ScheduleHelper import MOCTC2YHelper
from ScheduleHelper import AutoErpPlanHelper
from SqlHelper import MsSqlHelper
from BaseHelper import Logger
import sys
import os


loggerTest = Logger(sys.path[0] + '/Log/test.log')


def str_to_hex(s):
	# return '00'.join([hex(ord(c)).replace('0x', '') for c in s]).upper()
	returnStr = ''
	for c in s:
		strTmp = hex(ord(c)).replace('0x', '').upper()
		print(strTmp)
		print(len(strTmp))
		if len(strTmp) == 2:
			strTmp2 = strTmp + '00'
		else:
			print(str(strTmp[2:4]))
			strTmp2 = strTmp[2:4] + strTmp[0:2]
		returnStr += strTmp2
	return returnStr


def int_to_hex(i):
	# return str(hex(i)).replace('0x', '').rjust(2, '0').upper()
	returnStr = ''
	strTmp = str(hex(i)).replace('0x', '').rjust(2, '0').upper()
	if len(strTmp) == 2:
		strTmp2 = strTmp + '00'
	else:
		print(str(strTmp[2:4]))
		strTmp2 = strTmp[2:4] + strTmp[0:2]
	returnStr += strTmp2
	return returnStr


if __name__ == '__main__':
	# moctc2y = MOCTC2YHelper(debug=False)
	# moctc2y.work()

	# mssql = MsSqlHelper(host='192.168.1.61', user='sa', passwd='comfortgroup2016{', database='COMFORT')
	#
	autoPlan = AutoErpPlanHelper(host='192.168.0.99')
	if not autoPlan.workingFlag:
		autoPlan.work()
	# autoPlan.test()
	# loggerTest.logger.info('aaaa')
