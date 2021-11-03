import csv
from sqlalchemy import create_engine, Table, Column, MetaData, REAL

# create the database + what means echo=True?
engine = create_engine('sqlite:///FindingFunctions.db', echo=True)

metadata = MetaData()
# Define the table with sqlalchemy:

ideal_table = Table('ideal', metadata,
    Column('x', REAL),
    Column('y1', REAL),
    Column('y2', REAL),
    Column('y3', REAL),
    Column('y4', REAL),
    Column('y5', REAL),
    Column('y6', REAL),
    Column('y7', REAL),
    Column('y8', REAL),
    Column('y9', REAL),
    Column('y10', REAL),
    Column('y11', REAL),
    Column('y12', REAL),
    Column('y13', REAL),
    Column('y14', REAL),
    Column('y15', REAL),
    Column('y16', REAL),
    Column('y17', REAL),
    Column('y18', REAL),
    Column('y19', REAL),
    Column('y20', REAL),
    Column('y21', REAL),
    Column('y22', REAL),
    Column('y23', REAL),
    Column('y24', REAL),
    Column('y25', REAL),
    Column('y26', REAL),
    Column('y27', REAL),
    Column('y28', REAL),
    Column('y29', REAL),
    Column('y30', REAL),
    Column('y31', REAL),
    Column('y32', REAL),
    Column('y33', REAL),
    Column('y34', REAL),
    Column('y35', REAL),
    Column('y36', REAL),
    Column('y37', REAL),
    Column('y38', REAL),
    Column('y39', REAL),
    Column('y40', REAL),
    Column('y41', REAL),
    Column('y42', REAL),
    Column('y43', REAL),
    Column('y44', REAL),
    Column('y45', REAL),
    Column('y46', REAL),
    Column('y47', REAL),
    Column('y48', REAL),
    Column('y49', REAL),
    Column('y50', REAL),
)

metadata.create_all(engine)
insert_query = """INSERT INTO ideal (x, y1, y2, y3, y4, y5, y6, y7, y8, y9,
y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25,
y26, y27, y28, y29, y30, y31, y32, y33, y34, y35, y36, y37, y38, y39, y40, y41,
y42, y43, y44, y45, y46, y47, y48, y49, y50) VALUES (:x, :y1, :y2, :y3, :y4, :y5,
:y6, :y7, :y8, :y9, :y10, :y11, :y12, :y13, :y14, :y15, :y16, :y17, :y18, :y19, :y20, :y21, :y22,
:y23, :y24, :y25, :y26, :y27, :y28, :y29, :y30, :y31, :y32, :y33, :y34, :y35, :y36, :y37, :y38,
:y39, :y40, :y41, :y42, :y43, :y44, :y45, :y46, :y47, :y48, :y49, :y50)"""

# Or read the definition from the DB:
# metadata.reflect(engine, only=['MyTable'])
# my_table = Table('MyTable', metadata, autoload=True, autoload_with=engine)
# insert_query = my_table.insert()

# Or hardcode the SQL query:
# insert_query = "INSERT INTO MyTable (foo, bar) VALUES (:foo, :bar)"

with open('ideal.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    engine.execute(
        insert_query,
        [{"x": row[0], "y1": row[1], "y2": row[2], "y3": row[3], "y4": row[4],
        "y5": row[5], "y6": row[6], "y7": row[7], "y8": row[8], "y9": row[9], 
        "y10": row[10], "y11": row[11], "y12": row[12], "y13": row[13], "y14": row[14],
        "y15": row[15], "y16": row[16], "y17": row[17], "y18": row[18], "y19": row[19],
        "y20": row[20], "y21": row[21], "y22": row[22], "y23": row[23], "y24": row[24],
        "y25": row[25], "y26": row[26], "y27": row[27], "y28": row[28], "y29": row[29],
        "y30": row[30], "y31": row[31], "y32": row[32], "y33": row[33], "y34": row[34],
        "y35": row[35], "y36": row[36], "y37": row[37], "y38": row[38], "y39": row[39],
        "y40": row[40], "y41": row[41], "y42": row[42], "y43": row[43], "y44": row[44],
        "y45": row[45], "y46": row[46], "y47": row[47], "y48": row[48], "y49": row[49],
        "y50": row[50]} 
            for row in csv_reader]
    )