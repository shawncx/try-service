from requests import get

def test_login():
    print get('http://localhost:5000/login/chen_xi/worksap').json()
    print get('http://localhost:5000/login/cccc/worksap').json()


if __name__ == '__main__':
    test_login()
