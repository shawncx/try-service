from flask_restful import Resource, fields, marshal_with
import pymongo

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


class Login(Resource):
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        self.db = client.trydb
        super(Login, self).__init__()

    @marshal_with(result_fields)
    def get(self, username, password):
        user_cursor = self.db.users.find({'username': username, 'password': password})
        users = [user for user in user_cursor]
        if len(users) == 0:
            return {'isSuccess': False, 'message': 'username or password not right!'}
        else:
            return {'isSuccess': True, 'username': username, 'team': users[0]['team']}
