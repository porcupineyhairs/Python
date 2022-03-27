from flask import Flask, Blueprint, request, make_response, jsonify, session, render_template
from modules.CgPlanform.CgPlatform import *
from modules.GlobalModules.CheckSession import *


urlApi = Blueprint('api', __name__)


@urlApi.route('/test', methods=['POST', 'GET', 'DELETE', 'PUT'])
def apiIndex_DELETE():
	return jsonify({'method': request.method, 'url': request.url})


@urlApi.route('/testhtml', methods=['POST', 'GET'])
def testHtml():
	return render_template('urlTest/01.html')
