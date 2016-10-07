# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask_restful import reqparse, Resource
import uuid
from csv import DictReader
import pymongo

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


def cal_workload(workload, milestone, term):
    support_ratio = workload['supportRatio']
    milestone_total_available = milestone['developmentAvailableManDay'] + milestone['evaluationAvailableManDay']
    personal_workloads = {}
    total_cost = 0
    for ticket in workload['tickets']:
        (target_person, target_cost) = (ticket['developer'], ticket['developmentManDay']) if term == 'development' \
            else (ticket['evaluator'], ticket['evaluationManDay'])
        if personal_workloads.get(target_person):
            personal_workloads[target_person]['available'] = milestone_total_available
            personal_workloads[target_person]['support'] = milestone_total_available * support_ratio
            personal_workloads[target_person]['cost'] += target_cost
            personal_workloads[target_person]['remain'] -= target_cost
            total_cost += target_cost
        else:
            remain = milestone_total_available * support_ratio
            personal_workloads[target_person] = {
                'name': target_person,
                'available': milestone_total_available,
                'support': remain,
                'cost': target_cost,
                'remain': milestone_total_available - target_cost - remain,
            }
            total_cost += target_cost

    total_available = milestone_total_available * len(personal_workloads)
    total_support = total_available * support_ratio
    total_remain = total_available - total_support - total_cost

    return {
        'totalAvailable': total_available,
        'totalSupport': total_support,
        'totalCost': total_cost,
        'totalRemain': total_remain,
        'personalWorkloads': personal_workloads.values(),
    }


class WorkloadList(Resource):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client.trydb
        super(WorkloadList, self).__init__()

    def get(self, team, milestone_title):
        workload = self.db.workloads.find_one({'milestone': milestone_title}, {'team': team})
        milestone = self.db.milestones.find_one({'title': milestone_title})
        dev_workload = cal_workload(workload, milestone, 'development')
        eval_workload = cal_workload(workload, milestone, 'evaluation')
        return jsonify({
            'isSuccess': True,
            'tickets': workload['tickets'],
            'developmentWorkload': dev_workload,
            'evaluationWorkload': eval_workload,
        })


class Ticket(Resource):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client.trydb
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('team', type=str, location='json')
        self.parser.add_argument('milestone', type=str, location='json')
        self.parser.add_argument('ticket', type=dict, location='json')
        super(Ticket, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        team, milestone, ticket = args['team'], args['milestone'], args['ticket']
        self.db.workloads.update_one(
            {
                'team': team,
                'milestone': milestone,
                'tickets.no': ticket['no']
            },
            {
                '$set': {
                    'tickets.$.developmentManDay': ticket['developmentManDay'],
                    'tickets.$.developmentProgress': ticket['developmentProgress'],
                    'tickets.$.evaluationManDay': ticket['evaluationManDay'],
                    'tickets.$.evaluationProgress': ticket['evaluationProgress']
                }
            }
        )
        return jsonify({
            'isSuccess': True
        })


class TicketList(Resource):
    def post(self):
        import resource
        csv_file = request.files.get('ticketList')
        milestone = request.form.get('milestone')
        team = request.form.get('team')
        file_name = str(uuid.uuid4()) + '.csv'
        resource.uploads.save(csv_file, name=file_name)
        workload = self.db.workloads.find_one({'team': team, 'milestone': milestone})
        with open(resource.app.config['UPLOADED_UPLOADS_DEST'] + '/' + file_name, 'rb') as saved_file:
            reader = DictReader(saved_file)
            for row in reader:
                no, title, developer, evaluator = row['チケットNo'], row['概要'], row['開発担当者'], row['評価担当者']
                existed_ticket = filter(lambda t: t['no'] == no, workload['tickets'])
                if len(existed_ticket):
                    existed_ticket[0]['title'] = title
                    existed_ticket[0]['developer'] = developer
                    existed_ticket[0]['evaluator'] = evaluator
                else:
                    new_ticket = {
                        'no': int(no),
                        'title': title,
                        'developer': developer,
                        'evaluator': evaluator,
                        'developmentManDay': 0,
                        'developmentProgress': 0,
                        'evaluationManDay': 0,
                        'evaluationProgress': 0,
                    }
                    workload['tickets'].append(new_ticket)
        self.db.workloads.replace_one({'team': team, 'milestone': milestone}, workload)
        return jsonify({
            'isSuccess': True
        })
