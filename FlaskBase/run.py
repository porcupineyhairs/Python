from flask import Flask
from modules import *
from urls.web import web_blueprint
from urls.others import other_blueprint

# app文件的绝对路径 app.root_path

hostIp = '0.0.0.0'
hostPort = 8099
app = Flask(__name__)

app.register_blueprint(other_blueprint, url_prefix='/flask')
app.register_blueprint(web_blueprint, url_prefix='/flask/web')


if __name__ == '__main__':
	print('Status:', timeCompare())
	app.run(host=hostIp, port=hostPort, debug=False, threaded=True)
