from SqlHelper import MsSqlHelper
from BaseHelper import Logger
import sys


class INVMBBoxSize:
	def __init__(self, debug=False, logger=Logger(sys.path[0] + '/Log/debug.log'), host='192.168.0.99'):
		self.__logger = logger
		self.__debugMode = debug
		self.__host = host

		self.__mssql = None

		self.workingFlag = False

	def __log(self, string, mode='info'):
		if mode == 'info':
			self.__logger.logger.info('INVMBBoxSize: {}'.format(string))
		elif mode == 'error':
			self.__logger.logger.error('INVMBBoxSize: {}'.format(string))
		elif mode == 'warning':
			self.__logger.logger.warning('INVMBBoxSize: {}'.format(string))

	def __del(self):
		del self.__mssql
		self.__mssql = None

	def work(self):
		self.__log('Work Start')
		self.__mssql = MsSqlHelper(host=self.__host, user='sa', passwd='comfortgroup2016{', database='COMFORT')

		try:
			self.__work()
		except Exception as e:
			self.__log(mode='error', string=str(e))
		finally:
			self.__log('Work Finished')
			self.__mssql = None

	def __work(self):
		sqlStr = "SELECT RTRIM(MB001), RTRIM(MB003) FROM COMFORT.dbo.INVMB WHERE 1=1 AND MB025 = 'P' " \
		         "AND MB109 = 'Y' AND (MB002 LIKE '%纸箱%' OR MB002 LIKE '%彩盒%' OR MB002 LIKE '%天地盖%') ORDER BY MB001 "
		get = self.__mssql.sqlWork(sqlStr=sqlStr)
		if get is not None:
			for getTmp in get:
				if str(getTmp[1]).count('*') < 2:
					continue
				else:
					sizeStr = getTmp[1].split('/')[1]
					L, W, H = None, None, None
					if sizeStr.count('*') == 2:
						try:
							L = int(sizeStr.split('*')[0].split('(')[0].split('（')[0])
							W = int(sizeStr.split('*')[1].split('(')[0].split('（')[0])
							H = int(sizeStr.split('*')[2].split('(')[0].split('（')[0])
						except:
							continue
						finally:
							if all([L, W, H]):
								# print(getTmp[0], sizeStr, str(L)+'*'+str(W)+'*'+str(H), L*W*H)
								self.__update(getTmp[0], str(L)+'*'+str(W)+'*'+str(H), L*W*H)

	def __update(self, wlno, mbu01, mbu02):
		sqlStr = "update COMFORT.dbo.INVMB SET MBU01='{1}', MBU02={2} WHERE MB001 = '{0}' "
		self.__mssql.sqlWork(sqlStr=sqlStr.format(wlno, mbu01, mbu02))
