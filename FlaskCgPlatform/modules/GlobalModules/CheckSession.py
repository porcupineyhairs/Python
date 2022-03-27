from modules.Sql.MsSql import *
from modules.GlobalModules.CreateRandomCode import CreateRandomCode


class CheckSessionException(Exception):
	def __init__(self, errInf):
		self.__errInf = errInf
		super().__init__(self)

	def __str__(self):
		return self.__errInf


class CheckSession:
	@staticmethod
	def createToken(**kwargs):
		sql = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='CgPlatform')
		sqlStr = "insert into token(token_id, create_time, last_time, tkey, tvalue, remark) " \
		         "values ('{token}', getdate(), getdate(), '{key}', '{value}', '{remark}')"
		token = kwargs['token'] if 'token' in kwargs.keys() else CreateRandomCode.get32bRandomCode()
		value = kwargs['value'] if 'value' in kwargs.keys() else ''
		remark = kwargs['remark'] if 'remark' in kwargs.keys() else ''

		sql.sqlWork(sqlStr=sqlStr.format(token=token, key=kwargs['key'], value=value, remark=remark))
		del sql
		return token

	@staticmethod
	def updateTokenTime(**kwargs):
		sql = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='CgPlatform')
		sqlStr = "update token set last_time=getdate() where token_id='{token}' "
		sql.sqlWork(sqlStr=sqlStr.format(token=kwargs['token']))
		del sql

	@staticmethod
	def getTokenValue(**kwargs):
		sql = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='CgPlatform')
		sqlStr = "select tvalue from token where token_id='{token}' and tkey = '{key}'"
		get = sql.sqlWork(sqlStr.format(token=kwargs['token'], key=kwargs['key']))
		del sql
		if get is not None:
			return get[0][0]
		else:
			return None

	@staticmethod
	def existLiveToken(minutes=30, **kwargs):
		sql = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='CgPlatform')
		sqlStr = "select token_id from token where token_id='{token}' " \
		         "and getdate()<dateadd(minute, 30, last_time) "
		if 'key' in kwargs.keys():
			sqlStr += " and tkey='{key}' "
			get = sql.sqlWork(sqlStr=sqlStr.format(token=kwargs['token'], key=kwargs['key'], minutes=minutes))
		else:
			get = sql.sqlWork(sqlStr=sqlStr.format(token=kwargs['token'], minutes=minutes))
		del sql

		if get is not None:
			return True
		else:
			return False

	@staticmethod
	def deleteToken(**kwargs):
		sql = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='CgPlatform')
		sqlStr = "delete from token where token_id='{token}' "
		if 'key' in kwargs.keys():
			sqlStr += " and tkey='{key}' "
			sql.sqlWork(sqlStr=sqlStr.format(token=kwargs['token'], key=kwargs['key']))
		else:
			sql.sqlWork(sqlStr=sqlStr.format(token=kwargs['token']))
		del sql

	@staticmethod
	def cleanToken(**kwargs):
		sql = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='CgPlatform')
		sqlStr = "delete from token where token_id in " \
		         "(select distinct token_id from token where getdate() > DATEADD(minute, 30, last_time)) "
		sql.sqlWork(sqlStr)
		del sql

	@staticmethod
	def checkToken(token):
		if token is None:
			return False
		else:
			CheckSession.cleanToken()
			if CheckSession.existLiveToken(token=token):
				CheckSession.updateTokenTime(token=token)
				return True
			else:
				return False
