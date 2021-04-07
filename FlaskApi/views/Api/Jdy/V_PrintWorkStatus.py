
from flask_restful import Resource
from flask import request, jsonify
from modules.Jdy import PrintWorkStatus


class ApiJdy(Resource):
    def __init__(self):
        self.PrintWorkStatus = PrintWorkStatus()

    def post(self):
        if self.check_token(request.headers['Api-token']):
            if not request.json:
                return jsonify({'status': 'error', 'msg': 'json error'})
            else:
                print(request.json)
                return jsonify({'status': 'success', 'msg': '已打印'})
        else:
            return jsonify({'status': 'error', 'error': 'token error'})

    def options(self):
        return 'success', 200

    def check_token(self, token):
        if token == 'Comfort-Jdy':
            return True
        else:
            return False
