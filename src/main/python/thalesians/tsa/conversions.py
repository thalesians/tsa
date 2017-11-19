import datetime as dt

import numpy as np
import pandas as pd

import thalesians.tsa.checks as checks
import thalesians.tsa.times as times

def numpy_datetime64_to_python_datetime(x):
    if isinstance(x, np.datetime64):
        # For some reason, the following doesn't always work. Instead of a Python datetime, an int may be returned. This
        # may be due to a bug in NumPy. This function detects this issue and employs an alternative strategy to convert
        # x to a Python datetime.
        r = x.astype(dt.datetime)
        if isinstance(x, dt.datetime): return r
        year = x.astype('datetime64[Y]').astype(int) + 1970
        xm = x.astype('datetime64[M]')
        month = xm.astype(int) % 12 + 1
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
        if microsecond % 10 == 9: r += dt.timedelta(microseconds=1)
        return r
    raise ValueError('Unable to convert "%s" to Python datetime' % str(x))

def pandas_timestamp_to_python_datetime(x):
    if isinstance(x, pd.Timestamp): return x.to_pydatetime()
    raise ValueError('Unable to convert "%s" to Python datetime' % str(x))
    
def to_python_datetime(x, *args, **kwargs):
    if isinstance(x, np.datetime64): return numpy_datetime64_to_python_datetime(x, *args, **kwargs)
    elif isinstance(x, pd.Timestamp): return pandas_timestamp_to_python_datetime(x, *args, **kwargs)
    elif checks.is_string(x): return str_to_datetime(x, *args, **kwargs)
    raise ValueError('Unable to convert "%s" to Python datetime' % str(x))

def str_to_int(s, none_values=[''], none_result=None, raise_value_error=True):
    s = s.strip()
    if s in none_values: return none_result
    try: return int(s)
    except:
        if raise_value_error: raise ValueError('Unexpected int string: "%s"' % str(s))
        return none_result
            
def str_to_float(s, none_values=[''], none_result=float('nan'), raise_value_error=True):
    s = s.strip()
    if s in none_values: return none_result
    try: return float(s)
    except:
        if raise_value_error: raise ValueError('Unexpected float string: "%s"' % str(s))
        return none_result
            
def _str_to_x_return(obj, x_format, x_format_idx, return_extra_info):
    if return_extra_info:
        return obj, x_format, x_format_idx
    else:
        return obj
    
def _str_to_x(s, x_format, none_values, none_result, raise_value_error, return_extra_info, x_name, conv):
    if checks.is_string(x_format): x_format = [x_format]
    s = s.strip()
    if (s in none_values): return _str_to_x_return(none_result, None, None, return_extra_info)
    result = None
    for x_format_idx, x_format in enumerate(x_format):
        try:
            result = conv(s, x_format)
            break
        except: pass
    if result is None:
        if raise_value_error: raise ValueError('Unexpected %s string: "%s"' % (x_name, str(s)))
        return _str_to_x_return(none_result, None, None, return_extra_info)
    return _str_to_x_return(result, x_format, x_format_idx, return_extra_info)

_date_formats = ['%Y.%m.%d', '%Y-%m-%d', '%Y/%m/%d', '%Y%m%d']

def str_to_date(s, date_format=_date_formats, none_values=[''], none_result=None,
                raise_value_error=True, return_extra_info=False):
    return _str_to_x(s, date_format, none_values, none_result, raise_value_error, return_extra_info, 'date',
                     lambda s, f: dt.datetime.strptime(s, f).date())
    
_time_formats = ['%H:%M:%S.%f', '%H:%M:%S', '%H:%M']
    
def str_to_time(s, time_format=_time_formats, none_values=[''], none_result=None,
                raise_value_error=True, return_extra_info=False):
    return _str_to_x(s, time_format, none_values, none_result, raise_value_error, return_extra_info, 'time',
                     lambda s, f: dt.datetime.strptime(s, f).time())

_datetime_formats = []

for df in _date_formats:
    for tf in _time_formats:
        _datetime_formats.append('%s %s' % (df, tf))
        _datetime_formats.append('%sT%s' % (df, tf))
    
def str_to_datetime(s, datetime_format=_datetime_formats, none_values=[''], none_result=None,
                raise_value_error=True, return_extra_info=False):
    return _str_to_x(s, datetime_format, none_values, none_result, raise_value_error, return_extra_info, 'datetime',
                     lambda s, f: dt.datetime.strptime(s, f))
