import datetime as dt
import math
import unittest

import numpy as np
import pandas as pd

import thalesians.tsa.conversions as conv
import thalesians.tsa.timeconsts as timeconsts

class TestConversions(unittest.TestCase):
    def test_numpy_datetime64_to_python_datetime(self):
        numpy_datetime64 = np.datetime64('2019-09-10T14:19:31.357')
        python_datetime = dt.datetime(2019, 9, 10, 14, 19, 31, 357000)
        converted = conv.numpy_datetime64_to_python_datetime(numpy_datetime64)
        self.assertEqual(converted, python_datetime)
    
        numpy_datetime64s = [np.datetime64('2019-09-09T14:19:31.357'), np.datetime64('2019-09-10T14:19:31.357')]
        python_datetimes = [dt.datetime(2019, 9, 9, 14, 19, 31, 357000), dt.datetime(2019, 9, 10, 14, 19, 31, 357000)]
        converted = conv.numpy_datetime64_to_python_datetime(numpy_datetime64s)
        self.assertEqual(converted, python_datetimes)

    def test_pandas_timestamp_to_python_datetime(self):
        pandas_timestamp = pd.Timestamp(dt.datetime(2019, 9, 10, 14, 19, 31, 357000))
        python_datetime = dt.datetime(2019, 9, 10, 14, 19, 31, 357000)
        converted = conv.pandas_timestamp_to_python_datetime(pandas_timestamp)
        self.assertEqual(converted, python_datetime)
        
        pandas_timestamps = [pd.Timestamp(dt.datetime(2019, 9, 9, 14, 19, 31, 357000)), pd.Timestamp(dt.datetime(2019, 9, 10, 14, 19, 31, 357000))]
        python_datetimes = [dt.datetime(2019, 9, 9, 14, 19, 31, 357000), dt.datetime(2019, 9, 10, 14, 19, 31, 357000)]
        converted = conv.pandas_timestamp_to_python_datetime(pandas_timestamps)
        self.assertEqual(converted, python_datetimes)

    def test_numpy_timedelta64_to_python_timedelta(self):
        numpy_timedelta64 = np.timedelta64(5, 's')
        python_timedelta = dt.timedelta(seconds=5)
        converted = conv.numpy_timedelta64_to_python_timedelta(numpy_timedelta64)
        self.assertEqual(converted, python_timedelta)
    
        numpy_timedelta64s = [np.timedelta64(5, 's'), np.timedelta64(10, 's')]
        python_timedeltas = [dt.timedelta(seconds=5), dt.timedelta(seconds=10)]
        converted = conv.numpy_timedelta64_to_python_timedelta(numpy_timedelta64s)
        self.assertEqual(converted, python_timedeltas)
    
    def test_numpy_timedelta64_to_python_time(self):
        numpy_timedelta64 = np.timedelta64(5, 's')
        python_time = dt.time(0, 0, 5)
        converted = conv.numpy_timedelta64_to_python_time(numpy_timedelta64)
        self.assertEqual(converted, python_time)

        numpy_timedelta64s = [np.timedelta64(5, 's'), np.timedelta64(10, 's')]
        python_times = [dt.time(0, 0, 5), dt.time(0, 0, 10)]
        converted = conv.numpy_timedelta64_to_python_time(numpy_timedelta64s)
        self.assertEqual(converted, python_times)

    def test_pandas_timedelta_to_python_timedelta(self):
        pandas_timedelta = pd.Timedelta(5, 's')
        python_timedelta = dt.timedelta(seconds=5)
        converted = conv.pandas_timedelta_to_python_timedelta(pandas_timedelta)
        self.assertEqual(converted, python_timedelta)

        pandas_timedeltas = [pd.Timedelta(5, 's'), pd.Timedelta(10, 's')]
        python_timedeltas = [dt.timedelta(seconds=5), dt.timedelta(seconds=10)]
        converted = conv.pandas_timedelta_to_python_timedelta(pandas_timedeltas)
        self.assertEqual(converted, python_timedeltas)

    def test_to_python_date(self):
        python_datetime = dt.datetime(2019, 9, 10, 14, 19, 31, 357000)
        python_date = dt.date(2019, 9, 10)
        converted = conv.to_python_date(python_datetime)
        self.assertEquals(converted, python_date)

        python_datetimes = [dt.datetime(2019, 9, 9, 14, 19, 31, 357000), dt.datetime(2019, 9, 10, 14, 19, 31, 357000)]
        python_dates = [dt.date(2019, 9, 9), dt.date(2019, 9, 10)]
        converted = conv.to_python_date(python_datetimes)
        self.assertEquals(converted, python_dates)

        python_date = dt.date(2019, 9, 10)
        converted = conv.to_python_date(python_date)
        self.assertEqual(converted, python_date)
        
        python_dates = [dt.date(2019, 9, 9), dt.date(2019, 9, 10)]
        converted = conv.to_python_date(python_dates)
        self.assertEqual(converted, python_dates)
        
        numpy_datetime64 = np.datetime64('2019-09-10T14:19:31.357')
        python_date = dt.date(2019, 9, 10)
        converted = conv.to_python_date(numpy_datetime64)
        self.assertEqual(converted, python_date)
        
        numpy_datetime64s = [np.datetime64('2019-09-09T14:19:31.357'), np.datetime64('2019-09-10T14:19:31.357')]
        python_dates = [dt.date(2019, 9, 9), dt.date(2019, 9, 10)]
        converted = conv.to_python_date(numpy_datetime64s)
        self.assertEqual(converted, python_dates)
        
        pandas_timestamp = pd.Timestamp(dt.datetime(2019, 9, 10, 14, 19, 31, 357000))
        python_date = dt.date(2019, 9, 10)
        converted = conv.to_python_date(pandas_timestamp)
        self.assertEqual(converted, python_date)
        
        pandas_timestamps = [pd.Timestamp(dt.datetime(2019, 9, 9, 14, 19, 31, 357000)), pd.Timestamp(dt.datetime(2019, 9, 10, 14, 19, 31, 357000))]
        python_dates = [dt.date(2019, 9, 9), dt.date(2019, 9, 10)]
        converted = conv.to_python_date(pandas_timestamps)
        self.assertEqual(converted, python_dates)
        
        datetime_str = '2019.09.10'
        python_date = dt.date(2019, 9, 10)
        converted = conv.to_python_date(datetime_str)
        self.assertEqual(converted, python_date)
        
        datetime_strs = ['2019.09.09', '2019.09.10']
        python_dates = [dt.date(2019, 9, 9), dt.date(2019, 9, 10)]
        converted = conv.to_python_date(datetime_strs)
        self.assertEqual(converted, python_dates)
        
        misc = [pd.Timestamp(dt.datetime(2019, 9, 9, 14, 19, 31, 357000)), '2019.09.10']
        python_dates = [dt.date(2019, 9, 9), dt.date(2019, 9, 10)]
        converted = conv.to_python_date(misc)
        self.assertEqual(converted, python_dates)
    
    def test_to_python_time(self):
        python_time = dt.time(14, 19, 31, 357000)
        converted = conv.to_python_time(python_time)
        self.assertEquals(converted, python_time)
        
        python_times = [dt.time(13, 19, 31, 357000), dt.time(14, 19, 31, 357000)]
        converted = conv.to_python_time(python_times)
        self.assertEquals(converted, python_times)
        
        python_datetime = dt.datetime(2019, 9, 10, 14, 19, 31, 357000)
        python_time = dt.time(14, 19, 31, 357000)
        converted = conv.to_python_time(python_datetime)
        self.assertEquals(converted, python_time)

        python_datetimes = [dt.datetime(2019, 9, 10, 13, 19, 31, 357000), dt.datetime(2019, 9, 10, 14, 19, 31, 357000)]
        python_times = [dt.time(13, 19, 31, 357000), dt.time(14, 19, 31, 357000)]
        converted = conv.to_python_time(python_datetimes)
        self.assertEquals(converted, python_times)

        numpy_datetime64 = np.datetime64('2019-09-10T14:19:31.357')
        python_time = dt.time(14, 19, 31, 357000)
        converted = conv.to_python_time(numpy_datetime64)
        self.assertEqual(converted, python_time)
        
        numpy_datetime64s = [np.datetime64('2019-09-10T13:19:31.357'), np.datetime64('2019-09-10T14:19:31.357')]
        python_times = [dt.time(13, 19, 31, 357000), dt.time(14, 19, 31, 357000)]
        converted = conv.to_python_time(numpy_datetime64s)
        self.assertEqual(converted, python_times)
        
        pandas_timestamp = pd.Timestamp(dt.datetime(2019, 9, 10, 14, 19, 31, 357000))
        python_time = dt.time(14, 19, 31, 357000)
        converted = conv.to_python_time(pandas_timestamp)
        self.assertEqual(converted, python_time)
        
        pandas_timestamps = [pd.Timestamp(dt.datetime(2019, 9, 10, 13, 19, 31, 357000)), pd.Timestamp(dt.datetime(2019, 9, 10, 14, 19, 31, 357000))]
        python_times = [dt.time(13, 19, 31, 357000), dt.time(14, 19, 31, 357000)]
        converted = conv.to_python_time(pandas_timestamps)
        self.assertEqual(converted, python_times)
        
        python_time = dt.time(14, 19, 31, 357000)
        microseconds = 14 * timeconsts.MICROSECONDS_PER_HOUR +\
                19 * timeconsts.MICROSECONDS_PER_MINUTE +\
                31 * timeconsts.MICROSECONDS_PER_SECOND +\
                357000
        numpy_timedelta64 = np.timedelta64(microseconds, 'us')
        converted = conv.to_python_time(numpy_timedelta64)
        self.assertEqual(converted, python_time)
        
        python_times = [dt.time(13, 19, 31, 357000), dt.time(14, 19, 31, 357000)]
        microseconds1 = 13 * timeconsts.MICROSECONDS_PER_HOUR +\
                19 * timeconsts.MICROSECONDS_PER_MINUTE +\
                31 * timeconsts.MICROSECONDS_PER_SECOND +\
                357000
        microseconds2 = 14 * timeconsts.MICROSECONDS_PER_HOUR +\
                19 * timeconsts.MICROSECONDS_PER_MINUTE +\
                31 * timeconsts.MICROSECONDS_PER_SECOND +\
                357000
        numpy_timedelta64s = [np.timedelta64(microseconds1, 'us'), np.timedelta64(microseconds2, 'us')]
        converted = conv.to_python_time(numpy_timedelta64s)
        self.assertEqual(converted, python_times)
        
        time_str = '14:19:31.357'
        python_time = dt.time(14, 19, 31, 357000)
        converted = conv.to_python_time(time_str)
        self.assertEqual(converted, python_time)
    
        time_strs = ['13:19:31.357', '14:19:31.357']
        python_times = [dt.time(13, 19, 31, 357000), dt.time(14, 19, 31, 357000)]
        converted = conv.to_python_time(time_strs)
        self.assertEqual(converted, python_times)
        
        misc = [dt.time(13, 19, 31, 357000), '14:19:31.357']
        python_times = [dt.time(13, 19, 31, 357000), dt.time(14, 19, 31, 357000)]
        converted = conv.to_python_time(misc)
        self.assertEqual(converted, python_times)
    
    def test_to_python_datetime(self):
        pandas_timestamp = pd.Timestamp(dt.datetime(2019, 9, 10, 14, 19, 31, 357000))
        python_datetime = dt.datetime(2019, 9, 10, 14, 19, 31, 357000)
        converted = conv.to_python_datetime(pandas_timestamp)
        self.assertEqual(converted, python_datetime)
        
        pandas_timestamps = [pd.Timestamp(dt.datetime(2019, 9, 10, 13, 19, 31, 357000)), pd.Timestamp(dt.datetime(2019, 9, 10, 14, 19, 31, 357000))]
        python_datetimes = [dt.datetime(2019, 9, 10, 13, 19, 31, 357000), dt.datetime(2019, 9, 10, 14, 19, 31, 357000)]
        converted = conv.to_python_datetime(pandas_timestamps)
        self.assertEqual(converted, python_datetimes)
        
        numpy_datetime64 = np.datetime64('2019-09-10T14:19:31.357')
        python_datetime = dt.datetime(2019, 9, 10, 14, 19, 31, 357000)
        converted = conv.to_python_datetime(numpy_datetime64)
        self.assertEqual(converted, python_datetime)
        
        numpy_datetime64s = [np.datetime64('2019-09-10T13:19:31.357'), np.datetime64('2019-09-10T14:19:31.357')]
        python_datetimes = [dt.datetime(2019, 9, 10, 13, 19, 31, 357000), dt.datetime(2019, 9, 10, 14, 19, 31, 357000)]
        converted = conv.to_python_datetime(numpy_datetime64s)
        self.assertEqual(converted, python_datetimes)
        
        python_datetime = dt.datetime(2019, 9, 10, 14, 19, 31, 357000)
        converted = conv.to_python_datetime(python_datetime)
        self.assertEqual(converted, python_datetime)
        
        python_datetimes = [dt.datetime(2019, 9, 10, 13, 19, 31, 357000), dt.datetime(2019, 9, 10, 14, 19, 31, 357000)]
        converted = conv.to_python_datetime(python_datetimes)
        self.assertEqual(converted, python_datetimes)
        
        datetime_str = '2019.09.10T14:19:31.357'
        python_datetime = dt.datetime(2019, 9, 10, 14, 19, 31, 357000)
        converted = conv.to_python_datetime(datetime_str)
        self.assertEqual(converted, python_datetime)
        
        datetime_strs = ['2019.09.10T13:19:31.357', '2019.09.10T14:19:31.357']
        python_datetimes = [dt.datetime(2019, 9, 10, 13, 19, 31, 357000), dt.datetime(2019, 9, 10, 14, 19, 31, 357000)]
        converted = conv.to_python_datetime(datetime_strs)
        self.assertEqual(converted, python_datetimes)
        
        misc = [dt.datetime(2019, 9, 10, 13, 19, 31, 357000), '2019.09.10T14:19:31.357']
        python_datetimes = [dt.datetime(2019, 9, 10, 13, 19, 31, 357000), dt.datetime(2019, 9, 10, 14, 19, 31, 357000)]
        converted = conv.to_python_datetime(misc)
        self.assertEqual(converted, python_datetimes)
        
    def test_to_python_timedelta(self):
        numpy_timedelta64 = np.timedelta64(5, 's')
        python_timedelta = dt.timedelta(seconds=5)
        converted = conv.to_python_timedelta(numpy_timedelta64)
        self.assertEqual(converted, python_timedelta)

        numpy_timedelta64s = [np.timedelta64(5, 's'), np.timedelta64(10, 's')]
        python_timedeltas = [dt.timedelta(seconds=5), dt.timedelta(seconds=10)]
        converted = conv.to_python_timedelta(numpy_timedelta64s)
        self.assertEqual(converted, python_timedeltas)

        pandas_timedelta = pd.Timedelta(5, 's')
        python_timedelta = dt.timedelta(seconds=5)
        converted = conv.to_python_timedelta(pandas_timedelta)
        self.assertEqual(converted, python_timedelta)

        pandas_timedeltas = [pd.Timedelta(5, 's'), pd.Timedelta(10, 's')]
        python_timedeltas = [dt.timedelta(seconds=5), dt.timedelta(seconds=10)]
        converted = conv.to_python_timedelta(pandas_timedeltas)
        self.assertEqual(converted, python_timedeltas)

        python_timedelta = dt.timedelta(seconds=5)
        converted = conv.to_python_timedelta(python_timedelta)
        self.assertEqual(converted, python_timedelta)
        
        python_timedeltas = [dt.timedelta(seconds=5), dt.timedelta(seconds=10)]
        converted = conv.to_python_timedelta(python_timedeltas)
        self.assertEqual(converted, python_timedeltas)
        
    def test_to_python_int(self):
        self.assertEquals(conv.to_python_int(3), 3)
        with self.assertRaises(ValueError):
            conv.to_python_int(3.5)
        self.assertEquals(conv.to_python_int(3.5, allow_floats=True), 3)
        self.assertEquals(conv.to_python_int('3'), 3)
        self.assertEquals(conv.to_python_int('   3  '), 3)
        with self.assertRaises(ValueError):
            conv.to_python_int(None)
        self.assertEquals(conv.to_python_int(None, allow_none=True), None)
        self.assertEquals(conv.to_python_int([3.5, '   3  '], allow_floats=True), [3, 3])
    
    def test_to_python_float(self):
        self.assertEquals(conv.to_python_float(3.5), 3.5)
        with self.assertRaises(ValueError):
            conv.to_python_float(3)
        self.assertEquals(conv.to_python_float(3, allow_ints=True), 3.)
        self.assertEquals(conv.to_python_float('3.5'), 3.5)
        self.assertEquals(conv.to_python_float('   3.5  '), 3.5)
        with self.assertRaises(ValueError):
            conv.to_python_float(None)
        self.assertEquals(conv.to_python_float(None, allow_none=True), None)
        self.assertEquals(conv.to_python_float([3, '   3.5  '], allow_ints=True), [3., 3.5])
    
    def test_str_to_int(self):
        self.assertEqual(conv.str_to_int('5'), 5)
        self.assertEqual(conv.str_to_int('  5 '), 5)
        self.assertEqual(conv.str_to_int('  x ', raise_value_error=False), None)
        self.assertEqual(conv.str_to_int('  5.7 ', raise_value_error=False), None)
    
    def test_strs_to_int(self):
        self.assertEqual(conv.strs_to_int(['5', '  5 ']), [5, 5])

    def test_str_to_float(self):
        self.assertEqual(conv.str_to_float('5'), 5.)
        self.assertEqual(conv.str_to_float('5.7'), 5.7)
        self.assertEqual(conv.str_to_float('  5.7 '), 5.7)
        self.assertTrue(math.isnan(conv.str_to_float('  x ', raise_value_error=False)))
        self.assertEqual(conv.str_to_float('  x ', none_result=None, raise_value_error=False), None)
        
    def test_strs_to_float(self):
        self.assertEqual(conv.strs_to_float(['5', '5.7']), [5., 5.7])
    
    def test_str_to_date(self):
        self.assertEqual(conv.str_to_date('2019.09.10'), dt.date(2019, 9, 10))
        self.assertEqual(conv.str_to_date('2019-09-10'), dt.date(2019, 9, 10))
        self.assertEqual(conv.str_to_date('2019/09/10'), dt.date(2019, 9, 10))
        self.assertEqual(conv.str_to_date('20190910'), dt.date(2019, 9, 10))
                
    def test_strs_to_date(self):
        self.assertEqual(
                conv.strs_to_date(['2019.09.10', '2019-09-10', '2019/09/10', '20190910']),
                [dt.date(2019, 9, 10), dt.date(2019, 9, 10), dt.date(2019, 9, 10), dt.date(2019, 9, 10)])
    
    def test_str_to_time(self):
        self.assertEqual(conv.str_to_time('10:49:31.357289'), dt.time(10, 49, 31, 357289))
        self.assertEqual(conv.str_to_time('10:49:31.357'), dt.time(10, 49, 31, 357000))
        self.assertEqual(conv.str_to_time('10:49:31'), dt.time(10, 49, 31))
        self.assertEqual(conv.str_to_time('10:49'), dt.time(10, 49))
        
        self.assertEqual(conv.str_to_time(''), None)
        
    def test_strs_to_time(self):
        self.assertEqual(
            conv.strs_to_time(['10:49:31.357289', '10:49:31.357', '10:49:31', '10:49']),
            [dt.time(10, 49, 31, 357289), dt.time(10, 49, 31, 357000), dt.time(10, 49, 31), dt.time(10, 49)])
    
    def test_str_to_datetime(self):
        self.assertEqual(conv.str_to_datetime('2019.09.10 10:49:31.357289'), dt.datetime(2019, 9, 10, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2019.09.10 10:49:31.357'), dt.datetime(2019, 9, 10, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2019.09.10 10:49:31'), dt.datetime(2019, 9, 10, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2019.09.10 10:49'), dt.datetime(2019, 9, 10, 10, 49))

        self.assertEqual(conv.str_to_datetime('2019-09-10 10:49:31.357289'), dt.datetime(2019, 9, 10, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2019-09-10 10:49:31.357'), dt.datetime(2019, 9, 10, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2019-09-10 10:49:31'), dt.datetime(2019, 9, 10, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2019-09-10 10:49'), dt.datetime(2019, 9, 10, 10, 49))

        self.assertEqual(conv.str_to_datetime('2019/09/10 10:49:31.357289'), dt.datetime(2019, 9, 10, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2019/09/10 10:49:31.357'), dt.datetime(2019, 9, 10, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2019/09/10 10:49:31'), dt.datetime(2019, 9, 10, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2019/09/10 10:49'), dt.datetime(2019, 9, 10, 10, 49))

        self.assertEqual(conv.str_to_datetime('2019.09.10T10:49:31.357289'), dt.datetime(2019, 9, 10, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2019.09.10T10:49:31.357'), dt.datetime(2019, 9, 10, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2019.09.10T10:49:31'), dt.datetime(2019, 9, 10, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2019.09.10T10:49'), dt.datetime(2019, 9, 10, 10, 49))

        self.assertEqual(conv.str_to_datetime('2019-09-10T10:49:31.357289'), dt.datetime(2019, 9, 10, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2019-09-10T10:49:31.357'), dt.datetime(2019, 9, 10, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2019-09-10T10:49:31'), dt.datetime(2019, 9, 10, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2019-09-10T10:49'), dt.datetime(2019, 9, 10, 10, 49))

        self.assertEqual(conv.str_to_datetime('2019/09/10T10:49:31.357289'), dt.datetime(2019, 9, 10, 10, 49, 31, 357289))
        self.assertEqual(conv.str_to_datetime('2019/09/10T10:49:31.357'), dt.datetime(2019, 9, 10, 10, 49, 31, 357000))
        self.assertEqual(conv.str_to_datetime('2019/09/10T10:49:31'), dt.datetime(2019, 9, 10, 10, 49, 31))
        self.assertEqual(conv.str_to_datetime('2019/09/10T10:49'), dt.datetime(2019, 9, 10, 10, 49))

        self.assertEqual(conv.str_to_datetime(''), None)
        
    def test_strs_to_datetime(self):
        self.assertEqual(
                conv.strs_to_datetime(['2019.09.10 10:49:31.357289', '2019-09-10 10:49:31.357', '2019/09/10 10:49:31', '2019.09.10T10:49']),
                [dt.datetime(2019, 9, 10, 10, 49, 31, 357289), dt.datetime(2019, 9, 10, 10, 49, 31, 357000), dt.datetime(2019, 9, 10, 10, 49, 31), dt.datetime(2019, 9, 10, 10, 49)])
        
if __name__ == '__main__':
    unittest.main()
