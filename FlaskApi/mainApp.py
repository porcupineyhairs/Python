import sys
import logging
import json
from flask import Flask, request, Response
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from config import Config
from views import urlRoot, urlApi


app = Flask(__name__)
# app.config['SERVER_NAME'] ='harveykkk.com'

Bootstrap(app)

# 注册配置文件
app.config.from_object(Config)

# Logger
# 日志系统配置
handler = logging.FileHandler(app.config['LOG_FILE_PATH'], encoding='UTF-8')
# 设置日志文件，和字符编码
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

# 注册其他网页url
app.register_blueprint(urlRoot, url_prefix='/')
app.register_blueprint(urlApi, url_prefix='/api')


if __name__ == '__main__':
	app.run(debug=app.config['DEBUG'], host=app.config['APP_HOST'], port=app.config['APP_PORT'], threaded=True,
	        ssl_context=('ssl/server.crt', 'ssl/server.key'))
