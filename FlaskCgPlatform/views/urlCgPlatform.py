from flask import Blueprint, request, make_response, jsonify, session, render_template
from modules.Log.flaskLog import *
from modules.CgPlanform.CgPlatform import *
from modules.GlobalModules.CheckSession import *


urlCg = Blueprint('cg', __name__)


@urlCg.route('/shd/editshd', methods=['GET', 'POST'])
def editShd():
	return render_template('urlCgPlatform/shd.html')


@urlCg.route('/shd/getdata', methods=['POST'])
def apiGetData():
	token = session.get('token')
	if CheckSession.checkToken(token=token):
		inDict = request.get_json(force=True)
		cgPlatfrom = CgPlatform()
		rtnDict = cgPlatfrom.getData(token=token, inDict=inDict)
		flaskLog(mode='info', request=request, rtnDict=None)
		return jsonify(rtnDict)
	else:
		return ''


@urlCg.route('/shd/setdata', methods=['POST'])
def apiSetData():
	token = session.get('token')
	if CheckSession.checkToken(token=token):
		inDict = request.get_json(force=True)
		cgPlatfrom = CgPlatform()
		rtnDict = cgPlatfrom.setData(token=token, inDict=inDict)
		flaskLog(mode='info', request=request, rtnDict=None)
		return jsonify(rtnDict)
	else:
		return ''


@urlCg.route('/test', methods=['POST'])
def apiTest():
	token = session.get('token')
	if CheckSession.checkToken(token=token):
		inDict = request.get_json(force=True)
		# cgPlatfrom = CgPlatform()
		# rtnDict = cgPlatfrom.setData(token=token, inDict=inDict)
		flaskLog(mode='info', request=request, rtnDict=None)
		rtnDict = {"success": "yes"}
		return jsonify(rtnDict)
	else:
		return ''
