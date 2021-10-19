from flask import Flask, make_response, send_from_directory, redirect
import datetime
import urllib.request
import os
import json

# app文件的绝对路径 app.root_path

hostIp = '0.0.0.0'
hostPort = 8099
hostInfo = hostIp + str(hostPort)
app = Flask(__name__)


# 下载文件，外挂程序的更新下载
@app.route("/local/file/download/WgFile/<filename>", methods=['GET'])
def DownloadFile2(filename):
	if timeCompare():
		directory = app.root_path + '/WgFile/'  # 文件目录
		# 判断所需文件是否存在
		if os.path.exists(directory + filename):
			response = make_response(send_from_directory(directory, filename, as_attachment=True, conditional=True))
			response.headers["Content-Disposition"] = "attachment; filename={}".\
				format(filename.encode().decode('latin-1'))
			return response
		else:
			return r"Doesn't exist file! "
	else:
		return None


# 下载文件
@app.route("/local/file/download/downloadFile/<filename>", methods=['GET'])
def DownloadFile3(filename):
	if timeCompare():
		directory = app.root_path + '/DownLoadFile/'  # 文件目录
		# 判断所需文件是否存在
		if os.path.exists(directory + filename):
			response = make_response(send_from_directory(directory, filename, as_attachment=True, conditional=True))
			response.headers["Content-Disposition"] = "attachment; filename={}".\
				format(filename.encode().decode('latin-1'))
			return response
		else:
			return r"Doesn't exist file! "
	else:
		return None


# 主页重定向
@app.route('/', methods=['GET'])
@app.route('/local/file', methods=['GET'])
@app.route('/local/file/download', methods=['GET'])
def root():
	return redirect('/local/file/download/index')


# 文件下载索引页面
@app.route('/local/file/download/index', methods=['GET'])
def fileDownload():
	html = '<title>文件列表</title><h1>可下载文件</h1><br><br><h3>{0}</h3>'
	htmltmp = '<a href="/local/file/download/downloadFile/{0}">{0}</a><br>'
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


def getNetworkTime():
	intime = str(urllib.request.urlopen("http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp").read().decode())
	one = intime[:intime.rfind('"')]
	times = datetime.datetime.fromtimestamp(int(one[one.rfind('"')+1:-3]))
	return times


def timeCompare():
	netWorkTime = getNetworkTime()
	localTime = datetime.datetime.now()
	stopTime = datetime.datetime.strptime('2022-05-31', '%Y-%m-%d').date()
	return True if netWorkTime.date() < stopTime and localTime.date() < stopTime else False


if __name__ == '__main__':
	print('Status:', timeCompare())
	app.run(host=hostIp, port=hostPort, debug=False)
