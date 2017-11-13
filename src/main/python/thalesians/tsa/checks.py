import collections

import thalesians.tsa.settings as settings
import thalesians.tsa.utils as utils

def check(arg, message='Check failed', level=1):
    if settings.MIN_POSTCONDITION_LEVEL <= level:
        if not arg:
            if iscallable(message):
                message = message()
            raise AssertionError(message)
        
def checknotnone(arg, message='Argument is None', level=1):
    check(arg is not None, message, level)
    return arg

def isexactlyonenotnone(*args):
    return args.count(None) == len(args) - 1

def checkexactlyonenotnone(*args, **kwargs):
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is not 1'
    level = kwargs['level'] if 'level' in kwargs else 1
    check(isexactlyonenotnone(*args), message, level)
    
def isatmostonenotnone(*args):
    return args.count(None) >= len(args) - 1

def checkatmostonenotnone(*args, **kwargs):
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is neither 0 nor 1'
    level = kwargs['level'] if 'level' in kwargs else 1
    check(isatmostonenotnone(*args), message, level)
    
def checkinstance(arg, types, message='Argument is not of type %(expected)s, but of type %(actual)s', level=1):
    check(isinstance(arg, types), lambda: message % {'actual': type(arg), 'expected': types}, level)
    return arg

def checkint(arg, message='Argument is not an integer, but of type %(actual)s', level=1):
    check(isinstance(arg, int), lambda: message % {'actual': type(arg)}, level)
    return arg

def isiterable(arg):
    return isinstance(arg, collections.Iterable)

def checkiterable(arg, message='Argument of type %(actual)s is not iterable', level=1):
    check(isiterable(arg), lambda: message % {'actual': type(arg)}, level)
    return arg

def iscallable(arg):
    return hasattr(arg, '__call__') or isinstance(arg, collections.Callable)

def checkcallable(arg, message='Argument of type %(actual)s is not callable', level=1):
    check(iscallable(arg), lambda: message % {'actual': type(arg)}, level)
    return arg

def isiterableoverinstances(arg, types):
    if isiterable(arg):
        objs, iterable = utils.peek(iter(arg))
        if (len(objs) == 0): return False, iterable
        return isinstance(objs[0], types), iterable
    return False, arg
    
def checkiterableoverinstances(arg, types, message='Argument is not an iterable over type %(expected)s', level=1):
    result, iterable = isiterableoverinstances(arg, types)
    check(result, lambda: message % {'expected': types}, level)
    return iterable
