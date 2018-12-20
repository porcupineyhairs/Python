from Module.SelfModule import MsSql
from Module.ModuleDictionary import DataBase_Dict
from Module.GetDbSvrTime import GetSvrTime


class PDA_JH_GetInfo:
	def __init__(self):
		self.__Conn_ERP = DataBase_Dict['COMFORT']
		self.__mssql = MsSql()
		self.__getSvrTime = GetSvrTime()
		self.__back = {'Return': 'Error',
		               'Parameter': 'Done',
		               'Data': None}
		self.__Mode = None
		self.__Parameter = None
		self.__Data = None
	
	def MianWork(self, __json=None):
		self.__init__()
		try:
			self.__Mode = __json['Mode']
			self.__Parameter = __json['Parameter']
			self.__Data = __json['Data']
			
			if self.__Mode == 'Select':
				self.__ModeSelect()
			elif self.__Mode == 'Insert':
				self.__ModeInsert()
			elif self.__Mode == 'Complete':
				self.__ModeComplete()
			else:
				print('Mode Out Of Index :', self.__Mode)
				self.__Mode = 'Error'
			self.__SetReturnMode(self.__Mode)
			self.__SetReturnParameter(self.__Parameter)
		except:
			print('Json Input Error\n', __json)
		finally:
			return self.__back
	
	def __ModeSelect(self):
		if self.__Parameter == 'FlowID':
			pass
		elif self.__Parameter == 'MaterielID':
			pass
		elif self.__Parameter == 'SupplierID':
			pass
		elif self.__Parameter == 'TypeID':
			pass
		elif self.__Parameter == 'PositionID':
			pass
		else:
			print('Parameter Out Of Index :', self.__Parameter)
			self.__Parameter = 'Error'
	
	def __ModeInsert(self):
		pass
	
	def __ModeComplete(self):
		pass
	
	def __GetFlowID(self, __FlowId=None):
		__Time = self.__getSvrTime.GetTime({'Mode': 'Long'})
		__Time = __Time['Time']
		if __FlowId is None:
			__FlowId = 'JH' + __Time + '0001'
			return __FlowId
		else:
			__sqlstr = r"SELECT RTRIM(JHXA005) FROM COMFORT..JH_LYXA WHERE JHXA005 = '{0}' "
			__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(__FlowId))
			if __get[0] != 'None':
				__FlowId = 'JH' + __Time +  '0001'
				return self.__GetFlowID(__FlowId)
			else:
				return __FlowId
	
	def __GetTypeID(self, __TypeID):
		__sqlstr = (r"SELECT RTRIM(MQ001) 单别, RTRIM(MQ002) 单据名称, RTRIM(MQ019) 核对采购 "
		            r"FROM COMFORT..CMSMQ "
		            r"WHERE 1=1 "
		            r"AND MQ003 = '34' "
		            r"AND MQ001 LIKE '%{0}%' "
		            r"ORDER BY MQ001")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(__TypeID))
		if __get[0] != 'None':
			return __get
		else:
			return None
		
	def __GetPositionID(self, __PositionID):
		__sqlstr = (r"SELECT RTRIM(MC001) 仓库编号, RTRIM(MC002) 仓库名称, RTRIM(MC003) 工厂编号 "
		            r"FROM COMFORT..CMSMC "
		            r"WHERE MC001 LIKE '%{0}%' "
		            r"ORDER BY LEN(MC001) DESC, MC001")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(__PositionID))
		if __get[0] != 'None':
			return __get
		else:
			return None
	
	def __GetSupplierID(self, __SupplierID):
		__sqlstr = (r"SELECT RTRIM(MA001) 供应商编号, RTRIM(MA002) 简称 FROM COMFORT..PURMA "
		            r"WHERE MA001 LIKE '%{0}%' "
		            r"ORDER BY MA001")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(__SupplierID))
		if __get[0] != 'None':
			return __get
		else:
			return None
		
	def __GetMaterielID(self, __BarCode, __Number='0', __PositionID='0', __DeliveryID='0'):
		__sqlstr = (r"SELECT RTRIM(MB001) 品号, RTRIM(MB002) 品名, RTRIM(MB003) 规格, "
		            r"'{1}' 数量, '{2}' 仓库, RTRIM(MG006) 批号, RTRIM(MG006) 供应商, '{3}' 送货单, RTRIM(MG001) 条码 "
		            r"FROM INVMB "
		            r"INNER JOIN BMSMG ON MG002 = MB001 AND (MB032 = MG006 OR MB200 = MG006) "
		            r"WHERE 1=1 "
		            r"AND MG001 = '{0}'")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(__BarCode, __Number,
		                                                                              __PositionID, __DeliveryID))
		if __get[0] != 'None':
			return __get
		else:
			return None
	
	def __SetReturnMode(self, __Mode):
		self.__back['Return'] = __Mode
	
	def __SetReturnParameter(self, __Parameter):
		self.__back['Parameter'] = __Parameter
	
	def __SetReturnData(self, __Data):
		self.__back['Data'] = __Data


class PDA_JH_Handle:
	pass
