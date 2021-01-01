from flask import Flask, make_response, send_from_directory, redirect, request
import os

# app文件的绝对路径 app.root_path

hostIp = '0.0.0.0'
hostPort = 8099
hostInfo = hostIp + str(hostPort)
app = Flask(__name__)


# 下载文件，外挂程序的更新下载
@app.route("/Client/WG/Download/<filename>", methods=['GET'])
def DownloadFile1(filename):
	directory = app.root_path + '/WgFile/'  # 文件目录
	# 判断所需文件是否存在
	if os.path.exists(directory + filename):
		response = make_response(send_from_directory(directory, filename, as_attachment=True, conditional=False))
		response.headers["Content-Disposition"] = "attachment; filename={}".\
			format(filename.encode().decode('latin-1'))
		return response
	else:
		return 'Error'
        

# 下载文件，外挂程序的更新下载
@app.route("/download/<filename>", methods=['GET'])
def DownloadFile2(filename):
	directory = app.root_path + '/WgFile/'  # 文件目录
	# 判断所需文件是否存在
	if os.path.exists(directory + filename):
		response = make_response(send_from_directory(directory, filename, as_attachment=True, conditional=False))
		response.headers["Content-Disposition"] = "attachment; filename={}".\
			format(filename.encode().decode('latin-1'))
		return response
	else:
		return 'Error'


# 下载文件
@app.route("/downloadFile/<filename>", methods=['GET'])
def DownloadFile3(filename):
	directory = app.root_path + '/DownLoadFile/'  # 文件目录
	# 判断所需文件是否存在
	if os.path.exists(directory + filename):
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".\
			format(filename.encode().decode('latin-1'))
		return response
	else:
		return 'Error'


# 主页重定向
@app.route('/', methods=['GET'])
def root():
	return redirect('/list')


@app.route('/list', methods=['GET'])
def fileList():
	html = '<title>文件列表</title><h1>可下载文件</h1><h3>{0}</h3>'
	htmltmp = '<a href="/downloadFile/{0}">{0}</a><br>'
	ll = ''
	file = open(app.root_path + '/DownLoadFile/DownLoadList.txt', mode='r', encoding='GBK')
	lists = file.readlines()

	for tmp in lists:
		if len(tmp) > 2:
			if tmp[0:2] == '--':
				pass
			else:
				ll += htmltmp.format(tmp)
		else:
			pass
	return html.format(ll)


if __name__ == '__main__':
	app.run(host=hostIp, port=hostPort, debug=False)
