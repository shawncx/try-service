# -*- coding: utf-8 -*-
import pymongo


def init_collections(db):
    db.drop_collection('workloads')
    db.drop_collection('users')
    db.create_collection('workloads')
    db.create_collection('users')


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


def init_workload(db):
    workloads = [
        {
            "author": "chen_xi",
            "team": "Connector",
            "workloads": [
                {
                    "milestone": "12-VerUp",
                    "developmentStartDate": "2016-09-15",
                    "developmentEndDate": "2016-11-11",
                    "evaluationStartDate": "2016-11-14",
                    "evaluationEndDate": "2016-12-09",
                    "totalAvailableManDay": 100,
                    "developmentAvailableManDay": 80,
                    "evaluationAvailableManDay": 20,
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
                },
                {
                    "milestone": "10-PTF",
                    "developmentStartDate": "2016-09-15",
                    "developmentEndDate": "2016-11-11",
                    "evaluationStartDate": "2016-11-14",
                    "evaluationEndDate": "2016-12-09",
                    "totalAvailableManDay": 100,
                    "developmentAvailableManDay": 80,
                    "evaluationAvailableManDay": 20,
                    "supportRatio": 0.2,
                    "tickets": []
                },
                {
                    "milestone": "11-PTF",
                    "developmentStartDate": "2016-09-15",
                    "developmentEndDate": "2016-11-11",
                    "evaluationStartDate": "2016-11-14",
                    "evaluationEndDate": "2016-12-09",
                    "totalAvailableManDay": 100,
                    "developmentAvailableManDay": 80,
                    "evaluationAvailableManDay": 20,
                    "supportRatio": 0.2,
                    "tickets": []
                }
            ]
        },
        {
            "author": "hasegawa",
            "team": "Core",
            "workloads": []
        }
    ]
    db.workloads.insert_many(workloads)


if __name__ == '__main__':
    client = pymongo.MongoClient("localhost", 27017)
    db = client.mydb
    # init_collections(db)
    # init_users(db)
    # init_workload(db)
    # print 'init finished'
    users = db.users.find({'username': 'chen_xi1', 'password': 'worksap'})
    print [user for user in users]
