
import email
from sqlite3 import Cursor
from flask import Flask, request, jsonify, flash, redirect
from flask_restful import Resource, Api, reqparse
import pypyodbc as odbc 
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
api = Api(app)

requests ={}
class employees(Resource):
#1) Endpoint name -> CreateEndpoint
#    inputData-> Username, password, department, position
#    outputData-> token generated
#     Logic-> Creates new user
    def __init__(self):
        self.ID=''
        self.Email=''
        self.Password=''
        self.Department=''
        self.Line_manager=''
        self.Team_lead=''
        self.Employee=''
        self.create={'Email':str(self.Email), 'Password':str(self.Password),'Department':str(self.Department), 'Line Manager': bool(self.Line_manager),'Team Lead': bool(self.Team_lead), 'Employee':bool(self.Employee)}
    def post(self):
        return(self.create)
        #function to schedule days
    
    def get(self, create_employee):
        import pyodbc 
        connect = pyodbc.connect('Driver={SQL Server};'
        'Server=PESES-LAPTOP;'
        'Database=employeedb;'
        'Trusted_Connection=yes;')

        cursor = connect.cursor()

        cursor.execute('''INSERT INTO employeetable1 VALUES (4,'oluwapse.lo@wemabank.com', 'peseao','IT',0 , 0, 1, '0', 0, 1, 1, 1, 1, 1)''')
        connect.commit()
        
        return redirect('/')
api.add_resource(employees,'/createemployee')

class allrequests(Resource):
# 2) Endpoint name -> ShowallRequestsEndpoint
#    inputData-> Token	
#    outputData-> Displays all the requests sent by employees
#     Logic-> Once the endpoint is hit, the app returns the page that shows all the requests received by employees   

    def get(self, allrequest):


        drivername='SQL SERVER'
        servername='PESES-LAPTOP'
        database='employeerq'
        connection_string=f"""
         DRIVER={{{drivername}}};
         SERVER={servername};
        DATABASE={database};
        Trust_Connection=yes;
            """ 
        #connecting to the database
        readdata=odbc.connect(connection_string)
        #to read from sql database
        SQL_Query=pd.read_sql_query('''SELECT * FROM[dbo].[employeereqs]''',readdata)
        #storing sql database in python
        finaldatabase=SQL_Query.head()
        #coverting the table to a dictionar
        requests= finaldatabase.to_dict('records')
        return(requests)



api.add_resource(allrequests,'/allrequests')

class viewrequests(Resource):
# 3) Endpoint name -> ViewRequestEndpoint
#    inputData-> Token
#    outputData-> Shows the selected request
#     Logic-> Once the endpoint is hit, the app returns the page that shows the selected request
    
    def get(self, viewrequest):
       

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

api.add_resource(downloadreq, '/showallrequests/viewrequest/<requestid:str>/linemanagerapproval')

     