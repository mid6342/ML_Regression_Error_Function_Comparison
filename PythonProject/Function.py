import sqlite3
import numpy as np
#from operator import itemgetter
from bokeh.plotting import figure, show, output_file
from sqlalchemy.sql.expression import table

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
        return np.max(np.abs(np.array(self.get_column()) - np.array(train_column.get_column())))


class Train(Function):

    def __init__(self, column, train_name="train"):
        super().__init__(column, train_name)


class Criterion_1:

    def __init__(self, ideal, train, median_deviation):
        self.ideal = ideal
        self.train = train
        self.median_deviation = median_deviation

class Test(Function):

    def __init__(self, column, test_name = "test"):
        super().__init__(column, test_name)

class Criterion_2:
     def __init__(self, ideal, criterion_2):
        self.ideal = ideal
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

def visualize_ideal_and_train(four_ideal_fnc):

    x = Function("x", "train")
    x = x.get_column()

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

CRITERION 2. CODE


"""

def get_dev_and_maxdev(ideal_name = "ideal", train_name = "train", test_name = "test", ideal_len = 51, train_len = 5):
    # for loop to get all the deviations between each test point and each ideal function

    four_deviations = []
    hallo = Test("x", test_name)
    hallo2 = Test("y", test_name)
    x_column = hallo.get_column()
    y_column = hallo2.get_column()
    for i in four_ideal_functions(ideal_name, train_name, ideal_len, train_len):
        
        #first_time = True
        all_deviations = []
        deviation = []
        #y_test = []
        counter = 0
        for x in x_column:
            
            # connect to database
            conn = sqlite3.connect("FindingFunctions.db")   
            cur = conn.cursor()

            ideal_query = cur.execute("SELECT " + i.ideal + " FROM " + ideal_name + " WHERE x=" + str(x))
            for cell in ideal_query: 
                y_ideal = np.asarray(cell)

            deviation = abs(y_ideal - y_column[counter])
            all_deviations.append(deviation[0])
            counter = counter + 1
            
            # commit and close connection to database    
            conn. commit()
            conn.close()
        

        # calculate max deviation between the respective train and ideal function
        y = Ideal(i.ideal, ideal_name)
        f = Train(i.train, train_name)
        max_deviation = y.max_deviation(f)

        # ab hier test einer neuen methode
        criterion_2_array = []

        for x in all_deviations:
            if(x <= (max_deviation * np.sqrt(2))):

                #z = (max_deviation * np.sqrt(2)) - x
                np.array(criterion_2_array.append(x))

            else:

                y = "None"
                np.array(criterion_2_array.append(y))

        #print(criterion_2_array)
        criterion_2 = Criterion_2(i.ideal, criterion_2_array)
        four_deviations.append(criterion_2)

    return four_deviations
    
# for loop to get all the results of criterion 2 and save it to the Object

def get_endresult(x):
    deviation = ["None"]* len(x)
    result = ["None"]* len(x)
    for i in get_dev_and_maxdev():
        y=0
        for cell in i.criterion_2:

            if cell != "None":
                if deviation[y] == "None":
                    deviation[y] = cell
                    result[y] = i.ideal
                else:
                    deviation[y] = (deviation [y], cell)
                    result[y] = (result[y], i.ideal)
            y = y+1
    return deviation, result

"""

CRITERION 2. VISUALIZATION


"""

#output_file = 'index.html'
#evtl max y und max x von den testpoints verwenden
def visualize(x, y, x_1, y_1, x_error_band, y_error_band, y_error_band_minus, x_column, y_column):
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





        
def main():

    visualize_ideal_and_train(four_ideal_functions())

    x = Function("x", "test")
    x = x.get_column()
    print("endresult")
    endresult = get_endresult(x)
    print(endresult[0])
    print(endresult[1])

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
        y = Ideal(i.ideal)
        y_ideal_column.append(y.get_column()) 
        f = Train(i.train)
        f_y_column.append(f.get_column())
        y_error_band.append(y.get_column() + (y.max_deviation(f) * np.sqrt(2)))
        y_error_band_minus.append(y.get_column() - (y.max_deviation(f) * np.sqrt(2))) 
        visualize(x_ideal_column, y_ideal_column[k], x_ideal_column, f_y_column[k], x_ideal_column, y_error_band[k], y_error_band_minus[k], x_column, y_column)
        k = k+1

if __name__ == '__main__':
    main()

# commit and close connection to database    
conn. commit()
conn.close()

