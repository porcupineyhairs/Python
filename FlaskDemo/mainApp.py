import os
from flask import Flask, send_from_directory, current_app, redirect
from flask_bootstrap import Bootstrap
from config import Config
from router import urls_1


app = Flask(__name__)
Bootstrap(app)
# 注册配置文件
app.config.from_object(Config)

# 注册其他网页url
app.register_blueprint(urls_1, url_prefix='/u1')


# 收藏图标
@app.route('/favicon.ico')
def get_favicon_ico():
	return app.send_static_file('img/favicon.ico')


@app.route('/', methods=['GET'])
def hello_world():
	return 'Hello World!2'


if __name__ == '__main__':
	app.run(debug=True, host=app.config['APP_HOST'], port=app.config['APP_PORT'])
