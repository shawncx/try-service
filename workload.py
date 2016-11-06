# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask_restful import reqparse, Resource
import uuid
from csv import DictReader
import pymongo
from marshmallow import Schema, fields

class TicketSchema(Schema):
    no = fields.Integer()
    title = fields.Str()
    developer = fields.Str()
    evaluator = fields.Str()
    developmentManDay = fields.Float()
    developmentProgress = fields.Float()
    evaluationManDay = fields.Float()
    evaluationProgress = fields.Field()


def cal_workload(workload, milestone, term):
    support_ratio = workload['supportRatio']
    milestone_total_available = milestone['developmentAvailableManDay'] if term == 'development' \
        else milestone['evaluationAvailableManDay']
    personal_workloads = {}
    total_cost = 0
    total_remain_manday = 0
    for ticket in workload['tickets']:
        (target_person, target_cost, target_progress) = (
            ticket['developer'], ticket['developmentManDay'], ticket['developmentProgress']) if term == 'development' \
            else (ticket['evaluator'], ticket['evaluationManDay'], ticket['evaluationProgress'])
        developers = target_person.split(u',')
        for developer in developers:
            if len(filter(lambda d: developer == d, [u'津田 薫', u'羅 毅', u'陳霄', u'李 旭'])) == 0:
                continue
            personal_target_cost = target_cost / len(developers)
            personal_remained_manday = personal_target_cost - personal_target_cost * target_progress
            if personal_workloads.get(developer):
                personal_workloads[developer]['cost'] += personal_target_cost
                personal_workloads[developer]['remain'] -= personal_target_cost
                personal_workloads[developer]['remainedManDay'] += personal_remained_manday
            else:
                remain = milestone_total_available * support_ratio
                personal_workloads[developer] = {
                    'name': developer,
                    'available': milestone_total_available,
                    'support': remain,
                    'cost': personal_target_cost,
                    'remain': milestone_total_available - personal_target_cost - remain,
                    'remainedManDay': personal_remained_manday,
                }
            total_cost += personal_target_cost
            total_remain_manday += (personal_target_cost - personal_target_cost * target_progress)

    total_available = milestone_total_available * len(personal_workloads)
    total_support = total_available * support_ratio
    total_remain = total_available - total_support - total_cost

    return {
        'totalAvailable': total_available,
        'totalSupport': total_support,
        'totalCost': total_cost,
        'totalRemain': total_remain,
        'totalRemainedManDay': total_remain_manday,
        'personalWorkloads': personal_workloads.values(),
    }


class WorkloadList(Resource):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client.trydb
        super(WorkloadList, self).__init__()

    def get(self, team, milestone):
        workload = self.db.workloads.find_one({'milestone': milestone, 'team': team})
        if workload:
            schema = TicketSchema()
            tickets = [schema.dump(t).data for t in workload['tickets']]
            milestone_obj = self.db.milestones.find_one({'title': milestone})
            dev_workload = cal_workload(workload, milestone_obj, 'development')
            eval_workload = cal_workload(workload, milestone_obj, 'evaluation')
            return jsonify({
                'isSuccess': True,
                'tickets': tickets,
                'developmentWorkload': dev_workload,
                'evaluationWorkload': eval_workload,
            })
        else:
            return jsonify({
                'isSuccess': True,
                'tickets': [],
                'developmentWorkload': None,
                'evaluationWorkload': None,
            })


class Ticket(Resource):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client.trydb
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ticket', type=dict, location='json')
        super(Ticket, self).__init__()

    def put(self, team, milestone, no):
        args = self.parser.parse_args()
        ticket = args['ticket']
        self.db.workloads.update_one(
            {
                'team': team,
                'milestone': milestone,
                'tickets.no': no
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

    def delete(self, team, milestone, no):
        self.db.workloads.update_one(
            {
                'team': team,
                'milestone': milestone,
            },
            {
                '$pull': {
                    'tickets': {
                        'no': no
                    }
                }
            })
        return jsonify({
            'isSuccess': True
        })


class TicketList(Resource):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client.trydb
        super(TicketList, self).__init__()

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
                existed_ticket = filter(lambda t: t['no'] == int(no), workload['tickets'])
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


if __name__ == '__main__':
    print u'陳霄,長谷川 健博'.split(u',')
