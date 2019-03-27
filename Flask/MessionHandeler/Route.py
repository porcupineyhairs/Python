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
		
		# 模板
		@app.route('/Client/Default', methods=['POST'])
		def Default_C():
		# 	__back = None
		# 	__backDict = None
		# 	__get = __encryptDict.Decrypt(request.data.decode())
		# 	__back = __encryptDict.Encrypt(__backDict)
		# 	try:
		# 		__userManage = UserManege()
		# 		__log = Logger(app.root_path + '/Log/Login/Login.log', level='info')
		# 		__backDict = __userManage.UserLogin(__get)
		# 		__back = __encryptDict.Encrypt(__backDict)
		# 		__log.logger.info(
		# 			request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
		# 			str(__get) + ' - ' + 'back:' + str(__backDict) + '\n')
		# 	except Exception as e:
		# 		__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
		# 		__log_E.logger.info(
		# 			request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
		# 			str(__get) + ' - ' + 'back:' + str(__backDict) + ' - ' + 'Error:' + str(e) + '\n')
		# 	finally:
		# 		return Response(__back)
			pass
		
		# webservice功能测试
		@app.route('/Client/Test', methods=['POST', 'GET'])
		def Client_C():
			if request.method == 'POST':
				__backDict = {'name': 'me', 'password': 'you'}
				__getDict = request.get_json(force=True)
				return Response(json.dumps(__backDict))
			elif request.method == 'GET':
				return render_template('json table.html')
	
		# 连接测试，是否能连接成功，测试webservice是否正常
		@app.route('/Client/LinkTest', methods=['POST'])
		def LinkTest_C():
			__getDict = __encryptDict.Decrypt(request.data.decode())
			__backDict = {'Return': 'Yes'}
			__back = __encryptDict.Encrypt(__backDict)
			return Response(__back)
	
		# 获取198数据库服务器的时间
		@app.route('/Client/GetTime', methods=['POST'])
		def GetTime_C():
			__back = None
			__backDict = None
			__getDict = __encryptDict.Decrypt(request.data.decode())
			try:
				__getTime = GetSvrTime()
				__backDict = __getTime.GetTime(__getDict)
				__back = __encryptDict.Encrypt(__backDict)
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' +
				                    'get:' + str(__getDict) + ' - ' + 'back:' + str(__backDict) + ' - ' + 'Error:' +
				                    str(e) + '\n')
			finally:
				return Response(__back)
	
		# 外挂程序版本验证，是否返回更新链接
		@app.route('/Client/VersionManager', methods=['POST'])
		def VersionManager_C():
			__back = None
			__backDict = None
			__getDict = __encryptDict.Decrypt(request.data.decode())
			try:
				__getVersion = GetVersion()
				__backDict = __getVersion.Main(__getDict)
				__back = __encryptDict.Encrypt(__backDict)
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__getDict) + ' - ' + 'back:' + str(__backDict) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(__back)
	
		# 登录认证
		@app.route('/Client/UserManager', methods=['POST'])
		def UserManager_C():
			__back = None
			__backDict = None
			__getDict = __encryptDict.Decrypt(request.data.decode())
			__back = __encryptDict.Encrypt(__backDict)
			try:
				__userManage = UserManege()
				__log = Logger(app.root_path + '/Log/UserManager/UserManager.log', level='info')
				__backDict = __userManage.MainWork(__getDict)
				__back = __encryptDict.Encrypt(__backDict)
				__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                  str(__getDict) + ' - ' + 'back:' + str(__backDict) + '\n')
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__getDict) + ' - ' + 'back:' + str(__backDict) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(__back)
	
		# 码垛系统订单基本信息获取
		@app.route('/Client/MaDuo/GetInfo', methods=['POST'])
		def MD_GetInfo_C():
			__back = None
			__backDict = None
			__getDict = __encryptDict.Decrypt(request.data.decode())
			try:
				__log = Logger(app.root_path + '/Log/MaDuo/MaDuoInfo.log', level='info')
				__backDict = {'Return': 'OK'}
				__back = __encryptDict.Encrypt(__backDict)
				__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                  str(__getDict) + ' - ' + 'back:' + str(__backDict) + '\n')
				from Module.MaDuoSystem.MD_GetInfo import GetInfo
				if __getDict['Mode'] == 'Insert':
					__getInfo = GetInfo()
					t = threading.Thread(target=__getInfo.MainWork)
					t.start()
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__getDict) + ' - ' + 'back:' + str(__backDict) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(__back)
	
		# PDA扫描领料单
		@app.route('/Client/PDA/LL_LYXA', methods=['POST'])
		def LL_LYXA_C():
			__back = None
			__backDict = None
			__getDict = __encryptDict.Decrypt(request.data.decode())
			try:
				__log = Logger(app.root_path + '/Log/PDA/PDA_LL.log', level='info')
				# __pda_LL = PDA_LL()
				# __back = __pda_LL.MianWork(__get)
				__backDict = {'Return': 'OK'}
				__back = __encryptDict.Encrypt(__backDict)
				__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                  str(__getDict) + ' - ' + 'back:' + str(__backDict) + '\n')
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__getDict) + ' - ' + 'back:' + str(__backDict) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(__back)
	
		# PDA扫描进货单
		@app.route('/Client/PDA/JH_LYXA', methods=['POST'])
		def JH_LYXA_C():
			__back = None
			__backDict = None
			__getDict = __encryptDict.Decrypt(request.data.decode())
			try:
				__log = Logger(app.root_path + '/Log/PDA/PDA_JH.log', level='info')
				__pda_JH = PDA_JH_GetInfo()
				__backDict = __pda_JH.MainWork(__getDict)
				__back = __encryptDict.Encrypt(__backDict)
				__log.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                  str(__getDict) + ' - ' + 'back:' + str(__backDict) + '\n')
			except Exception as e:
				__log_E = Logger(app.root_path + '/Log/Error/Error.log', level='info')
				__log_E.logger.info(request.url + ' - ' + request.method + ' - ' + request.remote_addr + ' - ' + 'get:' +
				                    str(__getDict) + ' - ' + 'back:' + str(__backDict) + ' - ' + 'Error:' + str(e) + '\n')
			finally:
				return Response(__back)
	
		# 下载文件，联友生产辅助工具的更新下载
		@app.route("/Client/WG/Download/<filename>", methods=['GET'])
		def WG_DownloadFile(filename):
			directory = app.root_path + '/File/WG/'  # 文件目录
			# 判断所需文件是否存在
			if os.path.exists(directory + filename):
				response = make_response(send_from_directory(directory, filename, as_attachment=True))
				response.headers["Content-Disposition"] = "attachment; filename={}".\
					format(filename.encode().decode('latin-1'))
				return response
			else:
				return None
			
		@app.route('/Client/Test/0', methods=['POST'])
		def Test0():
			__getDict = None
			__backDict = None
			
			sqlWg = Sql(sqlType='mssql', connDict=DataBase_Dict['ROBOT_TEST'])
			# get = sqlWg.SqlWork(sqlStr=("SELECT Valid 有效码, PO_Class 订单属性, PO_Type 订单类别, TypeCode 类别编码 "
			#                             "FROM SplitTypeCode ORDER BY TypeCode "), getTitle=True)
			
			get = sqlWg.SqlWork(sqlStr=(r"SELECT K_ID 序号, BoxSize 纸箱尺寸, BoxCode 纸箱编码, "
			                            r"BoxSet 纸箱码放方式, Valid 有效码 "
			                            r"FROM BoxSizeCode ORDER BY K_ID "), getTitle=True)
			title = None
			detail = None
			if get is not None:
				title = get.pop(0)
				detail = get
				for index in range(len(detail)):
					detail[index][4] = True if detail[index][4] == 'Y' else False
			listBack = None
			
			if detail is not None and title is not None:
				listBack = []
				if len(title) == len(detail[0]):
					for rowIndex in range(len(detail)):
						dictBack = {}
						for colIndex in range(len(title)):
							dictTmp = {title[colIndex]: detail[rowIndex][colIndex]}
							dictBack.update(dictTmp)
						listBack.append(dictBack)
					
			print(json.dumps(listBack).replace(r'"', r'\"'))
			
			# print(json.dumps(__backDict))
			__back = __encryptDict.Encrypt(listBack)
			return Response(__back)
