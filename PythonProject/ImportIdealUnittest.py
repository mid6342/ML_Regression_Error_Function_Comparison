import csv
from sqlalchemy import create_engine, Table, Column, MetaData, REAL


# create the database + what means echo=True?
engine = create_engine('sqlite:///FindingFunctions.db', echo=True)

metadata = MetaData()
# Define the table with sqlalchemy:

ideal_unittest_table = Table('ideal_unittest', metadata,
    Column('x', REAL),
    Column('y1', REAL),
    Column('y2', REAL),
    
)

metadata.create_all(engine)
insert_query = """INSERT INTO ideal_unittest (x, y1, y2) VALUES (:x, :y1, :y2)"""


with open('ideal_unittest.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    engine.execute(
        insert_query,
        [{"x": row[0], "y1": row[1], "y2": row[2]} 
            for row in csv_reader]
    )