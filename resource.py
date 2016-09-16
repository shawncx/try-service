from login import Login
from milestone import MilestoneList
from workload import WorkloadList, Ticket
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(Login, '/login/<string:username>/<string:password>')
api.add_resource(MilestoneList, '/milestoneList')
api.add_resource(WorkloadList, '/workloadList/<string:team>/<string:milestone>')
api.add_resource(Ticket, '/ticket/update')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run()
