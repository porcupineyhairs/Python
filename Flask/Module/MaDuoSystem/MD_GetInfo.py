from Module.SelfModule import MsSql
from Module.ModuleDictionary import DataBase_Dict


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
		self.__GetBoxList()

	def __GetToday(self):
		__sqlstr = "SELECT CONVERT(VARCHAR(30), GETDATE(), 112) "
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ERP, SqlStr=__sqlstr)
		if __get[0] != 'None':
			self.__Today = str(__get[0][0])
			self.__LastDay = str(int(self.__Today) + 3)

	def __GetOrderList(self):
		__sqlstr = (r"SELECT SC001 FROM SCHEDULE WHERE SC038 = 'N' /*AND SC003 BETWEEN '{0}' AND '{1}' */ORDER BY KEY_ID")
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr.format(self.__Today, self.__LastDay))
		print(__get)
		if __get[0] != 'None':
			for __get_Item in __get:
				self.__GetOrderInfo(__get_Item[0])

	def __GetOrderInfo(self, __Item):
		__sqlstr = (r"SELECT "
		            r"(RTRIM(COPTD.TD001) + '-' + RTRIM(COPTD.TD002) + '-' + RTRIM(COPTD.TD003)) 订单号, "
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
		            r"(CASE WHEN COPTC.UDF09 = '是' THEN 'Y' ELSE 'N' END) 急单, "
		            r"(CASE WHEN COPTD.TD020 LIKE '%菜鸟条码%' THEN 'Y' ELSE 'N' END) 菜鸟条码 "
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
		__sqlstr = (r"UPDATE SCHEDULE SET SC038 = 'y', "
		            r"SC013 = '{1}', "
		            r"SC010 = '{2}', "
		            r"SC011 = '{3}', "
		            r"SC012 = '{4}', "
		            r"SC025 = '{5}', "
		            r"SC015 = '{6}', "
		            r"SC016 = '{7}', "
		            r"SC017 = '{8}', "
		            r"SC024 = '{9}', "
		            r"SC023 = '{10}', "
		            r"SC026 = '{11}', "
		            r"SC037 = '{12}' "
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
				__BoxSize = self.__GetBoxInfo(__get_Item)
				if __BoxSize is not None:
					self.__UpdBoxInfo(__get_Item, __BoxSize)
				else:
					self.__UpdBoxInfo(__get_Item, '0*0*0')

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
			return __BoxSize
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
			__Vol.append(__Size)
		return str(__Item[__Vol.index(max(__Vol))])

	def __UpdBoxInfo(self, __Item, __Size):
		__sqlstr = r"UPDATE SCHEDULE SET SC038 = 'Y', SC036 = '{1}' WHERE SC001 = '{0}'"
		self.__mssql.Sqlwork(DataBase=self.__Conn_ROBOT, SqlStr=__sqlstr.format(__Item, __Size))
