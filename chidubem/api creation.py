# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:17:29 2022

@author: hp
"""

from urllib import request
from xmlrpc.client import Boolean, boolean
from sqlalchemy import create_engine
import pypyodbc as odbc 
import pyodbc
import pandas as pd
from flask import Flask,jsonify,redirect,request
from flask_restful import Api,Resource
from hashlib import sha256
import json
#function to hash password
def hash(data):
        hash_var=sha256((data).encode())
        finalhash=hash_var.hexdigest()
        return finalhash
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
cursor = connect.cursor()
app=Flask(__name__)
api=Api(app)
class login(Resource):
    def post(self):
        email_pass=request.get_json()
        cursor = connect.cursor()
        self.email=email_pass['email']
        password=hash(email_pass['password'])
        self.connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
        self.engine = create_engine(self.connection_string)
        self.connection=self.engine.connect()
        sqltable=pd.read_sql_query('''SELECT * FROM [employeedb].[chidubem].[employe]''',self.connection)
        finaltable1=pd.DataFrame(sqltable)
        emailauthentication=(self.email in finaltable1['email'].unique())
        if (emailauthentication==True):
            passwordauthentication=(password in finaltable1['password'].unique())
            if (passwordauthentication==True):
                cursor = connect.cursor()
                normalemployee=cursor.execute("select [normal employee] from [employeedb].[chidubem].[employe] where email=? ",self.email)
                for i in normalemployee:
                    pass
                status=i[0]
                if (status=="line manager"):
                    employedas="you are a line manager"
                    #redirct(/"linemanager")
                    #take them line manger endpoint passed here
                elif(status=="employee"):
                    #redirect(/"employee")
                    employedas="you are an employee"
                else:
                    employedas="you dont have a role yet"
                cursor.execute("update [employeedb].[chidubem].[employe] set token = 1 where email =? ",(self.email))
                connect.commit()
                connectstat=" and you have been connected succesfully"
            else:
                employedas=""
                connectstat="incorrect password"
        else:
            employedas=""
            connectstat= "user does not exist"
        return employedas + ""+connectstat
api.add_resource(login,'/login')
class scheduledays(Resource):
    def post(self):
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
                return(self.days)
            except:
                return("could not update scheduled days")
    def patch(self,Monday,Tuesday,Wednesday,Thursday,Friday):
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
                return(self.days)
            except:
                return("could not update scheduled days")
api.add_resource(scheduledays,"/scheduleddays")
class logout(Resource):
    def post(self,email):
            self.email=email
            loggedout=cursor.execute("select token from [employeedb].[chidubem].[employe] where email=?",(self.email))
            for i in loggedout:
                pass
            a=i[0]
            success=int(a)
            if(success==0):
                #redirect('/login')
                return("you have been logged out succefully")
            else:
                return("error login out")
            
        #pass in the login page
api.add_resource(logout,'/logout/<string:email>')
# class linemanager(Resource):
#     def get(self):
#         #passed after login
#         self.email=email
#         linemanagerresponse=cursor.execute("select response from [employeedb].[chidubem].[employe] where email=?",(self.email))
#         for i in linemanagerresponse:
#             pass
#         a=i[0]
#         if(a=='approved'):
#             return("your response has been approved")
#         else:
#             return("your response has been denied and you are required to schedule your new remote days of work")
# api.add_resource(linemanager,"/linemanager")
if __name__ =="__main__":
    app.run(debug=True)