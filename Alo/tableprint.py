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
SQL_Query=pd.read_sql_query('''select * from employeetable2''',readdata)
#storing sql database in python
#coverting the table to a dictionar
emailtable= pd.DataFrame(SQL_Query)
print(emailtable)