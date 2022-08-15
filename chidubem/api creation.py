# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:17:29 2022

@author: hp
"""
import urllib
from urllib import response
from xmlrpc.client import Boolean, boolean
from sqlalchemy import create_engine
import pypyodbc as odbc 
import pandas as pd
from flask import Flask,jsonify
from flask_restful import Api,Resource
import requests
app=Flask(__name__)
api=Api(app)
SERVER='DESKTOP-IEVPBEO'
DATABASE='employeedb'
DRIVER='SQL Server Native Client 11.0'
USERNAME='chidubem'
PASSWORD='ogbuefi'
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
        finalogb=pd.read_sql_query('''SELECT * FROM [employeedb].[chidubem].[employe]''',self.connection)
        #modifying the days
        finalogb.iloc[0,5]=int(bool(self.Monday))
        finalogb.iloc[0,6]=int (bool (self.Tuesday))
        finalogb.iloc[0,7]=int(bool (self.Wednesday))
        finalogb.iloc[0,8]=int(bool (self.Thursday))
        finalogb.iloc[0,9]=int(bool (self.Friday))
        #storing the new data in sql
        finalogb.to_sql('employe',con=self.engine,if_exists='replace',index=False)
        self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
        return(self.days)
    def patch(self):
        self.connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
        self.engine = create_engine(self.connection_string)
        self.connection=self.engine.connect()
        finalogb=pd.read_sql_query('''SELECT * FROM [employeedb].[chidubem].[employe]''',self.connection)
        #modifying the days
        finalogb.iloc[0,5]=int(bool(self.Monday))
        finalogb.iloc[0,6]=int (bool (self.Tuesday))
        finalogb.iloc[0,7]=int(bool (self.Wednesday))
        finalogb.iloc[0,8]=int(bool (self.Thursday))
        finalogb.iloc[0,9]=int(bool (self.Friday))
        #storing the new data in sql
        finalogb.to_sql('employe',con=self.engine,if_exists='replace',index=False)
        self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
        return(self.days)

api.add_resource(scheduledays,'/scheduleddays')
class sqlconnector(Resource):
    def get(self):
        #sql database

        drivername='SQL SERVER'
        servername='DESKTOP-IEVPBEO'
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
        SQL_Query=pd.read_sql_query('''SELECT * FROM[dbo].[employees]''',readdata)
        #storing sql database in python
        finaldatabase=SQL_Query.head()
        #coverting the table to a dictionar
        employee= finaldatabase.to_dict('records')
        return(employee)
api.add_resource(sqlconnector,"/sqldb")
class logout(Resource):
    def post(self):
        pass
    #pass in the login page

class linemanager(Resource):
    def get(self):
        linemanagerresponse=False
        if (linemanagerresponse==False):
            #returning the updtae function
            response=requests.patch("http://127.0.0.1:5000/scheduledays")
            print(response.json())
api.add_resource(linemanager,"/linemanager")


if __name__ =="__main__":
    app.run(debug=True)