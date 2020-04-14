from datetime import datetime
from modules.Sql.MySql import *
from modules.GlobalModules import CheckSession
from modules.GlobalModules.CreateCheckCodeImg import getCheckCodeImgPath
from modules.GlobalModules.CreateRandomCode import CreateRandomCode


def getUserByToken(token):
	mysql = MySqlHelper(host='127.0.0.1', user='root', passwd='Tiamohui', database='WebApp')
	sqlStr = "select `user_name` from `user` inner join session on session.`key`='user' and session.`value`=`user`.`user` " \
	         "where session.session_id='{session}'"
	get = mysql.sqlWork(sqlStr.format(session=token))
	return '' if get is None else get[0][0]


class Login:
	def __init__(self, token, ip, mode):
		self.__ip = ip
		self.token = token
		self.__mode = mode

		self.tokenExist = False
		self.login = False
		self.checkCodeErr = True
		self.checkCodeImgPath = ''
		self.__checkCodeStr = ''

		self.errStr = ''

		self.__checkCode = None
		self.__user = None
		self.__pwd = None

		self.__mysql = MySqlHelper(host='127.0.0.1', user='root', passwd='Tiamohui', database='WebApp')

		if self.__mode == 'GET':
			self.__preWork()

	def __preWork(self):
		self.login = False
		self.tokenExist = False
		self.checkCodeImgPath = ''
		self.__checkCodeStr = ''
		self.errStr = ''

		self.__judgeToken()
		self.__getCheckCode()

	def __judgeToken(self):
		if self.token is None:
			self.tokenExist = False
			self.login = False
			self.token = CheckSession.createToken(key='live')
		else:
			self.tokenExist = True
			if CheckSession.checkToken(session=self.token, key='live'):
				self.login = True if CheckSession.checkToken(session=self.token, key='user') else False
				CheckSession.updateTokenTime(session=self.token)

			else:
				CheckSession.deleteToken(session=self.token)
				CheckSession.createToken(session=self.token, key='live')
				CheckSession.updateTokenTime(session=self.token, key='live')
				self.login = False

	def __getCheckCode(self):
		if not self.login:
			self.checkCodeImgPath, self.__checkCodeStr = getCheckCodeImgPath(self.__ip)
			get = CheckSession.checkToken(session=self.token, key='checkCode')
			if get is not None:
				CheckSession.deleteToken(session=self.token, key='checkCode')
			CheckSession.createToken(session=self.token, key='checkCode', value=self.__checkCodeStr)

	def judgeUser(self, user, pwd, checkCode):
		self.login = False
		self.errStr = ''

		self.errStr = '请输入验证码' if str(checkCode).rstrip().lstrip() == '' else ''

		self.__user = user
		self.__pwd = pwd
		self.__checkCode = checkCode.upper()

		if self.__judgeCheckCode():
			if self.__judgeUser():
				self.login = True
				self.checkCodeErr = False
				CheckSession.deleteToken(session=self.token, key='checkCode')
				CheckSession.deleteToken(session=self.token, key='user')
				CheckSession.createToken(session=self.token, key='user', value=self.__user)
		else:
			self.checkCodeErr = True
			self.errStr = '验证码错误'

	def __judgeCheckCode(self):
		sqlStr = "select `value` from session where session_id='{session}' and `key`='checkCode' "
		get = self.__mysql.sqlWork(sqlStr.format(session=self.token))
		if get is None:
			return False
		else:
			return True if get[0][0] == self.__checkCode else False

	def __judgeUser(self):
		sqlStr = "select `user` from `user` where `user`='{user}' and `pwd`='{pwd}' and valid=1 "
		get = self.__mysql.sqlWork(sqlStr.format(user=self.__user, pwd=self.__pwd))
		return False if get is None else True


class Logout:
	def __init__(self, token, ip):
		self.__token = token
		self.__ip = ip

	def __preWork(self):
		pass

	def logout(self):
		pass

