from flask import request, Response, make_response, send_from_directory, send_file, render_template
from Module import *
import os
import sys
import json
import threading


def Route(app=None, hostInfo=None):
	if app is None:
		pass
	else:
		__encryptDict = EncryptDict()
		
		# webservice功能测试
		@app.route('/Client/Test', methods=['POST', 'GET'])
		def Client_C():
			if request.method == 'POST':
				__back = {'name': 'me', 'password': 'you'}
				__get = request.get_json(force=True)
				return Response(json.dumps(__back))
			elif request.method == 'GET':
				return render_template('json table.html')
	
		# 连接测试，是否能连接成功，测试webservice是否正常
		@app.route('/Client/LinkTest', methods=['POST'])
		def LinkTest_C():
			__get = __encryptDict.Decrypt(request.data.decode())
			__backDict = {'Return': 'Yes'}
			__back = __encryptDict.Encrypt(__backDict)
			return Response(__back)
	
		# 获取198数据库服务器的时间
		@app.route('/Client/GetTime', methods=['POST'])
		def GetTime_C():
			__back = None
			__get = request.get_json(force=True)
			try:
				__getTime = GetSvrTime()
				__back = __getTime.GetTime(__get)
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__get) + ' - ' + 'back:' + str(__back) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(json.dumps(__back))
	
		# 外挂程序版本验证，是否返回更新链接
		@app.route('/Client/GetVersion', methods=['POST'])
		def GetVersion_C():
			__back = None
			__get = request.get_json(force=True)
			try:
				__getVersion = GetVersion()
				__log = Logger(app.root_path + '/Log/Connect/Connect.log', level='info')
				__back = __getVersion.Main(__get)
				__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                  str(__get) + ' - ' + 'back:' + str(__back) + '\n')
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__get) + ' - ' + 'back:' + str(__back) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(json.dumps(__back))
	
		# 登录认证
		@app.route('/Client/UserLogin', methods=['POST'])
		def UserLogin_C():
			__back = None
			__get = request.get_json(force=True)
			try:
				__userManage = UserManege()
				__log = Logger(app.root_path + '/Log/Login/Login.log', level='info')
				__back = __userManage.UserLogin(__get)
				__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                  str(__get) + ' - ' + 'back:' + str(__back) + '\n')
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__get) + ' - ' + 'back:' + str(__back) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(json.dumps(__back))
	
		# 码垛系统订单基本信息获取
		@app.route('/Client/MaDuo/GetInfo', methods=['POST'])
		def MD_GetInfo_C():
			__back = None
			__get = request.get_json(force=True)
			try:
				__log = Logger(app.root_path + '/Log/MaDuo/MaDuoInfo.log', level='info')
				__back = {'Return': 'OK'}
				__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                  str(__get) + ' - ' + 'back:' + str(__back) + '\n')
				from Module.MaDuoSystem.MD_GetInfo import GetInfo
				if __get['Mode'] == 'Insert':
					__getInfo = GetInfo()
					t = threading.Thread(target=__getInfo.MainWork)
					t.start()
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__get) + ' - ' + 'back:' + str(__back) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(json.dumps(__back))
	
		# PDA扫描领料单
		@app.route('/Client/PDA/LL_LYXA', methods=['POST'])
		def LL_LYXA_C():
			__back = None
			__get = request.get_json(force=True)
			try:
				__log = Logger(app.root_path + '/Log/PDA/PDA_LL.log', level='info')
				# __pda_LL = PDA_LL()
				# __back = __pda_LL.MianWork(__get)
				__back = {'Return': 'OK'}
				__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                  str(__get) + ' - ' + 'back:' + str(__back) + '\n')
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__get) + ' - ' + 'back:' + str(__back) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(json.dumps(__back))
	
		# PDA扫描进货单
		@app.route('/Client/PDA/JH_LYXA', methods=['POST'])
		def JH_LYXA_C():
			__back = None
			__get = request.get_json(force=True)
			try:
				__log = Logger(app.root_path + '/Log/PDA/PDA_JH.log', level='info')
				__pda_JH = PDA_JH_GetInfo()
				__back = __pda_JH.MainWork(__get)
				__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                  str(__get) + ' - ' + 'back:' + str(__back) + '\n')
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__get) + ' - ' + 'back:' + str(__back) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(json.dumps(__back))
	
		# 下载文件，联友生产辅助工具的更新下载
		@app.route("/Client/WG/Download/<filename>", methods=['GET'])
		def WG_DownloadFile(filename):
			__log = Logger(app.root_path + '/Log/Download/Download.log', level='info')
			__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + '\n')
			directory = app.root_path + '/File/WG/'  # 文件目录
			response = make_response(send_from_directory(directory, filename, as_attachment=True))
			response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
			return response
