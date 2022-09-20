
from flask import Flask, request, redirect, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS 
import pypyodbc as odbc 
import pandas as pd
import pyodbc
import requests
import os
from hashlib import sha256
import datetime
import jwt
from dotenv import load_dotenv
load_dotenv
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

app.config['SECRET_KEY'] = 'oluwapesealo'

def tokenauthent(Email,key):
        if 'tokenauth' in request.headers:
                token = request.headers['tokenauth']
                tokget=cursor.execute(os.getenv("tokenselect"),Email)
                for ai in tokget:
                    pass
                if(bool(ai[0])==True):
                    try:
                        decodedtoken=jwt.decode(ai[0], key=key, algorithms=['HS256', ])
                        if(decodedtoken['expiration']<str(datetime.utcnow())):
                            return{"message":"token expired"}
                        else:
                            return {"token":ai[0],"message":"token is valid"}
                    except:
                        return{"message":"token verification failed"}
        else:
            return{"message":"token not included"}

SERVER='PESES-LAPTOP'
DATABASE='wemabank'
DRIVER='SQL Server Native Client 11.0'
USERNAME='sa'
PASSWORD='sa'
connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=wemabank;'
            'Trusted_Connection=yes;')
connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
# connection_string=f'mssql://{str(os.getenv("USERNAME"))}:{str(os.getenv("PASSWORD"))}@{str(os.getenv("SERVER"))}/{str(os.getenv("DATABASE"))}?driver={str(os.getenv("DRIVER"))}'
cursor = connect.cursor()
#1) Endpoint name -> CreateEndpoint
#    inputData-> Username, password, department, position
#    outputData-> token generated
#     Logic-> Creates new user
class employees(Resource):

    def post(self, Email=''):
        self.Email=Email
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            content_type = request.headers.get('Content-Type')
            if (content_type == 'application/json'):
                json = request.get_json()
                print (json)
            else:
                return 'Content-Type not supported!'
            email = '?' , self.Email 

            name, _, _ = email.partition("@")  # returns before @, @, and after @
            fullname = name.split(".")        # splits on .

            drivername='SQL SERVER'
            servername='PESES-LAPTOP'
            database='wemabank'
            connection_string=f"""
            DRIVER={{{drivername}}};
            SERVER={servername};
            DATABASE={database};
            Trust_Connection=yes;
                """ 
            #connecting to the database
            readdata=odbc.connect(connection_string)
            #to read from sql database
            SQL_Query=pd.read_sql_query('''select Email from Staff''',readdata)
            #storing sql database in python
            #coverting the table to a dictionar
            emailtable= pd.DataFrame(SQL_Query)

            connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=wemabank;'
            'Trusted_Connection=yes;')
            
            Password=hash(json['unhashedpassword'])

            cursor = connect.cursor()
            emailexist=(json["Email"] in emailtable['email'].unique())
            if (emailexist==True):
                return "Email already exists "
            else:
                cursor.execute('''INSERT INTO Staff VALUES (?,?,?,?,?, NULL,NULL, ? )''',(json["StaffID"], json["Email"],Password, fullname, json["UnitID"],  json["DesignationID"]))
                connect.commit()
                success='sign up was successful'
                return success
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
            return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}
api.add_resource(employees,'/createemployee')

# def tokenauth():
#     auth = request.authorization
#     if auth and auth.password == 'Password':
#        token = jwt.encode({'user':auth.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60) }, app.config['SECRET_KEY'])

#        return jsonify({'message':'Token is valid, continue'})

class updateinfo(Resource):
    def patch(self):
        pass

# 2) Endpoint name -> ShowallRequestsEndpoint
#    inputData-> Token	
#    outputData-> Displays all the requests sent by employees
#     Logic-> Once the endpoint is hit, the app returns the page that shows all the requests received by employees   
class alltasks(Resource):
    def get(self, Email):
        self.Email=Email
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            drivername='SQL SERVER'
            servername='PESES-LAPTOP'
            database='wemabank'
            connection_string=f"""
            DRIVER={{{drivername}}};
            SERVER={servername};
            DATABASE={database};
            Trust_Connection=yes;
                """ 
            readdata=odbc.connect(connection_string)
            SQL_Query=pd.read_sql_query('''SELECT * FROM ScheduleDays''',readdata)
            requests= SQL_Query.to_dict('records')
            return(requests)
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
            return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}

api.add_resource(alltasks,'/alltasks')


