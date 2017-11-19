import unittest

import thalesians.tsa.times as times

class TestTimes(unittest.TestCase):
    def test_units(self):
        self.assertEqual(times.NANOSECONDS_PER_MICROSECOND, 1000)
        
        self.assertEqual(times.MICROSECONDS_PER_MILLISECOND, 1000)
        self.assertEqual(times.NANOSECONDS_PER_MILLISECOND, times.MICROSECONDS_PER_MILLISECOND * times.NANOSECONDS_PER_MICROSECOND)  
        
        self.assertEqual(times.MILLISECONDS_PER_SECOND, 1000)
        self.assertEqual(times.MICROSECONDS_PER_SECOND, times.MILLISECONDS_PER_SECOND * times.MICROSECONDS_PER_MILLISECOND)
        self.assertEqual(times.NANOSECONDS_PER_SECOND, times.MICROSECONDS_PER_SECOND * times.NANOSECONDS_PER_MICROSECOND)    
        
        self.assertEqual(times.SECONDS_PER_MINUTE, 60)
        self.assertEqual(times.MILLISECONDS_PER_MINUTE, times.SECONDS_PER_MINUTE * times.MILLISECONDS_PER_SECOND)
        self.assertEqual(times.MICROSECONDS_PER_MINUTE, times.MILLISECONDS_PER_MINUTE * times.MICROSECONDS_PER_MILLISECOND)
        self.assertEqual(times.NANOSECONDS_PER_MINUTE, times.MICROSECONDS_PER_MINUTE * times.NANOSECONDS_PER_MICROSECOND)
        
        self.assertEqual(times.MINUTES_PER_HOUR, 60)
        self.assertEqual(times.SECONDS_PER_HOUR, times.MINUTES_PER_HOUR * times.SECONDS_PER_MINUTE)
        self.assertEqual(times.MILLISECONDS_PER_HOUR, times.SECONDS_PER_HOUR * times.MILLISECONDS_PER_SECOND)
        self.assertEqual(times.MICROSECONDS_PER_HOUR, times.MILLISECONDS_PER_HOUR * times.MICROSECONDS_PER_MILLISECOND)
        self.assertEqual(times.NANOSECONDS_PER_HOUR, times.MICROSECONDS_PER_HOUR * times.NANOSECONDS_PER_MICROSECOND)
        
        self.assertEqual(times.HOURS_PER_DAY, 24)
        self.assertEqual(times.MINUTES_PER_DAY, times.HOURS_PER_DAY * times.MINUTES_PER_HOUR)
        self.assertEqual(times.SECONDS_PER_DAY, times.MINUTES_PER_DAY * times.SECONDS_PER_MINUTE)
        self.assertEqual(times.MILLISECONDS_PER_DAY, times.SECONDS_PER_DAY * times.MILLISECONDS_PER_SECOND)
        self.assertEqual(times.MICROSECONDS_PER_DAY, times.MILLISECONDS_PER_DAY * times.MICROSECONDS_PER_MILLISECOND)
        self.assertEqual(times.NANOSECONDS_PER_DAY, times.MICROSECONDS_PER_DAY * times.NANOSECONDS_PER_MICROSECOND)
    
if __name__ == '__main__':
    unittest.main()
    