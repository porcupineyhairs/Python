from flask import Flask, request
import requests

# app文件的绝对路径 app.root_path

hostIp = '0.0.0.0'
hostPort = 60000
app = Flask(__name__)


# 主页
@app.route('/', methods=['POST'])
def printer():
	data = request.get_data(as_text=True)
	print(data)
	data2 = data.split('"')[3]

	url = 'http://192.168.0.247:60002'
	response = requests.post(url=url, data=data2.encode('utf-8'), timeout=20)
	print(response.text)
	return 'ok'


if __name__ == '__main__':
	app.run(host=hostIp, port=hostPort, debug=False)
