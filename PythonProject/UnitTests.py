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
        
        max_deviation = []
        #all_deviations = []
        for i in result:
            max_deviation.append(i.criterion_2)
            #all_deviations.append(i.deviation)

        self.assertEqual(max_deviation[1], 2)
        #self.assertEqual(all_deviations[1], 1)

        

        

if __name__ == '__main__':
    unittest.main()


# commit and close connection to database    
conn. commit()
conn.close()
