import unittest

import tsa.utils as utils

# In case you are interested, the numbers used in these tests come from the A000108 sequence (Catalan numbers).

class TestUtils(unittest.TestCase):
    def testbatch(self):
        self.assertEqual(utils.batch(3, [429, 5, 2, 14, 42, 132, 1, 1]), [[429, 5, 2], [14, 42, 132], [1, 1]])
        self.assertEqual(utils.batch(4, range(10)), [range(0, 4), range(4, 8), range(8, 10)])
        
if __name__ == '__main__':
    unittest.main()
    