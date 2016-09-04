from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
import time

app = Flask(__name__)
api = Api(app)

fake_tickets = [
    {
        'leader': 'chen_xi',
        'tickets': [
            {
                'no': 123,
                'title': '[AD/LDAP]CN not found',
                'developManDay': 10,
                'developProgress': 0.3,
                'evaluationManDay': 5,
                'evaluationProgress': 0,
            },
            {
                'no': 124,
                'title': '[GoogleApps]Account is deleted',
                'developManDay': 15,
                'developProgress': 0,
                'evaluationManDay': 10,
                'evaluationProgress': 0,
            }
        ]
    }
]

nested_ticket = {
    'no': fields.Integer,
    'title': fields.String,
    'developManDay': fields.Integer,
    'developProgress': fields.Float,
    'evaluationManDay': fields.Integer,
    'evaluationProgress': fields.Float,
}

result_fields = {
    'isSuccess': fields.Boolean,
    'message': fields.String,
    'tickets': fields.Nested(nested_ticket),
}

@marshal_with(result_fields)
def fetch_ticket_list(leader):
    time.sleep(2)
    tickets = filter(lambda t: t['leader'] == leader, fake_tickets)
    if len(tickets):
        return {'isSuccess': True, 'message': None, 'tickets': tickets[0]['tickets']}
    else:
        return {'isSuccess': True, 'message': None, 'tickets': []}

class TicketList(Resource):
    def get(self, leader):
        return fetch_ticket_list(leader)



