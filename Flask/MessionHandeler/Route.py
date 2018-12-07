from flask import request, Response, make_response, send_from_directory, send_file
from Module import *
import os
import json
import threading


def Route(app):
	@app.route('/Client/Test', methods=['POST'])
	def Client_C():
		k = {'name': 'me', 'password': 'you'}
		j = request.get_json(force=True)
		return Response(json.dumps(k))

	@app.route('/Client/LinkTest', methods=['POST', 'GET'])
	def LinkTest_C():
		__get = request.get_json(force=True)
		return Response(json.dumps({'Return': 'Yes'}))
	
	@app.route('/Client/GetVersion', methods=['POST'])
	def GetVersion_C():
		getVersion = GetVersion()
		log = Logger('Log/Connect.log', level='info')
		__get = request.get_json(force=True)
		__back = getVersion.Main(__get)
		log.logger.info(request.url + ' - ' + request.remote_addr + ' - ' + 'get:' + str(__get))
		log.logger.info(request.url + ' - ' + request.remote_addr + ' - ' + 'back:' + str(__back))
		return Response(json.dumps(__back))

	@app.route('/Client/UserLogin', methods=['POST'])
	def UserLogin_C():
		__Usermanage = UserManege()
		log = Logger('Log/Login.log', level='info')
		__get = request.get_json(force=True)
		__back = __Usermanage.UserLogin(__get)
		log.logger.info(request.url + ' - ' + request.remote_addr + ' - ' + 'get:' + str(__get))
		log.logger.info(request.url + ' - ' + request.remote_addr + ' - ' + 'back:' + str(__back))
		return Response(json.dumps(__back))

	@app.route('/Client/MaDuo/GetInfo', methods=['POST'])
	def MD_GetInfo_C():
		log = Logger('Log/MaDuoInfo.log', level='info')
		__get = request.get_json(force=True)
		log.logger.info(request.url + ' - ' + request.remote_addr + ' - ' + 'get:' + str(__get))
		from Module.MaDuoSystem.MD_GetInfo import GetInfo
		if __get['Mode'] == 'Insert':
			__getInfo = GetInfo()
			t = threading.Thread(target=__getInfo.MainWork)
			t.start()
		return Response(json.dumps({'Mode': 'OK'}))
	
	@app.route("/Client/WG/Download/<filename>", methods=['GET'])
	def WG_DownloadFile(filename):
		log = Logger('Log/Download.log', level='info')
		log.logger.info(request.url + ' - ' + request.remote_addr + ' - ' + filename.encode().decode('latin-1'))
		directory = os.getcwd() + '/File/WG/'  # 文件目录
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
		return response
