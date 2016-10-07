# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource
import pymongo

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


class MilestoneList(Resource):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client.trydb
        super(MilestoneList, self).__init__()

    def get(self):
        milestones = self.db.milestones.find()
        return jsonify({
            'isSuccess': True,
            'message': None,
            'milestones': milestones
        })

