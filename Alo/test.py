import json
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


# # # 'Driver={SQL Server};'
# # # 'Server=PESES-LAPTOP;'
# # # 'Database=wemabank;'
# # # 'Trusted_Connection=yes;'

# app = Flask(__name__)
# api = Api(app)
# # class units(Resource): 
# #     def get(self):
# #         connect = pyodbc.connect('Driver={SQL Server};'
# #         'Server=PESES-LAPTOP;'
# #         'Database=wemabank;'
# #         'Trusted_Connection=yes;')
        
# #     #        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', unhashedpassword):
# #         # Password=hash(unhashedpassword)
# #     #       else:
# #     #          return 'Invalid Password'

# #         cursor = connect.cursor()
# #         aunits=cursor.execute("Select Unit_name FROM Unit ")
# #         units=[]
# #         i=1
# #         for row in aunits :
# #             units.append({"Unit" :row[0]})
# #             i=i+1
# #         return jsonify(units)
# # api.add_resource(units,"/units")

# # class departments(Resource):
# #     def get(self):

# #         connect = pyodbc.connect('Driver={SQL Server};'
# #         'Server=PESES-LAPTOP;'
# #         'Database=wemabank;'
# #         'Trusted_Connection=yes;')
        

# #         cursor = connect.cursor()
# #         adeparts=cursor.execute("Select Department_name FROM Department ")
# #         departments=[]
# #         i=1
# #         for row in adeparts:
# #             departments.append({"Department":row[0]})
# #             i=i+1
# #         return jsonify(departments)
# # api.add_resource(departments,"/departments")

# # class newdepartments(Resource):

# #     def post(self):
        
# #         content_type = request.headers.get('Content-Type')
# #         if (content_type == 'application/json'):
# #             json = request.get_json()
# #             print (json)
# #         else:
# #             return 'Error'
# #         connect = pyodbc.connect('Driver={SQL Server};'
# #         'Server=PESES-LAPTOP;'
# #         'Database=wemabank;'
# #         'Trusted_Connection=yes;')
        
# #     #        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', unhashedpassword):
# #         # Password=hash(unhashedpassword)
# #     #       else:
# #     #          return 'Invalid Password'

# #         cursor = connect.cursor()
# #         cursor.execute('''INSERT INTO Department VALUES (?,?)''',(json["Department_name"], json["Description"]))
        
# #         connect.commit()
# #         success='Department created successfully'
# #         return success
# # api.add_resource(newdepartments,"/departments/new")

# # class newunits(Resource):
# #     def post(selfs):
        
# #         content_type = request.headers.get('Content-Type')
# #         if (content_type == 'application/json'):
# #             json = request.get_json()
# #             print (json)
# #         else:
# #             return 'Error'
# #         connect = pyodbc.connect('Driver={SQL Server};'
# #         'Server=PESES-LAPTOP;'
# #         'Database=wemabank;'
# #         'Trusted_Connection=yes;')
        
# #     #        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', unhashedpassword):
# #         # Password=hash(unhashedpassword)
# #     #       else:
# #     #          return 'Invalid Password'

# #         cursor = connect.cursor()
# #         cursor.execute('''INSERT INTO Unit VALUES (?,?,?)''',(json["Unit_name"], json["DepartmentID"], json["Description"]))
        
# #         connect.commit()
# #         success='Unit created successfully'
# #         return success

# # api.add_resource(newunits,"/units/new")
# # if __name__ == '__main__':
# #     app.run(debug =True)


# def ret():
#         connect = pyodbc.connect('Driver={SQL Server};'
#         'Server=PESES-LAPTOP;'
#         'Database=wemabank;'
#         'Trusted_Connection=yes;')
        
#     #        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', unhashedpassword):
#         # Password=hash(unhashedpassword)
#     #       else:
#     #          return 'Invalid Password'

#         cursor = connect.cursor()
#         aunits=cursor.execute("Select Unit_name FROM Unit ")
#         units=[]
#         i=1
#         for row in aunits :
#             units.append({"Unit" :row[0]})
#             i=i+1
#             jsonify(units)
#             x = json.loads(units, object_hook=lambda d: SimpleNamespace(**d))    
#             a = print(x.Unit_name, x.DepartmentID)

#         return a

# ret()
# email = "some.name@somehost.com"

# name, _, _ = email.partition("@")  # returns before @, @, and after @
# splitname = name.split(".")        # splits on .

# print(splitname)
# import requests
# req=requests.get
# class downloadreq(Resource):
#     def get(self,Email=''):
        
       
#         self.Email=Email
        
#         connect = pyodbc.connect('Driver={SQL Server};'
#             'Server=PESES-LAPTOP;'
#             'Database=employeedb;'
#             'Trusted_Connection=yes;')
#         test1 = pd.read_sql_query('''select *from Requests where Email = ? '''+Email, connect)
#         df = pd.DataFrame(test1)
#         df.to_csv(Email+".csv")
#         return redirect('/allrequests')
       
# api.add_resource(downloadreq, '/allrequests/viewrequest/<string:Email>/linemanagerapproval/download')

# def download(Email):
        
#         # tokenfunc=tokenauthent(self.Email,str(os.getenv("key")))
#         # if (tokenfunc['message']=="token is valid"):
#         drivername='SQL SERVER'
#         servername='PESES-LAPTOP'
#         database='wemabank'
#         connection_string=f"""
#         DRIVER={{{drivername}}};
#         SERVER={servername};
#         DATABASE={database};
#         Trust_Connection=yes;
#             """ 
#         readdata=odbc.connect(connection_string)
#         SQL_Query=pd.read_sql_query('''select *from ScheduleDays where Email = '''+Email, readdata,)
#         df = pd.DataFrame(SQL_Query)
#         df.to_csv(Email+".csv")
#         success = 'Download was successful'
#         return success

# download('pese@wemabank.com')

import requests
 
downloadurl =  'https://www.w3.org/wiki/CORS_Enabled'

req = requests.get(downloadurl)


