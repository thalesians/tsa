import datetime as dt
import pytz

import thalesians.tsa.checks as checks
import thalesians.tsa.conversions as conv
from thalesians.tsa.timeconsts import *  # @UnusedWildImport
import thalesians.tsa.utils as utils

__all__ = [
        'NANOSECONDS_PER_MICROSECOND', 'MICROSECONDS_PER_MILLISECOND', 'NANOSECONDS_PER_MILLISECOND',
        'MILLISECONDS_PER_SECOND', 'MICROSECONDS_PER_SECOND', 'NANOSECONDS_PER_SECOND', 'SECONDS_PER_MINUTE', 
        'MILLISECONDS_PER_MINUTE', 'MICROSECONDS_PER_MINUTE', 'NANOSECONDS_PER_MINUTE', 'MINUTES_PER_HOUR',
        'SECONDS_PER_HOUR', 'MILLISECONDS_PER_HOUR', 'MICROSECONDS_PER_HOUR', 'NANOSECONDS_PER_HOUR', 'HOURS_PER_DAY',
        'MINUTES_PER_DAY', 'SECONDS_PER_DAY', 'MILLISECONDS_PER_DAY', 'MICROSECONDS_PER_DAY', 'NANOSECONDS_PER_DAY',
        'ONE_MICROSECOND', 'ONE_SECOND', 'ONE_MINUTE', 'ONE_HOUR', 'ONE_DAY'
    ]

_us_eastern = pytz.timezone('US/Eastern')
_london = pytz.timezone('Europe/London')
_paris = pytz.timezone('Europe/Paris')
_milan = pytz.timezone('Europe/Rome')
_frankfurt = pytz.timezone('Europe/Berlin')
_moscow = pytz.timezone('Europe/Moscow')
_hong_kong = pytz.timezone('Asia/Hong_Kong')
_shanghai = pytz.timezone('Asia/Shanghai')
_singapore = pytz.timezone('Asia/Singapore')
_tokyo = pytz.timezone('Asia/Tokyo')
_sydney = pytz.timezone('Australia/Sydney')

def utc_to_tz(datetime, tz):
    return pytz.utc.localize(datetime).astimezone(tz)
    
def utc_to_us_eastern(datetime):
    return utc_to_tz(datetime, _us_eastern)

def utc_to_new_york(datetime):
    return utc_to_us_eastern(datetime)

def utc_to_london(datetime):
    return utc_to_tz(datetime, _london)

def utc_to_paris(datetime):
    return utc_to_paris(datetime, _paris)

def utc_to_milan(datetime):
    return utc_to_milan(datetime, _milan)

def utc_to_frankfurt(datetime):
    return utc_to_tz(datetime, _frankfurt)

def utc_to_moscow(datetime):
    return utc_to_tz(datetime, _moscow)

def utc_to_hong_kong(datetime):
    return utc_to_tz(datetime, _hong_kong)

def utc_to_shanghai(datetime):
    return utc_to_tz(datetime, _shanghai)

def utc_to_singapore(datetime):
    return utc_to_tz(datetime, _singapore)

def utc_to_tokyo(datetime):
    return utc_to_tokyo(datetime, _tokyo)

def utc_to_sydney(datetime):
    return utc_to_sydney(datetime, _sydney)

def tz_to_utc(datetime, tz):
    return tz.localize(datetime).astimezone(pytz.utc)

def us_eastern_to_utc(datetime):
    return tz_to_utc(datetime, _us_eastern)

def new_york_to_utc(datetime):
    return us_eastern_to_utc(datetime)

def london_to_utc(datetime):
    return tz_to_utc(datetime, _london)

def paris_to_utc(datetime):
    return tz_to_utc(datetime, _paris)

def milan_to_utc(datetime):
    return tz_to_utc(datetime, _milan)

def frankfurt_to_utc(datetime):
    return tz_to_utc(datetime, _frankfurt)

def moscow_to_utc(datetime):
    return tz_to_utc(datetime, _moscow)

def hong_kong_to_utc(datetime):
    return tz_to_utc(datetime, _hong_kong)

def shanghai_to_utc(datetime):
    return tz_to_utc(datetime, _shanghai)

