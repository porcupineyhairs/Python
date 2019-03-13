from Module import MsSql
from Module import DataBase_Dict


# 用户权限信息类
class UserPerm:
	def __init__(self):
		self.__mssql = MsSql()

		self.__WG_Conn = DataBase_Dict['WG_DB']
		
		self.__userId = None
		self.__setPermList = None
		self.__getPermList = []

	def setUserPermission(self, userId, permList):
		self.__init__()
		self.__userId = userId
		self.__setPermList = permList
		self.__delPerm_Work()
		self.__setPerm_Work()
		
	def getUserPermission(self, userId):
		self.__init__()
		self.__userId = userId
		self.__getPerm_Work()
		return self.__getPermList
	
	def __delPerm_Work(self):
		__sqlstr = r"DELETE FROM WG_PERM_USER WHERE U_ID = '{0}'"
		self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr.format(self.__userId))
		
	def __setPerm_Work(self):
		__sqlstr = (r"INSERT INTO WG_PERM_USER (U_ID, U_NAME, Permission_ID) "
		            r"SELECT WG_USER.U_ID, WG_USER.U_NAME, WG_PERM_BASE.K_ID "
		            r"FROM WG_PERM_BASE "
		            r"INNER JOIN WG_USER ON 1=1 "
		            r"WHERE 1=1 "
		            r"AND WG_PERM_BASE.Name = '{1}' "
		            r"AND WG_USER.U_ID = '{0}' ")
		for __permList_tmp in self.__setPermList:
			self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr.format(self.__userId, __permList_tmp))
	
	def __getPerm_Work(self):
		__sqlstr = (r"SELECT Name FROM WG_PERM_BASE "
		            r"INNER JOIN WG_PERM_USER ON WG_PERM_USER.Permission_ID = WG_PERM_BASE.K_ID "
		            r"WHERE WG_PERM_USER.U_ID = '{0}' ")
		__get = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr.format(self.__userId))
		if __get[0] != 'None':
			for __get_tmp in __get:
				self.__getPermList.append(str(__get_tmp[0]))
		else:
			self.__getPermList = None


# 基础权限信息类
class BasePerm:
	def __init__(self):
		self.__mssql = MsSql()
		
		self.__WG_Conn = DataBase_Dict['WG_DB']
		
		self.__setPermList = None
	
	def setBasePermission(self, permList):
		self.__init__()
		self.__setPermList = permList
		self.__setPerm_Work()
		
	def __setPerm_Work(self):
		__sqlstrReset = r" UPDATE WG_PERM_BASE SET Valid = 'N' "
		__sqlstrFind = r" SELECT K_ID FROM WG_PERM_BASE WHERE Name = '{0}' "
		__sqlstrSet = r" UPDATE WG_PERM_BASE SET Valid = 'Y' WHERE Name = '{0}' "
		__sqlstrNew = r" INSERT INTO WG_PERM_BASE (Name) VALUES ('{0}')"
		self.__mssql.Sqlwork(self.__WG_Conn, __sqlstrReset)
		for __permList_tmp in self.__setPermList:
			__sqlget = self.__mssql.Sqlwork(self.__WG_Conn, __sqlstrFind.format(__permList_tmp))
			if __sqlget[0] != 'None':
				self.__mssql.Sqlwork(self.__WG_Conn, __sqlstrSet.format(__permList_tmp))
			else:
				self.__mssql.Sqlwork(self.__WG_Conn, __sqlstrNew.format(__permList_tmp))