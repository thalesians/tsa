import collections as col
import datetime as dt

import thalesians.tsa.settings as settings
import thalesians.tsa.utils as utils

def check(arg, message='Check failed', level=1):
    if settings.MIN_POSTCONDITION_LEVEL <= level:
        if is_callable(arg): arg = arg()
        if not arg:
            if is_callable(message):
                message = message()
            raise AssertionError(message)
        
def check_none(arg, message='Argument is not None', level=1):
    check(arg is None, message, level)
    return arg
        
def check_not_none(arg, message='Argument is None', level=1):
    check(arg is not None, message, level)
    return arg

def are_all_not_none(*args):
    return args.count(None) == 0

def check_all_not_none(*args, **kwargs):
    message = kwargs['message'] if 'message' in kwargs else 'At least one of the arguments is None'
    level = kwargs['level'] if 'level' in kwargs else 1
    check(are_all_not_none(*args), message, level)

def are_all_none(*args):
    return args.count(None) == len(args)

def check_all_none(*args, **kwargs):
    message = kwargs['message'] if 'message' in kwargs else 'At least one of the arguments is not None'
    level = kwargs['level'] if 'level' in kwargs else 1
    check(are_all_none(*args), message, level)

def is_exactly_one_not_none(*args):
    return args.count(None) == len(args) - 1

def check_exactly_one_not_none(*args, **kwargs):
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is not 1'
    level = kwargs['level'] if 'level' in kwargs else 1
    check(is_exactly_one_not_none(*args), message, level)
    
def is_at_least_one_not_none(*args):
    return args.count(None) < len(args)
    
def check_at_least_one_not_none(*args, **kwargs):
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is 0'
    level = kwargs['level'] if 'level' in kwargs else 1
    check(is_at_least_one_not_none(*args), message, level)
    
def is_at_most_one_not_none(*args):
    return args.count(None) >= len(args) - 1

def check_at_most_one_not_none(*args, **kwargs):
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is neither 0 nor 1'
    level = kwargs['level'] if 'level' in kwargs else 1
    check(is_at_most_one_not_none(*args), message, level)
    
def is_same_len(*args):
    if len(args) == 0: return True
    len0 = len(args[0])
    return all([len(x) == len0 for x in args])

def is_same_len_or_none(*args):
    the_len = None
    for x in args:
        if x is not None:
            if the_len is None: the_len = len(x)
            elif the_len != len(x): return False
    return True

def is_same_len_or_all_none(*args):
    seen_none = False
    the_len = None
    for x in args:
        if x is None:
            if the_len is not None: return False
            seen_none = True
        else:
            if seen_none: return False
            if the_len is None: the_len = len(x)
            elif the_len != len(x): return False
    return True

def is_instance(arg, types, allow_none=False):
    return (allow_none and arg is None) or isinstance(arg, types)
    
def check_instance(arg, types, allow_none=False, message='Argument "%(string)" is not of type %(expected)s, but of type %(actual)s', level=1):
    check(is_instance(arg, types, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg), 'expected': types}, level)
    return arg

def is_int(arg, allow_none=False):
    return is_instance(arg, int, allow_none)

