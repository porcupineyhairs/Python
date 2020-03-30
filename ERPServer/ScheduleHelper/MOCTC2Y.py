from SqlHelper.MsSql import MsSqlHelper
from BaseHelper.ErpMsg import MsgHelper
from BaseHelper import Logger
import sys


class MOCTC2YHelper:
	def __init__(self, debug=False, host='192.168.0.99', logger=Logger(sys.path[0] + '/Log/MOCTC2Y.log')):
		self.__debugMode = debug
		self.__host = host
		self.__logger = logger

		self.__mssql = None
		self.__erpMsg = None
		self.__getData = None
		self.__sendReceiver = None
		self.__sendMsgStr = None
		self.__creator = 'Robot'
		self.__returnStr = None

	def __log(self, string, mode='info'):
		if mode == 'info':
			self.__logger.logger.info('MOCTC2Y: {}'.format(string))
		elif mode == 'error':
			self.__logger.logger.error('MOCTC2Y: {}'.format(string))
		elif mode == 'warning':
			self.__logger.logger.warning('MOCTC2Y: {}'.format(string))

	def work(self):
		self.__mssql = MsSqlHelper(host=self.__host, user='sa', passwd='comfortgroup2016{', database='COMFORT')
		self.__erpMsg = MsgHelper(debug=self.__debugMode)

		self.__clean()
		self.__getDd()
		if self.__getData is not None:
			self.__returnStr = []
			self.__setSendStr()
			self.__log(str(self.__returnStr))
		else:
			self.__log('没有获取到数据')
			if self.__debugMode:
				print('没有获取到数据')

		if not self.__debugMode:
			self.__setFinishFlag()

		del self.__mssql
		self.__mssql = None
		# return str(self.__returnStr)

	def __clean(self):
		self.__getData = None
		self.__sendReceiver = None
		self.__sendMsgStr = None
		self.__returnStr = None

	def __getDd(self):
		sqlStr1 = "UPDATE COMFORT.dbo.MOCTC SET UDF08 = 'n' WHERE UDF08 = 'N' "
		sqlStr2 = "SELECT DISTINCT RTRIM(TA.TA026) TA026, RTRIM(TA.TA027) TA027 " \
		          "FROM COMFORT.dbo.MOCTC AS TC " \
		          "INNER JOIN COMFORT.dbo.MOCTE AS TE ON TC.TC001 = TE.TE001 AND TC.TC002 = TE.TE002 " \
		          "INNER JOIN COMFORT.dbo.MOCTB AS TB ON TE.TE011 = TB.TB001 AND TE.TE012 = TB.TB002 " \
		          "INNER JOIN COMFORT.dbo.MOCTA AS TA ON TB.TB001 = TA.TA001 AND TB.TB002 = TA.TA002 " \
		          "WHERE 1=1 " \
		          "AND NOT EXISTS( " \
		          "SELECT 1 FROM COMFORT.dbo.MOCTA AS TA2 " \
		          "INNER JOIN COMFORT.dbo.MOCTB AS TB2 ON TA2.TA001 = TB2.TB001 AND TA2.TA002 = TB2.TB002 " \
		          "INNER JOIN COMFORT.dbo.MOCTE AS TE2 ON TE2.TE011 = TB2.TB001 AND TE2.TE012 = TB2.TB002 " \
		          "INNER JOIN COMFORT.dbo.MOCTC AS TC2 ON TC2.TC001 = TE2.TE001 AND TC2.TC002 = TE2.TE002 " \
		          "WHERE 1=1 " \
		          "AND (TB2.TB004 - TB2.TB005 <=0 OR TC2.TC009 = 'N') " \
		          "AND TA011 NOT IN ('y', 'Y') " \
		          "AND TA.TA026 = TA2.TA026 AND TA.TA027 = TA2.TA027 ) " \
		          "AND TC.UDF08 = 'n' " \
		          "AND TA.TA026 != '2215'" \
		          "ORDER BY RTRIM(TA.TA026), RTRIM(TA.TA027)"
		self.__mssql.sqlWork(sqlStr=sqlStr1)
		self.__getData = self.__mssql.sqlWork(sqlStr=sqlStr2)

	def __getReceiver(self, TA026, TA027):
		sqlStr = "SELECT DISTINCT ERPID, RTRIM(MV.MV002) ERPNAME " \
		         "FROM COMFORT.dbo.MOCTA AS TA " \
		         "INNER JOIN COMFORT.dbo.CMSME AS ME ON ME.ME001 = TA.TA064 " \
		         "INNER JOIN CONFIG.dbo.ERPMSG AS ERPMSG ON ME.ME002 = ERPMSG.ERPDPT " \
		         "INNER JOIN COMFORT.dbo.CMSMV AS MV ON MV.MV001 = ERPID " \
		         "WHERE 1=1  " \
		         "AND TA.TA026 = '{0}' AND TA.TA027 = '{1}' " \
		         "ORDER BY ERPID "
		self.__sendReceiver = self.__mssql.sqlWork(sqlStr=sqlStr.format(TA026, TA027))

	def __setSendStr(self):
		self.__sendReceiver = None
		self.__sendMsgStr = None
		for info in self.__getData:
			self.__getReceiver(info[0], info[1])
			if self.__sendReceiver is not None:
				self.__returnStr.append([['订单', str(info[0]) + '-' + str(info[1])], ['收件人', self.__sendReceiver]])
				self.__sendMsgStr = '<P>&nbsp;</P><P>此订单已完成工单领料</P><P>订单号：{0}-{1}</P>'.format(info[0], info[1])
				self.__sendMsg()

	def __sendMsg(self):
		self.__erpMsg.sendMsg(creator=self.__creator, title='订单完成领料通知', receivers=self.__sendReceiver,
		                      msgText=self.__sendMsgStr)

	def __setFinishFlag(self):
		sqlStr = "UPDATE COMFORT.dbo.MOCTC SET UDF08 = 'Y' WHERE UDF08 = 'n' "
		self.__mssql.sqlWork(sqlStr)
