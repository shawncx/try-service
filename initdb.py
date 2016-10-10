# -*- coding: utf-8 -*-
import pymongo


def init_users(db):
    users = [
        {
            "username": "chen_xi",
            "password": "worksap",
            "team": "Connector",
        },
        {
            "username": "hasegawa",
            "password": "worksap",
            "team": "Core",
        }
    ]
    db.users.insert_many(users)


def init_milestones(db):
    milestones = [
        {
            'title': '12-VerUp',
            'developmentStartDate': '2016-09-15',
            'developmentEndDate': '2016-11-11',
            'evaluationStartDate': '2016-11-14',
            'evaluationEndDate': '2016-12-09',
            'developmentAvailableManDay': 80,
            'evaluationAvailableManDay': 20,
        },
        {
            'title': '10-PTF',
            'developmentStartDate': '2016-09-15',
            'developmentEndDate': '2016-11-11',
            'evaluationStartDate': '2016-11-14',
            'evaluationEndDate': '2016-12-09',
            'developmentAvailableManDay': 80,
            'evaluationAvailableManDay': 20,
        },
        {
            'title': '11-PTF',
            'developmentStartDate': '2016-09-15',
            'developmentEndDate': '2016-11-11',
            'evaluationStartDate': '2016-11-14',
            'evaluationEndDate': '2016-12-09',
            'developmentAvailableManDay': 80,
            'evaluationAvailableManDay': 20,
        }
    ]
    db.milestones.insert_many(milestones)


def init_workloads(db):
    workloads = [
        {
            "author": "chen_xi",
            "team": "Connector",
            "milestone": "12-VerUp",
            "supportRatio": 0.2,
            "tickets": [
                {
                    "no": 12152,
                    "title": "[Connector Document] Create document for CWS in gitbook",
                    "developer": "津田 薫",
                    "evaluator": "羅 毅",
                    "developmentManDay": 10,
                    "developmentProgress": 0.3,
                    "evaluationManDay": 5,
                    "evaluationProgress": 0,
                },
                {
                    "no": 12178,
                    "title": "[AD/LDAP] Support comma in CN",
                    "developer": "陳霄",
                    "evaluator": "",
                    "developmentManDay": 15,
                    "developmentProgress": 0,
                    "evaluationManDay": 10,
                    "evaluationProgress": 0,
                }
            ]
        }
    ]
    db.workloads.insert_many(workloads)


def init_collections(db):
    db.drop_collection('milestones')
    db.drop_collection('workloads')
    db.drop_collection('users')

    db.create_collection('milestones')
    db.create_collection('workloads')
    db.create_collection('users')

    init_users(db)
    init_milestones(db)
    init_workloads(db)


if __name__ == '__main__':
    client = pymongo.MongoClient("localhost", 27017)
    db = client.trydb
    init_collections(db)
    print 'init finished'
    # aa = db.workloads.find_one({
    #         'team': 'Connector',
    #         'milestone': '12-VerUp',
    #         'tickets.no': 12178
    #     })
    # print(aa)
    # db.workloads.update_one(
    #     {
    #         'team': 'Connector',
    #         'milestone': '12-VerUp',
    #         'tickets.no': 12178
    #     },
    #     {
    #         '$set': {'tickets.$.developmentManDay': 5000}
    #     }
    # )

