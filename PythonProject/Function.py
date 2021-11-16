import sqlite3
import numpy as np
#from operator import itemgetter

# connect to database
conn = sqlite3.connect("FindingFunctions.db")
cur = conn.cursor()

class Function:

    def __init__(self, column, table):
        self.column = column
        self.table = table

    def get_column(self):
        # get all the cells of the column and write them to a list
        query= cur.execute("SELECT " + self.column + " FROM " + self.table)
        column_list = []
        for cell in query: 
            column_list.append(cell[0])  
        # remove column head
        column_list.pop(0)
        return column_list

class Ideal(Function):

    def __init__(self, column):
        super().__init__(column, "ideal")

    def sum_of_squared_deviations(self, train_column):
        squared = np.square(np.array(self.get_column()) - np.array(train_column.get_column()))
        sum_of_squared = np.sum(squared)
        return sum_of_squared

    def max_deviation(self, train_column):
        return np.max(np.square(np.array(self.get_column()) - np.array(train_column.get_column())))

class Train(Function):

    def __init__(self, column):
        super().__init__(column, "train")


class Result:

    def __init__(self, ideal, train, deviation):
        self.ideal = ideal
        self.train = train
        self.deviation = deviation

y_2 = Ideal("y2")
print(y_2.get_column())

# calculating sum of sd for every train, ideal pair
all_the_sums = []
for i in range(1, 51):
    for k in range(1, 5):
        ideal_column = Ideal("y" + str(i))
        train_column = Train("y" + str(k))
        res = Result("y" + str(i), "y" + str(k), ideal_column.sum_of_squared_deviations(train_column))
        all_the_sums.append(res) 

# sort all deviations to get the 4 smallest
sorted_list = sorted(all_the_sums, key=lambda x: x.deviation)
four_ideal = sorted_list[:4]

# print 4 ideal functions
for i in four_ideal:
    print(i.ideal)
    print(i.train)
    print(i.deviation)

"""

all_deviations = []
deviation_2 = []
def get_y_in_ideal(column):
    y_test = []
    first_time = True
    for x_row in test_x:
        query = cur.execute("SELECT " + column + " FROM ideal WHERE x=" + str(x_row))
        for cell in query: 
            y_ideal = np.asarray(cell)
            #print("y wert of ideal function: " + str(y_ideal))
        # bis dahin passt alles, da es ja nur durch die ideal function geht
        query_2 = cur.execute("SELECT y FROM test WHERE " + "x" + "=" + str(x_row))
        for cell in query_2: 
            np.array(y_test.append(cell[0]))
        #print("y wert of test point: " + str(y_test))
        if(len(y_test) == 1):
            deviation = abs(y_test - y_ideal)
            #print("in between")
            #print(deviation)
        elif((len(y_test) == 2) & (first_time == True)):
            deviation = abs(y_test[0] - y_ideal)
            #print(first_time)
            #print(deviation)
            first_time = False
        else:
            deviation = abs(y_test[1] - y_ideal)
            #print(first_time)
            #print(deviation)
        y_test.clear()
        #deviation_squareroot = deviation * np.sqrt(2)
        all_deviations.append(deviation[0])
        #deviation_2.append(deviation[0])
        #print("----------------------------------------------------")
        #y_test = []
        #print("x wert of test point: " + str(x_row))
        #deviation = y_test - y_ideal
        #print(deviation)
        #print("----------------------------")


get_y_in_ideal("y31")
print("31")
#list of the deviation of all testpoints for the ideal function 31
print(all_deviations)
all_deviations.clear()

print("46")
get_y_in_ideal("y46")
print(all_deviations)
all_deviations.clear()

print("6")
get_y_in_ideal("y6")
print(all_deviations)
all_deviations.clear()

print("25")
get_y_in_ideal("y25")
print(all_deviations)
all_deviations.clear()

#print(deviation_2)
#print("y25")
#get_y_in_ideal("y25")


    
# commit and close connection to database    
conn. commit()
conn.close()
"""