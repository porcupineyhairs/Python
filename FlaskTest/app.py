from flask import Flask
from flask_bootstrap import Bootstrap
from Config import *

# app文件的绝对路径 app.root_path

# hostIp = '192.168.31.29'
hostIp = '192.168.1.60'
hostPort = 8099
hostInfo = hostIp + str(hostPort)

jobBom = False

########################################
app = Flask(__name__)

app.secret_key = '1234567'

bootstrap = Bootstrap(app)

SetRoute(app=app, hostInfo=hostInfo)

if __name__ == '__main__':
	app.run(host=hostIp, port=hostPort, debug=True, threaded=False)
