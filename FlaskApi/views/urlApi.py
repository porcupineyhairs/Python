from flask import current_app, Response, Blueprint, request, make_response, jsonify
from modules.Api import *
from modules.Sql.MsSql import *
from modules.Sql.MySql import *
from modules.Log import flaskLog


urlApi = Blueprint('api', __name__)

mysql = MySqlHelper(host='127.0.0.1', passwd='Tiamohui', user='root', database='eoffice')


@urlApi.route('', methods=['PUT', 'GET', 'POST', 'DELETE', 'PATCH', 'OPTIONS', 'VIEW', 'LOCK', 'UNLOCK'])
def apiIndex():
	rtnDict = {'method': request.method, 'url': request.url}
	flaskLog(mode='info', request=request, rtnDict=rtnDict)
	return jsonify(rtnDict)


@urlApi.route('/data', methods=['GET', 'PUT'])
def apiData():
	sqlstr = "select user_id, user_accounts, user_name from `user` order by user_id limit 20"
	data = mysql.sqlWork(sqlstr, getTitle=True)
	print(data)
	rtnDict = {}
	rtnDictTmp = {}
	for colIdx in range(0, len(data[0])):
		for rowIdx in range(1, data):
			pass
	return jsonify({data})
