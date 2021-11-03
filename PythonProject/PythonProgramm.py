import sqlite3
import csv
import pandas
import sqlalchemy as db
import numpy as np


conn = sqlite3.connect("FindingFunctions.db")
cur = conn.cursor()

# print ideal table
ideal_table = cur.execute("SELECT * FROM ideal")
for i in ideal_table:
    print(i)

print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")

# print train table
train_table = cur.execute("SELECT * FROM train")
for k in train_table:
    print(k)



#result=cur.fetchall()
#print(result)
#result = conn.execute("SELECT x, y1 FROM train")
#print(result)


          
conn. commit()

conn.close()