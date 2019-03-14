from flask import request, Response, make_response, send_from_directory, send_file
from Module import *
import os
import sys
import json
import threading

__mssql = MsSql()
__conn = DataBase_Dict['WG_DB']

def Route(app=None, hostInfo=None):
	if app is None:
		pass
	else:
		# webservice功能测试
		@app.route('/Test/Test2', methods=['POST', 'GET'])
		def Test_T():
			if request.method == 'POST':
				__get = request.get_json(force=True)
				__back = {'name': 'me', 'password': 'you'}
				print(__get)
				return Response(json.dumps(__back))
			elif request.method == 'GET':
				__back = {'name': 'me', 'password': 'you'}
				return Response(json.dumps(__back))
			
		@app.route('/Test/Test3', methods=['POST'])
		def Test3_T():
			aes16 = AES16()
			strin = request.data.decode()
			strin = aes16.Decrypt(strin)
			strin = json.loads(strin)
			strout = json.dumps({'name': 'me', 'password': 'you'})
			strout = aes16.Encrypt(strout)
			return Response(strout)
			
	@app.route('/Test/BasePower', methods=['POST'])
	def BasePower_T():
		__get = request.get_json(force=True)
		print(__get)
		__perm = str(__get['BasePower'])
		__sqlstrReset = r" UPDATE WG_PERM_BASE SET Valid = 'N' "
		__sqlstrFind = r" SELECT K_ID FROM WG_PERM_BASE WHERE Name = '{0}' "
		__sqlstrSet = r" UPDATE WG_PERM_BASE SET Valid = 'Y' WHERE Name = '{0}' "
		__sqlstrNew = r" INSERT INTO WG_PERM_BASE (Name) VALUES ('{0}')"
		__mssql.Sqlwork(__conn, __sqlstrReset)
		for __permItem in __perm.split(';'):
			__sqlget = __mssql.Sqlwork(__conn, __sqlstrFind.format(__permItem))
			if __sqlget[0] != 'None':
				__mssql.Sqlwork(__conn, __sqlstrSet.format(__permItem))
			else:
				__mssql.Sqlwork(__conn, __sqlstrNew.format(__permItem))
		return Response(json.dumps(__get))