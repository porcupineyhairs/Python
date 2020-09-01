from SqlHelper import MsSqlHelper
from BaseHelper import Logger
import sys


class GetBomList:
	def __init__(self, debug=False, logger=Logger(sys.path[0] + '/Log/debug.log'), host='192.168.0.99'):
		self.__logger = logger
		self.__debugMode = debug
		self.__host = host

		self.__mssql = None

		self.workingFlag = False

	def __log(self, string, mode='info'):
		if mode == 'info':
			self.__logger.logger.info('GetBomList: {}'.format(string))
		elif mode == 'error':
			self.__logger.logger.error('GetBomList: {}'.format(string))
		elif mode == 'warning':
			self.__logger.logger.warning('GetBomList: {}'.format(string))

	def __del(self):
		del self.__mssql
		self.__mssql = None

	def work(self, mode='title'):
		try:
			self.__log('Work Start')
			self.workingFlag = True

			self.__mssql = MsSqlHelper(host=self.__host, user='sa', passwd='comfortgroup2016{', database='COMFORT')

			while self.workingFlag:
				self.__work()

		except Exception as e:
			self.workingFlag = False
			self.__log(str(e), mode='error')

		finally:
			self.workingFlag = False
			self.__del()
			self.__log('Work Finished')

	def __work(self):
		sqlStr = "SELECT RTRIM(MB001) FROM INVMB(NOLOCK) INNER JOIN BOMCA(NOLOCK) ON CA003 = MB001 " \
		         "WHERE MB025 = 'M' AND MB109 = 'Y' AND (MB001 LIKE '1%' OR MB001 LIKE '2%') " \
		         "ORDER BY MB001 "
		get = self.__mssql.sqlWork(sqlStr=sqlStr)
		self.__log('成品号数量：' + str(len(get)))
		if get is not None:
			for tmp in get:
				wlno = tmp[0]
				self.__log(wlno)
				lists = self.__getBomWork(wlno)
				if lists is not None:
					self.__deleteList(wlno)
					self.__insertList(wlno, lists)
		self.workingFlag = False

	def __insertList(self, materials=None, lists=None):
		sqlStr = "INSERT INTO BOMCB_List VALUES('{0}', '{1}', '{2}', {3})"
		if len(lists) > 0:
			for tmp in lists:
				self.__mssql.sqlWork(sqlStr=sqlStr.format(materials, tmp[0], tmp[2], tmp[1]))

	def __deleteList(self, materials=None):
		if materials is not None:
			sqlStr = "delete from BOMCB_List where CB001 = '{0}'"
			self.__mssql.sqlWork(sqlStr=sqlStr.format(materials))

	def __getBomWork(self, materials):
		aa = self.getBom(materials)
		self.__getListSort(aa, lambda x: (x[0], x[2]))
		self.__getMaterialSum(getList=aa, cmpList=[0, 2], sumList=[1])
		return aa

	# 单阶BOM明细的SQL查询
	def __getBomListSelect(self, materials=None, typeC=False):
		sqlstr = (r"SELECT RTRIM(CB005) 品号, CAST(CB008 AS FLOAT)/CAST(CB009 AS FLOAT) 用量, "
		          r"MB025 品号属性, CB011 工艺 "
		          r"FROM BOMCB(NOLOCK) "
		          r"INNER JOIN INVMB(NOLOCK)  ON MB001= CB005 "
		          r"WHERE 1=1 "
		          r"AND MB109 = 'Y' "
		          r"AND (CB013 <= CONVERT(VARCHAR(20), GETDATE(), 112) OR CB013 IS NULL OR RTRIM(CB013) = '') "
		          r"AND (CB014 > CONVERT(VARCHAR(20), GETDATE(), 112) OR CB014 IS NULL OR RTRIM(CB014) = '') "
		          r"AND CB001 = '{0}' ")
		if typeC:
			sqlstr += r"AND CB015 = 'Y' "
		sqlstr += r"ORDER BY CB004"

		getList = self.__mssql.sqlWork(sqlStr=sqlstr.format(materials))
		if getList is None:
			getList = []
		return getList

	# BOM品号用量明细的递归循环逻辑
	def __getBomList(self, materials, listTmp=None, coefficient=1.0, typeC=False, getAll=True):
		if listTmp is None:
			listTmp = []

		getList = self.__getBomListSelect(materials=materials, typeC=typeC)

		for getListTmp in getList:
			rowTmp = []
			if getListTmp[2] in ('P', 'S'):
				rowTmp.append(getListTmp[0])
				rowTmp.append(coefficient * getListTmp[1])
				rowTmp.append(getListTmp[3])
				listTmp.append(rowTmp)
			elif getListTmp[2] == 'C' and not getAll:
				self.__getBomList(getListTmp[0], listTmp=listTmp, coefficient=getListTmp[1], typeC=True, getAll=getAll)
			else:
				self.__getBomList(getListTmp[0], listTmp=listTmp, coefficient=getListTmp[1], getAll=getAll)
		back = listTmp
		return back

	# BOM根据品号补全品号其他信息
	def __getMaterialInfo(self, materials):
		sqlstr = "SELECT RTRIM(MB004), RTRIM(MB002), RTRIM(MB003), RTRIM(MB032) FROM INVMB(NOLOCK) WHERE MB001 = '{0}' "

		getList = self.__mssql.sqlWork(sqlStr=sqlstr.format(materials))
		if getList is None:
			getList = []
		return getList[0]

	# 获取BOM明细的主入口
	def getBom(self, materials=None):
		if materials is None:
			return []
		else:
			getBom = self.__getBomList(materials, getAll=False)
			if len(getBom) == 0:
				return None
			else:
				for getBomTmp in getBom:
					# getMaterial = self.__getMaterialInfo(getBomTmp[0])
					# getBomTmp.extend(getMaterial)
					pass
				return getBom

	# # 二维列表列筛选、复制，可复用
	# def getNewList(getList=None, colList=None):
	# 	if len(numpy.array(getList).shape) == 2:
	# 		if colList is not None:
	# 			getListBck = getList[:]
	# 			getList.clear()
	# 			for getListBckTmp in getListBck:
	# 				rowTmp = []
	# 				for colListTmp in colList:
	# 					rowTmp.append(getListBckTmp[colListTmp])
	# 				getList.append(rowTmp)

	# 二维列表的排序，可复用
	def __getListSort(self, getList=None, key=None):
		getListBck = getList[:]
		getList.clear()
		getList.extend(sorted(getListBck, key=key))

	# 二维列表根据特定列汇总，可复用
	def __getMaterialSum(self, getList=None, cmpList=None, sumList=None):
		getListBck = getList[:]
		getList.clear()
		rowTmp2 = []
		rowTmp1 = []
		for getListBckTmp in getListBck:
			if len(getList) == 0:
				getList.append(getListBckTmp)
			else:
				rowTmp1.clear()
				rowTmp2.clear()
				for cmpListTmp in cmpList:
					rowTmp1.append(getList[-1][cmpListTmp])
					rowTmp2.append(getListBckTmp[cmpListTmp])
				if rowTmp1 == rowTmp2:
					for sumListTmp in sumList:
						getList[-1][sumListTmp] += getListBckTmp[sumListTmp]
				else:
					getList.append(getListBckTmp)
