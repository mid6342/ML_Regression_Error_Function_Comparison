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


class Test(Function):

    def __init__(self, column):
        super().__init__(column, "test")


class Result:

    def __init__(self, ideal, train, deviation):
        self.ideal = ideal
        self.train = train
        self.deviation = deviation

class FunctionAndMaxDev:

    def __init__(self, ideal, deviation, max_deviation, criterion_2):
        self.ideal = ideal
        self.deviation = deviation
        self.max_deviation = max_deviation
        self.criterion_2 = criterion_2

y_2 = Ideal("y2")
#print(y_2.get_column())
#print(Train("y3"))

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

x = Test("x")
x_column = x.get_column()
#print(x_column)


four_deviations = []

# for loop to get all the deviations between each test point and each ideal function, now criterion
for i in four_ideal:
    
    print(i.ideal)
    print(i.train)
    #print(i.deviation)

    first_time = True
    all_deviations = []
    y_test = []

    for x in x_column:

        query = cur.execute("SELECT " + i.ideal + " FROM ideal WHERE x=" + str(x))
        for cell in query: 
            y_ideal = np.asarray(cell)

        query_2 = cur.execute("SELECT y FROM test WHERE " + "x" + "=" + str(x))
        for cell in query_2: 
            np.array(y_test.append(cell[0]))

        if(len(y_test) == 1):
            deviation = abs(y_test - y_ideal)

        elif((len(y_test) == 2) & (first_time == True)):
            deviation = abs(y_test[0] - y_ideal)
            first_time = False

        else:
            deviation = abs(y_test[1] - y_ideal)

        y_test.clear()
        all_deviations.append(deviation[0]) # 0 nuir um die Ergebnisse im Arraay zhu nem array und keinem tuopel zu machen

    # calculate max deviation between the respective train and ideal function
    y = Ideal(i.ideal)
    f = Train(i.train)
    max_deviation = y.max_deviation(f)
    #four_deviations.append(all_deviations)   
    res = FunctionAndMaxDev(i.ideal, all_deviations, max_deviation, "None")
    four_deviations.append(res)

print(four_deviations)
    #res = Result(i.ideal, i.train, all_deviations)
    #four_deviations.append(res)


criterion_2_array = []
for i in four_deviations:   
    #print(i.deviation)
    print(i.ideal)
    #print(i.max_deviation)
    #print("Hello:  " + str(i.criterion_2))

    for x in i.deviation:
        if(x <= i.max_deviation + np.sqrt(2)):
            #print("Criterion2 = " + str((i.max_deviation + np.sqrt(2)) - x))
            z = i.max_deviation + np.sqrt(2) - x
            np.array(criterion_2_array.append(z))
        else:
            y = "None"
            np.array(criterion_2_array.append(y))
    print(criterion_2_array)
    criterion_2_array.clear()
            
    



       
# commit and close connection to database    
conn. commit()
conn.close()

