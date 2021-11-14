import csv
from sqlalchemy import create_engine, Table, Column, MetaData, REAL

# create the database + what means echo=True?
engine = create_engine('sqlite:///FindingFunctions.db', echo=True)

metadata = MetaData()
# Define the table with sqlalchemy:

train_table = Table('test', metadata,
    Column('x', REAL),
    Column('y', REAL),
)

metadata.create_all(engine)
insert_query = "INSERT INTO test (x, y) VALUES (:x, :y)"

# Or read the definition from the DB:
# metadata.reflect(engine, only=['MyTable'])
# my_table = Table('MyTable', metadata, autoload=True, autoload_with=engine)
# insert_query = my_table.insert()

# Or hardcode the SQL query:
# insert_query = "INSERT INTO MyTable (foo, bar) VALUES (:foo, :bar)"

with open('test.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    engine.execute(
        insert_query,
        [{"x": row[0], "y": row[1]} for row in csv_reader]
    )