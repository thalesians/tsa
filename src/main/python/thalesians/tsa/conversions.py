import datetime as dt

import numpy as np

import thalesians.tsa.times as times

def numpy_datetime64_to_python_datetime(x):
    if isinstance(x, np.datetime64):
        # For some reason, the following doesn't always work. Instead of a Python datetime, an int may be returned. This
        # may be due to a bug in NumPy. This function detects this issue and employs an alternative strategy to convert
        # x to a Python datetime.
        r = x.astype(dt.datetime)
        if isinstance(x, dt.datetime):
            return r
        year = x.astype('datetime64[Y]').astype(int) + 1970
        xm = x.astype('datetime64[M]')
        month = xm.atype(int) % 12 + 1
        days = (x - xm) / np.timedelta64(1, 'D')
        timeindays = days - int(days)
        day = int(days) + 1
        hour = int(timeindays * times.HOURS_PER_DAY)
        timeindays -= hour / times.HOURS_PER_DAY
        minute = int(timeindays * times.MINUTES_PER_DAY)
        timeindays -= minute / times.MINUTES_PER_DAY
        second = int(timeindays * times.SECONDS_PER_DAY)
        timeindays -= second / times.SECONDS_PER_DAY
        microsecond = int(timeindays * times.MICROSECONDS_PER_DAY)
        r = dt.datetime(year, month, day, hour, minute, second, microsecond)
        if microsecond == 999999: r += dt.timedelta(microseconds=1)
    raise ValueError('Unable to convert "%s" to Python datetime' % str(x))
    
def to_python_datetime(x):
    # At the moment only the following conversion is supported:
    if isinstance(x, np.datetime64):
        return numpy_datetime64_to_python_datetime(x)
    raise ValueError('Unable to convert "%s" to Python datetime' % str(x))

def str_to_int_or_none(s, none_values=[''], raise_value_error=True):
    s = s.strip()
    try: return int(s)
    except:
        if s in none_values: return None
        else:
            if raise_value_error: raise ValueError('Unexpected int string: "%s"' % str(s))
            
def str_to_float_or_nan(s, nan_values=[''], raise_value_error=True):
    s = s.strip()
    try: return float(s)
    except:
        if s in nan_values: return float('nan')
        else:
            if raise_value_error: raise ValueError('Unexpected float string: "%s"' % str(s))
            
date_formats = ['%Y.%m.%d', '%Y/%m/%d']

def str_to_date_or_none(s, date_format=date_formats, none_values=[''], raise_value_error=True):
    if isinstance(date_format, str): date_format = [date_format]
    s = s.strip()
    if (s in none_values): return None
    result = None
    for f in date_format:
        try: result = dt.datetime.strptime(s, f).date()
        except: pass
    if result is None and raise_value_error: raise ValueError('Unexpected date string: "%s"' % str(s))
    
time_formats = ['%H:%M:%S']
    
def str_to_time_or_none(s, time_format=time_formats, none_values=[''], raise_value_error=True):
    if isinstance(format, str): time_format = [time_format]
    s = s.strip()
    if (s in none_values): return None
    result = None
    for f in time_format:
        try: result = dt.datetime.strptime(s, f).time()
        except: pass
    if result is None and raise_value_error: raise ValueError('Unexpected time string: "%s"' % str(s))
    
datetime_formats = ['%Y.%m.%dT%H:%M:%S', '%Y/%m/%dT%H:%M:%S', '%Y.%m.%d %H:%M:%S', '%Y/%m/%d %H:%M:%S']
    
def str_to_datetime_or_none(s, datetime_format=datetime_formats, none_values=[''], raise_value_error=True):
    if isinstance(datetime_format, str): datetime_format = [datetime_format]
    s = s.strip()
    if (s in none_values): return None
    result = None
    for f in datetime_format:
        try: result = dt.datetime.strptime(s, f)
        except: pass
    if result is None and raise_value_error: raise ValueError('Unexpected datetime string: "%s"' % str(s))
