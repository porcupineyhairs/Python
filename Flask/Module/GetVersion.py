from Module import DataBase_Dict

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

Base = declarative_base()


def ConvertStr(_str):
	return _str.encode('GBK')


class WG_APP_INF(Base):
	__tablename__ = 'WG_APP_INF'
	ProgName = Column('ProgName', primary_key=True)
	Version = Column('Version')
	Valid = Column('Valid')


class GetVersion:
	def __init__(self):
		self.__FileName = None
		self.__FileVersion = None
		self.__NewVersion = None
		self.__NewVersionFlag = False
		self.__back = {'Mode': 'Yes',  'URL': None}
		
		engine = create_engine(r"mssql+pymssql://sa:COMfort123456@192.168.0.198/WG_DB?charset=GBK")
		
		self.DbSession = sessionmaker(bind=engine, autoflush=True, autocommit=False)
	
	def Main(self, __json):
		self.__init__()
		self.__FileName = __json['ProgName']
		self.__FileVersion = __json['Version']
		self.__MainWork()
		return self.__back
		
	def __MainWork(self):
		
		session = self.DbSession()
		
		__get = session.query(WG_APP_INF.Version).filter_by(ProgName=ConvertStr('联友生产辅助工具'), Valid='Y').all()
		
		if len(__get) == 0:
			self.__back['Mode'] = 'False'
			self.__back['URL'] = '若需使用功能，请登录网页：'
		else:
			self.__NewVersion = __get[0][0]
			self.__VersionCompare()
			if self.__NewVersionFlag:
				self.__back['Mode'] = 'New'
				self.__back['URL'] = '/Client/WG/Download/' + self.__FileName + '.exe'
			else:
				self.__back['Mode'] = 'Yes'
			
	def __VersionCompare(self):
		__FileVersion_List = self.__FileVersion.split('.')
		__NewVersion_list = self.__NewVersion.split('.')
		for i in range(4):
			if int(__NewVersion_list[i]) > int(__FileVersion_List[i]):
				self.__NewVersionFlag = True
