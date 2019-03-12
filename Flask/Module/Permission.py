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
		__sqlstr = (r" INSERT INTO WG_PERM_USER () VALUES () ")
		for __permList_tmp in self.__setPermList:
			self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr.format(self.__userId, __permList_tmp))
	
	def __getPerm_Work(self):
		__sqlstr = r" SELECT PERM FROM WG_PERM_USER WHERE U_ID = '{0}' "
		__get = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr.format(self.__userId))
		if __get[0] != 'None':
			for __get_tmp in __get:
				self.__getPermList.append(str(__get_tmp[0]))
		else:
			self.__getPermList = None
	
	# def __GetWGPerm(self):
	# 	__sqlstr = (r"SELECT U_ID, U_NAME,Permission_ID, Group_ID FROM WG_PERM_USER "
	# 				r"WHERE U_ID = '" + self.__U_ID + "'")
	# 	self.__get_WGPerm = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
	# 	for i in range(len(self.__get_WGPerm)):
	# 		self.permission.append(self.__get_WGPerm[i][2])
	#
	# def __GetPermID(self, perm_str):
	# 	__sqlstr = (r"SELECT K_ID FROM WG_PERM_BASE "
	# 				r"WHERE Name = '" + perm_str + "'")
	# 	self.__get_WGPermID = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
	# 	return self.__get_WGPermID[0]
	#
	# def __GetPermName(self, perm_id):
	# 	__sqlstr = (r"SELECT Name FROM WG_PERM_BASE "
	# 				r"WHERE K_ID = '" + perm_id + "'")
	# 	self.__get_WGPermName = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
	# 	return self.__get_WGPermName[0]
	#
	# def __GetGroupID(self, perm_id):
	# 	__sqlstr = (r"SELECT Group_ID FROM WG_GROUP "
	# 				r"WHERE Permission_ID = '" + perm_id + "'")
	# 	self.__get_GroupID = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
	# 	return self.__get_GroupID[0]
	#
	# def __InsertWGPerm(self):
	# 	__sqlstr = (r"INSERT INTO WG_PERM_USER (U_ID, U_NAME, Permission_ID,Group_ID) "
	# 				r"VALUES("
	# 				r"'" + self.__U_ID + "', "
	# 				r"'" + self.__U_NAME + "', "
	# 				r"'" + self.__Permission_ID + "', "
	# 				r"'" + self.__Group_ID + "', "
	# 				r")")
	# 	self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
	#
	# def __Update_WGPerm(self):
	# 	__sqlstr = (r"UPDATE WG_PERM_USER SET "
	# 				r"U_NAME = '" + self.__U_NAME + "', "
	# 				r"Permission_ID = '" + self.__Permission_ID + "', "
	# 				r"Group_ID = '" + self.__Group_ID +
	# 				r"WHERE U_ID = '" + self.__U_ID + "''")
	# 	self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
	#
	# def __Delete_Perm(self, perm_ID):
	# 	__sqlstr = ("DELETE FROM WG_PERM_USER WHERE U_ID = '" + self.__U_ID + "' AND Permission_ID = '" + perm_ID + "'")
	# 	self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
	#
	# def __Set_WGPerm(self, perm):
	# 	self.__Permission_ID = perm
	# 	self.__Group_ID = self.__GetGroupID(perm)
	# 	self.__back.append(self.__Permission_ID)


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
		pass
