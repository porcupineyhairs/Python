from Module.SelfModule import MsSql
from Module.ModuleDictionary import DataBase_Dict
from Module.GetDbSvrTime import GetSvrTime
import json


class PDA_JH_GetInfo:
	def __init__(self):
		self.__Conn_ERP = DataBase_Dict['COMFORT']
		self.__Conn_WG = DataBase_Dict['WG_DB']
		self.__mssql = MsSql()
		self.__getSvrTime = GetSvrTime()
		self.__back = {'Return': 'Error',
		               'Parameter': None,
		               'Data': None}
		self.__Mode = None
		self.__Parameter = None
		self.__Data = None
	
	def MainWork(self, __json=None):
		self.__init__()
		if __json is None:
			print('test')
		else:
			try:
				self.__Mode = __json['Mode']
				self.__Parameter = __json['Parameter']
				self.__Data = __json['Data']
				
				if self.__Mode == 'GetConfig':
					self.__ModeGetConfig()
				elif self.__Mode == 'Select':
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
			except Exception as e:
				print('Json Input Error\n', 'Input Json: ' + str(__json))
				self.__back.update({'Error': str(e)})
			finally:
				return self.__back
		
	def __ModeGetConfig(self):
		__sqlstr = (r"SELECT RTRIM(Type) FROM WG_DB..WG_CONFIG "
		            r"WHERE ConfigName = 'JH_LYXA_Scan' AND Vaild = 'Y' ")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_WG, SqlStr=__sqlstr)
		if __get[0] != 'None':
			self.__SetReturnParameter(__get[0][0])
			self.__SetReturnData(None)
			return self.__back
		else:
			self.__SetReturnParameter('Error')
			self.__SetReturnData(None)
			return self.__back
	
	def __ModeSelect(self):
		if self.__Parameter == 'FlowID':
			self.__SetReturnData(self.__GetFlowID())
		elif self.__Parameter == 'MaterielID':
			pass
		elif self.__Parameter == 'SupplierID':
			pass
		elif self.__Parameter == 'TypeID':
			__get = self.__GetTypeID(self.__Data)
			__data = {'单别': None, '单据名称': None, '核对采购': None}
			__data0 = []
			for __getList in __get:
				__data.update({'单别': __getList[0]})
				__data.update({'单据名称': __getList[1]})
				__data.update({'核对采购': __getList[2]})
				__data0.append(__data)
			print(__data0)
			
			self.__SetReturnData(json.dumps(__data))
			
		elif self.__Parameter == 'PositionID':
			pass
		else:
			print('Parameter Out Of Index :', self.__Parameter)
			self.__Parameter = 'Error'
	
	def __ModeInsert(self):
		pass
	
	def __ModeComplete(self):
		__FlowId = self.__Parameter
		__jh_handel = PDA_JH_Handle()
		__get = __jh_handel.MainWork(__FlowId)
		self.__SetReturnData(__get)
	
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
				__FlowId = 'JH' + __Time + '0001'
				return self.__GetFlowID(__FlowId)
			else:
				return __FlowId
	
	def __GetTypeID(self, __TypeID):
		__sqlstr = (r"SELECT RTRIM(MQ001) 单别, RTRIM(MQ002) 单据名称, RTRIM(MQ019) 核对采购 "
		            r"FROM CMSMQ "
		            r"WHERE 1=1 "
		            r"AND MQ003 = '34' "
		            r"AND MQ001 LIKE '%{0}%' "
		            r"ORDER BY MQ001 ")
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
	def __init__(self):
		self.__Conn_ERP = DataBase_Dict['COMFORT']
		self.__mssql = MsSql()
		self.__getSvrTime = GetSvrTime()
		self.__FlowId = None
		self.__Company = None
		self.__Uid = None
		self.__Ugroup = None
		self.__Time = None
		
		self.__Index = 0
		
		self.__Total = None
		
		self.__TG001 = None  # 单别
		self.__TG002 = None  # 单号
		self.__TG003 = None  # 进货日期
		self.__TG004 = '01'  # 工厂编号
		self.__TG005 = None  # 供应商编号
		self.__TG006 = None  # 送货单号
		self.__TG007 = None  # 币种
		self.__TG008 = None  # 汇率
		self.__TG009 = None  # 发票种类
		self.__TG010 = None  # 税种
		self.__TG013 = 'N'  # 审核码
		self.__TG014 = None  # 单据日期=进货日期
		self.__TG015 = 'N'  # 更新码
		self.__TG021 = None  # 供应商全称
		self.__TG030 = None  # 增值税率
		self.__TG033 = None  # 付款条件编号
		
		self.__TH003 = None  # 序号
		self.__TH004 = None  # 品号
		self.__TH005 = None  # 品名
		self.__TH006 = None  # 规格
		self.__TH007 = None  # 进货数量
		self.__TH008 = None  # 单位
		self.__TH009 = None  # 仓库
		self.__TH010 = None  # 批号
		self.__TH011 = None  # 采购单别
		self.__TH012 = None  # 采购单号
		self.__TH013 = None  # 采购序号
		self.__TH014 = None  # 验收日期
		self.__TH015 = None  # 验收数量
		self.__TH016 = None  # 计价数量
		self.__TH018 = None  # 原币单位今后价
		self.__TH019 = None  # 原币进货金额
		self.__TH027 = 'N'  # 超期码
		self.__TH033 = None  # 备注 订单信息
		self.__TH034 = None  # 验收库存数量
		self.__TH035 = None  # 小单位
		self.__TH042 = None  # 项目编号
		self.__TH064 = None  # 计价单温
		self.__TH065 = None  # 库存单位
		self.__THC02 = None  # 类型
		
	def MainWork(self, FlowId):
		self.__init__()
		self.__Time = self.__getSvrTime.GetTime({'Mode': 'Long'})['Time'] + '000'
		self.__FlowId = FlowId
		self.__GetHeadTG001()
		self.__GetHeadTG002()
		self.__SetHeadInfo()
		self.__GetMaterielInfo()
		self.__SetDetailMoney()
		self.__SetSumMoney()
		self.__UpdJHXAInfo()
		
		return self.__TG001 + '-' + self.__TG002
		
	def __GetHeadTG001(self):
		print('GetHeadInfo')
		__sqlstr = (r"SELECT DISTINCT RTRIM(JHXA.COMPANY) 公司别, RTRIM(JHXA.CREATOR) 创建人, RTRIM(JHXA.USR_GROUP) 用户组, "
		            r"RTRIM(JHXA001) 进货单别, RTRIM(JHXA004) 进货日期, RTRIM(JHXA002) 供应商编号, RTRIM(JHXA013) 送货单号, "
		            r"RTRIM(MA021) 交易币种, MG2.MG003 汇率, "
		            r"RTRIM(MA030) 发票种类, "
		            r"(CASE WHEN NOT (TC018 = '' OR TC018 IS NULL) THEN TC018 "
		            r"ELSE (CASE WHEN MA044 ='' OR MA044 IS NULL THEN '1' ELSE MA044 END ) END) AS TC018C, "
		            r"RTRIM(MA003) 供应商全称, "
		            r"(CASE WHEN TC026 IS NULL THEN MA064 ELSE TC026 END) AS TC026C, "
		            r"(CASE WHEN TC027 = '' OR TC027 IS NULL THEN MA055 ELSE TC027 END) AS TC027C "
		            r"FROM COMFORT.dbo.JH_LYXA AS JHXA "
		            r"LEFT JOIN COMFORT.dbo.PURTC AS PURTC ON 1=2 "
		            r"LEFT JOIN COMFORT.dbo.INVMB AS INVMB ON MB001=JHXA007 "
		            r"LEFT JOIN COMFORT.dbo.PURMA AS PURMA ON MA001=JHXA002 "
		            r"LEFT JOIN (SELECT CMSMG.MG003, CMSMG.MG001 FROM COMFORT.dbo.CMSMG "
		            r"INNER JOIN (SELECT MAX(MG002) MAXMG02, MG001 MAXMG01 FROM CMSMG GROUP BY MG001) AS MG "
		            r"ON MG.MAXMG01 = CMSMG.MG001 AND MG.MAXMG02 = CMSMG.MG002) AS MG2 ON MG2.MG001 = MA021 "
		            r"WHERE JHXA005 IN ('{0}') AND JHXA011 = 'N' ")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(self.__FlowId))
		if __get[0] != 'None':
			__get = __get[0]
			self.__Company = __get[0]
			self.__Uid = __get[1]
			self.__Ugroup = __get[2]
			self.__TG001 = __get[3]
			self.__TG003 = __get[4]
			self.__TG005 = __get[5]
			self.__TG006 = __get[6]
			self.__TG007 = __get[7]
			self.__TG008 = __get[8]
			self.__TG009 = __get[9]
			self.__TG010 = __get[10]
			self.__TG014 = self.__TG003
			self.__TG021 = __get[11]
			self.__TG030 = __get[12]
			self.__TG033 = __get[13]
	
	def __GetHeadTG002(self):
		__sqlstr = (r"SELECT (CASE WHEN A1 IS NULL THEN A2 + '0001' ELSE A1 END ) B FROM "
		            r"(SELECT MAX(TG002) + 1 A1, SUBSTRING(CONVERT(VARCHAR(10), GETDATE(), 112), 3, 4) A2 "
		            r"FROM PURTG "
		            r"WHERE TG001 = '{0}' AND SUBSTRING(TG002, 1, 4) = "
		            r"SUBSTRING(CONVERT(VARCHAR(10), GETDATE(), 112), 3, 4)) A")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(self.__TG001))
		if __get[0] != 'None':
			self.__TG002 = str(__get[0][0])
			print(self.__TG001 + '-' + self.__TG002)
			
	def __GetMaterielInfo(self):
		print('GetMaterielInfo')
		__sqlstr = (r"SELECT RTRIM(MB001), RTRIM(MB002), RTRIM(MB003), RTRIM(MB004), "
		            r"RTRIM(JHXA003), RTRIM(JHXA009) FROM INVMB "
		            r"INNER JOIN JH_LYXA ON JHXA007 = MB001 WHERE 1=1 AND JHXA005 = '{0}' ORDER BY ID")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(self.__FlowId))
		if __get[0] != 'None':
			for __Item in __get:
				self.__TH004 = __Item[0]
				self.__TH005 = __Item[1]
				self.__TH006 = __Item[2]
				self.__TH008 = __Item[3]
				self.__TH009 = __Item[4]
				self.__Total = float(__Item[5])
				
				self.__TH010 = self.__TG005
				self.__TH014 = self.__TG003
				
				self.__GetDetailInfo()
			
	def __GetDetailInfo(self):
		print('GetDetailInfo')
		__sqlstr = (r"SELECT DISTINCT TOP 200 TD008 - TD015 - ( SELECT isnull( SUM ( TH007 ), 0 ) "
		            r"FROM COMFORT.dbo.PURTH PURTH WHERE TH011 = TD001 AND TH012 = TD002 AND TH013 = TD003 "
		            r"AND TH030 = 'N' ) AS WJL, "
		            r"TD001, RTRIM(TD002), TD003, TD010, TD014, RTRIM(TD020), RTRIM(TD022), RTRIM(TDC03), TD012 "
		            r"FROM COMFORT.dbo.PURTD AS PURTD "
		            r"LEFT JOIN COMFORT.dbo.PURTC AS PURTC ON TC001 = TD001 AND TC002 = TD002 "
		            r"LEFT JOIN (SELECT XB005,XB006,XB007,MIN(XB003) XB003,XA001 FROM COMFORT.dbo.MPSXB MPSXB "
		            r"INNER JOIN COMFORT.dbo.MPSXA MPSXA ON XB001 = XA001 "
		            r"WHERE XA006 = 'Y' AND XA007 = 'Y' "
		            r"GROUP BY XB005,XB006,XB007,XA001) AS MPSXB ON CHARINDEX( '/' + RTRIM( XB006 ) + '/', '/' + "
		            r"RTRIM( TD014 ) + '/' ) > 0 "
		            r"WHERE TC004 = '{0}' AND TD004 = '{1}' "
		            r"AND (TD008 - TD015 - ( SELECT isnull( SUM ( TH007 ), 0 ) FROM COMFORT.dbo.PURTH PURTH "
		            r"WHERE TH011 = TD001 AND TH012 = TD002 AND TH013 = TD003 AND TH030 = 'N' )) > 0 "
		            r"AND TD016 = 'N' AND TC014 = 'Y' AND TC001 <> '3305' AND TC001 <> '3306' "
		            r"ORDER BY TD012, TD001, RTRIM(TD002), TD003 ")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(self.__TG005, self.__TH004))
		if __get[0] != 'None':
			self.__GetNumber(__get)
			
	def __GetNumber(self, __get):
		print('GetNumber')
		__Item = __get[0]
		self.__TH011 = __Item[1]
		self.__TH012 = __Item[2]
		self.__TH013 = __Item[3]
		self.__TH018 = round(float(__Item[4]), 6)
		self.__TH033 = __Item[5]
		self.__TH035 = __Item[6]
		self.__TH042 = __Item[7]
		self.__THC02 = __Item[8]
			
		if float(__Item[0]) >= self.__Total:
			self.__TH007 = str(round(float(self.__Total), 6))
			self.__SetDetailInfo()
		else:
			self.__TH007 = round(float(__Item[0]), 6)
			self.__Total -= float(__Item[0])
			self.__SetDetailInfo()
			del __get[0]
			self.__GetNumber(__get)
	
	def __SetHeadInfo(self):
		print('SetHeadInfo')
		__sqlstr = (r"INSERT INTO PURTG (COMPANY, CREATOR, USR_GROUP, CREATE_DATE, FLAG, TG001, TG002, TG003, TG004, TG005, "
		            r"TG006, TG007, TG008, TG009, TG010, TG013, TG014, TG015, TG021, TG030, TG033, TG016, TG043, TG052) "
		            r"VALUES('{0}', '{1}', '{2}', '{3}', '1', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', "
		            r"'{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '', '', '' )")
		self.__SqlWork(__sqlstr.format(self.__Company, self.__Uid, self.__Ugroup, self.__Time, self.__TG001, self.__TG002,
		                               self.__TG003, self.__TG004, self.__TG005, self.__TG006, self.__TG007,
		                               self.__TG008, self.__TG009, self.__TG010, self.__TG013, self.__TG014,
		                               self.__TG015, self.__TG021, self.__TG030, self.__TG033))
		
	def __SetDetailInfo(self):
		print('DetDetailInfo')
		self.__TH015 = self.__TH007
		self.__TH016 = self.__TH007
		self.__TH034 = self.__TH007
		self.__TH064 = self.__TH008
		self.__TH065 = self.__TH008
		self.__TH019 = round(float(self.__TH007) * float(self.__TH018), 6)
		self.__Index += 1
		self.__TH003 = str(self.__Index).zfill(4)
		
		__sqlstr = (r"INSERT INTO PURTH(COMPANY,CREATOR,USR_GROUP,CREATE_DATE,FLAG,"
		            r"TH001,TH002,TH003,TH004,TH005,TH006,TH007,TH008,TH009,TH010,"
		            r"TH011,TH012,TH013,TH014,TH015,TH016,TH018,TH019,TH026,TH027,"
		            r"TH029,TH030,TH031,TH032,TH033,TH034,TH035,TH042,TH043,TH044,"
		            r"TH060,TH064,TH065,TH071,TH072,THC02)"
		            r"VALUES('{0}','{1}','{2}','{3}',1,'{4}','{5}','{6}',"
		            r"'{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}',"
		            r"'{18}','{19}','{20}','{21}','N','{22}','N','N','N','N','{23}',"
		            r"'{24}','{25}','{26}','N','N','0','{27}','{28}','1','##########','{29}')")
		self.__SqlWork(__sqlstr.format(self.__Company, self.__Uid, self.__Ugroup, self.__Time, self.__TG001, self.__TG002,
		                               self.__TH003, self.__TH004, self.__TH005, self.__TH006, self.__TH007,
		                               self.__TH008, self.__TH009, self.__TH010, self.__TH011, self.__TH012,
		                               self.__TH013, self.__TH014, self.__TH015, self.__TH016,
		                               self.__TH018, self.__TH019, self.__TH027, self.__TH033, self.__TH034, self.__TH035,
		                               self.__TH042, self.__TH064, self.__TH065, self.__THC02))
		
	def __SetDetailMoney(self):
		print('SetDetailMoney')
		__sqlstr = (r"UPDATE COMFORT.dbo.PURTH  SET "
		            r"TH045 = CAST(ROUND(TH019/(1+CONVERT(FLOAT, TG030)),2) AS  NUMERIC(10,2)), "
		            r"TH046 = CAST(ROUND(TH019 - (TH019/(1+CONVERT(FLOAT, TG030))),2) AS  NUMERIC(10,2)), "
		            r"TH047 = CAST(ROUND((TH019 * CONVERT(FLOAT, TG008)/(1+CONVERT(FLOAT, TG030))),2) "
		            r"AS  NUMERIC(10,2)), "
		            r"TH048 = CAST(ROUND((TH019 * CONVERT(FLOAT, TG008)) - "
		            r"(TH019 * CONVERT(FLOAT, TG008)/(1+CONVERT(FLOAT, TG030))),2) AS  NUMERIC(10,2)) "
		            r"FROM PURTH INNER JOIN COMFORT.dbo.PURTG AS PURTG ON TG001 = TH001 AND TG002 = TH002 "
		            r"WHERE TG001= '{0}' AND TG002= '{1}' ")
		self.__SqlWork(__sqlstr.format(self.__TG001, self.__TG002))
	
	def __SetSumMoney(self):
		print('SetSumMoney')
		__sqlstr = (r"UPDATE A SET TG017=SUMTH019,TG019=SUMTH046,TG026=SUMTH015,TG028=SUMTH045,TG031=SUMTH047,"
		            r"TG032=SUMTH048,TG040=SUMTH050,TG041=SUMTH052,TG053=SUMTH007,TG054=SUMTH049 "
		            r"FROM COMFORT.dbo.PURTG A "
		            r"INNER JOIN (SELECT TH001,TH002,SUMTH019=SUM(TH019),SUMTH046=SUM(TH046), "
		            r"SUMTH007=SUM(CASE WHEN MA024='2' THEN FLOOR(TH007) ELSE TH007 END), "
		            r"SUMTH015=SUM(CASE WHEN MA024='2' THEN FLOOR(TH015) ELSE TH015 END),SUMTH045=SUM(TH045), "
		            r"SUMTH047=SUM(TH047),SUMTH048=SUM(TH048),SUMTH050=SUM(TH050),SUMTH052=SUM(TH052), "
		            r"SUMTH049=SUM(TH049) "
		            r"FROM COMFORT.dbo.PURTH "
		            r"INNER JOIN COMFORT.dbo.CMSMA ON 1=1 "
		            r"GROUP BY TH001,TH002)  AS B ON A.TG001=B.TH001 AND A.TG002=B.TH002 "
		            r"WHERE TG001= '{0}' AND TG002= '{1}' ")
		self.__SqlWork(__sqlstr.format(self.__TG001, self.__TG002))
		
	def __UpdJHXAInfo(self):
		print('UpdJHXA')
		__Time = self.__getSvrTime.GetTime({'Mode': 'Long'})['Time']
		__sqlstr = (r"UPDATE COMFORT.dbo.JH_LYXA SET COMPANY='{1}', MODIFIER='{2}', MODI_DATE='{3}', "
		            r"FLAG=(convert(int,COMFORT.dbo.JH_LYXA.FLAG))%999+1, JHXA011 = 'Y', "
		            r"UDF01 = '{4}' "
		            r"WHERE  JHXA005 = '{0}' ")
		self.__SqlWork(__sqlstr.format(self.__FlowId, self.__Company, self.__Uid,
		                               str(__Time), self.__TG001 + '-' + self.__TG002))
		
	def __SqlWork(self, __sqlstr):
		self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr)
