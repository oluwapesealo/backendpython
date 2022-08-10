
import email
from flask import Flask, request, jsonify, flash, redirect
from flask_restful import Resource, Api, reqparse
#import pandas as pd
#import ast

app = Flask(__name__)
api = Api(app)

requests ={}
class employees(Resource):
#1) Endpoint name -> CreateEndpoint
#    inputData-> Username, password, department, position
#    outputData-> token generated
#     Logic-> Creates new user
    def get(self, create_employee):
        return jsonify()

    def post(self, email, password1, password2, department, position):
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        department = request.form.get('department')
        position = request.form.get('position')

        new_employee = employees.query.filter_by(email=email).first()
        if email:
            flash('Email alraedy exists', category='error')

        if len(email) < 4:
            flash('Email is too short', category='error')

        elif len(firstname) < 2:
            flash('First Name is too short', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            
            flash('Account has been created successfully', category='success')
        return redirect('/')
api.add_resource(employees,'/createemployee')

class allrequests(Resource):
# 2) Endpoint name -> ShowallRequestsEndpoint
#    inputData-> Token	
#    outputData-> Displays all the requests sent by employees
#     Logic-> Once the endpoint is hit, the app returns the page that shows all the requests received by employees   

    def get(self, allrequest):
        return request[allrequest]
    

api.add_resource(allrequests,'/showallrequests')

class viewrequests(Resource):
# 3) Endpoint name -> ViewRequestEndpoint
#    inputData-> Token
#    outputData-> Shows the selected request
#     Logic-> Once the endpoint is hit, the app returns the page that shows the selected request
    
    def get(self, viewrequest):
        # {"sid": "SMxxxxxxxxxxxxxxx", 
        # "date_created": "Thu, 09 Aug 2018 17:26:08 +0000", 
        # "date_updated": "Thu, 09 Aug 2018 17:26:08 +0000", 
        # "date_sent": null, 
        # "to": "+15558675310",
        # "from": "+15017122661",
        # "body": "This is the ship that made the Kessel Run in fourteen parsecs?", 
        # "direction": "outbound-api",
        # "uri": "/2010-04-01/Accounts/ACxxxxxxxxx/Messages/SMxxxxxxxxxxxx.json
#}
        return requests[viewrequest]
api.add_resource(requests,'/showallrequests/viewrequest/<requestid:str>')

# 4) Endpoint name -> TeamLeadApprovalEndpoint
#    inputData-> Token Response give reason for decline
#    outputData-> 
#     Logic-> If it is declined, forwards the response to the sender of the request and goes back to the show all requests page 
# 	      If it is approved, forwards the request to the Line manager and goes back to the show all page

class teamapproval(Resource):

    def put(self, teamapproval):
        return redirect('/')
api.add_resource(requests,'/showallrequests/viewrequest/<requestid:str>/teamleadapproval')

# 5) Endpoint name -> LineManagerApprovalEndpoint
#    inputData-> Response and give reason for decline
#    outputData-> gives the option to download the request
#     Logic-> If it is denied, forwards the response to the sender of the request and goes back to the show all requests page 
# 	      If it is approved, gives the user the option to download the approved request  

class lineapproval:
    def put(self, lineapproval):
        return jsonify()
api.add_resource(lineapproval, '/showallrequests/viewrequest/<requestid:str>/linemanagerapproval')    

import pandas as pd
 # 6)Endpoint name -> DownloadRequestEndpoint
#    inputData-> Token
#    outputData-> File
#     Logic-> The request will be downloaded in a csv. format.
class downloadreq:
    def get(self, reqdownload):
        return requests[reqdownload]

api.add_resource(lineapproval, '/showallrequests/viewrequest/<requestid:str>/linemanagerapproval')

     