from msilib.schema import ODBCAttribute
import mysql.connector
from mysql.connector import Error
try: 
    connection =mysql.connector.connect(host='localhost:3307', database='employeerq', user='root', password='')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to Server", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Youre connected to the database: ", record)

except Error as e:
    print("Error while connecting to MYSQL")

finally:
    connection =mysql.connector.connect(host='localhost', database='employeerq', user='root', password='')
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MYSQL connection is closed")
# import pypyodbc as odbc
# import pandas as pd 
# def returnt():
    
#         drivername='SQL SERVER'
#         servername='DESKTOP-IEVPBEO'
#         database='employeedb'
#         connection_string=f"""
#          DRIVER={{{drivername}}};
#          SERVER={servername};
#         DATABASE={database};
#         Trust_Connection=yes;
#             """ 
#         #connecting to the database
#         readdata=ODBCAttribute.connect(connection_string)
#         #to read from sql database
#         SQL_Query=pd.read_sql_query('''SELECT * FROM[dbo].[employees]''',readdata)
#         #storing sql database in python
#         finaldatabase=SQL_Query.head()
#         #coverting the table to a dictionar
#         employee= finaldatabase.to_dict('records')
#         return(employee)

