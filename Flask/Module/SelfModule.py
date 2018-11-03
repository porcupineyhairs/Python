# -*- coding: utf-8 -*-
class SelfModule:
	def __str__(self):
		"""作者:Harvey.Z
		使用场合:私人使用"""

	def __init__(self):
		pass


class MsSql:
	def __str__(self):
		pass

	def __init__(self):
				# 数据库连接字转换
		self.__ConnStr = ''

		# Sqlwork方法传入参数
		self.__SqlStr = ''
		self.__DataBase = []
		self.__Mode = ''
		self.__GetRowCount = False

		# 数据返回前对其处理的临时变量
		self.__GetBackTmp1 = []
		self.__GetBackTmp2 = None

		# 数据库查询返回变量
		self.__GetBack = []
		self.__RowCount = 0

		# 是否继续流程的Flag
		self.__Flag = True

	# 判断传入数据库参数是否为空
	def __SetConnStr(self):
		if self.__DataBase is not None:
			self.__ConnStr = self.__DataBase
		else:
			self.__GetBack.append('Error')
			self.__GetBack.append('DataBaseNotFound')
			self.__Flag = False

	# 使用list数据来创建连接字及游标
	def __SetConn(self):
		import pymssql
		self.__Conn = pymssql.connect(host=self.__ConnStr[0], user=self.__ConnStr[1], password=self.__ConnStr[2],
										database=self.__ConnStr[3], charset='GBK')
		self.__Cur = self.__Conn.cursor()

	# 判断SqlStr是否为空
	def __SetSqlStrNull(self):
		if self.__SqlStr is None:
			self.__GetBack.append('Error')
			self.__GetBack.append('SqlStrIsNone')
			self.__Flag = False
		elif self.__SqlStr == '':
			self.__GetBack.append('Error')
			self.__GetBack.append('SqlStrIsNull')
			self.__Flag = False

	# 获取查询模式：select还是commit，并处理
	def __SetGetMode(self):
		# 根据SQL第一个关键字获取模式
		self.__Mode = self.__SqlStr.lstrip().split(' ')[0].upper()
		# 根据不同SQL关键字执行不同命令
		if self.__Mode == 'SELECT':
			self.__SqlExecute()
		elif self.__Mode in ('UPDATE', 'INSERT', 'DELETE'):
			self.__SqlCommit()
		else:
			self.__GetBack.append('Error')
			self.__GetBack.append('SqlStrNotFoundKeyWord')

	# 清除数据
	def __SetClean(self):
		# 清除连接字及游标
		self.__Cur.close()
		del self.__Cur
		del self.__Conn

	# 查询回来的数据整理成list，并且判断是否为空
	def __SetFormat(self):
		if len(self.__GetBackTmp1) == 0:
			self.__GetBack.append('None')
		else:
			for self.__GetBackTmp2 in self.__GetBackTmp1:
				self.__GetBack.append(list(self.__GetBackTmp2))

	# 主工作方法
	def Sqlwork(self, DataBase=None, SqlStr=None, GetRowCount=False):
		# 清空历史数据，以防递归出错
		self.__init__()

		# 传入变量转换
		self.__SqlStr = SqlStr
		self.__DataBase = DataBase
		self.__GetRowCount = GetRowCount

		# 处理逻辑
		self.__SetConnStr()

		if self.__Flag:
			self.__SetSqlStrNull()

		if self.__Flag:
			self.__SetConn()
			self.__SetGetMode()
			self.__SetFormat()
			# self.__DefClean()

		# 判断是否需要返回查询出的行数
		if self.__GetRowCount:
			if self.__Flag:
				self.__RowCount = self.__Cur.rowcount
				self.__SetClean()
			return self.__GetBack, self.__RowCount
		else:
			self.__SetClean()
			return self.__GetBack

	# 数据库查询方法
	def __SqlExecute(self):
		self.__Cur.execute(self.__SqlStr)
		self.__GetBackTmp1 = self.__Cur.fetchall()

	# 数据库任务提交方法
	def __SqlCommit(self):
		self.__Cur.commint(self.__SqlStr)
		self.__GetBackTmp1.append('Succeed')


