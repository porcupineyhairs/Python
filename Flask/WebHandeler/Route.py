from flask import redirect, render_template, send_from_directory, request
import os
import Module


def Route(app):
	# 收藏图标
	@app.route('/favicon.ico')
	def favicon():
		return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico')

	# 主页重指向
	@app.route('/', methods=['GET', 'POST'])
	def root():
		# return redirect('/workhour')
		return '<h1> Yes </h1>'

	@app.route('/workhour')
	def workhour():
		return render_template('testform.html')

	@app.route('/ip')
	def conn_ip():
		return '您的IP地址为：' + request.remote_addr
