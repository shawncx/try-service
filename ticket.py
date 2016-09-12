from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
import time

app = Flask(__name__)
api = Api(app)

fake_tickets = [
    {
        'no': 123,
        'title': '[AD/LDAP]CN not found',
        'developManDay': 10,
        'developProgress': 0.3,
        'evaluationManDay': 5,
        'evaluationProgress': 0,
        'milestone': '12-VerUp',
        'leader': 'chen_xi',
    },
    {
        'no': 124,
        'title': '[GoogleApps]Account is deleted',
        'developManDay': 15,
        'developProgress': 0,
        'evaluationManDay': 10,
        'evaluationProgress': 0,
        'milestone': '12-VerUp',
        'leader': 'chen_xi',
    },
    {
        'no': 125,
        'title': '[Output]Hashcode mismatch',
        'developManDay': 10,
        'developProgress': 0,
        'evaluationManDay': 10,
        'evaluationProgress': 0,
        'milestone': '10-PTF',
        'leader': 'chen_xi',
    },
    {
        'no': 125,
        'title': '[Workflow]Approve blank node',
        'developManDay': 10,
        'developProgress': 0,
        'evaluationManDay': 10,
        'evaluationProgress': 0,
        'milestone': '12-VerUp',
        'leader': 'Kawasaki',
    },
]

nested_ticket = {
    'no': fields.Integer,
    'title': fields.String,
    'developManDay': fields.Integer,
    'developProgress': fields.Float,
    'evaluationManDay': fields.Integer,
    'evaluationProgress': fields.Float,
    'leader': fields.String,
    'milestone': fields.String,
}

result_fields = {
    'isSuccess': fields.Boolean,
    'message': fields.String,
    'tickets': fields.Nested(nested_ticket),
}

@marshal_with(result_fields)
def fetch_ticket_list(leader, milestone):
    tickets = []
    tickets.append(filter(lambda t: t['leader'] == leader and t['milestone'] == milestone, fake_tickets))
    if len(tickets):
        return {'isSuccess': True, 'message': None, 'tickets': tickets[0]}
    else:
        return {'isSuccess': True, 'message': None, 'tickets': []}

class TicketList(Resource):
    def get(self, leader, milestone):
        return fetch_ticket_list(leader, milestone)



