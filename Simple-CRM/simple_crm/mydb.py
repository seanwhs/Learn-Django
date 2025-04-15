# Install MySQL on computer
# pip install mysqlclient
# pip install pymysql

import pymysql

conn = pymysql.connect(
    host="localhost", 
    user="root", 
    password="root", 
    database="crm"
    )


print("All Done!")
