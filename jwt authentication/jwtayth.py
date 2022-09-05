from base64 import decode
from flask import Flask, request, jsonify, make_response, request, render_template, session, flash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import urllib
app= Flask(__name__)
key=".ogb"
token = jwt.encode({
    'user': "email",

    # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
    'expiration': str(datetime.utcnow() + timedelta(seconds=60))
},key)
# ogb=jsonify ({'token':token.decode('utf-8')})
print(token)
decoded=jwt.decode(token, key=key, algorithms=['HS256', ])
print(decoded)
from datetime import datetime, timedelta
from genericpath import exists
from select import select
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
import os
import jwt
from dotenv import load_dotenv
load_dotenv()
app=Flask(__name__)
api=Api(app)
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
def tokenauthent():
    x=1
    if (x==0):
        return{"message":"your token has expired"}
    elif(x==1):
        return {"message":"token is valid"}
print(tokenauthent()['message'])