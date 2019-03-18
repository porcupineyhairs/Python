from Module import Sql
from Module.Permission import UserPermission, BasePermission
from Module import DataBase_Dict


class UserManege:
	def __init__(self):
		self.__sqlWg = Sql(sqlType='mssql', connDict=DataBase_Dict['WG_DB'])
		self.__sqlErp = Sql(sqlType='mssql', connDict=DataBase_Dict['COMFORT'])
		self.__userPerm = UserPermission()
		self.__basePerm = BasePermission()
		self.__getDict = None
		self.__backDict = {'Mode': str(None),
		                   'Status': None,
		                   'Uid': None,
		                   'Role': None,
		                   'Dpt': None,
		                   'Name': None,
		                   'Permission': None,
		                   'Message': '',
		                   }

		self.__Uid = None
		self.__Pwd = None
		self.__Status = None
		self.__Role = None
		self.__Dpt = None
		self.__Name = None

		self.__WgPwd = None
		self.__WgType = None
		self.__WgFlag = None
		self.__WgErpPwd = None

		self.__ErpPwd = None
		self.__ErpValid = None

		self.__getWg = None
		self.__getErp = None
		
		self.__Permission = None
		
	def __InitParameter(self):
		self.__getDict = None
		self.__backDict = {'Mode': str(None),
		                   'Status': None,
		                   'Uid': None,
		                   'Role': None,
		                   'Dpt': None,
		                   'Name': None,
		                   'Permission': None,
		                   'Message': '',
		                   }
		
		self.__Uid = None
		self.__Pwd = None
		self.__Status = None
		self.__Role = None
		self.__Dpt = None
		self.__Name = None
		
		self.__WgPwd = None
		self.__WgType = None
		self.__WgFlag = None
		self.__WgErpPwd = None
		
		self.__ErpPwd = None
		self.__ErpValid = None
		
		self.__getWg = None
		self.__getErp = None
		
		self.__Permission = None
		
	def MainWork(self, getDict):
		self.__InitParameter()
		self.__getDict = getDict
		
		if self.__getDict['Mode'] in ('UserLogin', 'SetUserPerm', 'SetBasePerm'):
			self.__backDict['Mode'] = self.__getDict['Mode']
			if self.__getDict['Mode'] == 'UserLogin':
				self.__UserLogin()
			elif self.__getDict['Mode'] == 'SetUserPerm':
				self.__SetUserPerm()
			elif self.__getDict['Mode'] == 'SetBasePerm':
				self.__SetBasePerm()
		else:
			self.__backDict['Mode'] = 'Error'
			self.__backDict['Message'] = '传入模式数据错误'
		
		self.__backDict['Permission'].rtrim('|')
		return self.__backDict

	# UserLogin部分
	def __UserLogin(self):
		self.__Uid = self.__getDict['Uid']
		self.__Pwd = self.__getDict['Pwd']

		self.__Get_ERPInf()
		self.__Get_WGInf()
		self.__Set_Inf()

		if self.__Judge_ERPExist():
			if self.__ErpValid == 'Y':
				if self.__Judge_WGExist():
					if self.__WgFlag == 'Y':
						if self.__Judge_WG_PwdSame():
							self.__Status = 'Y'
							self.__Set_UserInf()
						else:
							if not self.__Judge_ERP_PwdSame():
								self.__Status = 'Y'
								self.__Set_UserInf()
								self.__Update_WGInf()
					else:
						self.__Status = 'Y'
						self.__Set_UserInf()
						self.__Update_WGInf()
				else:
					self.__Status = 'Y'
					self.__Set_UserInf()
					self.__Insert_WGInf()
			else:
				self.__backDict['Status'] = 'y'

	def __Get_WGInf(self):
		__sqlstr = (r" SELECT U_ID, U_NAME, U_PWD, ERP_PWD, DPT, ROLE, FLAG, TYPE FROM WG_DB.dbo.WG_USER "
		            r" WHERE U_ID = '" + self.__Uid + "'")
		self.__getWg = self.__sqlWg.SqlWork(sqlStr=__sqlstr)

	def __Get_ERPInf(self):
		__sqlstr = (r" SELECT RTRIM(MA001), RTRIM(MA002), RTRIM(ME002), RTRIM(MA003), RTRIM(MA005) "
		            r" FROM DSCSYS.dbo.DSCMA AS DSCMA "
		            r" LEFT JOIN CMSMV ON MV001 = MA001 "
		            r" LEFT JOIN CMSME ON ME001 = MV004 "
		            r" WHERE MA001 = '" + self.__LoginUid + r"'")
		self.__getErp = self.__sqlErp.SqlWork(sqlStr=__sqlstr)
		print(self.__getErp)

	def __Judge_ERP_PwdSame(self):
		if self.__ErpPwd == self.__WgErpPwd:
			return True
		else:
			return False

	def __Judge_WG_PwdSame(self):
		if self.__WgPwd == self.__Pwd:
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
		__sqlstr = (r" INSERT INTO WG_DB.dbo.WG_USER (U_ID, U_NAME, U_PWD, ERP_PWD, DPT, ROLE, FLAG, TYPE) "
		            r" VALUES("
		            r"'" + self.__Uid + "', "
                    r"'" + self.__Name + "', "
                    r"'" + self.__WgPwd + "', "
                    r"'" + self.__ErpPwd + "', "
                    r"'" + self.__Dpt + "', "
                    r"'', 'Y', 'ERP'"
		            r")")
		self.__sqlWg.SqlWork(sqlStr=__sqlstr)

	def __Update_WGInf(self):
		self.__ErpPwd = self.__ErpPwd.replace("'", "''")
		__sqlstr = (r"UPDATE WG_DB.dbo.WG_USER SET "
		            r"U_NAME = '" + self.__Name + "', "
                    r"U_PWD = '" + self.__Pwd + "', "
                    r"ERP_PWD = '" + self.__ErpPwd + "', "
                    r"DPT = '" + self.__Dpt + "', "
                    r"FLAG = 'Y' "
		            r"WHERE U_ID = '" + self.__Uid + "'")
		self.__sqlWg.SqlWork(sqlStr=__sqlstr)

	def __Set_Inf(self):
		if self.__Judge_ERPExist():
			self.__Uid = str(self.__getErp[0][0])
			self.__Name = self.__getErp[0][1]
			self.__Dpt = self.__getErp[0][2]
			self.__ErpPwd = self.__getErp[0][3]
			self.__ErpValid = self.__getErp[0][4]

		if self.__Judge_WGExist():
			self.__WgPwd = self.__getWg[0][2]
			self.__WgErpPwd = self.__getWg[0][3]
			self.__Role = self.__getWg[0][5]
			self.__WgFlag = self.__getWg[0][6]
			self.__WgType = self.__getWg[0][7]
		else:
			self.__WgPwd = self.__Pwd

	def __Set_UserInf(self):
		self.__backDict['Status'] = self.__Status
		self.__backDict['Uid'] = self.__Uid
		self.__backDict['Dpt'] = self.__Dpt
		self.__backDict['Name'] = self.__Name
		
	def __GetUserPerm(self):
		__permList = self.__userPerm.getUserPermission(self.__Uid)
		self.__Permission = ''
		for __PermListTmp in __permList:
			self.__Permission += __PermListTmp + '|'

	# SetUserPerm部分
	def __SetUserPerm(self):
		self.__Uid = self.__getDict['Uid']
		self.__Permission = self.__getDict['Permission']
		self.__userPerm.setUserPermission(userId=self.__Uid, permList=self.__Permission.split('|'))
		self.__backDict['Status'] = 'Y'
		self.__backDict['Message'] = '用户：' + self.__Uid + '权限信息更新已完成!'
	
	# SetBasePerm部分
	def __SetBasePerm(self):
		self.__Permission = self.__getDict['Permission']
		self.__basePerm.setBasePermission(self.__Permission.split('|'))
		self.__backDict['Status'] = 'Y'
		self.__backDict['Message'] = '基础权限信息更新已完成!'
