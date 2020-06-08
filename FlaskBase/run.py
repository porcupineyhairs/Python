from flask import Flask, make_response, send_from_directory, redirect, request
import os

# app文件的绝对路径 app.root_path

hostIp = '0.0.0.0'
hostPort = 8099
hostInfo = hostIp + str(hostPort)
app = Flask(__name__)


# 下载文件，联友生产辅助工具的更新下载
@app.route("/Client/WG/Download/<filename>", methods=['GET'])
def WG_DownloadFile1(filename):
	directory = app.root_path + '/File/'  # 文件目录
	# 判断所需文件是否存在
	if os.path.exists(directory + filename):
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".\
			format(filename.encode().decode('latin-1'))
		return response
	else:
		return 'Error'
        

# 下载文件，联友生产辅助工具的更新下载
@app.route("/download/<filename>", methods=['GET'])
def WG_DownloadFile2(filename):
	directory = app.root_path + '/File/'  # 文件目录
	# 判断所需文件是否存在
	if os.path.exists(directory + filename):
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".\
			format(filename.encode().decode('latin-1'))
		return response
	else:
		return 'Error'


# 主页重指向
@app.route('/', methods=['GET', 'POST'])
def root():
	return redirect('/ip')


@app.route('/ip')
def conn_ip():
	return '<title>获取IP地址</title><h1>IP地址：' + request.remote_addr + '</h1>'


if __name__ == '__main__':
	app.run(host=hostIp, port=hostPort, debug=False)
