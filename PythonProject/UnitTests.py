import unittest
import Function
import sqlite3
import numpy as np
#from Function import four_ideal_functions

# connect to database
conn = sqlite3.connect("FindingFunctions.db")   
cur = conn.cursor()


class Test_four_ideal_functions(unittest.TestCase):
    def test_four_ideal_functions(self):
        result = Function.four_ideal_functions(
            ideal_name = "ideal_unittest", 
            train_name = "train_unittest", 
            ideal_len = 3, train_len = 2)
            
        ideal = []
        for i in result:
            ideal.append(i.ideal)

        sod = []
        for i in result:
            sod.append(i.median_deviation)

        self.assertEqual(ideal[0], "y2")
        self.assertEqual(sod[1], 5)
 

class Test_get_dev_and_max_dev(unittest.TestCase):
    def test_get_dev_and_max_dev(self):
        result = Function.get_dev_and_maxdev(
            ideal_name = "ideal_unittest", 
            train_name = "train_unittest", 
            test_name = "test_unittest",
            ideal_len = 3, train_len = 2)
        
        criterion_2 = []
        for i in result:
            criterion_2.append(i.criterion_2)

        # y1 of the test dataset
        test = criterion_2[0]
        # deviation of second testpoint
        self.assertEqual(test[1], 1)
        # fourth testpoint out of range
        self.assertEqual(test[3], "None")

class Test_get_endresult(unittest.TestCase):
    def test_get_endresult(self):
        result = Function.get_endresult(
            ideal_name = "ideal_unittest", 
            train_name = "train_unittest", 
            test_name = "test_unittest",
            ideal_len = 3, train_len = 2)
        
        # y1 of the test dataset
        deviation = result[0]
        ideal = result[1]
        # mapping result (deviation) for fifth testpoint
        self.assertEqual(deviation[4], 1)
        # mapping result (deviation) for fourth testpoint
        self.assertEqual(deviation[3], "None")
        # mapping result (ideal functions) for second testpoint
        self.assertEqual(ideal[1], ("y2", "y1"))

        

        

if __name__ == '__main__':
    unittest.main()


# commit and close connection to database    
conn. commit()
conn.close()
