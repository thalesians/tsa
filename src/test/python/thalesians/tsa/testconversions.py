import datetime as dt
import math
import unittest

import numpy as np
import pandas as pd

import thalesians.tsa.conversions as conv

class TestConversions(unittest.TestCase):
    def test_numpy_datetime64_to_python_datetime(self):
        self.assertEqual(conv.numpy_datetime64_to_python_datetime(np.datetime64('2017-11-19T10:49:31.357')), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
    
    def test_pandas_timestamp_to_python_datetime(self):
        self.assertEqual(conv.pandas_timestamp_to_python_datetime(pd.Timestamp(dt.datetime(2017, 11, 19, 10, 49, 31, 357000))), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
    
    def test_to_python_datetime(self):
        self.assertEqual(conv.to_python_datetime(np.datetime64('2017-11-19T10:49:31.357')), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
        self.assertEqual(conv.to_python_datetime(pd.Timestamp(dt.datetime(2017, 11, 19, 10, 49, 31, 357000))), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
        self.assertEqual(conv.to_python_datetime('2017.11.19T10:49:31.357'), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
    
    def test_str_to_int(self):
        self.assertEqual(conv.str_to_int('5'), 5)
        self.assertEqual(conv.str_to_int('  5 '), 5)
        self.assertEqual(conv.str_to_int('  x ', raise_value_error=False), None)
        self.assertEqual(conv.str_to_int('  5.7 ', raise_value_error=False), None)
    
    def test_str_to_float(self):
        self.assertEqual(conv.str_to_float('5'), 5.)
        self.assertEqual(conv.str_to_float('5.7'), 5.7)
        self.assertEqual(conv.str_to_float('  5.7 '), 5.7)
        self.assertTrue(math.isnan(conv.str_to_float('  x ', raise_value_error=False)))
        self.assertEqual(conv.str_to_float('  x ', none_result=None, raise_value_error=False), None)
    
    def test_str_to_date(self):
        self.assertEqual(conv.str_to_date('2017.11.19'), dt.date(2017, 11, 19))
        self.assertEqual(conv.str_to_date('2017-11-19'), dt.date(2017, 11, 19))
        self.assertEqual(conv.str_to_date('2017/11/19'), dt.date(2017, 11, 19))
        self.assertEqual(conv.str_to_date('20171119'), dt.date(2017, 11, 19))
        
        self.assertEqual(conv.str_to_date(''), None)
    
    def test_str_to_time(self):
        self.assertEqual(conv.str_to_time('10:49:31.357289'), dt.time(10, 49, 31, 357289))
        self.assertEqual(conv.str_to_time('10:49:31.357'), dt.time(10, 49, 31, 357000))
        self.assertEqual(conv.str_to_time('10:49:31'), dt.time(10, 49, 31))
        self.assertEqual(conv.str_to_time('10:49'), dt.time(10, 49))
        
        self.assertEqual(conv.str_to_time(''), None)
    
    def test_str_to_datetime(self):
        self.assertEqual(conv.str_to_datetime('2017.11.19 10:49:31.357289'), dt.datetime(2017, 11, 19, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2017.11.19 10:49:31.357'), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2017.11.19 10:49:31'), dt.datetime(2017, 11, 19, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2017.11.19 10:49'), dt.datetime(2017, 11, 19, 10, 49))

        self.assertEqual(conv.str_to_datetime('2017-11-19 10:49:31.357289'), dt.datetime(2017, 11, 19, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2017-11-19 10:49:31.357'), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2017-11-19 10:49:31'), dt.datetime(2017, 11, 19, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2017-11-19 10:49'), dt.datetime(2017, 11, 19, 10, 49))

        self.assertEqual(conv.str_to_datetime('2017/11/19 10:49:31.357289'), dt.datetime(2017, 11, 19, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2017/11/19 10:49:31.357'), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2017/11/19 10:49:31'), dt.datetime(2017, 11, 19, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2017/11/19 10:49'), dt.datetime(2017, 11, 19, 10, 49))

        self.assertEqual(conv.str_to_datetime('2017.11.19T10:49:31.357289'), dt.datetime(2017, 11, 19, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2017.11.19T10:49:31.357'), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2017.11.19T10:49:31'), dt.datetime(2017, 11, 19, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2017.11.19T10:49'), dt.datetime(2017, 11, 19, 10, 49))

        self.assertEqual(conv.str_to_datetime('2017-11-19T10:49:31.357289'), dt.datetime(2017, 11, 19, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2017-11-19T10:49:31.357'), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2017-11-19T10:49:31'), dt.datetime(2017, 11, 19, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2017-11-19T10:49'), dt.datetime(2017, 11, 19, 10, 49))

        self.assertEqual(conv.str_to_datetime('2017/11/19T10:49:31.357289'), dt.datetime(2017, 11, 19, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2017/11/19T10:49:31.357'), dt.datetime(2017, 11, 19, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2017/11/19T10:49:31'), dt.datetime(2017, 11, 19, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2017/11/19T10:49'), dt.datetime(2017, 11, 19, 10, 49))

        self.assertEqual(conv.str_to_datetime(''), None)
        
if __name__ == '__main__':
    unittest.main()
