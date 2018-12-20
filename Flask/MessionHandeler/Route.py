from flask import request, Response, make_response, send_from_directory, send_file
from Module import *
import os
import json
import threading


def Route(app):
	# webservice功能测试
	@app.route('/Client/Test', methods=['POST', 'GET'])
	def Client_C():
		__log = Logger('Test.log', level='info')
		__log.logger.info(request.url + '-' + request.method + ' - ' + request.remote_addr + '\n')
		if request.method == 'POST':
			k = {'name': 'me', 'password': 'you'}
			j = request.get_json(force=True)
			return Response(json.dumps(k))
		elif request.method == 'GET':
			k = {'name': 'me', 'password': 'you'}
			return Response(json.dumps(k))

	# 连接测试，是否能连接成功，测试webservice是否正常
	@app.route('/Client/LinkTest', methods=['POST', 'GET'])
	def LinkTest_C():
		__get = request.get_json(force=True)
		return Response(json.dumps({'Return': 'Yes'}))

	# 获取198数据库服务器的时间
	@app.route('/Client/GetTime', methods=['POST'])
	def GetTime_C():
		__getTime = GetSvrTime()
		__get = request.get_json(force=True)
		__back = __getTime.GetTime(__get)
		return Response(json.dumps(__back))

	# 外挂程序版本验证，是否返回更新链接
	@app.route('/Client/GetVersion', methods=['POST'])
	def GetVersion_C():
		__getVersion = GetVersion()
		__log = Logger('Log/Connect/Connect.log', level='info')
		__get = request.get_json(force=True)
		__back = __getVersion.Main(__get)
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back) + '\n')
		return Response(json.dumps(__back))

	# 登录认证
	@app.route('/Client/UserLogin', methods=['POST'])
	def UserLogin_C():
		__userManage = UserManege()
		__log = Logger('Log/Login/Login.log', level='info')
		__get = request.get_json(force=True)
		__back = __userManage.UserLogin(__get)
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back) + '\n')
		return Response(json.dumps(__back))

	# 码垛系统订单基本信息获取
	@app.route('/Client/MaDuo/GetInfo', methods=['POST'])
	def MD_GetInfo_C():
		__log = Logger('Log/MaDuo/MaDuoInfo.log', level='info')
		__get = request.get_json(force=True)
		__back = {'Return': 'OK'}
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back) + '\n')
		from Module.MaDuoSystem.MD_GetInfo import GetInfo
		if __get['Mode'] == 'Insert':
			__getInfo = GetInfo()
			t = threading.Thread(target=__getInfo.MainWork)
			t.start()
		return Response(json.dumps(__back))

	# PDA扫描领料单
	@app.route('/Client/PDA/LL_LYXA', methods=['POST'])
	def LL_LYXA_C():
		__log = Logger('Log/PDA/PDA_LL.log', level='info')
		__get = request.get_json(force=True)
		# __pda_LL = PDA_LL()
		# __back = __pda_LL.MianWork(__get)
		__back = {'Return': 'OK'}
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back) + '\n')
		return Response(json.dumps(__back))

	# PDA扫描进货单
	@app.route('/Client/PDA/JH_LYXA', methods=['POST'])
	def JH_LYXA_C():
		__log = Logger('Log/PDA/PDA_JH.log', level='info')
		__get = request.get_json(force=True)
		__pda_JH = PDA_JH()
		__back = __pda_JH.MianWork(__get)
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - '
						  + 'get:' + str(__get) + ' - ' + 'back:' + str(__back) + '\n')
		return Response(json.dumps(__back))

	# 下载文件，联友生产辅助工具的更新下载
	@app.route("/Client/WG/Download/<filename>", methods=['GET'])
	def WG_DownloadFile(filename):
		__log = Logger('Log/Download/Download.log', level='info')
		__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + '\n')
		directory = os.getcwd() + '/File/WG/'  # 文件目录
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
		return response
