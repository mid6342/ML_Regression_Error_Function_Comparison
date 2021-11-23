import csv
from sqlalchemy import create_engine, Table, Column, MetaData, REAL
from os import path

# create the database + what means echo=True?
engine = create_engine('sqlite:///FindingFunctions.db', echo=True)

metadata = MetaData()
# Define the table with sqlalchemy:

train_unittest_table = Table('train_unittest', metadata,
    Column('x', REAL),
    Column('y1', REAL),
)

metadata.create_all(engine)
insert_query = "INSERT INTO train_unittest (x, y1) VALUES (:x, :y1)"

if path.exists('data//train_unittest.csv') != True:
    raise Exception("Please put the file into a seperate folder called data")

with open('data//train_unittest.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    engine.execute(
        insert_query,
        [{"x": row[0], "y1": row[1]} 
            for row in csv_reader]
    )