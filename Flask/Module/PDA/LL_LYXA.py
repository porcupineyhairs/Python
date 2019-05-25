from Module.SelfModule import MsSql
from Module.ModuleDictionary import DataBase_Dict


class PDA_LL:
	def __init__(self):
		self.__Conn_ERP = DataBase_Dict['COMFORT']
		self.__mssql = MsSql()
		self.__back = {'Mode': 'Error',
		               'Parameter': 'Done',
		               'Data': None}
		self.__Mode = None
		self.__Parameter = None
		self.__Data = None
	
	def MianWork(self, __json):
		self.__init__()
		try:
			self.__Mode = __json['Mode']
			self.__Parameter = __json['Parameter']
			self.__Data = __json['Data']
			
		except:
			print('Parameter Input Error\n', __json)
		finally:
			return self.__back
