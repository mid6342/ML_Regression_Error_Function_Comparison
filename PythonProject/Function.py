import sqlite3
import numpy as np
#from operator import itemgetter
from bokeh.plotting import figure, show, output_file

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

"""

CRITERION 1.


"""

# calculating sum of sd for every train, ideal pair

#def calculate_4_ideal_functions():
all_the_sums = []
for ideal_index in range(1, 51):

    for train_index in range(1, 5):
            
        ideal_column = Ideal("y" + str(ideal_index))
        train_column = Train("y" + str(train_index))
        res = Result("y" + str(ideal_index), "y" + str(train_index), 
        ideal_column.sum_of_squared_deviations(train_column))
        all_the_sums.append(res) 

# sort all deviations to get the 4 smallest
sorted_list = sorted(all_the_sums, key=lambda x: x.deviation)
four_ideal = sorted_list[:4]

"""

CRITERION 2.


"""

hallox = Test("x")
x_column = hallox.get_column()
halloy = Test("y")
y_column = halloy.get_column()

#output_file = 'index.html'
#evtl max y und max x von den testpoints verwenden
def visualize(x, y, x_1, y_1, x_error_band, y_error_band, y_error_band_minus):
    p = figure(
        title = 'ideal_1',
        x_axis_label = 'X',
        y_axis_label = 'Y',
        #y_range = (-30, 30) # am bestenhier die max y werte der jew column nehmen, das ist das sinnvollstae
    )
    p.line(x, y, line_color='red', line_width = 1.25)
    p.line(x_1, y_1, line_width = 1.25) #, line_width = '2')
    p.circle(x_column, y_column, size =5, color = 'green')
    p.line(x_error_band, y_error_band, line_color='orange', line_width = 1.25)
    p.line(x_error_band, y_error_band_minus, line_color='orange', line_width = 1.25)
    show(p)

#plotting an ideal function
x_ideal = Ideal("x")
x_ideal_column = x_ideal.get_column()

y_ideal_column = []
f_y_column = []
y_error_band = []
y_error_band_minus = []
k = 0
for i in four_ideal:
    #print(i.ideal)
    y = Ideal(i.ideal)
    y_ideal_column.append(y.get_column()) 
    f = Train(i.train)
    f_y_column.append(f.get_column())
    y_error_band.append(y.get_column() + (0.24 * np.sqrt(2)))
    y_error_band_minus.append(y.get_column() - (0.24 * np.sqrt(2))) 
    visualize(x_ideal_column, y_ideal_column[k], x_ideal_column, f_y_column[k], x_ideal_column, y_error_band[k], y_error_band_minus[k])
    k = k+1

#print(y_ideal_column[0])
#print(x_ideal_column)

four_deviations = []

# for loop to get all the deviations between each test point and each ideal function, now criterion
for i in four_ideal:
    
    #print(i.ideal)
    #print(i.train)
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

print("the four deviations")
for i in four_deviations:
    print(i.max_deviation)
#print(four_deviations)
    #res = Result(i.ideal, i.train, all_deviations)
    #four_deviations.append(res)


# for loop to get all the results of criterion 2 and save it to the Object
all = []

for i in four_deviations:   

    criterion_2_array = []

    for x in i.deviation:
        if(x <= (i.max_deviation * np.sqrt(2))):
            z = (i.max_deviation * np.sqrt(2)) - x
            np.array(criterion_2_array.append(z))
        else:
            y = "None"
            np.array(criterion_2_array.append(y))

    res = FunctionAndMaxDev(i.ideal, i.deviation, i.max_deviation, criterion_2_array)
    all.append(res)

#print("here it starts")
#for i in all:
#    print(i.criterion_2)  


result = []
for i in range(len(x_column)):
    np.array(result.append("no Match"))

#print(result)

      
for i in all:

    #print(i.criterion_2)
    #print(i.ideal)
    y=0
    for x in i.criterion_2:
        #print(x)
        if x != "None":
            if result[y] == "no Match":
                result[y] = i.ideal
            else:
                result[y] = (result[y], i.ideal)
        #print(y)
        y = y+1

#print("hier gehts los----------------------------------------------------")
#for i in result:
#    print(i)

       
# commit and close connection to database    
conn. commit()
conn.close()

