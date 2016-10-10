# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource
import pymongo
from marshmallow import Schema, fields


class MilestoneSchema(Schema):
    title = fields.Str()
    developmentStartDate = fields.Str()
    developmentEndDate = fields.Str()
    evaluationStartDate = fields.Str()
    evaluationEndDate = fields.Str()
    developmentAvailableManDay = fields.Str()
    evaluationAvailableManDay = fields.Str()


class MilestoneList(Resource):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client.trydb
        super(MilestoneList, self).__init__()

    def get(self):
        cursor = self.db.milestones.find()
        schema = MilestoneSchema()
        milestones = [schema.dump(m).data for m in cursor]
        return jsonify({
            'isSuccess': True,
            'message': None,
            'milestones': milestones
        })

