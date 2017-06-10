import tsa.settings as settings
import tsa.utils as utils

def check(arg, message='Check failed', level=1):
    if settings.MIN_POSTCONDITION_LEVEL <= level:
        if not arg:
            if utils.iscallable(message):
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
    
def checkisinstance(arg, type, message='Argument is not of type %(expected), but of type %(actual)', level=1):
    check(isinstance(arg, type), lambda: message % {'actual': str(type(arg)), 'expected': str(type)}, level)
