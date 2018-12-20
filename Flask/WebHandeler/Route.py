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
		return redirect('/ip')
		# return '<h1> Yes </h1>'

	@app.route('/workhour')
	def workhour():
		return render_template('testform.html')

	@app.route('/ip')
	def conn_ip():
		return ('<title>获取IP地址</title>' +
		        '<h1>您的IP地址为：' + request.remote_addr + '</h1>')
	
	@app.route('/PDA')
	def PDA():
		return ('<title>PDA</title>' +
		        '<h1>PDA_URL</h1>'
		        '<br/>'
		        '<h2>内容待添加</h2>')