def check_int(arg, allow_none=False, message='Argument "%(string)" is not an integer, but of type %(actual)s', level=1):
    check(is_int(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_numpy_int(arg, allow_none=False):
    import numpy as np
    return is_instance(arg, (np.int, np.int0, np.int8, np.int16, np.int32, np.int64), allow_none)

def check_some_numpy_int(arg, allow_none=False, message='Argument "%(string)" is not a NumPy int*, but of type %(actual)s', level=1):
    check(is_some_numpy_int(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_numpy_uint(arg, allow_none=False):
    import numpy as np
    return is_instance(arg, (np.uint, np.uint0, np.uint8, np.uint16, np.uint32, np.uint64), allow_none)

def check_some_numpy_uint(arg, allow_none=False, message='Argument "%(string)" is not a NumPy uint*, but of type %(actual)s', level=1):
    check(is_some_numpy_uint(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_int(arg, allow_none=False):
    return is_int(arg, allow_none) or is_some_numpy_int(arg, allow_none) or is_some_numpy_uint(arg, allow_none)

def check_some_int(arg, allow_none=False, message='Argument "%(string)" is not some (u)int*, but of type %(actual)s', level=1):
    check(is_some_int(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_float(arg, allow_none=False):
    return is_instance(arg, float, allow_none)

def check_float(arg, allow_none=False, message='Argument "%(string)" is not a float, but of type %(actual)s', level=1):
    check(is_float(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_numpy_float(arg, allow_none=False):
    import numpy as np
    return is_instance(arg, (np.float, np.float16, np.float32, np.float64), allow_none)

def check_some_numpy_float(arg, allow_none=False, message='Argument "%(string)" is not a NumPy float*, but of type %(actual)s', level=1):
    check(is_some_numpy_float(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_numpy_double(arg, allow_none=False):
    import numpy as np
    return is_instance(arg, (np.double, np.longdouble), allow_none)

def check_some_numpy_double(arg, allow_none=False, message='Argument "%(string)" is not a NumPy double/longdouble, but of type %(actual)s', level=1):
    check(is_some_numpy_double(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_float(arg, allow_none=False):
    return is_float(arg, allow_none) or is_some_numpy_float(arg, allow_none) or is_some_numpy_double(arg, allow_none)

def check_some_float(arg, allow_none=False, message='Argument "%(string)" is not some float*/double/longdouble, but of type %(actual)s', level=1):
    check(is_some_float(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_number(arg, allow_none=False):
    return is_some_int(arg, allow_none) or is_some_float(arg, allow_none)

def check_some_number(arg, allow_none=False, message='Argument "%(string)" is not some number, but of type %(actual)s', level=1):
    check(is_some_number(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_numpy_array(arg, allow_none=False):
    import numpy as np
    return is_instance(arg, np.ndarray, allow_none)

def check_numpy_array(arg, allow_none=False, message='Argument "%(string)" is not a NumPy array, but of type %(actual)s', level=1):
    check(is_numpy_array(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_string(arg, allow_none=False):
    return is_instance(arg, str, allow_none)

def check_string(arg, allow_none=False, message='Argument "%(string)" of type %(actual)s is not a string', level=1):
    check(is_string(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_date(arg, allow_none=False):
    return is_instance(arg, dt.date, allow_none)

def check_date(arg, message='Argument "%(string)" of type %(actual)s is not a date', level=1):
    check(is_date(arg), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_time(arg, allow_none=False):
    return is_instance(arg, dt.time, allow_none)

def check_time(arg, allow_none=False, message='Argument "%(string)" of type %(actual)s is not a time', level=1):
    check(is_time(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_datetime(arg, allow_none=False):
    return is_instance(arg, dt.datetime, allow_none)

def check_datetime(arg, allow_none=False, message='Argument "%(string)" of type %(actual)s is not a datetime', level=1):
    check(is_datetime(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_timedelta(arg, allow_none=False):
    return is_instance(arg, dt.timedelta, allow_none)

def check_timedelta(arg, allow_none=False, message='Argument "%(string)" of type %(actual)s is not a timedelta', level=1):
    check(is_timedelta(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_timedelta(arg, allow_none=False):
    import numpy as np
    import pandas as pd
    return is_instance(arg, (dt.timedelta, np.timedelta64, pd.Timedelta), allow_none)

def is_iterable(arg, allow_none=False):
    return is_instance(arg, col.Iterable, allow_none)

def check_iterable(arg, allow_none=False, message='Argument "%(string)" of type %(actual)s is not iterable', level=1):
    check(is_iterable(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_iterable_not_string(arg, allow_none=False):
    return (allow_none and arg is None) or ((not is_string(arg)) and is_iterable(arg))

def check_iterable_not_string(arg, allow_none=False, message='Argument "%(string)" of type %(actual)s is either not iterable or a string', level=1):
    check(is_iterable_not_string(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_dict(arg, allow_none=False):
    return is_instance(arg, dict, allow_none)

def check_dict(arg, allow_none=False, message='Argument "%(string)" of type %(actual)s is not a dict', level=1):
    check(is_dict(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_dict(arg, allow_none=False):
    return (allow_none and arg is None) or hasattr(arg, 'keys')

def check_some_dict(arg, allow_none=False, message='Argument "%(string)" of type %(actual)s is not a dictionary', level=1):
    check(is_some_dict(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_callable(arg, allow_none=False):
    return (allow_none and arg is None) or (hasattr(arg, '__call__') or isinstance(arg, col.Callable))

def check_callable(arg, allow_none=False, message='Argument "%(string)" of type %(actual)s is not callable', level=1):
    check(is_callable(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_iterable_over_instances(arg, types, allow_none=False, allow_empty=False):
    if (allow_none and arg is None): return True, arg
    if is_iterable(arg):
        objs, iterable = utils.peek(iter(arg))
        if (len(objs) == 0): return allow_empty, iterable
        return isinstance(objs[0], types), iterable
    return False, arg
    
def check_iterable_over_instances(arg, types, allow_none=False, allow_empty=False, message='Argument is not an iterable over type %(expected)s', level=1):
    result, iterable = is_iterable_over_instances(arg, types, allow_none, allow_empty)
    check(result, lambda: message % {'expected': types}, level)
    return iterable

def is_type(arg, allow_none=False):
    return is_instance(arg, type, allow_none)
