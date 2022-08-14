# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:17:29 2022

@author: hp
"""
import urllib
from xmlrpc.client import Boolean, boolean
from sqlalchemy import create_engine
import pypyodbc as odbc 
import pandas as pd
from flask import Flask,jsonify
from flask_restful import Api,Resource
app=Flask(__name__)
api=Api(app)
class scheduledays(Resource):
    def __init__(self):
        self.Monday=''
        self.Tuesday=''
        self.Wednesday=''
        self.Thursday=''
        self.Friday='1'
        self.days={'Monday':bool(self.Monday),'Tuesday':bool(self.Tuesday),'Wednesday':bool(self.Wednesday),'Thursday':bool(self.Thursday),'Friday':bool(self.Friday)}
    def post(self):
        return(self.days)
        #function to schedule days
    def get(self):
        #function to submit days
        SERVER='DESKTOP-IEVPBEO'
        DATABASE='employeedb'
        DRIVER='SQL Server Native Client 11.0'
        USERNAME='chidubem'
        PASSWORD='ogbuefi'
         #connecting to the databasE
        connection_string=f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
        engine = create_engine(connection_string)
        connection=engine.connect()
        finalogb=pd.read_sql_query('''SELECT * FROM [employeedb].[chidubem].[employe]''',connection)
        #modifying the days
        finalogb.iloc[0,5]=int(bool(self.Monday))
        finalogb.iloc[0,6]=int (bool (self.Tuesday))
        finalogb.iloc[0,7]=int(bool (self.Wednesday))
        finalogb.iloc[0,8]=int(bool (self.Thursday))
        finalogb.iloc[0,9]=int(bool (self.Friday))
        #storing the new data in sql
        finalogb.to_sql('employe',con=engine,if_exists='replace',index=False)
        return(self.days)
api.add_resource(scheduledays,'/scheduleddays')
class submit(Resource):
    def patch(self):
        data=str(input("input the data"))
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
class HelloWorld(Resource):
    def get(self):
        return{"data":"helloworld"}

if __name__ =="__main__":
    app.run(debug=True)