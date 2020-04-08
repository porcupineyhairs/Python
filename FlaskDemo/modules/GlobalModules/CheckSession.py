from modules.Sql.MySql import *
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
		mysql = MySqlHelper(host='127.0.0.1', user='root', passwd='Tiamohui', database='WebApp')
		sqlStr = "insert into session(session_id, create_time, last_time, `key`, `value`, remark) " \
		         "values ('{session}', now(), now(), '{key}', '{value}', '{remark}')"
		session = kwargs['session'] if 'session' in kwargs.keys() else CreateRandomCode.get32bRandomCode()
		value = kwargs['value'] if 'value' in kwargs.keys() else ''
		remark = kwargs['remark'] if 'remark' in kwargs.keys() else ''

		mysql.sqlWork(sqlStr=sqlStr.format(session=session, key=kwargs['key'], value=value, remark=remark))
		del mysql
		return session

	@staticmethod
	def updateTokenTime(**kwargs):
		mysql = MySqlHelper(host='127.0.0.1', user='root', passwd='Tiamohui', database='WebApp')
		sqlStr = "update session set last_time=now() where session_id='{session}' "
		mysql.sqlWork(sqlStr=sqlStr.format(session=kwargs['session']))
		del mysql

	@staticmethod
	def checkToken(minutes=30, **kwargs):
		mysql = MySqlHelper(host='127.0.0.1', user='root', passwd='Tiamohui', database='WebApp')
		sqlStr = "select session_id from session where session_id='{session}' " \
		         "and now()<date_add(last_time, interval {minutes} minute) "
		if 'key' in kwargs.keys():
			sqlStr += " and `key`='{key}' "
			get = mysql.sqlWork(sqlStr=sqlStr.format(session=kwargs['session'], key=kwargs['key'], minutes=minutes))
		else:
			get = mysql.sqlWork(sqlStr=sqlStr.format(session=kwargs['session'], minutes=minutes))
		del mysql

		if get is not None:
			return True
		else:
			return False

	@staticmethod
	def deleteToken(**kwargs):
		mysql = MySqlHelper(host='127.0.0.1', user='root', passwd='Tiamohui', database='WebApp')
		sqlStr = "delete from session where session_id='{session}' "
		if 'key' in kwargs.keys():
			sqlStr += " and `key`='{key}' "
			mysql.sqlWork(sqlStr=sqlStr.format(session=kwargs['session'], key=kwargs['key']))
		else:
			mysql.sqlWork(sqlStr=sqlStr.format(session=kwargs['session']))
		del mysql
