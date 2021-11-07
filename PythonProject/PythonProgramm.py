import sqlite3

# connect to database
conn = sqlite3.connect("FindingFunctions.db")
cur = conn.cursor()

# function to get a whole column in form of a list
def get_list_of_column(column, table):
    # get all the cells of the column and write them to a list
    query= cur.execute("SELECT " + column + " FROM " + table)
    list_of_column = []
    for cell in query: 
        list_of_column.append(cell[0])  
    # remove column head
    list_of_column.pop(0)
    return list_of_column
    
print(get_list_of_column("x", "train"))

# commit and close connection to database    
conn. commit()
conn.close()