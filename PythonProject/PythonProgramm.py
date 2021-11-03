import sqlite3
import csv
import pandas
import sqlalchemy as db

conn = sqlite3.connect("FindingFunctions.db")

cur = conn.cursor()


cur.execute("SELECT x FROM train")
result=cur.fetchall()
print(result)
#result = conn.execute("SELECT x, y1 FROM train")
#print(result)


          
conn. commit()

conn.close()