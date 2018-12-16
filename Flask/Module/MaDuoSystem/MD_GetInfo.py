from Module.SelfModule import MsSql
from Module.ModuleDictionary import DataBase_Dict
from Module import Num2Char


class GetInfo:
	def __init__(self):
		self.__mssql = MsSql()
		self.__Conn_ROBOT = DataBase_Dict['ROBOT_TEST']
		self.__Conn_ERP = DataBase_Dict['COMFORT']
		self.__Today = None
		self.__LastDay = None

	def MainWork(self):
		self.__init__()
		self.__GetToday()
		self.__GetOrderList()
		self.__GetOrderTypeIn()
		self.__GetOrderTypeOut()
		self.__GetBoxList()
		print('Done')

	def __GetToday(self):
		__sqlstr = "SELECT CONVERT(VARCHAR(30), GETDATE(), 112) "
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr)
		if __get[0] != 'None':
			self.__Today = str(__get[0][0])
			self.__LastDay = str(int(self.__Today) + 3)

	def __GetOrderList(self):
		__sqlstr = (r"SELECT SC001 FROM SCHEDULE WHERE SC038 = 'N' /*AND SC003 BETWEEN '{0}' AND '{1}'*/ ORDER BY KEY_ID")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr.format(self.__Today, self.__LastDay))
		if __get[0] != 'None':
			for __get_Item in __get:
				self.__GetOrderInfo(__get_Item[0])

	def __GetOrderInfo(self, __Item):
		__sqlstr = (r"SELECT "
		            r"(RTRIM(COPTD.TD001) + '-' + RTRIM(COPTD.TD002) + '-' + RTRIM(COPTD.TD003)) 订单号, "
		            r"(CASE WHEN TC004='0118' THEN '内销' ELSE '外销' END) 订单类型, "
		            r"CONVERT(INT, COPTD.TD008) 订单数量, "
		            r"RTRIM(COPTD.TD005) 品名, "
		            r"RTRIM(COPTD.UDF08) 保友品名, "
		            r"RTRIM(COPTD.TD006) 规格, "
		            r"RTRIM(COPTD.UDF10) 电商代码, "
		            r"RTRIM(COPTD.TD053) 配置方案, "
		            r"RTRIM(COPTQ.TQ003) 配置描述, "
		            r"RTRIM(COPTD.TD020) 描述备注, "
		            r"RTRIM(COPTD.UDF05) 客户编码, "
		            r"(CASE WHEN TC004 = '0118' THEN RTRIM(INVMB.UDF04) ELSE RTRIM(INVMB.UDF05) END) 生产车间, "
		            r"(CASE WHEN COPTC.UDF09 = '是' THEN 'Y' ELSE 'N' END) 急单 "
		            r"FROM COPTD "
		            r"LEFT JOIN COPTC ON COPTD.TD001 = COPTC.TC001 and COPTD.TD002 = COPTC.TC002 "
		            r"LEFT JOIN COPTQ ON COPTD.TD053 = COPTQ.TQ002 and COPTD.TD004 = COPTQ.TQ001 "
		            r"LEFT JOIN INVMB ON COPTD.TD004 = INVMB.MB001 "
		            r"WHERE 1 = 1 AND COPTC.TC027 = 'Y' "
		            r"AND COPTD.TD004 NOT LIKE '6%' "
		            r"AND COPTD.TD004 NOT LIKE '7%' "
		            r"AND RTRIM(COPTD.TD001) + '-' + RTRIM(COPTD.TD002) + '-' + RTRIM(COPTD.TD003) "
		            r"= '{0}' ")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(__Item))
		print(__get)
		if __get[0] != 'None':
			for __get_Item in __get:
				self.__UpdOrderInfo(__get_Item)

	def __UpdOrderInfo(self, __Item):
		__sqlstr = (r"UPDATE SCHEDULE SET SC038 = 'n', "
		            r"SC002 = '{1}', "
		            r"SC013 = '{2}', "
		            r"SC010 = '{3}', "
		            r"SC011 = '{4}', "
		            r"SC012 = '{5}', "
		            r"SC025 = '{6}', "
		            r"SC015 = '{7}', "
		            r"SC016 = '{8}', "
		            r"SC017 = '{9}', "
		            r"SC024 = '{10}', "
		            r"SC023 = '{11}', "
		            r"SC026 = '{12}' "
		            r"WHERE SC001 = '{0}'")
		print(__sqlstr.format(__Item[0], __Item[1], __Item[2],
		                      __Item[3], __Item[4], __Item[5], __Item[6], __Item[7], __Item[8], __Item[9], __Item[10],
		                      __Item[11], __Item[12]))
		self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr.format(__Item[0], __Item[1], __Item[2],
		                     __Item[3], __Item[4], __Item[5], __Item[6], __Item[7], __Item[8], __Item[9], __Item[10],
		                     __Item[11], __Item[12]))

	def __GetBoxList(self):
		__sqlstr = r"SELECT SC001 FROM SCHEDULE WHERE 1=1 AND SC038 = 'y' ORDER BY KEY_ID "
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr)
		if __get[0] != 'None':
			for __get_Item in __get:
				__get_Item = __get_Item[0]
				__BoxCode = self.__GetBoxInfo(__get_Item)
				if __BoxCode is not None:
					self.__UpdBoxInfo(__get_Item, __BoxCode)
				else:
					self.__UpdBoxInfo(__get_Item, 'NULL')

	def __GetBoxInfo(self, __Item):
		__BoxSize = '0*0*0'
		__sqlstr = (r"SELECT TB013 FROM MOCTB "
		            r"INNER JOIN MOCTA ON TA001 = TB001 AND TA002 = TB002 "
		            r"WHERE TB006 LIKE '%0801%' "
		            r"AND TB012 LIKE '%纸箱%' "
		            r"AND RTRIM(TA076) + '-' + RTRIM(TA077) + '-' + RTRIM(TA078) = '{0}'")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr.format(__Item))
		if __get[0] != 'None':
			__BoxSize = self.__GetBoxSize(__get)
			__Code = self.__GetBoxSizeCode(__BoxSize)
			return __Code
		else:
			return None

	def __GetBoxSizeCode(self, __Size):
		__sqlstr = r"SELECT BoxCode FROM BoxSizeCode WHERE BoxSize = '{0}'"
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr.format(__Size))
		if __get[0] != 'None':
			__Code = __get[0][0]
			return __Code
		else:
			return None

	def __GetBoxSize(self, __Item):  # 数据库出来的字符串处理
		__Size_List = []
		for __Item_Item in __Item:
			for __Str_List in __Item_Item[0].split('/'):
				if __Str_List.count('*') == 2:
					__Size_List.append(__Str_List)
		__BoxSize = self.__GetBoxMaxSize(__Size_List)
		return __BoxSize

	def __GetBoxMaxSize(self, __Item):
		__Vol = []
		for __i in range(len(__Item)):
			__Num = __Item[__i].split('*')
			for __k in range(len(__Num)):
				__Num[__k] = str(__Num[__k]).split('(')[0]
				__Num[__k] = str(__Num[__k]).split('（')[0]

			__Size = int(__Num[0]) * int(__Num[1]) * int(__Num[2])
			__Item[__i] = str(__Num[0]) + '*' + str(__Num[1]) + '*' + str(__Num[2])
			__Vol.append(__Size)
		return str(__Item[__Vol.index(max(__Vol))])

	def __UpdBoxInfo(self, __Item, __Code):
		__sqlstr = r"UPDATE SCHEDULE SET SC038 = 'Y', SC036 = '{1}' WHERE SC001 = '{0}'"
		print(__sqlstr.format(__Item, __Code))
		self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr.format(__Item, __Code))
		
	def __GetOrderTypeIn(self):
		__listStr = self.__GetTypeStr()
		__sqlstr = (r"SELECT SC001, {0} FROM SCHEDULE "
		            r"WHERE SC002 = '内销' AND SC038 = 'n' ORDER BY KEY_ID").format(__listStr)
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr)
		if __get[0] != 'None':
			for __Item_List in __get:
				self.__UptOrderType(__Item_List[0], __Item_List[1])
		else:
			pass
		
	def __GetTypeStr(self):
		__get = self.__GetTypeList()
		if __get is not None:
			__returnStr = r" (CASE {0} ELSE 'A' END ) "
			__str = r""
			__listStr = r" WHEN SC017 LIKE '%{0}%' THEN '{1}' "
			for __Item in __get:
				__str += __listStr.format(__Item[0], __Item[1])
			return __returnStr.format(__str)
		else:
			return None
	
	def __GetTypeList(self):
		__sqlstr = (r"SELECT PO_Type, TypeCode FROM SplitTypeCode "
		            r"WHERE Valid = 'Y' AND PO_Class = '内销' AND PO_Type != '内销' "
		            r"ORDER BY K_ID")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr)
		if __get[0] != 'None':
			return __get
		else:
			print('获取内销订单类别码失败')
			return None
	
	def __GetOrderTypeOut(self):
		__sqlstr = (r"SELECT SC001, SUBSTRING(SC001, 1, 4) FROM SCHEDULE "
		            r"WHERE SC002 = '外销' AND SC038 = 'n'  ORDER BY KEY_ID")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr)
		if __get[0] != 'None':
			for __Item_List in __get:
				__Code = self.__GetExistOrderType('外销', __Item_List[1])
				self.__UptOrderType(__Item_List[0], __Code)
		else:
			pass

	def __GetExistOrderType(self, __Class, __Type):
		__sqlstr = (r"SELECT TypeCode FROM SplitTypeCode "
		            r"WHERE PO_Class = '{0}' AND PO_Type = '{1}' ")
		print(__sqlstr.format(__Class, __Type))
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr.format(__Class, __Type))
		if __get[0] != 'None':
			return __get[0][0]
		else:
			__Max = self.__GetMaxOrderType()
			if __Max is not None:
				__Code = Num2Char.changeNumToChar(int(__Max))
				self.__AddOrderType(__Class, __Type, __Code)
				return __Code
			else:
				print('获取订单类型码失败，获取不到最大K_ID(SplitTypeCode)')
				return None
	
	def __GetMaxOrderType(self):
		__sqlstr = (r"SELECT MAX(K_ID) + 1 "
		            r"FROM SplitTypeCode")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr)
		if __get[0] != 'None':
			return __get[0][0]
		else:
			return None
			
	def __AddOrderType(self, __Class, __Type, __Code):
		__sqlstr = (r"INSERT INTO  SplitTypeCode(PO_Class, PO_Type, TypeCode, Valid) "
		            r"VALUES ('{0}', '{1}', '{2}', 'Y')")
		print(__sqlstr.format(__Class, __Type, __Code))
		self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr.format(__Class, __Type, __Code))

	def __UptOrderType(self, __Item, __Code):
		__sqlstr = r"UPDATE SCHEDULE SET SC038 = 'y', SC037 = '{1}' WHERE SC001 = '{0}' "
		print(__sqlstr.format(__Item, __Code))
		self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr.format(__Item, __Code))
