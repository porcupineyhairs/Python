from flask import current_app, Blueprint, redirect, render_template, request, flash, session, jsonify
from datetime import timedelta
from modules.User.UserLogin import *
from modules.GlobalModules.CheckSession import *
from modules.Log.flaskLog import *


urlUser = Blueprint('user', __name__)


# api部分
# 用户登出
@urlUser.route('/api/logout', methods=['GET', 'POST'])
def userApiLogout():
	CheckSession.deleteToken(token=session.get('token'))
	rtnDict = {'success': 'yes', 'url': '/user/login'}
	flaskLog(mode='info', request=request, rtnDict=rtnDict)
	return jsonify(rtnDict)


# 用户登录
@urlUser.route('/api/login', methods=['POST'])
def userApiLogin():
	token = session.get('token')
	if CheckSession.checkToken(token=token):
		inDict = request.get_json(force=True)
		login = Login()
		rtnDict = login.login(user=inDict['user'], pwd=inDict['pwd'], checkCode=inDict['checkCode'], token=token)
		_ = rtnDict.update({'url': '/main'}) if rtnDict['success'] == 'yes' else None
		flaskLog(mode='info', request=request, rtnDict=rtnDict)
		return jsonify(rtnDict)
	else:
		return ''


# 生成验证码，并且返回验证码图片的目录
@urlUser.route('/api/checkcode', methods=['GET', 'POST'])
def userApiVerifyCode():
	rtnDict = getCheckCodePath(session.get('token'), request.remote_addr)
	flaskLog(mode='info', request=request, rtnDict=rtnDict)
	_ = rtnDict.pop('err') if 'err' in rtnDict.keys() else None
	return jsonify(rtnDict)


# 用户登录后，获取用户信息
@urlUser.route('/api/userinfo', methods=['GET', 'POST'])
def userApiInfo():
	rtnDict = getUserInfo(token=session.get('token'))
	flaskLog(mode='info', request=request, rtnDict=rtnDict)
	_ = rtnDict.pop('err') if 'err' in rtnDict.keys() else None
	return jsonify(rtnDict)


# 获取用户的权限
@urlUser.route('/api/userpermission', methods=['GET', 'POST'])
def userPermission():
	rtnDict = getUserPermission(token=session.get('token'))
	flaskLog(mode='info', request=request, rtnDict=rtnDict)
	return jsonify(rtnDict)


# html部分
@urlUser.route('/login/', methods=['GET', 'POST'])
def userLogin():
	session.permanent = True
	# 设置session过期时间
	current_app.permanent_session_lifetime = timedelta(days=1)

	token = session.get('token')

	if CheckSession.checkToken(token):
		if CheckSession.existLiveToken(token=token, key='user'):
			return redirect('/main')
		else:
			return render_template('urlUser/login.html')
	else:
		_ = session.pop('token') if token is not None else None
		newToken = CheckSession.createToken(key='live')
		session['token'] = newToken
		return render_template('urlUser/login.html')
