from Module import DataBase_Dict
from Module.SelfModule import MsSql


class GetVersion:
	def __init__(self):
		self.__FileName = None
		self.__FileVersion = None
		self.__NewVersion = None
		self.__NewVersionFlag = False
		self.__back = {'Mode': 'Yes',  'URL': None}
		
		self.__Conn_WG = DataBase_Dict['WG_DB']
		self.__mssql = MsSql()
	
	def Main(self, __json):
		self.__init__()
		self.__FileName = __json['ProgName']
		self.__FileVersion = __json['Version']
		self.__MainWork()
		return self.__back
		
	def __MainWork(self):
		__sqlstr = r"SELECT Version FROM WG_APP_INF WHERE Vaild = 'Y' AND ProgName = '联友生产辅助工具' "
		__get = self.__mssql.Sqlwork(DataBase=self.__Conn_WG, SqlStr=__sqlstr)
		print(__get)
		if __get[0] == 'None':
			self.__back['Mode'] = 'False'
			self.__back['URL'] = '若需使用功能，请登录网页：'
		else:
			self.__NewVersion = __get[0][0]
			self.__VersionCompare()
			if self.__NewVersionFlag:
				self.__back['Mode'] = 'New'
				self.__back['URL'] = 'http://192.168.7.251:8099/Client/WG/Download/' + self.__FileName + '.exe'
			else:
				self.__back['Mode'] = 'Yes'
			
	def __VersionCompare(self):
		__FileVersion_List = self.__FileVersion.split('.')
		__NewVersion_list = self.__NewVersion.split('.')
		for i in range(3):
			if int(__NewVersion_list[i]) > int(__FileVersion_List[i]):
				self.__NewVersionFlag = True
