from flask import Blueprint, request, jsonify
import json
import datetime


api_test_blueprint = Blueprint('api_test_blueprint', __name__)


@api_test_blueprint.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def test_index():
	method = request.method
	data = request.data
	rtn_data = {
		'data': ['2', '2', '3', '4', '5']
	}
	return jsonify(rtn_data)


@api_test_blueprint.route('/test1', methods=['GET', 'POST', 'DELETE', 'PUT'])
def test_test1():
	method = request.method
	data = request.data
	rtn_data = {
		'data': ['2', '2', '3', '4', '5']
	}
	return jsonify(rtn_data)


@api_test_blueprint.route('/test2', methods=['GET', 'POST', 'DELETE', 'PUT'])
def test_test2():
	method = request.method
	data = request.data
	rtn_data = {
		'data': ['2', '2', '3', '4', '5']
	}
	return jsonify(rtn_data)


@api_test_blueprint.route('/test3', methods=['GET', 'POST', 'DELETE', 'PUT'])
def test_test3():
	method = request.method
	data = request.data
	rtn_data = {
		'data': ['2', '2', '3', '4', '5']
	}
	return jsonify(rtn_data)

