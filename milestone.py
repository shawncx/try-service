# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

fake_milestones = [
    {
        'title': '12-VerUp',
        'developmentStartDate': '2016-09-15',
        'developmentEndDate': '2016-11-11',
        'evaluationStartDate': '2016-11-14',
        'evaluationEndDate': '2016-12-09',
        'totalAvailableManDay': 100,
        'developmentAvailableManDay': 80,
        'evaluationAvailableManDay': 20,
        'supportRatio': 0.2,
    },
    {
        'title': '10-PTF',
        'developmentStartDate': '2016-09-15',
        'developmentEndDate': '2016-11-11',
        'evaluationStartDate': '2016-11-14',
        'evaluationEndDate': '2016-12-09',
        'totalAvailableManDay': 100,
        'developmentAvailableManDay': 80,
        'evaluationAvailableManDay': 20,
        'supportRatio': 0.2,
    },
    {
        'title': '11-PTF',
        'developmentStartDate': '2016-09-15',
        'developmentEndDate': '2016-11-11',
        'evaluationStartDate': '2016-11-14',
        'evaluationEndDate': '2016-12-09',
        'totalAvailableManDay': 100,
        'developmentAvailableManDay': 80,
        'evaluationAvailableManDay': 20,
        'supportRatio': 0.2,
    }
]

def fetch_milestone_list():
    return jsonify({
        'isSuccess': True,
        'message': None,
        'milestones': fake_milestones
    })


class MilestoneList(Resource):
    def get(self):
        return fetch_milestone_list()

