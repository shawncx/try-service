# -*- coding: utf-8 -*-
from requests import get, post
import time
import json


def test_login():
    print get('http://localhost:5000/login/chen_xi/worksap').json()
    print get('http://localhost:5000/login/cccc/worksap').json()


def test_milestone_list():
    print json.dumps(get('http://localhost:5000/milestoneList').json(), indent=4)


def test_workload_list():
    print json.dumps(get('http://localhost:5000/workloadList/Connector/12-VerUp').json(), indent=4)
    print json.dumps(get('http://localhost:5000/workloadList/chen_xi/aaa').json(), indent=4)


def test_ticket_update():
    print json.dumps(
        post('http://localhost:5000/ticket/update',
             json={
                 'team': 'Connector',
                 'milestone': '12-VerUp',
                 'ticket': {
                     'no': 12178,
                     'title': 'NNNNNNNNNNNNNNNNNNN',
                     'developer': 'chen_xi',
                     'evaluator': 'luo yi',
                     'developmentManDay': 9999,
                     'developmentProgress': 888,
                     'evaluationManDay': 777,
                     'evaluationProgress': 666,
                 }
             }).json(),
        indent=4)
    time.sleep(1)
    print json.dumps(get('http://localhost:5000/workloadList/Connector/12-VerUp').json(), indent=4)


def test_ticket_list_update_merge():
    files = {'file': open('exportCsv.csv', 'rb')}
    data = {'milestone': '12-VerUp', 'team': 'Connector', 'mode': 'merge'}
    print json.dumps(post('http://localhost:5000/ticketList/update', files=files, data=data).json(), indent=4)
    time.sleep(1)
    print json.dumps(get('http://localhost:5000/workloadList/Connector/12-VerUp').json(), indent=4)


# def test_ticket_list_update_override():
#     files = {'file': open('exportCsv.csv', 'rb')}
#     data = {'milestone': '12-VerUp', 'team': 'Connector', 'mode': 'override'}
#     print post('http://localhost:5000/ticketList/update', files=files, data=data).json()
#     time.sleep(1)
#     print get('http://localhost:5000/workloadList/Connector/12-VerUp').json()


if __name__ == '__main__':
    # test_login()
    # test_milestone_list()
    # test_workload_list()
    test_ticket_update()
    # test_ticket_list_update_merge()
