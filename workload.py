from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with

app = Flask(__name__)
api = Api(app)

fake_workloads = [
    {
        'id': 1,
        'team': 'Connector',
        'milestone': '12-VerUp',
    },
]

fake_tickets = [
    {
        'workloadId': 1,
        'no': 123,
        'title': '[AD/LDAP]CN not found',
        'developer': 'chen_xi',
        'evaluator': 'luo yi',
        'developmentManDay': 10,
        'developmentProgress': 0.3,
        'evaluationManDay': 5,
        'evaluationProgress': 0,
    },
    {
        'workloadId': 1,
        'no': 124,
        'title': '[GoogleApps]Account is deleted',
        'developer': 'chen_xi',
        'evaluator': 'luo yi',
        'developmentManDay': 15,
        'developmentProgress': 0,
        'evaluationManDay': 10,
        'evaluationProgress': 0,
    },
    {
        'workloadId': 1,
        'no': 125,
        'title': '[Output]Hashcode mismatch',
        'developer': 'chen_xi',
        'evaluator': 'luo yi',
        'developmentManDay': 10,
        'developmentProgress': 0,
        'evaluationManDay': 10,
        'evaluationProgress': 0,
    },
    {
        'workloadId': 1,
        'no': 125,
        'title': '[Workflow]Approve blank node',
        'developer': 'chen_xi',
        'evaluator': 'luo yi',
        'developmentManDay': 10,
        'developmentProgress': 0,
        'evaluationManDay': 10,
        'evaluationProgress': 0,
    },
]

fake_workload_summary = [
    {
        'workloadId': 1,
        'id': 1,
        'phrase': 'development',
        'available': 100,
        'support': 20,
        'cost': 60,
        'remain': 20,
    },
    {
        'workloadId': 1,
        'id': 2,
        'phrase': 'evaluation',
        'available': 80,
        'support': 15,
        'cost': 50,
        'remain': 10,
    }
]

fake_personal_workload = [
    {
        'summaryId': 1,
        'name': 'chen_xi',
        'available': 50,
        'support': 10,
        'cost': 30,
        'remain': 10,
    },
    {
        'summaryId': 1,
        'name': 'luo yi',
        'available': 50,
        'support': 10,
        'cost': 30,
        'remain': 10,
    },
    {
        'summaryId': 2,
        'name': 'chen_xi',
        'available': 50,
        'support': 10,
        'cost': 30,
        'remain': 10,
    },
    {
        'summaryId': 2,
        'name': 'luo yi',
        'available': 50,
        'support': 10,
        'cost': 30,
        'remain': 10,
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
def fetch_workload_list(team, milestone):
    workload = None
    for w in fake_workloads:
        if w['team'] == team and w['milestone'] == milestone:
            workload = w
            break
    if workload is None:
        return {'isSuccess': True, 'message': None, 'tickets': [], 'developmentWorkload': None, 'evaluationWorkload': None}

    tickets = filter(lambda t: t['workloadId'] == workload['id'], fake_tickets)

    for s in fake_workload_summary:
        if s['workloadId'] == workload['id']:
            if s['phrase'] == 'development':
                dev_summary = s
            elif s['phrase'] == 'evaluation':
                eval_summary = s

    dev_personal_workload = filter(lambda pw: pw['summaryId'] == dev_summary['id'], fake_personal_workload) \
        if dev_summary is not None else None
    eval_personal_workload = filter(lambda pw: pw['summaryId'] == eval_summary['id'], fake_personal_workload) \
        if eval_summary is not None else None

    if dev_summary is not None:
        dev_workload = {
            'totalAvailable': dev_summary['available'],
            'totalSupport': dev_summary['support'],
            'totalCost': dev_summary['cost'],
            'totalRemain': dev_summary['remain'],
            'personalWorkloads': dev_personal_workload,
        }

    if eval_summary is not None:
        eval_workload = {
            'totalAvailable': eval_summary['available'],
            'totalSupport': eval_summary['support'],
            'totalCost': eval_summary['cost'],
            'totalRemain': eval_summary['remain'],
            'personalWorkloads': eval_personal_workload,
        }
    return {
        'isSuccess': True,
        'message': None,
        'tickets': tickets,
        'developmentWorkload': dev_workload,
        'evaluationWorkload': eval_workload
    }


class WorkloadList(Resource):
    def get(self, team, milestone):
        return fetch_workload_list(team, milestone)


