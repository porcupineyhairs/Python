from flask import Flask, request, jsonify, Response, render_template, current_app
from config import Config
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from views import *
import json


app = Flask(__name__)

# 实例化一个 Jdy 对象，用来创建、管理 RESTful Jdy
api = Api(app)

# 设置跨域
CORS(app, resources=r'/apisys/*', supports_credentials=True)

# 注册配置文件
app.config.from_object(Config)


# 收藏图标
@app.route('/favicon.ico', methods=['GET'])
def get_favicon_ico():
	return current_app.send_static_file('img/favicon.ico')


# 主页
@app.route('/', methods=['GET'])
def getWebIndex():
	return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">' \
		   '<title>主页</title></head><body><br><h3>主页</h3></body></html>'


api.add_resource(ApiJdy, '/apisys/jdy', endpoint='jdy')
api.add_resource(ApiJdy, '/apitest/jdy', endpoint='jdytest')
api.add_resource(ApiTest, '/apisys/test', endpoint='test')


if __name__ == '__main__':
	app.run(debug=app.config['DEBUG'], host=app.config['APP_HOST'], port=app.config['APP_PORT'], threaded=True)
