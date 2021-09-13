import pymssql
import pandas as pd


class MsSqlHelperException(Exception):
	def __init__(self, errInf):
		self.__errInf = errInf
		super().__init__(self)

	def __str__(self):
		return self.__errInf


class MsSqlHelper:
	def __doc__(self):
		return 'Class Name: MsSqlHelper \n' \
		       'This the class to use MsSql for Select, Update, Delete, Insert and so on. \n' \
		       'But the Proc is not test now, if use be careful! \n' \
		       'Author：Harvey \n' \
		       'CreateDate：2020.03.11 '

	def __init__(self, host=None, port=1433, user=None, passwd=None, database=None, charset='GBK'):
		self.__host = host
		self.__port = port
		self.__user = user
		self.__passwd = passwd
		self.__db = database
		self.__charset = charset

		self.__conn = None
		self.__cur = None
		self.__sqlStr = None

		self.__columns = None
		self.__data = None

		self.__sqlMode = None
		self.__getNoNone = None

		self.__getBackTmp = None

		self.__createObj()

	def __del__(self):
		del self.__host
		del self.__port
		del self.__user
		del self.__passwd
		del self.__db
		del self.__charset

		self.__conn.close()
		self.__cur.close()

		del self.__conn
		del self.__cur
		del self.__sqlStr
		del self.__columns
		del self.__data
		del self.__sqlMode
		del self.__getNoNone
		del self.__getBackTmp

	# 一下为OBJ创建
	def __createObj(self):
		if (self.__host is None or self.__host == '' or self.__user is None or self.__user == '' or
				self.__passwd is None or self.__passwd == '' or self.__db is None or self.__db == ''):
			raise MsSqlHelperException('Input Parameter is Error.')

		self.__conn = pymssql.connect(host=self.__host, user=self.__user, password=self.__passwd, database=self.__db,
		                              charset=self.__charset)
		self.__cur = self.__conn.cursor()

	# 以下为SQL语句处理
	def sqlWork(self, sqlStr=None, getNoNone=True):
		self.__clean()
		self.__sqlStr = sqlStr
		self.__getNoNone = getNoNone

		self.__work()
		self.__formatData()
		self.__setNoNone()
		if self.__data is not None:
			self.__formatTitle()
			return pd.DataFrame(data=self.__data, columns=self.__columns)
		else:
			return None

	def __clean(self):
		self.__sqlStr = None
		self.__sqlMode = None
		self.__columns = None
		self.__data = None
		self.__getBackTmp = None

	def __work(self):
		if self.__sqlStr is None:
			raise MsSqlHelperException('Sql Str is None.')
		# 根据SQL第一个关键字获取模式
		self.__sqlMode = self.__sqlStr.lstrip().split(' ')[0].upper()
		# 根据不同SQL关键字执行不同命令
		if self.__sqlMode in ('SELECT', 'EXEC', 'IF', 'DECLARE'):
			self.__sqlExecute()
		elif self.__sqlMode in ('UPDATE', 'INSERT', 'DELETE', 'TRUNCATE'):
			self.__sqlCommit()
		else:
			raise MsSqlHelperException('Can Not Get Sql Mode, Please Check Sql Sentence. Sql: ' + self.__sqlStr)

	# 数据库查询方法
	def __sqlExecute(self):
		self.__cur.execute(self.__sqlStr)
		if self.__sqlMode in ('EXEC', 'IF', 'DECLARE'):
			try:
				self.__getBackTmp = self.__cur.fetchall()
			except Exception as e:
				self.__getBackTmp = None
		else:
			self.__getBackTmp = self.__cur.fetchall()

	# 数据库任务提交方法
	def __sqlCommit(self):
		self.__cur.execute(self.__sqlStr)
		self.__conn.commit()

	def __formatData(self):
		# 整理需要返回的数据
		try:
			if len(self.__getBackTmp) == 0:
				self.__getBackTmp = None
			else:
				self.__data = []
				for __rowIndex in range(len(self.__getBackTmp)):
					self.__data.append(list(self.__getBackTmp[__rowIndex]))
		except Exception as e:
			self.__data = None

	def __setNoNone(self):
		# 判断是否需要把返回结果中的None变更为''
		if self.__getNoNone and self.__data is not None:
			__rowCount = len(self.__data)
			__colCount = len(self.__data[0])
			for __romIndex in range(__rowCount):
				for __colIndex in range(__colCount):
					if self.__data[__romIndex][__colIndex] is None:
						self.__data[__romIndex][__colIndex] = ''

	def __formatTitle(self):
		__title = []
		for __TitleTmp in self.__cur.description:
			__title.append(__TitleTmp[0])
		self.__columns = __title


