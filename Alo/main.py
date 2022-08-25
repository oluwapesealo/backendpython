import email
import json
from sqlite3 import Cursor
from flask import Flask, request, jsonify, flash, redirect
from flask_restful import Resource, Api, reqparse
import pypyodbc as odbc 
import mysql.connector
from mysql.connector import Error
import pandas as pd
import pyodbc


app = Flask(__name__)
api = Api(app)

requests ={}

#1) Endpoint name -> CreateEndpoint
#    inputData-> Username, password, department, position
#    outputData-> token generated
#     Logic-> Creates new user
class employees(Resource):
    def __init__(self, Email='', Password='', Department='', Status=''):
        self.Email= Email
        self.Password=Password
        self.Department=Department
        self.Status=Status


    
    def post(self, Email, Password, Department, Status):
        import pyodbc 
        connect = pyodbc.connect('Driver={SQL Server};'
        'Server=PESES-LAPTOP;'
        'Database=employeedb;'
        'Trusted_Connection=yes;')

        cursor = connect.cursor()
        # Email = input('Email: ')
        # Password = input('Password: ')
        # Department = input('Department: ')
        # Status = input('Status: ')
        

        cursor.execute('''INSERT INTO employeetable2 VALUES (?,?,?,?,'NULL', 'NULL', 'NULL', 0, 0, 0, 0, 0)''',(Email, Password, Department, Status))

        connect.commit()
        
        return redirect('/')
api.add_resource(employees,'/createemployee/<string:Email>/<string:Password>/<string:Department>/<string:Status>')


# 2) Endpoint name -> ShowallRequestsEndpoint
#    inputData-> Token	
#    outputData-> Displays all the requests sent by employees
#     Logic-> Once the endpoint is hit, the app returns the page that shows all the requests received by employees   
class allrequests(Resource):
    def get(self):


        drivername='SQL SERVER'
        servername='PESES-LAPTOP'
        database='employeedb'
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


# 3) Endpoint name -> ViewRequestEndpoint
#    inputData-> Token
#    outputData-> Shows the selected request
#     Logic-> Once the endpoint is hit, the app returns the page that shows the selected request
# requests={}
class viewrequests(Resource):
    def __init__(self, Email=''):
        self.Email= Email

    def get(self,Email=''):
        # requests=[]
        # connect = pyodbc.connect('Driver={SQL Server};'
        #     'Server=PESES-LAPTOP;'
        #     'Database=employeedb;'
        #     'Trusted_Connection=yes;')

        # cursor = connect.cursor()
        # cursor.execute('''select *from employeereqs where Email = ?''', (Email))
        # vrequests=cursor.fetchall()
        # for request in vrequests:
        #     requests.append([x for x in request])
        # return json.dumps(requests)


        drivername='SQL SERVER'
        servername='PESES-LAPTOP'
        database='employeedb'
        connection_string=f"""
         DRIVER={{{drivername}}};
         SERVER={servername};
        DATABASE={database};
        Trust_Connection=yes;
            """ 
        #connecting to the database
        readdata=odbc.connect(connection_string)
        #to read from sql database
        SQL_Query=pd.read_sql_query('''select *from employeereqs where Email ='''+Email, readdata,)
        #storing sql database in python
        finaldatabase=SQL_Query.head()
        #coverting the table to a dictionar
        vrequests= finaldatabase.to_dict('records')
        return(vrequests)
        
        

api.add_resource(viewrequests,'/allrequests/viewrequest/<string:Email>')


# 4) Endpoint name -> TeamLeadApprovalEndpoint
#    inputData-> Token Response give reason for decline
#    outputData-> 
#     Logic-> If it is declined, forwards the response to the sender of the request and goes back to the show all requests page 
# 	      If it is approved, forwards the request to the Line manager and goes back to the show all page
class teamapproval(Resource):
    def __init__(self):
        self.TeamLead_Approval=''
        self.Reason_for_Decline=''
        self.approval={'Approval':bool(self.TeamLead_Approval), 'Reason for Decline':str(self.Reason_for_Decline)}
    

        # return(self.approval)

    
    def patch(self, Email=''):
            self.Email=Email
            connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=employeedb;'
            'Trusted_Connection=yes;')

            cursor = connect.cursor()
            if self.TeamLead_Approval == True:
                cursor.execute('''update employeereqs set TeamLead_Approval = 1 where Email =?''', self.Email)
                connect.commit()
            if self.TeamLead_Approval == False:
                cursor.execute('''update employeereqs set TeamLead_Approval = 0 where Email =?''', self.Email) 
                cursor.execute('''update employeereqs set Reason_for_Decline = "Traffic" where Email =?''', self.Email)  
            return redirect('/allrequests')
api.add_resource(teamapproval,'/allrequests/viewrequest/<string:Email>/teamleadapproval')

# 5) Endpoint name -> LineManagerApprovalEndpoint
#    inputData-> Response and give reason for decline
#    outputData-> gives the option to download the request
#     Logic-> If it is denied, forwards the response to the sender of the request and goes back to the show all requests page 
# 	      If it is approved, gives the user the option to download the approved request  

class linemanager(Resource):
    def __init__(self):
        self.LineManager_Approval=''
        self.Reason_for_Decline=''
        self.approval={'Approval':bool(self.LineManager_Approval), 'Reason for Decline':str(self.Reason_for_Decline)}
    

        # return(self.approval)

    
    def patch(self, Email=''):
            self.Email=Email
            connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=employeedb;'
            'Trusted_Connection=yes;')

            cursor = connect.cursor()
            if self.LineManager_Approval == True:
                cursor.execute('''update employeereqs set LineManager_Approval = 1 where Email =?''', self.Email)
                connect.commit()
            if self.LineManager_Approval == False:
                cursor.execute('''update employeereqs set LineManager_Approval = 0 where Email =?''', self.Email) 
                cursor.execute('''update employeereqs set Reason_for_Decline = "Traffic" where Email =?''', self.Email)  
            return redirect('/allrequests')
api.add_resource(linemanager,'/allrequests/viewrequest/<string:Email>/linemanagerapproval')


#  6)Endpoint name -> DownloadRequestEndpoint
#    inputData-> Token
#    outputData-> File
#     Logic-> The request will be downloaded in a csv. format.

class downloadreq(Resource):

    def __init__(self, Email=''):
        self.Email= Email
    import pandas as pd
    import pyodbc
    def get(self,Email=''):
        self.Email=Email
        
        connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=employeedb;'
            'Trusted_Connection=yes;')
        test1 = pd.read_sql_query('''select *from employeereqs where Email = '''+Email, connect)
        df = pd.DataFrame(test1)
        df.to_csv(Email+".csv")
        return redirect('/allrequests')

api.add_resource(downloadreq, '/allrequests/viewrequest/<string:Email>/linemanagerapproval/download')

     


if __name__ == '__main__':
    app.run(debug =True)
#loopholes
#active directory
# can not pick days that consecutively follow friday and monday
# eg. Monday and Friday, Mondays and Tuesday
# line manager can not approve his own request, needs to be sent to a line manager of another department
#can not yet select whcich request to view
#uses static viewing
