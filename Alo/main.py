import json
import re
from sqlalchemy import create_engine
from sqlite3 import Cursor
from flask import Flask, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS 
import pypyodbc as odbc 
import pandas as pd
import pyodbc
from hashlib import sha256
def hash(data):
        hash_var=sha256((data).encode())
        finalhash=hash_var.hexdigest()
        return finalhash

app = Flask(__name__)
api = Api(app)
CORS(app)
cors = CORS(app, resources={
    r"/*":{
        "origins": "*"
    }
})


#1) Endpoint name -> CreateEndpoint
#    inputData-> Username, password, department, position
#    outputData-> token generated
#     Logic-> Creates new user
class employees(Resource):
    # def __init__(self, Email='', unhashedpassword='', Department='', Status=''):
    #     self.Email= Email
    #     self.Password=unhashedpassword
    #     self.Department=Department
    #     self.Status=Status

    
    def post(self, Email='', unhashedpassword='', Department='', Status=''):
 
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()
            print (json)
        else:
            return 'Content-Type not supported!'
        
        connect = pyodbc.connect('Driver={SQL Server};'
        'Server=PESES-LAPTOP;'
        'Database=employeedb;'
        'Trusted_Connection=yes;')
        
#        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', unhashedpassword):
       # Password=hash(unhashedpassword)
 #       else:
  #          return 'Invalid Password'

        cursor = connect.cursor()
        cursor.execute('''INSERT INTO employeetable2 VALUES (?,?,?,?,'NULL', 'NULL', 'NULL', 0, 0, 0, 0, 0)''',(json["Email"], json["unhashedpassword"], json["Department"], json["Status"]))
        
        connect.commit()
        success='sign up was successful'
        return success
api.add_resource(employees,'/createemployee')


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
   # def __init__(self, Email=''):
   #     self.Email= Email

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
    # def __init__(self):
    #     self.TeamLead_Approval=''
    #     self.Reason_for_Decline=''
    #     self.approval={'Approval':bool(self.TeamLead_Approval), 'Reason for Decline':str(self.Reason_for_Decline)}
    

    #     # return(self.approval)

    
    def patch(self, Email='', TeamLead_Approval='',Reason_For_Decline=''):
            self.Email=Email
            self.TeamLead_Approval=TeamLead_Approval
            self.Reason_For_Decline= Reason_For_Decline
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
                cursor.execute('''update employeereqs set Reason_for_Decline = ? where Email =?''', self.Email, self.Reason_For_Decline )  
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

    
    def patch(self, Email='', Linemanager_Approval='', Reason_For_Decline=''):
            self.Email=Email
            self.LineManager_Approval=Linemanager_Approval
            self.Reason_for_Decline=Reason_For_Decline
            connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=employeedb;'
            'Trusted_Connection=yes;')

            cursor = connect.cursor()
            if self.LineManager_Approval == True:
                cursor.execute('''update employeereqs set LineManager_Approval = 1 where Email =?
                                update employeetable2

                                set  employeetable2.Monday = employeereqs.Monday,
	                            employeetable2.Tuesday = employeereqs.Tuesday,
	                            employeetable2.Wednesday = employeereqs.Wednesday,
	                            employeetable2.Thursday = employeereqs.Thursday,
	                            employeetable2.Friday = employeereqs.Friday
                                from employeereqs, employeetable2
                                where employeereqs.Email = employeetable2.Email''', self.Email)
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

    # def __init__(self, Email=''):
    #     self.Email= Email
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

# SERVER='PESES-LAPTOP'
# DATABASE='employeedb'
# DRIVER='SQL Server Native Client 11.0'
# USERNAME='sa'
# PASSWORD='sa'
# connect = pyodbc.connect('Driver={SQL Server};'
#             'Server=PESES-LAPTOP;'
#             'Database=employeedb;'
#             'Trusted_Connection=yes;')
# connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
# cursor = connect.cursor()
# # app=Flask(__name__)
# # api=Api(app)
# class login(Resource):
#     def get(self,Email='',unhashedpassword=''):
#         cursor = connect.cursor()
#         self.Email=Email
#         password=hash(unhashedpassword)
#         self.connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
#         self.ensgine = create_engine(self.connection_string)
#         self.connection=self.engine.connect()
#         sqltable=pd.read_sql_query('''SELECT * FROM employeetable2''',self.connection)
#         finaltable1=pd.DataFrame(sqltable)
#         emailauthentication=(self.Email in finaltable1['Email'].unique())
#         if (emailauthentication==True):
#             passwordauthentication=(password in finaltable1['Password'].unique())
#             if (passwordauthentication==True):
#                 # cursor = connect.cursor()
#                 # normalemployee=cursor.execute("select Status from employeetable2 where Email=? ",self.Email)
#                 # for i in normalemployee:
#                 #     pass
#                 # status=i[0]
#                 # if (status=="line manager"):
#                 #     employedas="you are a line manager"
#                 #     #redirct(/"linemanager")
#                 #     #take them line manger endpoint passed here
#                 # elif(status=="employee"):
#                 #     #redirect(/"employee")
#                 #     employedas="you are an employee"
#                 # else:
#                 #     employedas="you dont have a role yet"
#                 # cursor.execute("update employeetable2 set token = 1 where Email =? ",(self.Email))
#                 # connect.commit()
               
