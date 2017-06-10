import unittest
import datetime as dt

import numpy as np
import numpy.testing as npt

import tsa.random as rnd
import tsa.numpyutils as npu

# In case you are interested, the numbers used in these tests come from the A000108 sequence (Catalan numbers)

class TestRandom(unittest.TestCase):
    def testrandomstate(self):
        rs = np.random.RandomState(seed=42)
        rnd.randomstate(rs, force=True)
        self.assertEqual(rnd.randomstate(), rs)
        with self.assertRaises(npu.NumericError):
            rnd.randomstate(rs)
        rs = np.random.RandomState(seed=132)
        rnd.randomstate(rs, force=True)
        self.assertEqual(rnd.randomstate(), rs)
            
    def testexponential(self):
        rnd.randomstate(np.random.RandomState(seed=42), force=True)

        values = rnd.exponential(.25, size=5)
        npt.assert_almost_equal(values, np.array([ 0.117317 ,  0.7525304,  0.3291864,  0.2282356,  0.0424062]))
        
        values = rnd.exponential(.25, size=1000000)
        npt.assert_almost_equal(np.mean(values), .25, decimal=3)
        
        values = rnd.exponential(dt.timedelta(minutes=25), size=5)
        values = [v.total_seconds() for v in values]
        npt.assert_almost_equal(values, np.array([1138.023383, 2274.520394, 265.023984, 221.528354, 3365.675561]))
        
        values = rnd.exponential(dt.timedelta(minutes=25), size=1000000)
        npt.assert_almost_equal(np.mean([v.total_seconds() for v in values]), 1497.6779794581771, decimal=3)
        
if __name__ == '__main__':
    unittest.main()
    