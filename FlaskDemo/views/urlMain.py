from flask import current_app, Blueprint, redirect, render_template, \
	request, flash, session, url_for
from modules.GlobalModules import CheckSession
from modules.User.Login import getUserByToken


urlMain = Blueprint('main', __name__)


@urlMain.route('/', methods=['GET', 'POST'])
def mainIndexRedirect():
	return redirect('/main/index')


@urlMain.route('/index/', methods=['GET', 'POST'])
def mainIndex():
	token = session.get('token')
	user = getUserByToken(token)
	return render_template('urlMain/index.html', imgFile='/static/img/error/head404.png', user=user)


@urlMain.route('/table/', methods=['GET', 'POST'])
def mainTable():
	if request.method == 'GET':
		labels = ['品号', '品名', '规格', '应送数量', '日期', '可送数量']
		content = [['ph001', 'pm001', 'gg001', 10, '2020-01-01', ''],
		           ['ph002', 'pm002', 'gg002', 11, '2020-01-01', ''],
		           ['ph003', 'pm003', 'gg003', 12, '2020-01-01', ''],
		           ['ph004', 'pm004', 'gg004', 13, '2020-01-01', ''],
		           ['ph005', 'pm005', 'gg005', 14, '2020-01-01', '']]
		return render_template('urlMain/table.html', labels=labels, content=content)
	else:
		pass


@urlMain.route('/live/', methods=['GET'])
def mainKeepLive():
	token = session.get('token')
	CheckSession.updateTokenTime(session=token)
	return ''


@urlMain.route('/index/download/<path:url>')
def mainDownload(url):
	url2 = url.replace('/', '-')
	return redirect('/download/{}'.format(url2))