#                 # connectstat=" and you have been connected succesfully"
#                 success = 'Welcome User'
#                 return success            
#             else:
#                 employedas=""
#                 connectstat="incorrect password"
#         else:
#             employedas=""
#             connectstat= "user does not exist"
#         return employedas + ""+connectstat
# api.add_resource(login,'/login')
# class scheduledays(Resource):
#     def post(self,email,Monday,Tuesday,Wednesday,Thursday,Friday):
#         self.email=email
#         y=cursor.execute("select token from [employeedb].[chidubem].[employe]  where email=? ",(self.email))
#         for a in y:
#             pass
#         newexpiry=int(a[0])
#         if (newexpiry==1):
#             x=0
#             self.Monday=Monday
#             self.Tuesday=Tuesday
#             self.Wednesday=Wednesday
#             self.Thursday=Thursday
#             self.Friday=Friday
#             days=[self.Monday,self.Tuesday,self.Wednesday,self.Thursday,self.Friday]
#             for i in days:
#                 if(i==1):
#                     x=x+1
#             if (self.Monday==1 and self.Tuesday==1):
#                 return "you cannot pick consecutive days that follow monday and friday"
#             elif (self.Monday==1 and self.Friday==1):
#                 return "you cannot pick consecutive days that follow monday and friday"
#             elif (self.Thursday==1 and self.Friday==1):
#                 return "you cannot pick consecutive days that follow monday and friday"           
#             elif(x>2):
#                 return("Error you chose more than the required amount of days required to work remotely please select only two days ")
#             else:
#                 cursor.execute("update [employeedb].[chidubem].[employe] set monday = ? where email =? ",(self.Monday,self.email))
#                 cursor.execute("update [employeedb].[chidubem].[employe] set tuesday = ? where email =? ",(self.Tuesday,self.email))
#                 cursor.execute("update [employeedb].[chidubem].[employe] set wednesday = ? where email =? ",(self.Wednesday,self.email))
#                 cursor.execute("update [employeedb].[chidubem].[employe] set thursday = ? where email =? ",(self.Thursday,self.email))
#                 cursor.execute("update [employeedb].[chidubem].[employe] set friday = ? where email =? ",(self.Friday,self.email))
#                 pddays=cursor.execute("select monday,tuesday,wednesday,thursday,friday FROM [employeedb].[chidubem].[employe]  where email=?",(self.email))
#                 xy=pd.DataFrame(pddays)
#                 self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
#                 return(self.days)
#         else:
#             return"your session has expired"
#     def patch(self,Monday,Tuesday,Wednesday,Thursday,Friday):
#         y=cursor.execute("select token from [employeedb].[chidubem].[employe]  where email=? ",(self.email))
#         for a in y:
#             pass
#         newexpiry=int(a[0])
#         if (newexpiry==1):
#             x=0
#             self.Monday=Monday
#             self.Tuesday=Tuesday
#             self.Wednesday=Wednesday
#             self.Thursday=Thursday
#             self.Friday=Friday
#             days=[self.Monday,self.Tuesday,self.Wednesday,self.Thursday,self.Friday]
#             for i in days:
#                 if(i==1):
#                     x=x+1
#             if(x>2):
#                 return("Error you chose more than the required amount of days required to work remotely please select only two days ")
#             else:
#                 cursor.execute("update [employeedb].[chidubem].[employe] set monday = ? where email =? ",(self.Monday,self.email))
#                 cursor.execute("update [employeedb].[chidubem].[employe] set tuesday = ? where email =? ",(self.Tuesday,self.email))
#                 cursor.execute("update [employeedb].[chidubem].[employe] set wednesday = ? where email =? ",(self.Wednesday,self.email))
#                 cursor.execute("update [employeedb].[chidubem].[employe] set thursday = ? where email =? ",(self.Thursday,self.email))
#                 cursor.execute("update [employeedb].[chidubem].[employe] set friday = ? where email =? ",(self.Friday,self.email))
#                 connect.commit()
#                 self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
#                 return(self.days)
#         else:
#             return"your session has expired"
# api.add_resource(scheduledays,"/scheduleddays/<string:email>/<int:Monday>/<int:Tuesday>/<int:Wednesday>/<int:Thursday>/<int:Friday>")
# class logout(Resource):
#     def post(self,email):
#             self.email=email
#             cursor.execute("update [employeedb].[chidubem].[employe] set token = 0 where email =? ",(self.email))
#             connect.commit()
#             loggedout=cursor.execute("select token from [employeedb].[chidubem].[employe] where email=?",(self.email))
#             for i in loggedout:
#                 pass
#             a=i[0]
#             success=int(a)
#             if(success==0):
#                 #redirect('/login')
#                 return("you have been logged out succefully")
#             else:
#                 return("error login out")
            
#         #pass in the login page
# api.add_resource(logout,'/logout/<string:email>')

     


if __name__ == '__main__':
    app.run(debug =True)
#loopholes
#active directory
# can not pick days that consecutively follow friday and monday
# eg. Monday and Friday, Mondays and Tuesday
# line manager can not approve his own request, needs to be sent to a line manager of another department
#can not yet select whcich request to view
#uses static viewing