class MySql:
	def __str__(self):
		pass

	def __init__(self):
		pass
	pass


class Oracle:
	def __str__(self):
		pass

	def __init__(self):
		pass
	pass


class Sqlite:
	def __str__(self):
		pass

	def __init__(self):
				# 数据库连接字转换
		self.__ConnStr = ''

		# Sqlwork方法传入参数
		self.__SqlStr = ''
		self.__DataBase = []
		self.__Mode = ''
		self.__GetRowCount = False

		# 数据返回前对其处理的临时变量
		self.__GetBackTmp1 = []
		self.__GetBackTmp2 = None

		# 数据库查询返回变量
		self.__GetBack = []
		self.__RowCount = 0

		# 是否继续流程的Flag
		self.__Flag = True

	# 判断传入数据库参数是否为空
	def __SetConnStr(self):
		if self.__DataBase is not None:
			self.__ConnStr = self.__DataBase
		else:
			self.__GetBack.append('Error')
			self.__GetBack.append('DataBaseNotFound')
			self.__Flag = False

	# 使用list数据来创建连接字及游标
	def __SetConn(self):
		import pymssql
		self.__Conn = pymssql.connect(host=self.__ConnStr[0], user=self.__ConnStr[1], password=self.__ConnStr[2],
										database=self.__ConnStr[3], charset='GBK')
		self.__Cur = self.__Conn.cursor()

	# 判断SqlStr是否为空
	def __SetSqlStrNull(self):
		if self.__SqlStr is None:
			self.__GetBack.append('Error')
			self.__GetBack.append('SqlStrIsNone')
			self.__Flag = False
		elif self.__SqlStr == '':
			self.__GetBack.append('Error')
			self.__GetBack.append('SqlStrIsNull')
			self.__Flag = False

	# 获取查询模式：select还是commit，并处理
	def __SetGetMode(self):
		# 根据SQL第一个关键字获取模式
		self.__Mode = self.__SqlStr.lstrip().split(' ')[0].upper()
		# 根据不同SQL关键字执行不同命令
		if self.__Mode == 'SELECT':
			self.__SqlExecute()
		elif self.__Mode in ('UPDATE', 'INSERT', 'DELETE'):
			self.__SqlCommit()
		else:
			self.__GetBack.append('Error')
			self.__GetBack.append('SqlStrNotFoundKeyWord')

	# 清除数据
	def __SetClean(self):
		# 清除连接字及游标
		self.__Cur.close()
		del self.__Cur
		del self.__Conn

	# 查询回来的数据整理成list，并且判断是否为空
	def __SetFormat(self):
		if len(self.__GetBackTmp1) == 0:
			self.__GetBack.append('None')
		else:
			for self.__GetBackTmp2 in self.__GetBackTmp1:
				self.__GetBack.append(list(self.__GetBackTmp2))

	# 主工作方法
	def Sqlwork(self, DataBase=None, SqlStr=None, GetRowCount=False):
		# 清空历史数据，以防递归出错
		self.__init__()

		# 传入变量转换
		self.__SqlStr = SqlStr
		self.__DataBase = DataBase
		self.__GetRowCount = GetRowCount

		# 处理逻辑
		self.__SetConnStr()

		if self.__Flag:
			self.__SetSqlStrNull()

		if self.__Flag:
			self.__SetConn()
			self.__SetGetMode()
			self.__SetFormat()
			# self.__DefClean()

		# 判断是否需要返回查询出的行数
		if self.__GetRowCount:
			if self.__Flag:
				self.__RowCount = self.__Cur.rowcount
				self.__SetClean()
			return self.__GetBack, self.__RowCount
		else:
			self.__SetClean()
			return self.__GetBack

	# 数据库查询方法
	def __SqlExecute(self):
		self.__Cur.execute(self.__SqlStr)
		self.__GetBackTmp1 = self.__Cur.fetchall()

	# 数据库任务提交方法
	def __SqlCommit(self):
		self.__Cur.commint(self.__SqlStr)
		self.__GetBackTmp1.append('Succeed')