class MsSqlHelperBasic:
	def __doc__(self):
		return 'Class Name: MsSqlHelper \n' \
		       'This the class to use MsSql for Select, Update, Delete, Insert and so on. \n' \
		       'But the Proc is not test now, if use be careful! \n' \
		       'Author：Harvey \n' \
		       'CreateDate：2020.03.11 '

	def __init__(self, host=None, port=1433, user=None, passwd=None, database=None, charset='GBK'):
		self.__host = host
		self.__port = port
		self.__user = user
		self.__passwd = passwd
		self.__db = database
		self.__charset = charset

		self.__conn = None
		self.__cur = None
		self.__sqlStr = None
		self.__getTitle = False
		self.__getRowCount = False

		self.__sqlMode = None
		self.__getNoNone = None

		self.__getBackTmp = None
		self.__getBack = None

		self.__createObj()

	def __del__(self):
		del self.__host
		del self.__port
		del self.__user
		del self.__passwd
		del self.__db
		del self.__charset

		self.__conn.close()
		self.__cur.close()

		del self.__conn
		del self.__cur
		del self.__sqlStr
		del self.__getTitle
		del self.__getRowCount
		del self.__sqlMode
		del self.__getNoNone
		del self.__getBack
		del self.__getBackTmp

	# 一下为OBJ创建
	def __createObj(self):
		if (self.__host is None or self.__host == '' or self.__user is None or self.__user == '' or
				self.__passwd is None or self.__passwd == '' or self.__db is None or self.__db == ''):
			raise MsSqlHelperException('Input Parameter is Error.')

		self.__conn = pymssql.connect(host=self.__host, user=self.__user, password=self.__passwd, database=self.__db,
		                              charset=self.__charset)
		self.__cur = self.__conn.cursor()

	# 以下为SQL语句处理
	def sqlWork(self, sqlStr=None, getNoNone=True, getTitle=False):
		self.__clean()
		self.__sqlStr = sqlStr
		self.__getNoNone = getNoNone
		self.__getTitle = getTitle

		self.__work()
		self.__formatData()
		self.__setNoNone()
		self.__setTitle()

		return self.__getBack

	def __clean(self):
		self.__sqlStr = None
		self.__sqlMode = None
		self.__getBackTmp = None
		self.__getBack = None

	def __work(self):
		if self.__sqlStr is None:
			raise MsSqlHelperException('Sql Str is None.')
		# 根据SQL第一个关键字获取模式
		self.__sqlMode = self.__sqlStr.lstrip().split(' ')[0].upper()
		# 根据不同SQL关键字执行不同命令
		if self.__sqlMode in ('SELECT', 'EXEC', 'IF', 'DECLARE'):
			self.__sqlExecute()
		elif self.__sqlMode in ('UPDATE', 'INSERT', 'DELETE', 'TRUNCATE'):
			self.__sqlCommit()
		else:
			raise MsSqlHelperException('Can Not Get Sql Mode, Please Check Sql Sentence. Sql: ' + self.__sqlStr)

	# 数据库查询方法
	def __sqlExecute(self):
		self.__cur.execute(self.__sqlStr)
		if self.__sqlMode in ('EXEC', 'IF', 'DECLARE'):
			try:
				self.__getBackTmp = self.__cur.fetchall()
			except Exception as e:
				self.__getBackTmp = None
		else:
			self.__getBackTmp = self.__cur.fetchall()

	# 数据库任务提交方法
	def __sqlCommit(self):
		self.__cur.execute(self.__sqlStr)
		self.__conn.commit()

	def __formatData(self):
		# 整理需要返回的数据
		try:
			if len(self.__getBackTmp) == 0:
				self.__getBackTmp = None
			else:
				self.__getBack = []
				for __rowIndex in range(len(self.__getBackTmp)):
					self.__getBack.append(list(self.__getBackTmp[__rowIndex]))
		except Exception as e:
			self.__getBack = None

	def __setNoNone(self):
		# 判断是否需要把返回结果中的None变更为''
		if self.__getNoNone and self.__getBack is not None:
			__rowCount = len(self.__getBack)
			__colCount = len(self.__getBack[0])
			for __romIndex in range(__rowCount):
				for __colIndex in range(__colCount):
					if self.__getBack[__romIndex][__colIndex] is None:
						self.__getBack[__romIndex][__colIndex] = ''

	def __setTitle(self):
		if self.__getTitle and self.__getBack is not None:
			__title = []
			for __TitleTmp in self.__cur.description:
				__title.append(__TitleTmp[0])
			self.__getBack.insert(0, __title)
