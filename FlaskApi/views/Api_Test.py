
from flask_restful import Resource
from flask import request, jsonify


data = [{"id": "0112", "custmer": "a"}, {"id": "0113", "custmer": "b"}]


class ApiTest(Resource):
    def post(self):
        if not request.json:
            print(request.json)
            return jsonify(data)

    def delete(self):
        pass

    def options(self):
        return 'success', 200

    pass
