from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with

app = Flask(__name__)
api = Api(app)

fake_user = [
    {
        'username': 'chen_xi',
        'password': 'worksap',
        'team': 'Connector',
    },
    {
        'username': 'works',
        'password': 'hoge',
        'team': 'Source',
    }
]

result_fields = {
    'isSuccess': fields.Boolean,
    'message': fields.String,
    'username': fields.String,
    'team': fields.String,
}


@marshal_with(result_fields)
def check_login(username, password):
    # time.sleep(1)
    users = filter(lambda u: u['username'] == username, fake_user)
    if len(users) == 0 or users[0]['password'] != password:
        return {'isSuccess': False, 'message': 'username or password not right!'}
    else:
        return {'isSuccess': True, 'username': username, 'team': users[0]['team']}

class Login(Resource):

    def get(self, username, password):
        return check_login(username, password)





