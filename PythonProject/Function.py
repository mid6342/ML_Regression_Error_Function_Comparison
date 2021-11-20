import sqlite3
import numpy as np
#from operator import itemgetter
from bokeh.plotting import figure, show, output_file
from sqlalchemy.sql.expression import table

#from Classes import Function, Ideal, Train, Test, MeanDeviation, FunctionAndMaxDev
#from ImportIdeal import import_ideal
#from ImportTrain import import_train
#from ImportTest import import_test


"""

CLASSES


"""

# connect to database
conn = sqlite3.connect("FindingFunctions.db")   
cur = conn.cursor()

class Function:
    

    def __init__(self, column, table):
        self.column = column
        self.table = table

    def get_column(self):
        # connect to database
        conn = sqlite3.connect("FindingFunctions.db")   
        cur = conn.cursor()

        # get all the cells of the column and write them to a list
        query= cur.execute("SELECT " + self.column + " FROM " + self.table)
        column_list = []
        for cell in query: 
            column_list.append(cell[0])  
        # remove column head
        column_list.pop(0)

        # commit and close connection to database    
        conn. commit()
        conn.close()
        return column_list
    

class Ideal(Function):

    def __init__(self, column, ideal_name = "ideal", sum_of_squared_deviations = None):
        super().__init__(column, ideal_name)
        self.sum_of_squared_deviations = sum_of_squared_deviations

    def get_median_deviation(self, train_column):
        squared = np.square(np.array(self.get_column()) - np.array(train_column.get_column()))
        return np.sum(squared)
        
    def max_deviation(self, train_column):
        return np.max(np.square(np.array(self.get_column()) - np.array(train_column.get_column())))


class Train(Function):

    def __init__(self, column, train_name="train"):
        super().__init__(column, train_name)


class Criterion_1:

    def __init__(self, ideal, train, median_deviation):
        self.ideal = ideal
        self.train = train
        self.median_deviation = median_deviation

class Test(Function):

    def __init__(self, column):
        super().__init__(column, "test")

class FunctionAndMaxDev:

    def __init__(self, ideal, deviation, max_deviation, criterion_2):
        self.ideal = ideal
        self.deviation = deviation
        self.max_deviation = max_deviation
        self.criterion_2 = criterion_2

    


"""

CRITERION 1.


"""

def four_ideal_functions(ideal_name = "ideal", train_name = "train", ideal_len = 51, train_len = 5):
    all_deviations = []

    # calculating sum of sd for every train, ideal pair
    for ideal_index in range(1, ideal_len):
        for train_index in range(1, train_len):    

            ideal_fnc = Ideal("y" + str(ideal_index), ideal_name)
            train_fnc = Train("y" + str(train_index), train_name)

            res = Criterion_1(ideal_fnc.column, train_fnc.column, 
            ideal_fnc.get_median_deviation(train_fnc))

            all_deviations.append(res) 

    # sort all median deviations to get the 4 ideal functions with the smallest median deviation
    four_ideal = sorted(all_deviations, key=lambda x: x.median_deviation)
    return four_ideal[:4]

def visualize_ideal_and_train(four_ideal_fnc, x):

    for i in four_ideal_fnc:

        p = figure(
            title = 'ideal_and_train',
            x_axis_label = 'X',
            y_axis_label = 'Y',
        )

        # get the right columns
        y_ideal = Ideal(i.ideal)
        y_ideal = y_ideal.get_column()
        y_train = Train(i.train)
        y_train = y_train.get_column()

        p.line(x, y_ideal, line_color='red', line_width = 1.25)
        p.line(x, y_train, line_width = 1.25)
        show(p)

"""

CRITERION 2. VISUALIZATION


"""

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

# hier werden die x und y columns für test dataset erstellt
hallox = Test("x")
x_column = hallox.get_column()
halloy = Test("y")
y_column = halloy.get_column()



#plotting an ideal function
x_ideal = Ideal("x")
x_ideal_column = x_ideal.get_column()

y_ideal_column = []
f_y_column = []
y_error_band = []
y_error_band_minus = []
k = 0
for i in four_ideal_functions():
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



"""

CRITERION 2. CODE


"""

def get_dev_and_maxdev():
    # for loop to get all the deviations between each test point and each ideal function
    four_deviations = []
    for i in four_ideal_functions():
        
        first_time = True
        all_deviations = []
        y_test = []

        for x in x_column:

            ideal_query = cur.execute("SELECT " + i.ideal + " FROM ideal WHERE x=" + str(x))
            for cell in ideal_query: 
                y_ideal = np.asarray(cell)

            test_query = cur.execute("SELECT y FROM test WHERE " + "x" + "=" + str(x))
            for cell in test_query: 
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

    return four_deviations
    
# for loop to get all the results of criterion 2 and save it to the Object


def get_criterion_2():
    all = []
    for i in get_dev_and_maxdev():   

        criterion_2_array = []

        for x in i.deviation:
            if(x <= (i.max_deviation * np.sqrt(2))):
                z = (i.max_deviation * np.sqrt(2)) - x
                np.array(criterion_2_array.append(z))
            else:
                y = "None"
                np.array(criterion_2_array.append(y))

        res = FunctionAndMaxDev(x_column, y_column, i.max_deviation, criterion_2_array)
        all.append(res)
    return all


#print("here it starts")
#for i in all:
#    print(i.criterion_2)  


# es fehlt noch die information über die deviation der ideal fnc!!
# ausgeklammert, da erst schritt für schritt durchs programm

def get_matched_functions(x_c, y_c):
    all_2 = []
    #len4    
    for i in get_criterion_2():

        #print(i.criterion_2)
        print(i.ideal)
        y=0
        
        deviation = ["no Match"] * len(i.criterion_2)
        result = ["no Match"] * len(i.criterion_2)

        print(deviation)
        
        for cell in i.criterion_2:
            #print(x)
            print(cell)
            print(i.max_deviation)
            if cell != "None":
                if result[y] == "no Match":
                    result[y] = i.max_deviation
                    deviation[y] = i.criterion_2
                    #print(result[y])
                    #print(deviation[y])
                else:
                    result[y] = (result[y], i.max_deviation)
                    deviation[y] = (deviation[y], i.criterion_2)
            #print(y)
            y = y+1
        #print(deviation)
        res = FunctionAndMaxDev(x_c, y_c, deviation, result)
        all_2.append(res)

    return all_2

#print("hier gehts los----------------------------------------------------")
#for i in result:
#    print(i)

def main():
    
    #import_ideal()
    #import_train()
    #import_test()
    x = Function("x", "train")
    x = x.get_column()
    
    visualize_ideal_and_train(four_ideal_functions(), x)

    print("the median_deviation")
    for i in four_ideal_functions():
        print(i.median_deviation)
    print(len(four_ideal_functions()))

    #get_dev_and_maxdev()

    print("the four deviations")
    for i in get_dev_and_maxdev():
        print(i.max_deviation)
        print(i.deviation)
    print(len(get_dev_and_maxdev()))
    
    print("criterion 2:")
    for i in get_criterion_2():
        print(i.criterion_2)    
    """
    x_test = Function("x", "test")
    x_test = x_test.get_column()
    y_test = Function("y", "test")
    y_test = y_test.get_column()
        
    for i in get_matched_functions(x_test, y_test):
        print("ignore ideal")
        print(i.ideal)
        #print(i.deviation)
        #print(i.max_deviation)
        #print(i.criterion_2)
    """



if __name__ == '__main__':
    main()

# commit and close connection to database    
conn. commit()
conn.close()

