from flask import current_app, Blueprint, redirect, render_template, \
	request, flash, session, url_for
from datetime import timedelta


urlUser = Blueprint('user', __name__)


@urlUser.route('/', methods=['GET', 'POST'])
def userIndexRedirect():
	return redirect('/user/login')


@urlUser.route('/download/<path:url>')
def userDownload(url):
	url2 = url.replace('/', '-')
	return redirect('/download/{}'.format(url2))


@urlUser.route('/redirect/<path:url>')
def userRedirect(url):
	return redirect(url)


@urlUser.route('/login/', methods=['GET', 'POST'])
def userLogin():
	session.permanent = True
	current_app.permanent_session_lifetime = timedelta(minutes=30)
	if request.method == 'POST':
		user = request.form.get('user')
		pwd = request.form.get('pwd')
		if all([user, pwd]):
			if user == '333':
				# 如果用户存在，判断密码是否正确
				if pwd == '222':
					# 登录成功后，session['admin_id']存入数据，
					# 其他页面用来判断用户到登录状态
					session['admin_id'] = user
					flash('登陆成功')
			# 		# 登录成功后跳转到首页，对图书进行管理
					return session.get('admin_id')
				else:
					flash('密码错误')
			else:
				flash('用户名不存在')
		else:
			flash('用户名、密码不完整')
		return render_template('urlUser/login.html')

	else:
		if session.get('admin_id') is not None:
			return session.get('admin_id')
		else:
			return render_template('urlUser/login.html')