class alltasks(Resource):

    def get(self,Email='', UnitID = ''):
        self.Email=Email
        self.UnitID=UnitID
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            drivername='SQL SERVER'
            servername='PESES-LAPTOP'
            database='wemabank'
            connection_string=f"""
            DRIVER={{{drivername}}};
            SERVER={servername};
            DATABASE={database};
            Trust_Connection=yes;
                """ 
            readunit =  odbc.connect(connection_string)
            UnitID = pd.read_sql_query('''select UnitID  where Email =?'''+Email,readunit)
            readdata=odbc.connect(connection_string)
            SQL_Query=pd.read_sql_query('''select Staff.Fullname, Unit.Unit, Staff.Email, Roles.Roles, ScheduleDays.LineManager_Approval , ScheduleDays.DateSent

                                            from Staff
                                            Left Join Unit
                                            On  Staff.UnitID = Unit.UnitID
                                            Left Join Roles
                                            On Staff.RolesID = Roles.RolesID
                                            Left Join ScheduleDays
                                            On Staff.StaffID = ScheduleDays.StaffID;

                                            where UnitID ='''+UnitID, readdata,)
            vrequests= SQL_Query.to_dict('records')
            return(vrequests)
        
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
            return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}
    
api.add_resource(alltasks,'/alltasks/<string:Email>')


# 3) Endpoint name -> ViewRequestEndpoint
#    inputData-> Token
#    outputData-> Shows the selected request
#     Logic-> Once the endpoint is hit, the app returns the page that shows the selected request
# requests={}
class viewtask(Resource):

    def get(self,Email=''):
        self.Email=Email
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            drivername='SQL SERVER'
            servername='PESES-LAPTOP'
            database='wemabank'
            connection_string=f"""
            DRIVER={{{drivername}}};
            SERVER={servername};
            DATABASE={database};
            Trust_Connection=yes;
                """ 
            readdata=odbc.connect(connection_string)
            SQL_Query=pd.read_sql_query('''select *from ScheduleDays where Email ='''+Email, readdata,)
            vtask= SQL_Query.to_dict('records')
            return(vtask)
        
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
            return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}
    
api.add_resource(viewtask,'/allrequests/viewrequest/<string:Email>')





# 4) Endpoint name -> TeamLeadApprovalEndpoint
#    inputData-> Token Response give reason for decline
#    outputData-> 
#     Logic-> If it is declined, forwards the response to the sender of the request and goes back to the show all requests page 
# 	      If it is approved, forwards the request to the Line manager and goes back to the show all page
class teamapproval(Resource):

    def patch(self, Email='', TeamLead_Approval='',Reason_For_Decline=''):
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            self.Email=Email
            self.TeamLead_Approval=TeamLead_Approval
            self.Reason_For_Decline= Reason_For_Decline
            connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=wemabank;'
            'Trusted_Connection=yes;')

            cursor = connect.cursor()
            if self.TeamLead_Approval == True:
                cursor.execute('''update ScheduleDays set TeamLead_Approval = 1 where Email =?''', self.Email)
                connect.commit()
            if self.TeamLead_Approval == False:
                cursor.execute('''update ScheduleDays set TeamLead_Approval = 0 where Email =?''', self.Email) 
                cursor.execute('''update ScheduleDays set Reason_for_Decline = ? where Email =?''', self.Email, self.Reason_For_Decline )  
            return redirect('/allrequests')

        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
            return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}
api.add_resource(teamapproval,'/alltasks/viewtask/<string:Email>/teamleadapproval')

# 5) Endpoint name -> LineManagerApprovalEndpoint
#    inputData-> Response and give reason for decline
#    outputData-> gives the option to download the request
#     Logic-> If it is denied, forwards the response to the sender of the request and goes back to the show all requests page 
# 	      If it is approved, gives the user the option to download the approved request  

class linemanager(Resource):
    
    def patch(self, Email='', Linemanager_Approval='', Reason_For_LineManager_Decline=''):
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            self.Email=Email
            self.LineManager_Approval=Linemanager_Approval
            self.Reason_For_LineManager_Decline=Reason_For_LineManager_Decline
            connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=wemabank;'
            'Trusted_Connection=yes;')

            cursor = connect.cursor()
            if self.LineManager_Approval == True:
                cursor.execute('''update ScheduleDays set LineManager_Approval = 1 where Email =?

                                # set  RemoteWorkdays.Monday = Requests.Monday,
	                            # RemoteWorkdays.Tuesday = Requests.Tuesday,
	                            # RemoteWorkdays.Wednesday = Requests.Wednesday,
	                            # RemoteWorkdays.Thursday = Requests.Thursday,
	                            # RemoteWorkdays.Friday = Requests.Friday
                                # from Requests, RemoteWorkdays
                                # where Requests.RequestID = RemoteWorkdays.RequestID''', self.Email)
                connect.commit()
            if self.LineManager_Approval == False:
                cursor.execute('''update Requests set LineManager_Approval = 0 where Email =?''', self.Email) 
                cursor.execute('''update Requests set Reason_For_LineManager_Decline = ? where Email =?''', self.Email, self.Reason_For_LineManager_Decline)  
            return redirect('/allrequests')
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
            return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}
