from flask import Flask
from config import Config
from views import urlRoot, urlDownload, urlMain, urlUser, urlApi, urlCg
import logging


app = Flask(__name__)

# 注册配置文件
app.config.from_object(Config)

# Logger
# 日志系统配置
handler = logging.FileHandler(app.config['LOG_FILE_PATH'], encoding='UTF-8')
# 设置日志文件，和字符编码
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

app.secret_key = 'XMVMDULVDCU555SQAA780KX7J7C9X4AYharvey'

# 注册其他网页url
app.register_blueprint(urlRoot, url_prefix='/')
app.register_blueprint(urlApi, url_prefix='/api')
app.register_blueprint(urlMain, url_prefix='/main')
app.register_blueprint(urlDownload, url_prefix='/download')
app.register_blueprint(urlUser, url_prefix='/user')
app.register_blueprint(urlCg, url_prefix='/cg')


if __name__ == '__main__':
	app.run(debug=app.config['DEBUG'], host=app.config['APP_HOST'], port=app.config['APP_PORT'], threaded=True)
