from flask import Flask
from flask_restful import reqparse, Api, Resource, fields, marshal_with

app = Flask(__name__)
api = Api(app)

fake_tickets = [
    {
        'milestone': '12-VerUp',
        'no': 123,
        'title': '[AD/LDAP]CN not found',
        'developer': 'chen_xi',
        'evaluator': 'luo yi',
        'developmentManDay': 10,
        'developmentProgress': 0.3,
        'evaluationManDay': 5,
        'evaluationProgress': 0,
        'team': 'Connector',
    },
    {
        'milestone': '12-VerUp',
        'no': 124,
        'title': '[GoogleApps]Account is deleted',
        'developer': 'luo yi',
        'evaluator': 'chen_xi',
        'developmentManDay': 15,
        'developmentProgress': 0,
        'evaluationManDay': 10,
        'evaluationProgress': 0,
        'team': 'Connector',
    },
    {
        'milestone': '12-VerUp',
        'no': 125,
        'title': '[Output]Hashcode mismatch',
        'developer': 'chen_xi',
        'evaluator': 'luo yi',
        'developmentManDay': 10,
        'developmentProgress': 0,
        'evaluationManDay': 10,
        'evaluationProgress': 0,
        'team': 'Connector',
    },
    {
        'milestone': '12-VerUp',
        'no': 125,
        'title': '[Workflow]Approve blank node',
        'developer': 'chen_xi',
        'evaluator': 'luo yi',
        'developmentManDay': 10,
        'developmentProgress': 0,
        'evaluationManDay': 10,
        'evaluationProgress': 0,
        'team': 'Connector',
    },
]

nested_ticket = {
    'no': fields.Integer,
    'title': fields.String,
    'developer': fields.String,
    'evaluator': fields.String,
    'developmentManDay': fields.Integer,
    'developmentProgress': fields.Float,
    'evaluationManDay': fields.Integer,
    'evaluationProgress': fields.Float,
}

nested_personal_workload = {
    'name': fields.String,
    'available': fields.Float,
    'support': fields.Float,
    'cost': fields.Float,
    'remain': fields.Float,
}

nested_workload = {
    'totalAvailable': fields.Float,
    'totalSupport': fields.Float,
    'totalCost': fields.Float,
    'totalRemain': fields.Float,
    'personalWorkloads': fields.Nested(nested_personal_workload),
}

result_fields = {
    'isSuccess': fields.Boolean,
    'message': fields.String,
    'tickets': fields.Nested(nested_ticket),
    'developmentWorkload': fields.Nested(nested_workload),
    'evaluationWorkload': fields.Nested(nested_workload),
}


@marshal_with(result_fields)
def fetch_workload_list(team, milestone_title):
    tickets = filter(lambda t: t['team'] == team and t['milestone'] == milestone_title, fake_tickets)
    milestone = fetch_milestion(milestone_title)
    dev_workload = cal_workload(team, milestone, 'development')
    eval_workload = cal_workload(team, milestone, 'evaluation')
    return {
        'isSuccess': True,
        'tickets': tickets,
        'developmentWorkload': dev_workload,
        'evaluationWorkload': eval_workload,
    }


def fetch_milestion(title):
    return {
        'title': '12-VerUp',
        'developmentStartDate': '2016-09-15',
        'developmentEndDate': '2016-11-11',
        'evaluationStartDate': '2016-11-14',
        'evaluationEndDate': '2016-12-09',
        'totalAvailableManDay': 100,
        'developmentAvailableManDay': 80,
        'evaluationAvailableManDay': 20,
        'supportRatio': 0.2,
    }


@marshal_with(result_fields)
def update_ticket(ticket):
    tickets = filter(lambda t: t['no'] == ticket['no'], fake_tickets)
    if len(tickets):
        tickets[0]['developmentManDay'], tickets[0]['developmentProgress'], tickets[0]['evaluationManDay'], tickets[0][
            'evaluationProgress'] = ticket['developmentManDay'], ticket['developmentProgress'], ticket[
            'evaluationManDay'], ticket['evaluationProgress']
    else:
        fake_tickets.append(ticket)
    return {
        'isSuccess': True,
    }


def cal_workload(team, milestone, term):
    tickets = filter(lambda t: t['team'] == team and t['milestone'] == milestone['title'], fake_tickets)
    personal_workloads = {}
    total_cost = 0
    for ticket in tickets:
        (target_person, target_cost) = (ticket['developer'], ticket['developmentManDay']) if term == 'development' \
            else (ticket['evaluator'], ticket['evaluationManDay'])
        if personal_workloads.get(target_person):
            personal_workloads[target_person]['available'] = milestone['totalAvailableManDay']
            personal_workloads[target_person]['support'] = milestone['totalAvailableManDay'] * milestone['supportRatio']
            personal_workloads[target_person]['cost'] += target_cost
            personal_workloads[target_person]['remain'] -= target_cost
            total_cost += target_cost
        else:
            remain = milestone['totalAvailableManDay'] * milestone['supportRatio']
            personal_workloads[target_person] = {
                'name': target_person,
                'available': milestone['totalAvailableManDay'],
                'support': remain,
                'cost': target_cost,
                'remain': milestone['totalAvailableManDay'] - target_cost - remain,
            }
            total_cost += target_cost

    total_available = milestone['totalAvailableManDay'] * len(personal_workloads)
    total_support = total_available * milestone['supportRatio']
    total_remain = total_available - total_support - total_cost

    return {
        'totalAvailable': total_available,
        'totalSupport': total_support,
        'totalCost': total_cost,
        'totalRemain': total_remain,
        'personalWorkloads': personal_workloads.values(),
    }


class WorkloadList(Resource):
    def get(self, team, milestone):
        return fetch_workload_list(team, milestone)


class Ticket(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')


    def post(self):
        args = parser.parse_args()
        print args
        return update_ticket(args)

