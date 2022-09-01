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

# 'Driver={SQL Server};'
# 'Server=PESES-LAPTOP;'
# 'Database=wemabank;'
# 'Trusted_Connection=yes;'

app = Flask(__name__)
api = Api(app)

# @app.route("/designations")
# def get(self):

#     drivername='SQL SERVER'
#     servername='PESES-LAPTOP'
#     database='wemabank'
#     connection_string=f"""
#         DRIVER={{{drivername}}};
#         SERVER={servername};
#     DATABASE={database};
#     Trust_Connection=yes;
#         """ 
#     #connecting to the database
#     readdata=odbc.connect(connection_string)
#     #to read from sql database
#     SQL_Query=pd.read_sql_query('''SELECT Designation FROM[dbo].[Designation]''',readdata)
#     #storing sql database in python
#     finaldatabase=SQL_Query.head()
#     #coverting the table to a dictionar
#     designations= finaldatabase.to_dict('records')
#     return(designations)

# @app.route("/roles")
# def get(self):

#     drivername='SQL SERVER'
#     servername='PESES-LAPTOP'
#     database='wemabank'
#     connection_string=f"""
#         DRIVER={{{drivername}}};
#         SERVER={servername};
#     DATABASE={database};
#     Trust_Connection=yes;
#         """ 
#     #connecting to the database
#     readdata=odbc.connect(connection_string)
#     #to read from sql database
#     SQL_Query=pd.read_sql_query('''SELECT Roles FROM[dbo].[Roles]''',readdata)
#     #storing sql database in python
#     finaldatabase=SQL_Query.head()
#     #coverting the table to a dictionar
#     roles= finaldatabase.to_dict('records')
#     return(roles)

# @app.route("/units")
# def get(self):

#     drivername='SQL SERVER'
#     servername='PESES-LAPTOP'
#     database='wemabank'
#     connection_string=f"""
#         DRIVER={{{drivername}}};
#         SERVER={servername};
#     DATABASE={database};
#     Trust_Connection=yes;
#         """ 
#     #connecting to the database
#     readdata=odbc.connect(connection_string)
#     #to read from sql database
#     SQL_Query=pd.read_sql_query('''SELECT Unit FROM[dbo].[Unit_name]''',readdata)
#     #storing sql database in python
#     finaldatabase=SQL_Query.head()
#     #coverting the table to a dictionar
#     units= finaldatabase.to_dict('records')
#     return(units)

@app.route("/departments")
def department():

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
    SQL_Query=pd.read_sql_query('''SELECT Department_name from Department ''',readdata)
    #storing sql database in python
    finaldatabase=SQL_Query.head()
    #coverting the table to a dictionar
    departments= finaldatabase.to_dict('records')
    return(departments)

# @app.route("/departments/new")
# def post(self):
    
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.get_json()
#         print (json)
#     else:
#         return 'Error'
#     connect = pyodbc.connect('Driver={SQL Server};'
#     'Server=PESES-LAPTOP;'
#     'Database=wemabank;'
#     'Trusted_Connection=yes;')
    
# #        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', unhashedpassword):
#     # Password=hash(unhashedpassword)
# #       else:
# #          return 'Invalid Password'

#     cursor = connect.cursor()
#     cursor.execute('''INSERT INTO Department VALUES (0,?,?)''',(json["Department_name"], json["Description"]))
    
#     connect.commit()
#     success='Department created successfully'
#     return success

# @app.route("/units/new")
# def post(self):
    
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.get_json()
#         print (json)
#     else:
#         return 'Error'
#     connect = pyodbc.connect('Driver={SQL Server};'
#     'Server=PESES-LAPTOP;'
#     'Database=wemabank;'
#     'Trusted_Connection=yes;')
    
# #        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', unhashedpassword):
#     # Password=hash(unhashedpassword)
# #       else:
# #          return 'Invalid Password'

#     cursor = connect.cursor()
#     cursor.execute('''INSERT INTO Unit VALUES (?,?,?)''',(json["Unit_name"], json["DepartmentID"], json["Description"]))
    
#     connect.commit()
#     success='Unit created successfully'
#     return success


if __name__ == '__main__':
    app.run(debug =True)