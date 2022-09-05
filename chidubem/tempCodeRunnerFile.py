from datetime import datetime,timedelta
from urllib import request
from xmlrpc.client import Boolean, boolean
from sqlalchemy import create_engine
import pypyodbc as odbc 
import pyodbc
import pandas as pd
from flask import Flask,jsonify,redirect,request
from flask_restful import Api,Resource
from hashlib import sha256
import json,jwt
#function to hash password
def hash(data):
        hash_var=sha256((data).encode())
        finalhash=hash_var.hexdigest()
        return finalhash
key=hash("wemabank")
print(key)