api.add_resource(linemanager,'/alltasks/viewtask/<string:Email>/linemanagerapproval')


#  6)Endpoint name -> DownloadRequestEndpoint
#    inputData-> Token
#    outputData-> File
#     Logic-> The request will be downloaded in a csv. format.

class downloadreq(Resource):
    def get(self,Email=''):
        self.Email=Email
        # tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        # if (tokenfunc['message']=="token is valid"):
        drivername='SQL SERVER'
        servername='PESES-LAPTOP'
        database='wemabank'
        connection_string=f"""
        DRIVER={{{drivername}}};
        SERVER={servername};
        DATABASE={database};
        Trust_Connection=yes;
            """ 
        readdata=odbc.connect(connection_string)
        SQL_Query=pd.read_sql_query('''select *from Requests where Email ='''+Email, readdata,)
        df = pd.DataFrame(SQL_Query)
        down = df.to_csv(Email+".csv")
        success = 'Download was successful'
        
        return down


    def donwload(url, filename=''):
        downloadurl = '/allrequests/viewrequest/<string:Email>/linemanagerapproval/download'
        if filename:
            pass
        else:
            filename = req.url[downloadurl.rfind('/')+1:]

        with requests.get(url) as req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size =8192):
                    if chunk:
                        f.write(chunk)
            return filename

        # elif (tokenfunc['message']=="token expired"):
        #     return{"message":"token expired"}

        # elif(tokenfunc['message']=="token verification failed"):
        #     return{"message":"token verification failed"}

        # else:
        #     return{"message":"token not inlcuded"}
api.add_resource(downloadreq, '/alltasks/viewtask/<string:Email>/linemanagerapproval/download')




#IDENTITY MANAGEMENT 



class units(Resource): 
    def get(self, Email=''):
        self.Email=Email
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            drivername='SQL SERVER'
            servername='PESES-LAPTOP'
            database='wemabank'
            connection_string=f"""
                DRIVER={{{drivername}}};
                SERVER={servername};
            DATABASE={database};
            Trust_Connection=yes;
                """ 
            readdata=odbc.connect(connection_string)
            SQL_Query=pd.read_sql_query('''Select Unit FROM Unit''', readdata)
            unit= SQL_Query.to_dict('records')
            
            units = (unit)
            return jsonify(units)


        

api.add_resource(units,"/units")

class departments(Resource):
    def get(self, Email=''):
        self.Email=Email
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            drivername='SQL SERVER'
            servername='PESES-LAPTOP'
            database='wemabank'
            connection_string=f"""
                DRIVER={{{drivername}}};
                SERVER={servername};
            DATABASE={database};
            Trust_Connection=yes;
                """ 
            readdata=odbc.connect(connection_string)
            SQL_Query=pd.read_sql_query('''Select Department FROM Department''', readdata)
            depart= SQL_Query.to_dict('records')
            
            departments =(depart)
            return jsonify(departments)
api.add_resource(departments,"/departments")

class newdepartments(Resource):

    def post(self,Email=''):
        self.Email=Email
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            content_type = request.headers.get('Content-Type')
            if (content_type == 'application/json'):
                json = request.get_json()
                print (json)
            else:
                return 'Error'
            connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=wemabank;'
            'Trusted_Connection=yes;')

            cursor = connect.cursor()
            cursor.execute('''INSERT INTO Department VALUES (?,?)''',(json["Department_name"], json["Description"]))
            
            connect.commit()
            success='Department created successfully'
            return success
api.add_resource(newdepartments,"/departments/new")

class newunits(Resource):
    def post(self,Email=''):
        self.Email=Email
        tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            content_type = request.headers.get('Content-Type')
            if (content_type == 'application/json'):
                json = request.get_json()
                print (json)
            else:
                return 'Error'
            connect = pyodbc.connect('Driver={SQL Server};'
            'Server=PESES-LAPTOP;'
            'Database=wemabank;'
            'Trusted_Connection=yes;')
            
            cursor = connect.cursor()
            cursor.execute('''INSERT INTO Unit VALUES (?,?,?)''',(json["Unit_name"], json["DepartmentID"], json["Description"]))
            
            connect.commit()
            success='Unit created successfully'
            return success

api.add_resource(newunits,"/units/new")

if __name__ == '__main__':
    app.run(debug =True)


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
