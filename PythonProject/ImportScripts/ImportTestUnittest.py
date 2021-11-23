import csv
from sqlalchemy import create_engine, Table, Column, MetaData, REAL
from os import path



# create the database + what means echo=True?
engine = create_engine('sqlite:///FindingFunctions.db', echo=True)

metadata = MetaData()
# Define the table with sqlalchemy:

test_unittest_table = Table('test_unittest', metadata,
    Column('x', REAL),
    Column('y', REAL),  
)

metadata.create_all(engine)
insert_query = """INSERT INTO test_unittest (x, y) VALUES (:x, :y)"""

if path.exists('data//test_unittest.csv') != True:
    raise Exception("Please put the file into a seperate folder called data")

with open('data//test_unittest.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    engine.execute(
        insert_query,
        [{"x": row[0], "y": row[1]} 
            for row in csv_reader]
    )