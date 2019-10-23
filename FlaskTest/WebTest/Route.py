from flask import redirect, render_template, send_from_directory, request
import os
import WebHandeler.gongshi as Gongshi


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
		
		@app.route('/ip')
		def conn_ip():
			return '<title>获取IP地址</title>' + '<h1>您的IP地址为：' + request.remote_addr + '</h1>'
		
		@app.route('/test')
		def GongShi():
			kk = Gongshi.test()
			return '<title>税务收集工单工时</title>' + '<h1>您的IP地址为：' + str(kk) + '</h1>'
