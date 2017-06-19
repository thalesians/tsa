import unittest

import thalesians.tsa.exceptions as exc

class TestExceptions(unittest.TestCase):
        
    def testNumericError(self):
        with self.assertRaises(exc.NumericError):
            raise exc.NumericError('Failed to converge')
        
if __name__ == '__main__':
    unittest.main()
    