import MessionHandeler
import WebHandeler
import Comand
import os
import socket
import sys

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler

# app文件的绝对路径 app.root_path

# Web配置的IP与端口，IP采取自动获取方式
hostIp = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
hostPort = 80
hostInfo = hostIp + str(hostPort)

########################################
app = Flask(__name__)
scheduler = APScheduler()

app.secret_key = '1234567'

bootstrap = Bootstrap(app)

# 页面报错的信息 403, 404, 500
WebHandeler.Error(app=app, hostInfo=hostInfo)

# 客户端服务请求
MessionHandeler.Route(app=app, hostInfo=hostInfo)

# 网页端服务请求
WebHandeler.Route(app=app, hostInfo=hostInfo)

# 高级外链服务处理--OA
Comand.Route(app=app, hostInfo=hostInfo)


if __name__ == '__main__':
	app.run(host=hostIp, port=hostPort, debug=True, threaded=True)
