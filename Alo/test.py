#import pymysql

# connection =pymysql.connect(host='localhost', user='sa', passwd='sa')

# cursor = connection.cursor()
# sql = "INSERT INTO `employeetb` (`userid`,`Firstname`,`Lastname`,`staffID`) VALUES(%s, %s, %s, %s)"

# cursor.execute(sql, (5,'Pese','Alo','IND19'))
# connection.commit()

# sql = "SELECT FROM `employeetb`"
# cursor.execute(sql)

# result = cursor.fetchall()
# for i in result:
#     print(i)
# from msilib.schema import SelfReg
# import urllib
# from xmlrpc.client import Boolean, boolean
# from sqlalchemy import create_engine
# import pypyodbc as odbc 
# import pandas as pd
# from flask import Flask,jsonify
# from flask_restful import Api,Resource 
# def get(self):
#         #function to submit days
#         SERVER='DESKTOP-IEVPBEO'
#         DATABASE='employeedb'
#         DRIVER='SQL Server Native Client 11.0'
#         USERNAME='chidubem'
#         PASSWORD='ogbuefi'
#          #connecting to the databasE
#         connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
#         engine = create_engine(connection_string)
#         connection=engine.connect()
#         finalogb=pd.read_sql_query('''SELECT * FROM [employeedb].[chidubem].[employe]''',connection)
#         #modifying the days
#         finalogb.iloc[0,5]=int(bool(self.Monday))
#         finalogb.iloc[0,6]=int (bool (self.Tuesday))
#         finalogb.iloc[0,7]=int(bool (self.Wednesday))
#         finalogb.iloc[0,8]=int(bool (self.Thursday))
#         finalogb.iloc[0,9]=int(bool (self.Friday))
#         #storing the new data in sql
#         finalogb.to_sql('employe',con=engine,if_exists='replace',index=False)
#         return(self.days)
# get(self)

import urllib
from urllib import response
from xmlrpc.client import Boolean, boolean
from sqlalchemy import create_engine
import pypyodbc as odbc 
import pandas as pd
from flask import Flask,jsonify,redirect
from flask_restful import Api,Resource
import requests
app=Flask(__name__)
api=Api(app)
SERVER='PESES-LAPTOP'
DATABASE='beginnercmd'
DRIVER='SQL Server Native Client 11.0'
USERNAME='sa'
PASSWORD='sa'
class scheduledays(Resource):
    def __init__(self):
        self.Monday=''
        self.Tuesday=''
        self.Wednesday=''
        self.Thursday=''
        self.Friday=''
        self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
    def post(self):
        return(self.days)
        #function to schedule days
    def get(self):
        self.Monday='1'
        self.Tuesday='1'
        self.Wednesday='1'
        self.Thursday='1'
        self.Friday='1'
         #connecting to the databasE
        self.connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
        self.engine = create_engine(self.connection_string)
        self.connection=self.engine.connect()
        finalogb=pd.read_sql_query('''SELECT * FROM [employeedb].[dbo].[employeetable1]''',self.connection)
        #modifying the days
        finalogb.iloc[0,5]=int(bool(self.Monday))
        finalogb.iloc[0,6]=int (bool (self.Tuesday))
        finalogb.iloc[0,7]=int(bool (self.Wednesday))
        finalogb.iloc[0,8]=int(bool (self.Thursday))
        finalogb.iloc[0,9]=int(bool (self.Friday))
        #storing the new data in sql
        finalogb.to_sql('employeetable1',con=self.engine,if_exists='replace',index=False)
        self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
        return(self.days)
    def patch(self):
        self.connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
        self.engine = create_engine(self.connection_string)
        self.connection=self.engine.connect()
        finalogb=pd.read_sql_query('''SELECT * FROM [employeedb].[dbo].[employeetable1]''',self.connection)
        #modifying the days
        finalogb.iloc[0,5]=int(bool(self.Monday))
        finalogb.iloc[0,6]=int (bool (self.Tuesday))
        finalogb.iloc[0,7]=int(bool (self.Wednesday))
        finalogb.iloc[0,8]=int(bool (self.Thursday))
        finalogb.iloc[0,9]=int(bool (self.Friday))
        #storing the new data in sql
        finalogb.to_sql('employeetable1',con=self.engine,if_exists='replace',index=False)
        self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
        return(self.days)

api.add_resource(scheduledays,'/scheduleddays')
class sqlconnector(Resource):
    def get(self):
        #sql database

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
api.add_resource(sqlconnector,"/allrequests")

class viewrequests(Resource):
# 3) Endpoint name -> ViewRequestEndpoint
#    inputData-> Token
#    outputData-> Shows the selected request
#     Logic-> Once the endpoint is hit, the app returns the page that shows the selected request
    
    def get(self):
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
        SQL_Query=pd.read_sql_query('''select *from employeereqs where userid = 1''',readdata)
        #storing sql database in python
        finaldatabase=SQL_Query.head()
        #coverting the table to a dictionar
        vrequests= finaldatabase.to_dict('records')
        return(vrequests)

api.add_resource(viewrequests,'/allrequests/viewrequest1')

class teamapproval(Resource):
# 4) Endpoint name -> TeamLeadApprovalEndpoint
#    inputData-> Token Response give reason for decline
#    outputData-> 
#     Logic-> If it is declined, forwards the response to the sender of the request and goes back to the show all requests page 
# 	      If it is approved, forwards the request to the Line manager and goes back to the show all page
    def __init__(self):
        self.TeamLead_Approval=''
        self.Reason_for_Decline=''
        self.approval={'Approvals':bool(self.TeamLead_Approval), 'Reason for Decline':str(self.Reason_for_Decline)}
    

        # return(self.approval)

    
    def patch(self):
        
            import pyodbc 
            connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=employeedb;'
            'Trusted_Connection=yes;')

            cursor = connect.cursor()
            if self.TeamLead_Approval == True:
                cursor.execute('''update employeereqs set TeamLead_Approval = 1 where userid =3''')
                connect.commit()
            if self.TeamLead_Approval == False:
                cursor.execute('''update employeereqs set TeamLead_Approval = 0 where userid =3''') 
                cursor.execute('''update employeereqs set Reason_for_Decline = "Traffic" where userid =3''')  
            return redirect('/allrequests')
api.add_resource(teamapproval,'/allrequests/viewrequest1/teamleadapproval')


# class linemanager(Resource):
#     def get(self):
#         linemanagerresponse=False
#         if (linemanagerresponse==False):
#             #returning the updtae function
#             response=requests.patch("http://127.0.0.1:5000/scheduledays")
#             print(response.json())
# api.add_resource(linemanager,"/linemanager")


if __name__ =="__main__":
    app.run(debug=True)

# import pyodbc 
# connect = pyodbc.connect('Driver={SQL Server};'
# 'Server=PESES-LAPTOP;'
# 'Database=employeedb;'
# 'Trusted_Connection=yes;')

# cursor = connect.cursor()

# cursor.execute('''INSERT INTO employeetable1 VALUES (4,'oluwapse.lo@wemabank.com', 'peseao','IT',0 , 0, 1, '0', 0, 1, 1, 1, 1, 1)''')
# connect.commit()