class Mdns:
	def __str__(self):
		pass

	def __init__(self):
		pass

	class Creator:
		def __init__(self):
			self.__addr = ''
			self.__port = 0
			self.__name = ''
			self.__server = ''
			self.__details = {}

			self.__name_server = ''
			self.__GoOnFlag = True
			self.__GetBack = ''

		def creator(self, addr=None, port=None, name=None, server=None, details=None):
			self.__addr = addr
			self.__port = port
			self.__name = name
			self.__server = server
			self.__details = details

			self.__judge()
			if self.__GoOnFlag:
				self.__name_server = self.name + '.' + self.server
				self.__creator_work()
			return self.__GetBack

		def __judge(self):
			if None in (self.addr, self.port, self.name, self.server, self.details):
				self.__GoOnFlag = False
				self.__GetBack = 'Lack of parameter!'

		def __creator_work(self):
			import socket
			from zeroconf import ServiceInfo, Zeroconf

			self.__r = Zeroconf()
			self.__info = ServiceInfo(self.__server, self.__name_server, socket.inet_aton(self.__addr), self.__port, 0, 0, self.__details)
			self.__r.register_service(self.__info)
			self.__GetBack = 'Create success'
			del self.__r

	class Deleter:
		def __init__(self):
			self.__server = ''
			self.__name = ''
			self.__name_server = ''

			self.__GoOnFlag = True
			self.__GetBack = ''

		def deleter(self, server=None, name=None):
			self.__server = server
			self.__name = name
			self.__judge()
			if self.__GoOnFlag:
				self.__name_server = self.__name + '.' + self.__server
				self.__delete_work()
			return self.__GetBack

		def __judge(self):
			if None in (self.__server, self.__name):
				self.__GoOnFlag = False
				self.__GetBack = 'Lack of parameter!'

		def __delete_work(self):
			from zeroconf import Zeroconf

			self.__r = Zeroconf()
			self.__info = self.__r.get_service_info(self.__server, self.__name_server)
			if self.__info is not None:
				self.__r.unregister_service(self.__info)
				self.__GetBack = 'Delete success'
			else:
				self.__GetBack = 'Note found service!'
			del self.__r

	class Finder:
		pass

	class Listener:
		pass


class Socket:
	def __str__(self):
		pass

	def __init__(self):
		self.__send_addr = ''
		self.__send_port = 0
		self.__send_str = ''
		self.__GetBack = ''

	def send(self, Send_Addr=None, Send_Port=None, Send_Str=None):
		# 变量初始化
		self.__send_addr = Send_Addr
		self.__send_port = Send_Port
		self.__send_str = Send_Str
		self.__sendWork()

	def __sendWork(self):
		import socket
		self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__s.connect((str(self.__send_addr), self.__send_port))
		self.__s.settimeout(5)
		self.__s.send(bytes(str(self.__send_str).encode(encoding='utf-8')))
		self.__s.close()
		del socket


class SocketServer:
	pass


class Logging:
	def __str__(self):
		pass

	def __init__(self):
		pass


class XML2Class:
	pass


class Class2XML:
	pass


class Json2Class:
	pass


class Class2Json:
	pass


class Normal:
	def __str__(self):
		pass

	def __init__(self):
		self.__name = ''
		self.__namelist = []
		self.__systeminfo = ''
		self.__localip = ''

	def getsysteminfo(self):
		import platform
		self.__name = platform.uname()
		self.__namelist = str(self.__name).split('(')[1].rstrip(')').split(',')
		for self.__name in self.__namelist:
			if self.__name.find('system=') != -1:
				self.__systeminfo = self.__name.split('\'')[1].rstrip('\'')
		del self.__name
		del self.__namelist
		del platform
		return self.__systeminfo

	def getlocalip(self):
		import os
		self.__systeminfo = self.getsysteminfo()
		if self.__systeminfo == 'Linux':
			# Linux
			self.__localip = os.popen(
			"ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()
		elif self.__systeminfo == 'Darwin':
			# MAC
			self.__localip = os.popen(
				"ifconfig | grep 'inet' |grep -v 'inet6'|grep -v '127.0.0.1' | cut -d: -f2| awk '{print $2}'| head -1").read()
		else:
			self.__localip = None
		del self.__systeminfo
		del os
		return self.__localip
