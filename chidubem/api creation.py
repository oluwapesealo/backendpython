# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:17:29 2022

@author: hp
"""
from asyncio.windows_events import NULL
from datetime import datetime,timedelta
from urllib import request
from sqlalchemy import create_engine
import pypyodbc as odbc 
import pyodbc
import pandas as pd
from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from hashlib import sha256
import jwt
import os
from dotenv import load_dotenv
load_dotenv()
#function to hash password
def hash(data):
        hash_var=sha256((data).encode())
        finalhash=hash_var.hexdigest()
        return finalhash
def tokenauthent(email,key):
        if 'tokenauth' in request.headers:
                token = request.headers['tokenauth']
                tokget=cursor.execute("select token from [employeedb].[chidubem].[employe] where email=?",email)
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

SERVER='DESKTOP-IEVPBEO'
DATABASE='employeedb'
DRIVER='SQL Server Native Client 11.0'
USERNAME='chidubem'
PASSWORD='ogbuefi'
connect = pyodbc.connect('Driver={SQL Server};'
            'Server=DESKTOP-IEVPBEO;'
            'Database=employeedb;'
            'Trusted_Connection=yes;')
connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
# connection_string=f'mssql://{str(os.getenv("USERNAME"))}:{str(os.getenv("PASSWORD"))}@{str(os.getenv("SERVER"))}/{str(os.getenv("DATABASE"))}?driver={str(os.getenv("DRIVER"))}'
cursor = connect.cursor()
app=Flask(__name__)
api=Api(app)
class login(Resource):
    def post(self):
        email_pass=request.get_json()
        cursor = connect.cursor()
        self.email=email_pass['email']
        password=hash(email_pass['password'])
        self.connection_string=connection_string
        self.engine = create_engine(self.connection_string)
        self.connection=self.engine.connect()
        sqltable=pd.read_sql_query(str(os.getenv("selectall")),self.connection)
        finaltable1=pd.DataFrame(sqltable)
        emailauthentication=(self.email in finaltable1['email'].unique())
        if (emailauthentication==True):
            passwordauthentication=(password in finaltable1['password'].unique())
            if (passwordauthentication==True):
                cursor = connect.cursor()
                normalemployee=cursor.execute(str(os.getenv("normalemployee")),self.email)
                for i in normalemployee:
                    pass
                status=i[0]
                if (status=="line manager"):
                    key=str(os.getenv("key"))
                    encodedtoken = jwt.encode({
                     'email': self.email,
                     "status":"line manager",
                     "message":"you are connected",
                    'expiration': str(datetime.utcnow() + timedelta(seconds=999))
                    },key)
                    cursor.execute(str(os.getenv("updatetoken")),str(encodedtoken),self.email)
                    connect.commit()
                elif(status=="employee"):
                    key=str(os.getenv("key"))
                    encodedtoken = jwt.encode({
                     'email': self.email,
                     "status":"employee",
                     "message":"connected",
                    'expiration': str(datetime.utcnow() + timedelta(seconds=999))
                    },key)
                    cursor.execute("update [employeedb].[chidubem].[employe] set token=? where email=?",str(encodedtoken),self.email)
                    connect.commit()
            
            else:
                
                return {"message":"incorrect password"}
        else:
            
            return {"message":"user does not exist"}
        return  jwt.decode(encodedtoken, key=str(os.getenv("key")), algorithms=['HS256', ])
api.add_resource(login,'/login')
class scheduledays(Resource):
    def post(self):
        data=request.get_json()
        self.email=data['email']
        tokenfunc=tokenauthent(self.email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            data=request.get_json()
            self.email=data['email']
            x=0
            self.Monday=data['Monday']
            self.Tuesday=data['Tuesday']
            self.Wednesday=data['Wednesday']
            self.Thursday=data['Thursday']
            self.Friday=data['Friday']
            days=[self.Monday,self.Tuesday,self.Wednesday,self.Thursday,self.Friday]
            for i in days:
                if(i==1):
                    x=x+1
            if (self.Monday==1 and self.Tuesday==1):
                return "you cannot pick consecutive days that follow monday and friday"
            elif (self.Monday==1 and self.Friday==1):
                return "you cannot pick consecutive days that follow monday and friday"
            elif (self.Thursday==1 and self.Friday==1):
                return "you cannot pick consecutive days that follow monday and friday"           
            elif(x>2):
                return("Error you chose more than the required amount of days required to work remotely please select only two days ")
            else:
                try:
                    cursor.execute("update [employeedb].[chidubem].[employe] set monday = ? where email =? ",(self.Monday,self.email))
                    cursor.execute("update [employeedb].[chidubem].[employe] set tuesday = ? where email =? ",(self.Tuesday,self.email))
                    cursor.execute("update [employeedb].[chidubem].[employe] set wednesday = ? where email =? ",(self.Wednesday,self.email))
                    cursor.execute("update [employeedb].[chidubem].[employe] set thursday = ? where email =? ",(self.Thursday,self.email))
                    cursor.execute("update [employeedb].[chidubem].[employe] set friday = ? where email =? ",(self.Friday,self.email))
                    connect.commit()
                    self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
                    return{"message":"token is valid and scheduleddays assinged succefully"}
                except:
                    return{"message":("could not update scheduled days")}
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
            return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}
    def patch(self,Monday,Tuesday,Wednesday,Thursday,Friday):
        data=request.get_json()
        self.email=data['email']
        tokenfunc=tokenauthent(self.email,os.getenv("key"))
        if (tokenfunc['message']=="token is valid"):
            data=request.get_json()
            self.email=data['email']
            x=0
            self.Monday=data['Monday']
            self.Tuesday=data['Tuesday']
            self.Wednesday=data['Wednesday']
            self.Thursday=data['Thursday']
            self.Friday=data['Friday']
            days=[self.Monday,self.Tuesday,self.Wednesday,self.Thursday,self.Friday]
            for i in days:
                if(i==1):
                    x=x+1
            if (self.Monday==1 and self.Tuesday==1):
                return "you cannot pick consecutive days that follow monday and friday"
            elif (self.Monday==1 and self.Friday==1):
                return "you cannot pick consecutive days that follow monday and friday"
            elif (self.Thursday==1 and self.Friday==1):
                return "you cannot pick consecutive days that follow monday and friday"           
            elif(x>2):
                return("Error you chose more than the required amount of days required to work remotely please select only two days ")
            else:
                try:
                    cursor.execute("update [employeedb].[chidubem].[employe] set monday = ? where email =? ",(self.Monday,self.email))
                    cursor.execute("update [employeedb].[chidubem].[employe] set tuesday = ? where email =? ",(self.Tuesday,self.email))
                    cursor.execute("update [employeedb].[chidubem].[employe] set wednesday = ? where email =? ",(self.Wednesday,self.email))
                    cursor.execute("update [employeedb].[chidubem].[employe] set thursday = ? where email =? ",(self.Thursday,self.email))
                    cursor.execute("update [employeedb].[chidubem].[employe] set friday = ? where email =? ",(self.Friday,self.email))
                    connect.commit()
                    self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
                    return{"message":"token is valid and scheduleddays assinged succefully"}
                except:
                    return{"message":("could not update scheduled days")}
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}
        else:
            return{"message":"token not inlcuded"}
api.add_resource(scheduledays,"/scheduleddays")
class logout(Resource):
    def post(self):
            data=request.get_json()
            self.email=data['email']
            loggedout=cursor.execute("select token from [employeedb].[chidubem].[employe] where email=?",(self.email))
            for i in loggedout:
                pass
            token=i[0]
            decodedtoken=jwt.decode(token,key=str(os.getenv("key")), algorithms=['HS256'])
            decodedtoken['expiration']=str(datetime.utcnow() - timedelta(seconds=999))
            loggedouttoken=jwt.encode((decodedtoken),key=str(os.getenv("key")))
            try:
                cursor.execute("update [employeedb].[chidubem].[employe] set token=? where email=?",str(loggedouttoken),self.email)
                connect.commit()
                return{"message":"you have been logged out succefully"}
            except:
                return{"message":"error login you out"}
            
        #pass in the login page
api.add_resource(logout,'/logout')



# IDENTITY MANAGEMENT


class roles(Resource):
    def get(self):
        data=request.get_json()
        self.email=data['email']
        tokenfunc=tokenauthent(self.email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            # to return available roles
            x=cursor.execute("Select [roles] , [Description_] FROM [employeedb].[dbo].[Roles] ")
            roles=[]
            for row in x:
                roles.append({"role" :row[0],"Description":row[1]})
            return jsonify(roles)
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
            return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}

    def post(self):
        data=request.get_json()
        self.email=data['email']
        tokenfunc=tokenauthent(self.email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            try:
                cursor.execute("INSERT INTO [employeedb].[dbo].[Roles] (Roles, DesignationID,Description_) VALUES (?, ?,?)",(data['Role'],data['DesignationID'],data['Description']))
                connect.commit()
                return{"message":"role added succesfully"}
            except:
                return {"message":"failed to add role"}

        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
            return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}

api.add_resource(roles,"/roles")
class designtion(Resource):
    def get(self):
        data=request.get_json()
        self.email=data['email']
        tokenfunc=tokenauthent(self.email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            # to return available roles
            x=cursor.execute("Select [Designation],[Description_] FROM [employeedb].[dbo].[Designation] ")
            roles=[]
            for row in x:
                roles.append({"Description":row[1],"Designation":row[0]})
            return jsonify(roles)
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
                return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}
    def post(self):
        data=request.get_json()
        self.email=data['email']
        tokenfunc=tokenauthent(self.email,str(os.getenv("key")))
        if (tokenfunc['message']=="token is valid"):
            try:
                cursor.execute("INSERT INTO [employeedb].[dbo].[Designation] (Designation,Description_) VALUES (?, ?)",(data['Designation'],data['Description']))
                connect.commit()
                return{"message":"desingtion added succesfully"}
            except:
                return {"message":"failed to add destination"}
        elif (tokenfunc['message']=="token expired"):
            return{"message":"token expired"}

        elif(tokenfunc['message']=="token verification failed"):
                return{"message":"token verification failed"}

        else:
            return{"message":"token not inlcuded"}
api.add_resource(designtion,"/designation")
if __name__ =="__main__":
    app.run(debug=True)
    