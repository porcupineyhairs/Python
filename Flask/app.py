import MessionHandeler
import WebHandeler
import Comand
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

app.secret_key = '1234567'

bootstrap = Bootstrap(app)

# 页面报错的信息 403, 404, 500
WebHandeler.Error(app=app)

# 客户端服务请求
MessionHandeler.Route(app=app)

# 网页端服务请求
WebHandeler.Route(app=app)

# 高级外链服务处理--OA
Comand.Route(app=app)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
