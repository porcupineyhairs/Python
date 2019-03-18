from Module import DataBase_Dict
from Module import Sql


# 用户权限信息类
class UserPermission:
	def __init__(self):
		self.__sqlWg = Sql(sqlType='mssql', connDict=DataBase_Dict['WG_DB'])
		
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
		__sqlStr = r"DELETE FROM WG_PERM_USER WHERE U_ID = '{0}'"
		self.__sqlWg.SqlWork(sqlStr=__sqlStr.format(self.__userId))
		
	def __setPerm_Work(self):
		__sqlStr = (r"INSERT INTO WG_PERM_USER (U_ID, U_NAME, Permission_ID) "
		            r"SELECT WG_USER.U_ID, WG_USER.U_NAME, WG_PERM_BASE.K_ID "
		            r"FROM WG_PERM_BASE "
		            r"INNER JOIN WG_USER ON 1=1 "
		            r"WHERE 1=1 "
		            r"AND WG_PERM_BASE.Name = '{1}' "
		            r"AND WG_USER.U_ID = '{0}' ")
		for __permList_tmp in self.__setPermList:
			self.__sqlWg.SqlWork(sqlStr=__sqlStr.format(self.__userId, __permList_tmp))
	
	def __getPerm_Work(self):
		__sqlStr = (r"SELECT Name FROM WG_PERM_BASE "
		            r"INNER JOIN WG_PERM_USER ON WG_PERM_USER.Permission_ID = WG_PERM_BASE.K_ID "
		            r"WHERE WG_PERM_USER.U_ID = '{0}' ")
		__get = self.__sqlWg.SqlWork(sqlStr=__sqlStr.format(self.__userId))
		if __get[0] != 'None':
			for __get_tmp in __get:
				self.__getPermList.append(str(__get_tmp[0]))
		else:
			self.__getPermList = None


# 基础权限信息类
class BasePermission:
	def __init__(self):
		self.__sqlWg = Sql(sqlType='mssql', connDict=DataBase_Dict['WG_DB'])
		
		self.__setPermList = None
	
	def setBasePermission(self, permList):
		self.__init__()
		self.__setPermList = permList
		self.__setPerm_Work()
		
	def __setPerm_Work(self):
		__sqlStrReset = r" UPDATE WG_PERM_BASE SET Valid = 'N' "
		__sqlStrFind = r" SELECT K_ID FROM WG_PERM_BASE WHERE Name = '{0}' "
		__sqlStrSet = r" UPDATE WG_PERM_BASE SET Valid = 'Y' WHERE Name = '{0}' "
		__sqlStrNew = r" INSERT INTO WG_PERM_BASE (Name) VALUES ('{0}')"
		self.__sqlWg.SqlWork(sqlStr=__sqlStrReset)
		
		for __permListTmp in self.__setPermList:
			__sqlGet = self.__sqlWg.SqlWork(sqlStr=__sqlStrFind.format(__permListTmp))
			if __sqlGet[0] != 'None':
				self.__sqlWg.SqlWork(sqlStr=__sqlStrSet.format(__permListTmp))
			else:
				self.__sqlWg.SqlWork(sqlStr=__sqlStrNew.format(__permListTmp))
