import json
from pickle import APPEND
import re
from sqlalchemy import create_engine
from sqlite3 import Cursor
from flask import Flask, request, redirect,jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import pypyodbc as odbc
import pandas as pd
from types import SimpleNamespace
import pyodbc
def get():
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
    SQL_Query=pd.read_sql_query('''Select Unit_name FROM Unit''', readdata)
    vrequests= SQL_Query.to_dict('records')
    
    units =print(vrequests)
    return units
get()