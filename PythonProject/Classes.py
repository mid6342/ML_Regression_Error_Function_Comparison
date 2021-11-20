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
        # get all the cells of the column and write them to a list
        query= cur.execute("SELECT " + self.column + " FROM " + self.table)
        column_list = []
        for cell in query: 
            column_list.append(cell[0])  
        # remove column head
        column_list.pop(0)
        return column_list

class Ideal(Function):

    def __init__(self, column, sum_of_squared_deviations = None):
        super().__init__(column, "ideal")
        self.sum_of_squared_deviations = sum_of_squared_deviations

    def get_median_deviation(self, train_column):
        squared = np.square(np.array(self.get_column()) - np.array(train_column.get_column()))
        return np.sum(squared)
        
    def max_deviation(self, train_column):
        return np.max(np.square(np.array(self.get_column()) - np.array(train_column.get_column())))


class Train(Function):

    def __init__(self, column):
        super().__init__(column, "train")


class MeanDeviation:

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

# commit and close connection to database    
conn. commit()
conn.close()
