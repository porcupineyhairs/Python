from flask import request, Response, make_response, send_from_directory, send_file
from Module import *
import os
import json
import threading


def Route(app):
	@app.route('/Client/Test', methods=['POST', 'GET'])
	def Client_C():
		__log = Logger('Test.log', level='info')
		__log.logger.info(request.url + '-' + request.method + ' - ' + request.remote_addr)
		if request.method == 'POST':
			k = {'name': 'me', 'password': 'you'}
			j = request.get_json(force=True)
			return Response(json.dumps(k))
		elif request.method == 'GET':
			k = {'name': 'me', 'password': 'you'}
			return Response(json.dumps(k))

	@app.route('/Client/LinkTest', methods=['POST', 'GET'])
	def LinkTest_C():
		__get = request.get_json(force=True)
		return Response(json.dumps({'Return': 'Yes'}))

	@app.route('/Client/GetTime', methods=['POST'])
	def GetTime_C():
		__getTime = GetSvrTime()
		__get = request.get_json(force=True)
		__back = __getTime.GetTime(__get)
		return Response(json.dumps(__back))
	
	@app.route('/Client/GetVersion', methods=['POST'])
	def GetVersion_C():
		__getVersion = GetVersion()
		__log = Logger('Log/Connect/Connect.log', level='info')
		__get = request.get_json(force=True)
		__back = __getVersion.Main(__get)
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back))
		return Response(json.dumps(__back))

	@app.route('/Client/UserLogin', methods=['POST'])
	def UserLogin_C():
		__userManage = UserManege()
		__log = Logger('Log/Login/Login.log', level='info')
		__get = request.get_json(force=True)
		__back = __userManage.UserLogin(__get)
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back))
		return Response(json.dumps(__back))

	@app.route('/Client/MaDuo/GetInfo', methods=['POST'])
	def MD_GetInfo_C():
		__log = Logger('Log/Maduo/MaDuoInfo.log', level='info')
		__get = request.get_json(force=True)
		__back = {'Return': 'OK'}
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back))
		from Module.MaDuoSystem.MD_GetInfo import GetInfo
		if __get['Mode'] == 'Insert':
			__getInfo = GetInfo()
			t = threading.Thread(target=__getInfo.MainWork)
			t.start()
		return Response(json.dumps(__back))

	@app.route('/Client/PDA/LL_LYXA', methods=['POST'])
	def LL_LYXA_C():
		__log = Logger('Log/PDA/PDA_LL.log', level='info')
		__get = request.get_json(force=True)
		__back = {'Return': 'OK'}
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back))
		return Response(json.dumps(__back))

	@app.route('/Client/PDA/JH_LYXA', methods=['POST'])
	def JH_LYXA_C():
		__log = Logger('Log/PDA/PDA_JH.log', level='info')
		__get = request.get_json(force=True)
		__back = {'Return': 'OK'}
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back))
		return Response(json.dumps(__back))
	
	@app.route("/Client/WG/Download/<filename>", methods=['GET'])
	def WG_DownloadFile(filename):
		__log = Logger('Log/Download/Download.log', level='info')
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' +
						  filename.encode().decode('latin-1'))
		directory = os.getcwd() + '/File/WG/'  # 文件目录
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
		return response
