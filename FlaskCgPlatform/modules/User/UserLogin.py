from datetime import datetime
from modules.Sql.MsSql import *
from modules.GlobalModules import CheckSession
from modules.GlobalModules.CreateCheckCodeImg import getCheckCodeImgPath


def getCheckCodePath(token, ip):
	if CheckSession.checkToken(token=token):
		rtnDict = {'success': 'no'}
		try:
			imgPath, checkCodeStr = getCheckCodeImgPath(ip)
			if CheckSession.existLiveToken(token=token, key='checkCode') is not None:
				CheckSession.deleteToken(token=token, key='checkCode')
			CheckSession.createToken(token=token, key='checkCode', value=checkCodeStr)
			rtnDict.update({'checkCodePath': imgPath})
			rtnDict.update({'success': 'yes'})
			CheckSession.updateTokenTime(token=token)
		except Exception as e:
			rtnDict.update({'msg': '验证码获取失败', 'err': str(e)})
		finally:
			return rtnDict
	else:
		return {}


def getUserInfo(token):
	if CheckSession.checkToken(token=token):
		rtnDict = {'success': 'no'}
		try:
			rtnDict.update({'user_name': CheckSession.getTokenValue(token=token, key='user_name'),
			                'company_id': CheckSession.getTokenValue(token=token, key='company_id'),
			                'company_name': CheckSession.getTokenValue(token=token, key='company_name')})
			rtnDict.update({'success': 'yes'})
			CheckSession.updateTokenTime(token=token)
		except Exception as e:
			rtnDict.update({'msg': '获取用户信息失败', 'err': str(e)})
		finally:
			return rtnDict
	else:
		return {}


def getUserPermission(token):
	if CheckSession.checkToken(token=token):
		rtnDict = {'success': 'no'}
		try:
			rtnDict.update({'perm': '录入送货单'})
		except Exception as e:
			rtnDict.update({'msg': '获取用户权限失败', 'err': str(e)})
		finally:
			return rtnDict
	else:
		return {}


class Login:
	def __init__(self):
		self.__sql = MsSqlHelper(host='192.168.0.198', user='sa', passwd='COMfort123456', database='CgPlatform')

	def login(self, user, pwd, checkCode, token):
		rtnDict = {'success': 'no'}
		if checkCode.upper() == CheckSession.getTokenValue(token=token, key='checkCode'):
			sqlStr = "select user_id, pwd, user_name, company_id, company_name, valid from user_info where user_id = '{}'"
			get = self.__sql.sqlWork(sqlStr=sqlStr.format(user))
			if get is not None:
				if int(get[0][5]) == 1:
					if get[0][1] == pwd:
						rtnDict.update({'success': 'yes'})
						CheckSession.deleteToken(token=token, key='checkCode')
						CheckSession.createToken(token=token, key='user', value=get[0][0])
						CheckSession.createToken(token=token, key='user_name', value=get[0][2])
						CheckSession.createToken(token=token, key='company_id', value=get[0][3])
						CheckSession.createToken(token=token, key='company_name', value=get[0][4])
					else:
						rtnDict.update({'msg': '账户或密码错误'})
				else:
					rtnDict.update({'msg': '该用户已禁止登录'})
			else:
				rtnDict.update({'msg': '账户不存在'})
		else:
			rtnDict.update({'msg': '验证码错误'})
		return rtnDict
