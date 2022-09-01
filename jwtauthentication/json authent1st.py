from urllib import request
from xmlrpc.client import Boolean, boolean
from sqlalchemy import create_engine
import pypyodbc as odbc 
import pyodbc
import pandas as pd
from flask import Flask,jsonify,request,render_template,session,make_response
from flask_restful import Api,Resource
from hashlib import sha256
import datetime
import jwt
from functools import wraps
#function to hash password
app= Flask(__name__)
app.config['SECRET_KEY']='ogb'
def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token=request/args.get('token')
        if not token:
            return jsonify({'Alert!':'token is missing'})
        try:
            payload=jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'Alert':'invalid token'})
    return decorated
@app.route('/')
def home():
    if not session.get('logged in'):
        return render_template('login.html')
    else:
        return 'logged in currently'
@app.route('/public')
def public():
    return 'for public'
# authentication

@app.route('/auth')
@token_required
def auth():
    return 'jwt is verified .welcome to dashboard'
@app.route('/login',methods=['POST'])

# login
def login():
    if request.form['username'] and request.form['password']=='123456':
        session['logged in']=True
        token=jwt.encode({
            'user':request.form['username'],
            'expiration':str(datetime.utcnow()+timedelta(seconds=120))
    },
            app.config['SECRET_KEY'])
        return jsonify ({'token':token.decode('utf-8')})
    else:
        return make_response('unable to verify ',403,{'www-authenticate':'Basic raelm:Authentication failed'})
if __name__ =="__main__":
    app.run(debug=True)
    