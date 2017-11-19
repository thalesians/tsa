import datetime as dt

import numpy as np
import pandas as pd

import thalesians.tsa.checks as checks
import thalesians.tsa.times as times
import thalesians.tsa.utils as utils

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

def str_to_x(s, none_values, none_result, raise_value_error, x_name, conv):
    s = s.strip()
    if s in none_values: return none_result
    try: return conv(s)
    except:
        if raise_value_error: raise ValueError('Unexpected %s string: "%s"' % (x_name, str(s)))
        return none_result

def _strs_to_x(ss, none_values, none_result, raise_value_error, min_success_rate, str_to_x):
    success_count = 0
    total_count = 0
    results = []
    for s in ss:
        try:
            result = str_to_x(s, none_values, none_result, raise_value_error=True)
            success_count += 1
        except:
            result = none_result
        total_count += 1
        results.append(result)
    if float(success_count) / total_count < min_success_rate:
        if raise_value_error: raise ValueError('Unable to parse strings')
        results = None
    return results

def str_to_int(s, none_values=[''], none_result=None, raise_value_error=True):
    return str_to_x(s, none_values, none_result, raise_value_error, 'int', int)
            
def strs_to_int(ss, none_values=[''], none_result=None, raise_value_error=True):
    return _strs_to_x(ss, none_values, none_result, raise_value_error, str_to_int)
            
def str_to_float(s, none_values=[''], none_result=float('nan'), raise_value_error=True):
    return str_to_x(s, none_values, none_result, raise_value_error, 'float', float)

def strs_to_float(ss, none_values=[''], none_result=float('nan'), raise_value_error=True):
    return _strs_to_x(ss, none_values, none_result, raise_value_error, str_to_float)
            
def _str_to_x_1_return(obj, x_format, x_format_idx, return_extra_info):
    if return_extra_info:
        return obj, x_format, x_format_idx
    else:
        return obj
    
def _str_to_x_1(s, x_format, none_values, none_result, raise_value_error, return_extra_info, x_name, conv):
    if checks.is_string(x_format): x_format = [x_format]
    s = s.strip()
    if (s in none_values): return _str_to_x_1_return(none_result, None, None, return_extra_info)
    result = None
    for x_format_idx, x_format in enumerate(x_format):
        try:
            result = conv(s, x_format)
            break
        except: pass
    if result is None:
        if raise_value_error: raise ValueError('Unexpected %s string: "%s"' % (x_name, str(s)))
        return _str_to_x_1_return(none_result, None, None, return_extra_info)
    return _str_to_x_1_return(result, x_format, x_format_idx, return_extra_info)

def _strs_to_x_1(ss, x_format, none_values, none_result, raise_value_error, return_extra_info, min_success_rate, str_to_x_1):
    if checks.is_string(x_format): x_format = [x_format]
    success_count = 0
    total_count = 0
    results = []
    x_format_idxs = []
    for s in ss:
        try:
            result, x_format, x_format_idx = \
                    str_to_x_1(s, x_format, none_values, none_result, raise_value_error=True, return_extra_info=True)
            success_count += 1
        except:
            result, x_format, x_format_idx = none_result, None, None
        total_count += 1
        results.append(result)
        x_format_idxs.append(x_format_idx)
    if float(success_count) / total_count >= min_success_rate:
        most_common_x_format_idx = utils.most_common(x_format_idxs)
        most_common_x_format = x_format[most_common_x_format_idx]
    else:
        if raise_value_error: raise ValueError('Unable to parse strings')
        results, most_common_x_format, most_common_x_format_idx = None, None, None
    return (results, most_common_x_format, most_common_x_format_idx) if return_extra_info else results

_date_formats = ['%Y.%m.%d', '%Y-%m-%d', '%Y/%m/%d', '%Y%m%d']

def str_to_date(s, date_format=_date_formats, none_values=[''], none_result=None,
                raise_value_error=True, return_extra_info=False):
    return _str_to_x_1(s, date_format, none_values, none_result, raise_value_error, return_extra_info, 'date',
                     lambda s, f: dt.datetime.strptime(s, f).date())
    
def strs_to_date(ss, date_format=_date_formats, none_values=[''], none_result=None,
                 raise_value_error=True, return_extra_info=False, min_success_rate=0.5):
    return _strs_to_x_1(ss, date_format, none_values, none_result, raise_value_error, return_extra_info, min_success_rate,
                      str_to_date)

_time_formats = ['%H:%M:%S.%f', '%H:%M:%S', '%H:%M']
    
def str_to_time(s, time_format=_time_formats, none_values=[''], none_result=None,
                raise_value_error=True, return_extra_info=False):
    return _str_to_x_1(s, time_format, none_values, none_result, raise_value_error, return_extra_info, 'time',
                     lambda s, f: dt.datetime.strptime(s, f).time())

def strs_to_time(ss, time_format=_time_formats, none_values=[''], none_result=None,
                 raise_value_error=True, return_extra_info=False, min_success_rate=0.5):
    return _strs_to_x_1(ss, time_format, none_values, none_result, raise_value_error, return_extra_info, min_success_rate,
                      str_to_time)

_datetime_formats = []

for df in _date_formats:
    for tf in _time_formats:
        _datetime_formats.append('%s %s' % (df, tf))
        _datetime_formats.append('%sT%s' % (df, tf))
    
def str_to_datetime(s, datetime_format=_datetime_formats, none_values=[''], none_result=None,
                    raise_value_error=True, return_extra_info=False):
    return _str_to_x_1(s, datetime_format, none_values, none_result, raise_value_error, return_extra_info, 'datetime',
                     lambda s, f: dt.datetime.strptime(s, f))

def strs_to_datetime(ss, datetime_format=_datetime_formats, none_values=[''], none_result=None,
                     raise_value_error=True, return_extra_info=False, min_success_rate=0.5):
    return _strs_to_x_1(ss, datetime_format, none_values, none_result, raise_value_error, return_extra_info, min_success_rate,
                      str_to_datetime)
