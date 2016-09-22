# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask_restful import reqparse, Resource
import uuid
from csv import DictReader

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
        tickets = filter(lambda t: t['team'] == team and t['milestone'] == milestone, fake_tickets)
        milestone = fetch_milestion(milestone)
        dev_workload = cal_workload(team, milestone, 'development')
        eval_workload = cal_workload(team, milestone, 'evaluation')
        return jsonify({
            'isSuccess': True,
            'tickets': tickets,
            'developmentWorkload': dev_workload,
            'evaluationWorkload': eval_workload,
        })


class Ticket(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ticket', type=dict, location='json')
        super(Ticket, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        ticket = args['ticket']
        tickets = filter(lambda t: t['no'] == ticket['no'], fake_tickets)
        if len(tickets):
            tickets[0]['developmentManDay'] = ticket['developmentManDay']
            tickets[0]['developmentProgress'] = ticket['developmentProgress']
            tickets[0]['evaluationManDay'] = ticket['evaluationManDay']
            tickets[0]['evaluationProgress'] = ticket['evaluationProgress']
        else:
            fake_tickets.append(ticket)
        return jsonify({
            'isSuccess': True
        })


class TicketList(Resource):
    def post(self):
        import resource
        csv_file = request.files.get('ticketList')
        milestone = request.form.get('milestone')
        team = request.form.get('team')
        mode = request.form.get('mode')
        file_name = str(uuid.uuid4()) + '.csv'
        resource.uploads.save(csv_file, name=file_name)
        upload_tickets = []
        with open(resource.app.config['UPLOADED_UPLOADS_DEST'] + '/' + file_name, 'rb') as saved_file:
            reader = DictReader(saved_file)
            for row in reader:
                no = row['チケットNo']
                title = row['概要']
                developer = row['開発担当者']
                evaluator = row['評価担当者']
                existed_ticket = filter(lambda t: t['no'] == no, fake_tickets)
                if len(existed_ticket):
                    existed_ticket[0]['title'] = title
                    existed_ticket[0]['developer'] = developer
                    existed_ticket[0]['evaluator'] = evaluator
                    upload_tickets.append(existed_ticket[0])
                else:
                    new_ticket = {
                        'milestone': milestone,
                        'no': int(no),
                        'title': title,
                        'developer': developer,
                        'evaluator': evaluator,
                        'developmentManDay': 0,
                        'developmentProgress': 0,
                        'evaluationManDay': 0,
                        'evaluationProgress': 0,
                        'team': team,
                    }
                    fake_tickets.append(new_ticket)
                    upload_tickets.append(new_ticket)
        if mode == 'override':
            not_merged_tickets = [t for t in fake_tickets if t not in upload_tickets]
            for t in not_merged_tickets:
                fake_tickets.remove(t)
        return jsonify({
            'isSuccess': True
        })
