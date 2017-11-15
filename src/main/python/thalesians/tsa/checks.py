import collections

import thalesians.tsa.settings as settings
import thalesians.tsa.utils as utils

def check(arg, message='Check failed', level=1):
    if settings.MIN_POSTCONDITION_LEVEL <= level:
        if not arg:
            if is_callable(message):
                message = message()
            raise AssertionError(message)
        
def check_not_none(arg, message='Argument is None', level=1):
    check(arg is not None, message, level)
    return arg

def is_exactly_one_not_none(*args):
    return args.count(None) == len(args) - 1

def check_exactly_one_not_none(*args, **kwargs):
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is not 1'
    level = kwargs['level'] if 'level' in kwargs else 1
    check(is_exactly_one_not_none(*args), message, level)
    
def is_at_most_one_not_none(*args):
    return args.count(None) >= len(args) - 1

def check_at_most_one_not_none(*args, **kwargs):
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is neither 0 nor 1'
    level = kwargs['level'] if 'level' in kwargs else 1
    check(is_at_most_one_not_none(*args), message, level)
    
def check_instance(arg, types, message='Argument is not of type %(expected)s, but of type %(actual)s', level=1):
    check(isinstance(arg, types), lambda: message % {'actual': type(arg), 'expected': types}, level)
    return arg

def check_int(arg, message='Argument is not an integer, but of type %(actual)s', level=1):
    check(isinstance(arg, int), lambda: message % {'actual': type(arg)}, level)
    return arg

def is_iterable(arg):
    return isinstance(arg, collections.Iterable)

def check_iterable(arg, message='Argument of type %(actual)s is not iterable', level=1):
    check(is_iterable(arg), lambda: message % {'actual': type(arg)}, level)
    return arg

def is_callable(arg):
    return hasattr(arg, '__call__') or isinstance(arg, collections.Callable)

def check_callable(arg, message='Argument of type %(actual)s is not callable', level=1):
    check(is_callable(arg), lambda: message % {'actual': type(arg)}, level)
    return arg

def is_iterable_over_instances(arg, types):
    if is_iterable(arg):
        objs, iterable = utils.peek(iter(arg))
        if (len(objs) == 0): return False, iterable
        return isinstance(objs[0], types), iterable
    return False, arg
    
def check_iterable_over_instances(arg, types, message='Argument is not an iterable over type %(expected)s', level=1):
    result, iterable = is_iterable_over_instances(arg, types)
    check(result, lambda: message % {'expected': types}, level)
    return iterable
