# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:17:29 2022

@author: hp
"""

from xmlrpc.client import Boolean, boolean
from sqlalchemy import create_engine
import pypyodbc as odbc 
import pyodbc
import pandas as pd
from flask import Flask,jsonify
from flask_restful import Api,Resource
from hashlib import sha256
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
cursor = connect.cursor()
email='chiamakaogbuefi@gmail.com'
password=hash('chiamaka')
app=Flask(__name__)
api=Api(app)
class login(Resource):
    def get(self):
        cursor = connect.cursor()
        self.email=email
        self.password=password
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
                    #take them line manger endpoint passed here
                if(status=="employee"):
                    employedas="you are an employee"
                cursor.execute("update [employeedb].[chidubem].[employe] set token = 1 where email =? ",(self.email))
                connect.commit()
                connectstat=" and you have been connected succesfully"
            else:
                connectstat="incorrect password"
        else:
            connectstat= "user does not exist"
        return employedas + ""+connectstat
api.add_resource(login,'/login')
class scheduledays(Resource):
    def post(self,Monday,Tuesday,Wednesday,Thursday,Friday):
        self.email=email
        y=cursor.execute("select token from [employeedb].[chidubem].[employe]  where email=? ",(self.email))
        for a in y:
            pass
        newexpiry=int(a[0])
        if (newexpiry==1):
            x=0
            self.Monday=Monday
            self.Tuesday=Tuesday
            self.Wednesday=Wednesday
            self.Thursday=Thursday
            self.Friday=Friday
            days=[self.Monday,self.Tuesday,self.Wednesday,self.Thursday,self.Friday]
            for i in days:
                if(i==1):
                    x=x+1
            if(x>2):
                return("Error you chose more than the required amount of days required to work remotely please select only two days ")
            else:
                cursor.execute("update [employeedb].[chidubem].[employe] set monday = ? where email =? ",(self.Monday,self.email))
                cursor.execute("update [employeedb].[chidubem].[employe] set tuesday = ? where email =? ",(self.Tuesday,self.email))
                cursor.execute("update [employeedb].[chidubem].[employe] set wednesday = ? where email =? ",(self.Wednesday,self.email))
                cursor.execute("update [employeedb].[chidubem].[employe] set thursday = ? where email =? ",(self.Thursday,self.email))
                cursor.execute("update [employeedb].[chidubem].[employe] set friday = ? where email =? ",(self.Friday,self.email))
                connect.commit()
                self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
                return(self.days)
        else:
            return"your session has expired"
    def patch(self,Monday,Tuesday,Wednesday,Thursday,Friday):
        y=cursor.execute("select token from [employeedb].[chidubem].[employe]  where email=? ",(self.email))
        for a in y:
            pass
        newexpiry=int(a[0])
        if (newexpiry==1):
            x=0
            self.Monday=Monday
            self.Tuesday=Tuesday
            self.Wednesday=Wednesday
            self.Thursday=Thursday
            self.Friday=Friday
            days=[self.Monday,self.Tuesday,self.Wednesday,self.Thursday,self.Friday]
            for i in days:
                if(i==1):
                    x=x+1
            if(x>2):
                return("Error you chose more than the required amount of days required to work remotely please select only two days ")
            else:
                cursor.execute("update [employeedb].[chidubem].[employe] set monday = ? where email =? ",(self.Monday,self.email))
                cursor.execute("update [employeedb].[chidubem].[employe] set tuesday = ? where email =? ",(self.Tuesday,self.email))
                cursor.execute("update [employeedb].[chidubem].[employe] set wednesday = ? where email =? ",(self.Wednesday,self.email))
                cursor.execute("update [employeedb].[chidubem].[employe] set thursday = ? where email =? ",(self.Thursday,self.email))
                cursor.execute("update [employeedb].[chidubem].[employe] set friday = ? where email =? ",(self.Friday,self.email))
                connect.commit()
                self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
                return(self.days)
        else:
            return"your session has expired"
api.add_resource(scheduledays,"/scheduleddays/<int:Monday>/<int:Tuesday>/<int:Wednesday>/<int:Thursday>/<int:Friday>")
class logout(Resource):
    def post(self):
            self.email=email
            cursor.execute("update [employeedb].[chidubem].[employe] set token = 0 where email =? ",(self.email))
            connect.commit()
            loggedout=cursor.execute("select token from [employeedb].[chidubem].[employe] where email=?",(self.email))
            for i in loggedout:
                pass
            a=i[0]
            success=int(a)
            if(success==0):
                return("you have been logged out succefully")
            else:
                return("error login out")
        #pass in the login page
api.add_resource(logout,'/logout')
class linemanager(Resource):
    def get(self):
        self.email=email
        linemanagerresponse=cursor.execute("select response from [employeedb].[chidubem].[employe] where email=?",(self.email))
        for i in linemanagerresponse:
            pass
        a=i[0]
        if(a=='approved'):
            return("your response has been approved")
        else:
            return("your response has been denied and you are required to schedule your new remote days of work")
api.add_resource(linemanager,"/linemanager")

if __name__ =="__main__":
    app.run(debug=True)