def singapore_to_utc(datetime):
    return tz_to_utc(datetime, _singapore)

def tokyo_to_utc(datetime):
    return tz_to_utc(datetime, _tokyo)

def sydney_to_utc(datetime):
    return tz_to_utc(datetime, _sydney)

def time_plus_timedelta(time, timedelta, on_overflow='raise'):
    date = dt.date(2000, 1, 1)
    if not isinstance(timedelta, dt.timedelta): timedelta = conv.to_python_timedelta(timedelta)
    new_datetime = dt.datetime.combine(date, time) + timedelta
    if new_datetime.date() < date:
        if on_overflow == 'raise': raise ValueError('Adding the timedelta causes the time to underflow below the date boundary')
        elif on_overflow == 'allow': return new_datetime.time()
        elif on_overflow == 'truncate': return dt.time(0)
        else: raise ValueError('Invalid on_overflow argument: "%s"' % str(on_overflow))
    elif new_datetime.date() > date:
        if on_overflow == 'raise': raise ValueError('Adding the timedelta causes the time to overflow above the date boundary')
        elif on_overflow == 'allow': return new_datetime.time()
        elif on_overflow == 'truncate': return dt.time(hour=23, minute=59, second=59, microsecond=999999)
        else: raise ValueError('Invalid on_overflow argument: "%s"' % str(on_overflow))
    return new_datetime.time()

def plus_timedelta(x, timedelta, on_overflow='raise', raise_value_error=True):
    if isinstance(x, dt.time): return time_plus_timedelta(x, timedelta, on_overflow)
    elif checks.is_some_datetime(x): return conv.to_python_datetime(x, allow_dates=True) + timedelta
    else:
        if raise_value_error: raise ValueError('Invalid timedelta: "%s"' % str(timedelta))
        return None

def _temporal_comparison(x, y, comp, return_pandas_series=True):
    import pandas as pd
    if checks.is_iterable_not_string(x):
        if checks.is_iterable_not_string(y):
            result = [_temporal_comparison(ex, ey, comp) for ex, ey in zip(x, y)]
            return pd.Series(result) if return_pandas_series else result
        else:
            result = [_temporal_comparison(ex, y, comp) for ex in x]
            return pd.Series(result) if return_pandas_series else result
    elif checks.is_iterable_not_string(y):
        result = [_temporal_comparison(x, ey, comp) for ey in y]
        return pd.Series(result) if return_pandas_series else result
    elif checks.is_some_time(x) or checks.is_some_time(y): return comp(conv.to_python_time(x), conv.to_python_time(y))
    elif checks.is_some_date(x) or checks.is_some_date(y): return comp(conv.to_python_date(x), conv.to_python_date(y))
    else: return comp(conv.to_python_datetime(x), conv.to_python_datetime(y))
    
def temporal_cmp(x, y, return_pandas_series=True):
    return _temporal_comparison(x, y, lambda x1, y1: utils.cmp(x1, y1), return_pandas_series)
    
def temporal_eq(x, y, return_pandas_series=True):
    return _temporal_comparison(x, y, lambda x1, y1: x1 == y1, return_pandas_series)

def temporal_ne(x, y, return_pandas_series=True):
    return _temporal_comparison(x, y, lambda x1, y1: x1 != y1, return_pandas_series)

def temporal_lt(x, y, return_pandas_series=True):
    return _temporal_comparison(x, y, lambda x1, y1: x1 < y1, return_pandas_series)

def temporal_le(x, y, return_pandas_series=True):
    return _temporal_comparison(x, y, lambda x1, y1: x1 <= y1, return_pandas_series)

def temporal_gt(x, y, return_pandas_series=True):
    return _temporal_comparison(x, y, lambda x1, y1: x1 > y1, return_pandas_series)

def temporal_ge(x, y, return_pandas_series=True):
    return _temporal_comparison(x, y, lambda x1, y1: x1 >= y1, return_pandas_series)

def first_day_of_week(date):
    date = conv.to_python_date(date, allow_datetimes=True)
    if checks.is_iterable(date): return [first_day_of_week(x) for x in date]
    week = date.isocalendar()[1]
    while date.isocalendar()[1] == week: date -= ONE_DAY
    return date + ONE_DAY
