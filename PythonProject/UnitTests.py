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


if __name__ == '__main__':
    unittest.main()


# commit and close connection to database    
conn. commit()
conn.close()
