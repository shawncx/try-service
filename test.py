from requests import get

def test_login():
    print get('http://localhost:5000/login/chen_xi/worksap').json()
    print get('http://localhost:5000/login/cccc/worksap').json()

def test_milestone_list():
    print get('http://localhost:5000/milestoneList').json()

def test_ticket_list():
    print get('http://localhost:5000/ticketList/chen_xi/12-VerUp').json()
    print get('http://localhost:5000/ticketList/chen_xi/aaa').json()


if __name__ == '__main__':
    test_login()
    test_milestone_list()
    test_ticket_list()
