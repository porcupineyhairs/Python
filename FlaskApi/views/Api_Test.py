
from flask_restful import Resource
from flask import request, jsonify


class ApiTest(Resource):
    def post(self):
        if request.json:
            print(request.json)
            return request.json
        else:
            return jsonify({'msg': 'input need json'})

    def delete(self):
        return 'error', 404

    def options(self):
        return 'success', 200

    pass
