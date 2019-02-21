from flask import redirect, render_template, send_from_directory, request
import os
import Module


def Route(app=None, hostInfo=None):
	if app is None:
		pass
	else:
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
		
		# @app.route('/gongshi/201811')
		# def gs201811():
		# 	from WebHandeler import gongshi
		# 	get = gongshi.gongshi('201811')
		# 	return ('<title>收集工单工时</title>' +
		# 	        '<h1>201811工单工时已收集</h1>'
		# 	        '<br/>'
		# 	        '<h2>其他内容待添加</h2>')
		
		# @app.route('/gongshi/201812')
		# def gs201812():
		# 	from WebHandeler import gongshi
		# 	get = gongshi.gongshi('201812')
		# 	return ('<title>收集工单工时</title>' +
		# 	        '<h1>201812工单工时已收集</h1>'
		# 	        '<br/>'
		# 	        '<h2>其他内容待添加</h2>')
