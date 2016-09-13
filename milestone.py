from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with

app = Flask(__name__)
api = Api(app)

fake_milestones = [
    {
        'title': '12-VerUp',
    },
    {
        'title': '10-PTF',
    },
    {
        'title': '11-PTF',
    }
]

nested_milestone = {
    'title': fields.String
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

