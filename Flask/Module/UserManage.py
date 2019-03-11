from Module import MsSql
from Module import DataBase_Dict


class UserManege:
	def __init__(self):
		self.__mssql = MsSql()
		self.__json = None
		self.__back = {'Login_Status': 'N',
		               'Login_Uid': None,
		               'Login_Role': None,
		               'Login_Dpt': None,
		               'Login_Name': None,
		               }

		self.__Login_Uid = None
		self.__Login_Pwd = None
		self.__Login_Status = 'N'
		self.__Login_Role = None
		self.__Login_Dpt = None
		self.__Login_Name = None

		self.__WG_Pwd = None
		self.__WG_Type = None
		self.__WG_Flag = None
		self.__WG_ERP_Pwd = None

		self.__ERP_Pwd = None
		self.__ERP_Valid = None

		self.__get_WG = None
		self.__get_ERP = None

		self.__WG_Conn = DataBase_Dict['WG_DB']
		self.__ERP_Conn = DataBase_Dict['COMFORT']

	def UserLogin(self, _json):
		self.__init__()

		self.__json = _json
		# print(self.__json)
		self.__Login_Uid = self.__json['Login_Uid']
		self.__Login_Pwd = self.__json['Login_Pwd']

		self.__Login_Work()

		return self.__back

	def __Login_Work(self):
		self.__Get_ERPInf()
		self.__Get_WGInf()
		self.__Set_Inf()

		if self.__Judge_ERPExist():
			if self.__ERP_Valid == 'Y':
				if self.__Judge_WGExist():
					if self.__WG_Flag == 'Y':
						if self.__Judge_WG_PwdSame():
							self.__Login_Status = 'Y'
							self.__Set_UserInf()
						else:
							if not self.__Judge_ERP_PwdSame():
								self.__Login_Status = 'Y'
								self.__Set_UserInf()
								self.__Update_WGInf()
					else:
						self.__Login_Status = 'Y'
						self.__Set_UserInf()
						self.__Update_WGInf()
				else:
					self.__Login_Status = 'Y'
					self.__Set_UserInf()
					self.__Insert_WGInf()
			else:
				self.__back['Login_Status'] = 'y'

	def __Get_WGInf(self):
		__sqlstr = (r"SELECT U_ID, U_NAME, U_PWD, ERP_PWD, DPT, ROLE, FLAG, TYPE FROM WG_USER "
		            r"WHERE U_ID = '" + self.__Login_Uid + "'")
		self.__get_WG = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)

	def __Get_ERPInf(self):
		__sqlstr = (r"SELECT RTRIM(MA001), RTRIM(MA002), RTRIM(ME002), RTRIM(MA003), RTRIM(MA005) "
		            r"FROM DSCSYS..DSCMA AS DSCMA "
		            r"LEFT JOIN CMSMV ON MV001 = MA001 "
		            r"LEFT JOIN CMSME ON ME001 = MV004 "
		            r"WHERE MA001 = '" + self.__Login_Uid + r"'")
		self.__get_ERP = self.__mssql.Sqlwork(DataBase=self.__ERP_Conn, SqlStr=__sqlstr)

	def __Judge_ERP_PwdSame(self):
		if self.__ERP_Pwd == self.__WG_ERP_Pwd:
			return True
		else:
			return False

	def __Judge_WG_PwdSame(self):
		if self.__WG_Pwd == self.__Login_Pwd:
			return True
		else:
			return False

	def __Judge_WGExist(self):
		# if len(self.__get_WG) > 0:
		if self.__get_WG[0] is not 'None':
			return True
		else:
			return False

	def __Judge_ERPExist(self):
		# if len(self.__get_ERP) > 0:
		if self.__get_ERP[0] is not 'None':
			return True
		else:
			return False

	def __Insert_WGInf(self):
		self.__ERP_Pwd = self.__ERP_Pwd.replace("'", "''")
		if self.__Login_Dpt is not None:
			__sqlstr = (r"INSERT INTO WG_USER (U_ID, U_NAME, U_PWD, ERP_PWD, DPT, ROLE, FLAG, TYPE) "
			            r"VALUES("
			            r"'" + self.__Login_Uid + "', "
	                    r"'" + self.__Login_Name + "', "
	                    r"'" + self.__WG_Pwd + "', "
	                    r"'" + self.__ERP_Pwd + "', "
	                    r"'" + self.__Login_Dpt + "', "
	                    r"'', 'Y', 'ERP'"
			            r")")
		else:
			__sqlstr = (r"INSERT INTO WG_USER (U_ID, U_NAME, U_PWD, ERP_PWD, ROLE, FLAG, TYPE) "
			            r"VALUES("
			            r"'" + self.__Login_Uid + "', "
                        r"'" + self.__Login_Name + "', "
                        r"'" + self.__WG_Pwd + "', "
                        r"'" + self.__ERP_Pwd + "', "
                        r"'', 'Y', 'ERP'"
                        r")")
		self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)

	def __Update_WGInf(self):
		self.__ERP_Pwd = self.__ERP_Pwd.replace("'", "''")
		if self.__Login_Dpt is not None:
			__sqlstr = (r"UPDATE WG_USER SET "
			            r"U_NAME = '" + self.__Login_Name + "', "
	                    r"U_PWD = '" + self.__Login_Pwd + "', "
	                    r"ERP_PWD = '" + self.__ERP_Pwd + "', "
	                    r"DPT = '" + self.__Login_Dpt + "', "
	                    r"FLAG = 'Y' "
			            r"WHERE U_ID = '" + self.__Login_Uid + "'")
		else:
			__sqlstr = (r"UPDATE WG_USER SET "
			            r"U_NAME = '" + self.__Login_Name + "', "
			            r"U_PWD = '" + self.__Login_Pwd + "', "
			            r"ERP_PWD = '" + self.__ERP_Pwd + "', "
			            r"FLAG = 'Y' "
			            r"WHERE U_ID = '" + self.__Login_Uid + "'")
		self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)

	def __Set_Inf(self):
		if self.__Judge_ERPExist():
			self.__Login_Uid = str(self.__get_ERP[0][0])
			self.__Login_Name = self.__get_ERP[0][1]
			self.__Login_Dpt = self.__get_ERP[0][2]
			self.__ERP_Pwd = self.__get_ERP[0][3]
			self.__ERP_Valid = self.__get_ERP[0][4]

		if self.__Judge_WGExist():
			self.__WG_Pwd = self.__get_WG[0][2]
			self.__WG_ERP_Pwd = self.__get_WG[0][3]
			self.__Login_Role = self.__get_WG[0][5]
			self.__WG_Flag = self.__get_WG[0][6]
			self.__WG_Type = self.__get_WG[0][7]
		else:
			self.__WG_Pwd = self.__Login_Pwd

	def __Set_UserInf(self):
		self.__back['Login_Status'] = self.__Login_Status
		self.__back['Login_Uid'] = self.__Login_Uid
		self.__back['Login_Role'] = self.__Login_Role
		self.__back['Login_Dpt'] = self.__Login_Dpt
		self.__back['Login_Name'] = self.__Login_Name
