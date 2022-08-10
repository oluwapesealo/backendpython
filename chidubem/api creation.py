# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:17:29 2022

@author: hp
"""
import urllib
from sqlalchemy import create_engine
import pypyodbc as odbc 
import pandas as pd
from flask import Flask,jsonify
from flask_restful import Api,Resource
app=Flask(__name__)
api=Api(app)
class HelloWorld(Resource):
    def get(self):
        return{"data":"helloworld"}
api.add_resource(HelloWorld,"/helloworld")

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
class submit(Resource):
    def post(self):
        data=str(input("input the data"))
class scheduledays(Resource):
    def post(self):
        "function to schedule days"
class scheduledays(Resource):
    def post(self):
        "function to schedule days"
class scheduledays(Resource):
    def post(self):
        "function to schedule days"

if __name__ =="__main__":
    app.run(debug=True)