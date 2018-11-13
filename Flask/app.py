import Module
import MessionHandeler
import WebHandeler
import os


from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(__name__)

app.secret_key = '1234567'

bootstrap = Bootstrap(app)


# 页面报错的信息 403, 404, 500
WebHandeler.Error.error(app=app)

# 客户端服务请求
MessionHandeler.Route.Route(app=app)

# 网页端服务请求
WebHandeler.Route.Route(app=app)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8099, debug=True, threaded=True, )
