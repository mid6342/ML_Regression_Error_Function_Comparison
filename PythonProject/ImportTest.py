import csv
from sqlalchemy import create_engine, Table, Column, MetaData, REAL

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

# Or read the definition from the DB:
# metadata.reflect(engine, only=['MyTable'])
# my_table = Table('MyTable', metadata, autoload=True, autoload_with=engine)
# insert_query = my_table.insert()

# Or hardcode the SQL query:
# insert_query = "INSERT INTO MyTable (foo, bar) VALUES (:foo, :bar)"

with open('train.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    engine.execute(
        insert_query,
        [{"x": row[0], "y1": row[1], "y2": row[2], "y3": row[3], "y4": row[4]} 
            for row in csv_reader]
    )