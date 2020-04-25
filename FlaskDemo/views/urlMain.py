from flask import current_app, Blueprint, redirect, render_template, \
	request, flash, session, url_for, jsonify
from modules.GlobalModules import CheckSession
from modules.User.UserLogin import getUserByToken
from random import choice


urlMain = Blueprint('main', __name__)


@urlMain.route('/', methods=['GET', 'POST'])
def mainIndexRedirect():
	return redirect('/main/index')


@urlMain.route('/index', methods=['GET', 'POST'])
def mainIndex():
	token = session.get('token')
	user = getUserByToken(token)
	return render_template('urlMain/index.html', imgFile='/static/img/error/head404.png', user=user, barcodeText='345000000')


@urlMain.route('/jsondata', methods=['GET', 'POST'])
def infos():
	print(request.remote_addr)
	"""
	 请求的数据源，该函数模拟数据库中存储的数据，返回以下这种数据的列表：
	{'name': '香蕉', 'id': 1, 'price': '10'}
	{'name': '苹果', 'id': 2, 'price': '10'}
	"""
	data = []
	names = ['香', '草', '瓜', '果', '桃', '梨', '莓', '橘', '蕉', '苹']
	for i in range(1, 20):
		d = {}
		d['id'] = i
		d['name'] = choice(names) + choice(names)  # 随机选取汉字并拼接
		d['price'] = '10'
		data.append(d)
	if request.method == 'POST':
		print('post')
	if request.method == 'GET':
		info = request.values
		limit = info.get('limit', 50)  # 每页显示的条数
		offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
		# print('get', limit)
		# print('get  offset', offset)
		return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
		# 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
		# 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了


@urlMain.route('/t2', methods=['GET', 'POST'])
def t2():
	# print(request.data)
	return render_template('urlMain/bootstrap.html')


@urlMain.route('/uploaddata', methods=['POST'])
def uploadData():
	print('upload')
	print(request.get_json(force=True))
	return jsonify({"success": "yes"})


@urlMain.route('/live', methods=['GET'])
def mainKeepLive():
	token = session.get('token')
	CheckSession.updateTokenTime(session=token)
	return ''


@urlMain.route('/index/download/<path:url>')
def mainDownload(url):
	url2 = url.replace('/', '-')
	return redirect('/download/{}'.format(url2))

