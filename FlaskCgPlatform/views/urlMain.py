from flask import current_app, Blueprint, redirect, render_template, \
	request, flash, session, url_for, jsonify
from modules.GlobalModules import *
from modules.User.UserLogin import *
from random import choice


urlMain = Blueprint('main', __name__)


@urlMain.route('', methods=['GET', 'POST'])
def mainIndexRedirect():
	return redirect('/main/index')


@urlMain.route('/index', methods=['GET', 'POST'])
def mainIndex():
	token = session.get('token')
	if not all([CheckSession.getTokenValue(token=token, key='user')]):
		return redirect('/user/login')
	else:
		return render_template('urlMain/index.html')


# 心跳url
@urlMain.route('/keepAlive', methods=['GET'])
def mainKeepLive():
	CheckSession.cleanToken()
	token = session.get('token')
	if CheckSession.checkToken(token=token):
		CheckSession.updateTokenTime(token=token)
	return ''
