import csv
from sqlalchemy import create_engine, Table, Column, MetaData, REAL
from os import path

# create the database + what means echo=True?
engine = create_engine('sqlite:///FindingFunctions.db', echo=True)

metadata = MetaData()
# Define the table with sqlalchemy:

train_table = Table('train', metadata,
    Column('x', REAL),
    Column('y1', REAL),
    Column('y2', REAL),
    Column('y3', REAL),
    Column('y4', REAL),
)

metadata.create_all(engine)
insert_query = "INSERT INTO train (x, y1, y2, y3, y4) VALUES (:x, :y1, :y2, :y3, :y4)"

if path.exists('data//train.csv') != True:
    raise Exception("Please put the file into a seperate folder called data")

with open('data//train.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    engine.execute(
        insert_query,
        [{"x": row[0], "y1": row[1], "y2": row[2], "y3": row[3], "y4": row[4]} 
            for row in csv_reader]
    )