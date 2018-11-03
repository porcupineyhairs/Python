from flask import request, Response
from Module import *
import os
import json


def Route(app):
	@app.route('/Client/Test', methods=['POST'])
	def Client_C():
		k = {'name': 'me', 'password': 'you'}
		j = request.get_json(force=True)
		return Response(json.dumps(k))

	@app.route('/Client/LinkTest', methods=['POST'])
	def LinkTest_C():
		__ConnIp = request.remote_addr
		__get = request.get_json(force=True)
		return Response(json.dumps({'Return': 'Yes'}))

	@app.route('/Client/UserLogin', methods=['POST'])
	def UserLogin_C():
		__Usermanage = UserManege()
		__get = request.get_json(force=True)
		__back = __Usermanage.UserLogin(__get)
		return Response(json.dumps(__back))
