import sqlite3
import numpy as np

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

# function for subtracting 2 lists
def subtract_lists(list_1, list_2):
    return np.array(list_1) - np.array(list_2)
    
# print(get_list_of_column("x", "train"))
# all my columns
ideal_y1 = get_list_of_column("y1", "ideal")
train_y1 = get_list_of_column("y1", "train")
print(subtract_lists(ideal_y1, train_y1))

# commit and close connection to database    
conn. commit()
conn.close()