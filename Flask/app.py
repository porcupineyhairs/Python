from flask import Flask
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler
from Config import *

# app文件的绝对路径 app.root_path

# hostIp = '192.168.31.29'
hostIp = '192.168.1.60'
hostPort = 8099
hostInfo = hostIp + str(hostPort)

jobBom = False
	

########################################
app = Flask(__name__)
# scheduler = APScheduler()

app.secret_key = '1234567'

# app.config.from_object(ApScheduleConfig())
#
# scheduler.init_app(app)
# scheduler.start()

bootstrap = Bootstrap(app)

SetRoute(app=app, hostInfo=hostInfo)


if __name__ == '__main__':
	app.run(host=hostIp, port=hostPort, debug=False, threaded=False)
