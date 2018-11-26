from flask import request, Response, make_response, send_from_directory, send_file
from Module import *
import os
import json
import threading
import _thread


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
		__get = request.get_json(force=True)
		print(__get)
		getVersion = GetVersion()
		__back = getVersion.Main(__get)
		print(__back)
		return Response(json.dumps(__back))

	@app.route('/Client/UserLogin', methods=['POST'])
	def UserLogin_C():
		__Usermanage = UserManege()
		__get = request.get_json(force=True)
		print(__get)
		__back = __Usermanage.UserLogin(__get)
		print(__back)
		return Response(json.dumps(__back))

	@app.route('/Client/MaDuo/GetInfo', methods=['POST'])
	def MD_GetInfo_C():
		__get = request.get_json(force=True)
		print(__get)
		from Module.MaDuoSystem.MD_GetInfo import GetInfo
		if __get['Mode'] == 'Insert':
			__getInfo = GetInfo()
			__getInfo.MainWork()

		return Response(json.dumps({'Mode': 'OK'}))
	
	@app.route("/Client/WG/Download/<filename>", methods=['GET'])
	def WG_DownloadFile(filename):
		directory = os.getcwd() + '/File/WG/'  # 假设在当前目录
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
		return response
