from requests import get, post


def test_login():
    print get('http://localhost:5000/login/chen_xi/worksap').json()
    print get('http://localhost:5000/login/cccc/worksap').json()


def test_milestone_list():
    print get('http://localhost:5000/milestoneList').json()


def test_workload_list():
    print get('http://localhost:5000/workloadList/Connector/12-VerUp').json()
    print get('http://localhost:5000/workloadList/chen_xi/aaa').json()


def test_ticket_update():
    print post('http://localhost:5000/ticket/update',
               {
                   'ticket': {
                       'milestone': '12-VerUp',
                       'no': 999,
                       'title': 'NNNNNNNNNNNNNNNNNNN',
                       'developer': 'chen_xi',
                       'evaluator': 'luo yi',
                       'developmentManDay': 10,
                       'developmentProgress': 0,
                       'evaluationManDay': 10,
                       'evaluationProgress': 0,
                       'team': 'Connector',
                   }
               }).json()
    print get('http://localhost:5000/workloadList/Connector/12-VerUp').json()


if __name__ == '__main__':
    test_login()
    test_milestone_list()
    test_workload_list()
    test_ticket_update()
