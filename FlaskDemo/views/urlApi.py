from flask import Response, Flask, Blueprint, request, make_response, jsonify
from modules.Api import *
import json


urlApi = Blueprint('api', __name__)


@urlApi.route('/', methods=['GET'])
def apiIndex_GET():
	return 'api_' + request.method


@urlApi.route('/', methods=['DELETE'])
def apiIndex_DELETE():
	return Response(json.dumps({'book': '123'}))


@urlApi.route('/', methods=['POST'])
def apiIndex_POST():
	return jsonify({'book': '123'})


@urlApi.route('/', methods=['PUT'])
def apiIndex_PUT():
	return 'api_' + request.method
