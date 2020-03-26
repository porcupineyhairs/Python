from flask import current_app, Blueprint, redirect, render_template, \
	request, flash, session, url_for


urlMain = Blueprint('main', __name__)


@urlMain.route('/', methods=['GET', 'POST'])
def mainIndexRedirect():
	return redirect('/main/index')


@urlMain.route('/index/', methods=['GET', 'POST'])
def mainIndex():
	return render_template('urlMain/index.html')


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


@urlMain.route('/index/download/<path:url>')
def mainDownload(url):
	url2 = url.replace('/', '-')
	return redirect('/download/{}'.format(url2))


@urlMain.route('/index/redirect/<path:url>')
def mainRedirect(url):
	return redirect('/' + url)
