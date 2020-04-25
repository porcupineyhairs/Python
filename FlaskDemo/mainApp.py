
from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from config import Config
from views import urlRoot, urlClient, urlTest, urlDownload, urlReport, urlMain, urlUser, urlApi


app = Flask(__name__)

# Admin 管理页面
# admin = Admin(app, name='管理后台', template_mode='bootstrap3')

# app.config['SERVER_NAME'] ='192.168.1.60:8900'

Bootstrap(app)

# 注册配置文件
app.config.from_object(Config)

app.secret_key = 'XMVMDULVDCU555SQAA780KX7J7C9X4AYharvey'

# 注册其他网页url
app.register_blueprint(urlRoot, url_prefix='/')
app.register_blueprint(urlApi, url_prefix='/api')
app.register_blueprint(urlTest, url_prefix='/test')
app.register_blueprint(urlClient, url_prefix='/Client')
app.register_blueprint(urlMain, url_prefix='/main')
app.register_blueprint(urlDownload, url_prefix='/download')
app.register_blueprint(urlReport, url_prefix='/report')
app.register_blueprint(urlUser, url_prefix='/user')


if __name__ == '__main__':
	app.run(debug=app.config['DEBUG'], host=app.config['APP_HOST'], port=app.config['APP_PORT'], threaded=True)
