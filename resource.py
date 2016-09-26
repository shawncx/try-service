# -*- coding: utf-8 -*-
from login import Login
from milestone import MilestoneList
from workload import WorkloadList, Ticket, TicketList
from flask import Flask
from flask_restful import Api
from flask_uploads import UploadSet, configure_uploads


app = Flask(__name__)
api = Api(app)

app.config['UPLOADED_UPLOADS_DEST'] = '/Users/chenxiao/Documents'
uploads = UploadSet('uploads')
configure_uploads(app, uploads)

api.add_resource(Login, '/login/<string:username>/<string:password>')
# api.add_resource(MilestoneList, '/milestoneList/<string:team>')
api.add_resource(MilestoneList, '/milestoneList')
api.add_resource(WorkloadList, '/workloadList/<string:team>/<string:milestone>')
api.add_resource(Ticket, '/ticket/update')
api.add_resource(TicketList, '/ticketList/update')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run()
