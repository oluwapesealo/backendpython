import json
from types import SimpleNamespace
import re
from sqlalchemy import create_engine
from sqlite3 import Cursor
from flask import Flask, request, redirect,jsonify
from flask_restful import Resource, Api
from flask_cors import CORS 
import pypyodbc as odbc 
import pandas as pd
import pyodbc

# 'Driver={SQL Server};'
# 'Server=PESES-LAPTOP;'
# 'Database=wemabank;'
# 'Trusted_Connection=yes;'

app = Flask(__name__)
api = Api(app)
class units(Resource): 
    def get(self):
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


    # Parse JSON into an object with attributes corresponding to dict keys.
    

api.add_resource(units,"/units")

class departments(Resource):
    def get(self):
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

    def post(self):
        
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
        
    #        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', unhashedpassword):
        # Password=hash(unhashedpassword)
    #       else:
    #          return 'Invalid Password'

        cursor = connect.cursor()
        cursor.execute('''INSERT INTO Department VALUES (?,?)''',(json["Department_name"], json["Description"]))
        
        connect.commit()
        success='Department created successfully'
        return success
api.add_resource(newdepartments,"/departments/new")

class newunits(Resource):
    def post(selfs):
        
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
        
    #        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', unhashedpassword):
        # Password=hash(unhashedpassword)
    #       else:
    #          return 'Invalid Password'

        cursor = connect.cursor()
        cursor.execute('''INSERT INTO Unit VALUES (?,?,?)''',(json["Unit_name"], json["DepartmentID"], json["Description"]))
        
        connect.commit()
        success='Unit created successfully'
        return success

api.add_resource(newunits,"/units/new")
if __name__ == '__main__':
    app.run(debug =True)
