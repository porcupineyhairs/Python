
from flask_restful import Resource
from flask import request, jsonify
from modules.Jdy import PlanInfo


data = [{"id": "0112", "custmer": "a"}, {"id": "0113", "custmer": "b"}]


class ApiJdy(Resource):
    def __init__(self):
        self.planInfo = PlanInfo()

    def post(self):
        if not request.json:
            return jsonify({'msg': 'need json'})
        else:
            print(request.json)
            return jsonify(self.planInfo.get(date='20210323'))

    def delete(self):
        pass

    def options(self):
        return 'success', 200

    pass
