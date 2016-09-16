from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with

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

nested_milestone = {
    'title': fields.String,
    'developmentStartDate': fields.String,
    'developmentEndDate': fields.String,
    'EvaluationStartDate': fields.String,
    'EvaluationEndDate': fields.String,
    'totalAvailableManDay': fields.Float,
    'developmentAvailableManDay': fields.Float,
    'evaluationAvailableManDay': fields.Float,
}

result_field = {
    'isSuccess': fields.Boolean,
    'message': fields.String,
    'milestones': fields.Nested(nested_milestone)
}


@marshal_with(result_field)
def fetch_milestone_list():
    return {
        'isSuccess': True,
        'message': None,
        'milestones': fake_milestones
    }


class MilestoneList(Resource):
    def get(self):
        return fetch_milestone_list()

