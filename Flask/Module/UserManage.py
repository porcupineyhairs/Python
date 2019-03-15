from Module import Sql
from Module import DataBase_Dict
from Module import Permission


class UserManege:
	def __init__(self):
		self.__sqlWg = Sql(sqlType='mssql', connDict=DataBase_Dict['WG_DB'])
		self.__sqlErp = Sql(sqlType='mssql', connDict=DataBase_Dict['COMFORT'])
		self.__userPerm = Permission.UserPermission()
		self.__basePerm = Permission.BasePermission()
		self.__get = None
		self.__back = {'LoginStatus': 'N',
		               'LoginUid': None,
		               'LoginRole': None,
		               'LoginDpt': None,
		               'LoginName': None,
		               'LoginPermission': None,
		               'ErrorMsg': None,
		               }

		self.__LoginUid = None
		self.__LoginPwd = None
		self.__LoginStatus = 'N'
		self.__LoginRole = None
		self.__LoginDpt = None
		self.__LoginName = None

		self.__WgPwd = None
		self.__WgType = None
		self.__WgFlag = None
		self.__WgErpPwd = None

		self.__ErpPwd = None
		self.__ErpValid = None

		self.__getWg = None
		self.__getErp = None

	def UserLogin(self, __get):
		self.__init__()

		self.__get = __get
		self.__LoginUid = self.__get['LoginUid']
		self.__LoginPwd = self.__get['LoginPwd']

		self.__Login_Work()

		return self.__back

	def __Login_Work(self):
		self.__Get_ERPInf()
		self.__Get_WGInf()
		self.__Set_Inf()

		if self.__Judge_ERPExist():
			if self.__ErpValid == 'Y':
				if self.__Judge_WGExist():
					if self.__WgFlag == 'Y':
						if self.__Judge_WG_PwdSame():
							self.__LoginStatus = 'Y'
							self.__Set_UserInf()
						else:
							if not self.__Judge_ERP_PwdSame():
								self.__LoginStatus = 'Y'
								self.__Set_UserInf()
								self.__Update_WGInf()
					else:
						self.__LoginStatus = 'Y'
						self.__Set_UserInf()
						self.__Update_WGInf()
				else:
					self.__LoginStatus = 'Y'
					self.__Set_UserInf()
					self.__Insert_WGInf()
			else:
				self.__back['Login_Status'] = 'y'

	def __Get_WGInf(self):
		__sqlstr = (r"SELECT U_ID, U_NAME, U_PWD, ERP_PWD, DPT, ROLE, FLAG, TYPE FROM WG_DB.dbo.WG_USER "
		            r"WHERE U_ID = '" + self.__LoginUid + "'")
		self.__getWg = self.__sqlWg.SqlWork(sqlStr=__sqlstr)

	def __Get_ERPInf(self):
		__sqlstr = (r"SELECT RTRIM(MA001), RTRIM(MA002), RTRIM(ME002), RTRIM(MA003), RTRIM(MA005) "
		            r"FROM DSCSYS.dbo.DSCMA AS DSCMA "
		            r"LEFT JOIN CMSMV ON MV001 = MA001 "
		            r"LEFT JOIN CMSME ON ME001 = MV004 "
		            r"WHERE MA001 = '" + self.__LoginUid + r"'")
		self.__getErp = self.__sqlErp.SqlWork(sqlStr=__sqlstr)
		print(self.__getErp)

	def __Judge_ERP_PwdSame(self):
		if self.__ErpPwd == self.__WgErpPwd:
			return True
		else:
			return False

	def __Judge_WG_PwdSame(self):
		if self.__WgPwd == self.__LoginPwd:
			return True
		else:
			return False

	def __Judge_WGExist(self):
		if self.__getWg is not None:
			return True
		else:
			return False

	def __Judge_ERPExist(self):
		if self.__getErp is not None:
			return True
		else:
			return False

	def __Insert_WGInf(self):
		self.__ErpPwd = self.__ErpPwd.replace("'", "''")
		__sqlstr = (r"INSERT INTO WG_DB.dbo.WG_USER (U_ID, U_NAME, U_PWD, ERP_PWD, DPT, ROLE, FLAG, TYPE) "
		            r"VALUES("
		            r"'" + self.__LoginUid + "', "
                    r"'" + self.__LoginName + "', "
                    r"'" + self.__WgPwd + "', "
                    r"'" + self.__ErpPwd + "', "
                    r"'" + self.__LoginDpt + "', "
                    r"'', 'Y', 'ERP'"
		            r")")
		self.__sqlWg.SqlWork(sqlStr=__sqlstr)

	def __Update_WGInf(self):
		self.__ErpPwd = self.__ErpPwd.replace("'", "''")
		__sqlstr = (r"UPDATE WG_DB.dbo.WG_USER SET "
		            r"U_NAME = '" + self.__LoginName + "', "
                    r"U_PWD = '" + self.__LoginPwd + "', "
                    r"ERP_PWD = '" + self.__ErpPwd + "', "
                    r"DPT = '" + self.__LoginDpt + "', "
                    r"FLAG = 'Y' "
		            r"WHERE U_ID = '" + self.__LoginUid + "'")
		print(type(self.__LoginDpt))
		self.__sqlWg.SqlWork(sqlStr=__sqlstr)

	def __Set_Inf(self):
		if self.__Judge_ERPExist():
			self.__LoginUid = str(self.__getErp[0][0])
			self.__LoginName = self.__getErp[0][1]
			self.__LoginDpt = self.__getErp[0][2]
			self.__ErpPwd = self.__getErp[0][3]
			self.__ErpValid = self.__getErp[0][4]

		if self.__Judge_WGExist():
			self.__WgPwd = self.__getWg[0][2]
			self.__WgErpPwd = self.__getWg[0][3]
			self.__LoginRole = self.__getWg[0][5]
			self.__WgFlag = self.__getWg[0][6]
			self.__WgType = self.__getWg[0][7]
		else:
			self.__WgPwd = self.__LoginPwd

	def __Set_UserInf(self):
		self.__back['LoginStatus'] = self.__LoginStatus
		self.__back['LoginUid'] = self.__LoginUid
		self.__back['LoginRole'] = self.__LoginRole
		self.__back['LoginDpt'] = self.__LoginDpt
		self.__back['LoginName'] = self.__LoginName
