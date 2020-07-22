"""
`thalesians.tsa.checks`
=======================

A collection of utility functions for checking whether given conditions hold.

Those functions that start with `is_` or `are_` return `False` if a given condition does not hold and `True` if it does
hold. Those functions that start with `check_` return their argument if a given condition holds and raise an
`AssertionError` if it does not hold.
"""

import collections.abc

import thalesians.tsa.tsa_settings as tsa_settings
import thalesians.tsa.utils as utils

def check(arg, message='Check failed', level=1):
    """
    Checks whether `arg` is `True`.
    
    If the check succeeds, the function returns the argument. If the check fails, the function raises an
    `AssertionError` with a given `message`.

    Parameters
    ----------
    arg : bool, callable
        The argument whose truth value is to be checked. If `arg` is callable, then it will be called with no arguments
        to obtain the argument.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    bool
        The argument. If the `arg` passed to the function was callable, then `arg()` is returned.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------

    >>> check(True)
    True
    >>> check(True is True)
    True
    >>> check(False is False)
    True
    >>> check(1 < 3)
    True
    >>> check(3 == 3)
    True
    >>> check(3 > 1)
    True
    >>> check(False)
    Traceback (most recent call last):
        ...
    AssertionError: Check failed
    >>> check(True is False)
    Traceback (most recent call last):
        ...
    AssertionError: Check failed
    >>> check(False is True)
    Traceback (most recent call last):
        ...
    AssertionError: Check failed
    >>> check(1 >= 3)
    Traceback (most recent call last):
        ...
    AssertionError: Check failed
    >>> check(3 != 3)
    Traceback (most recent call last):
        ...
    AssertionError: Check failed
    >>> check(3 <= 1)
    Traceback (most recent call last):
        ...
    AssertionError: Check failed
    """
    if is_callable(arg): arg = arg()
    if level < tsa_settings.MIN_CHECK_LEVEL or arg:
        return arg
    else:
        if is_callable(message):
            message = message()
        raise AssertionError(message)
        
def check_none(arg, message='Argument is not None', level=1):
    """
    Checks whether `arg` is `None`.
    
    If the check succeeds (the argument is `None`), the function returns the argument. If the check fails, the function
    raises an `AssertionError` with a given `message`.

    Parameters
    ----------
    arg : bool, callable
        The argument to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    None
        The argument.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_none(None)
    >>> check_none(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument is not None
    """
    check(arg is None, message, level)
    return arg
    
def check_not_none(arg, message='Argument is None', level=1):
    """
    Checks whether `arg` is not `None`.
    
    If the check succeeds (the argument is not `None`), the function returns the argument. If the check fails, the
    function raises an `AssertionError` with a given `message`.

    Parameters
    ----------
    arg : bool, callable
        The argument to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    not None
        The argument.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_not_none(3)
    3
    >>> check_not_none(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument is None
    """
    check(arg is not None, message, level)
    return arg

def are_all_not_none(*args):
    """
    Returns `True` if all arguments are not `None`, otherwise `False`.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> are_all_not_none(1, 2, 3)
    True
    >>> are_all_not_none(None, 2, 3)
    False
    >>> are_all_not_none(1, None, 3)
    False
    >>> are_all_not_none(1, 2, None)
    False
    >>> are_all_not_none(1, None, None)
    False
    >>> are_all_not_none(None, 2, None)
    False
    >>> are_all_not_none(None, None, 3)
    False
    
    >>> are_all_not_none(1, 2, 3, 'hi')
    True
    >>> are_all_not_none(None, 2, 3, 'hi')
    False
    >>> are_all_not_none(1, None, 3, 'hi')
    False
    >>> are_all_not_none(1, 2, None, 'hi')
    False
    >>> are_all_not_none(1, None, None, 'hi')
    False
    >>> are_all_not_none(None, 2, None, 'hi')
    False
    >>> are_all_not_none(None, None, 3, 'hi')
    False
    
    >>> are_all_not_none(None, None, None)
    False
    
    >>> are_all_not_none(None)
    False
    """
    return args.count(None) == 0

def check_all_not_none(*args, **kwargs):
    """
    Checks whether all arguments are not `None`.
    
    If the check succeeds (all arguments are not `None`), the function returns `True`. If the check fails, the function
    raises an `AssertionError` with a given `message`.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    bool
        `True` if the check succeeds.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_all_not_none(1, 2, 3)
    True
    >>> check_all_not_none(None, 2, 3)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(1, None, 3)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(1, 2, None)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(1, None, None)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(None, 2, None)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(None, None, 3)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    
    >>> check_all_not_none(1, 2, 3, 'hi')
    True
    >>> check_all_not_none(None, 2, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(1, None, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(1, 2, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(1, None, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(None, 2, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(None, None, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(None, None, None)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    >>> check_all_not_none(None)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is None
    """
    message = kwargs['message'] if 'message' in kwargs else 'At least one of the arguments is None'
    level = kwargs['level'] if 'level' in kwargs else 1
    return check(are_all_not_none(*args), message, level)

def are_all_none(*args):
    """
    Returns `True` if all arguments are `None`, otherwise `False`.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> are_all_none(1, 2, 3)
    False
    >>> are_all_none(None, 2, 3)
    False
    >>> are_all_none(1, None, 3)
    False
    >>> are_all_none(1, 2, None)
    False
    >>> are_all_none(1, 2, 3)
    False
    >>> are_all_none(1, None, None)
    False
    >>> are_all_none(None, 2, None)
    False
    >>> are_all_none(None, None, 3)
    False
    
    >>> are_all_none(1, 2, 3, 'hi')
    False
    >>> are_all_none(None, 2, 3, 'hi')
    False
    >>> are_all_none(1, None, 3, 'hi')
    False
    >>> are_all_none(1, 2, None, 'hi')
    False
    >>> are_all_none(1, None, None, 'hi')
    False
    >>> are_all_none(None, 2, None, 'hi')
    False
    >>> are_all_none(None, None, 3, 'hi')
    False
    
    >>> are_all_none(None, None, None)
    True
    
    >>> are_all_none(None)
    True
    """
    return args.count(None) == len(args)

def check_all_none(*args, **kwargs):
    """
    Checks whether all arguments are `None`.
    
    If the check succeeds (all arguments are `None`), the function returns `True`. If the check fails, the function
    raises an `AssertionError` with a given `message`.
    
    The `message` and `level`, if they are specified, must be passed in as keyword arguments. The other arguments must
    be passed in as non-keyword arguments.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    bool
        `True` if the check succeeds.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_all_none(1, 2, 3)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(None, 2, 3)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(1, None, 3)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(1, 2, None)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(1, None, None)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(None, 2, None)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(None, None, 3)
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    
    >>> check_all_none(1, 2, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(None, 2, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(1, None, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(1, 2, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(1, None, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(None, 2, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(None, None, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: At least one of the arguments is not None
    >>> check_all_none(None, None, None)
    True
    >>> check_all_none(None)
    True
    """
    message = kwargs['message'] if 'message' in kwargs else 'At least one of the arguments is not None'
    level = kwargs['level'] if 'level' in kwargs else 1
    return check(are_all_none(*args), message, level)

def is_exactly_one_not_none(*args):
    """
    Returns `True` if exactly one of the arguments is not `None`, otherwise `False`.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_exactly_one_not_none(1, 2, 3)
    False
    >>> is_exactly_one_not_none(None, 2, 3)
    False
    >>> is_exactly_one_not_none(1, None, 3)
    False
    >>> is_exactly_one_not_none(1, 2, None)
    False
    >>> is_exactly_one_not_none(1, None, None)
    True
    >>> is_exactly_one_not_none(None, 2, None)
    True
    >>> is_exactly_one_not_none(None, None, 3)
    True
    
    >>> is_exactly_one_not_none(1, 2, 3, 'hi')
    False
    >>> is_exactly_one_not_none(None, 2, 3, 'hi')
    False
    >>> is_exactly_one_not_none(1, None, 3, 'hi')
    False
    >>> is_exactly_one_not_none(1, 2, None, 'hi')
    False
    >>> is_exactly_one_not_none(1, None, None, 'hi')
    False
    >>> is_exactly_one_not_none(None, 2, None, 'hi')
    False
    >>> is_exactly_one_not_none(None, None, 3, 'hi')
    False
    
    >>> is_exactly_one_not_none(None, None, None)
    False
    
    >>> is_exactly_one_not_none(None)
    False
    """
    return args.count(None) == len(args) - 1

def check_exactly_one_not_none(*args, **kwargs):
    """
    Checks whether exactly one of the arguments is not `None`.
    
    If the check succeeds (exactly one of the arguments is not `None`), the function returns `True`. If the check fails,
    the function raises an `AssertionError` with a given `message`.
    
    The `message` and `level`, if they are specified, must be passed in as keyword arguments. The other arguments must
    be passed in as non-keyword arguments.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    bool
        `True` if the check succeeds.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_exactly_one_not_none(1, 2, 3)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(None, 2, 3)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(1, None, 3)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(1, 2, None)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(1, None, None)
    True
    >>> check_exactly_one_not_none(None, 2, None)
    True
    >>> check_exactly_one_not_none(None, None, 3)
    True
    
    >>> check_exactly_one_not_none(1, 2, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(None, 2, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(1, None, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(1, 2, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(1, None, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(None, 2, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(None, None, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(None, None, None)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    >>> check_exactly_one_not_none(None)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is not 1
    """
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is not 1'
    level = kwargs['level'] if 'level' in kwargs else 1
    return check(is_exactly_one_not_none(*args), message, level)
    
def is_at_least_one_not_none(*args):
    """
    Returns `True` if at least one of the arguments is not `None`, otherwise `False`.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_at_least_one_not_none(1, 2, 3)
    True
    >>> is_at_least_one_not_none(None, 2, 3)
    True
    >>> is_at_least_one_not_none(1, None, 3)
    True
    >>> is_at_least_one_not_none(1, 2, None)
    True
    >>> is_at_least_one_not_none(1, None, None)
    True
    >>> is_at_least_one_not_none(None, 2, None)
    True
    >>> is_at_least_one_not_none(None, None, 3)
    True
    
    >>> is_at_least_one_not_none(1, 2, 3, 'hi')
    True
    >>> is_at_least_one_not_none(None, 2, 3, 'hi')
    True
    >>> is_at_least_one_not_none(1, None, 3, 'hi')
    True
    >>> is_at_least_one_not_none(1, 2, None, 'hi')
    True
    >>> is_at_least_one_not_none(1, None, None, 'hi')
    True
    >>> is_at_least_one_not_none(None, 2, None, 'hi')
    True
    >>> is_at_least_one_not_none(None, None, 3, 'hi')
    True
    
    >>> is_at_least_one_not_none(None, None, None)
    False
    
    >>> is_at_least_one_not_none(None)
    False
    """
    return args.count(None) < len(args)
    
def check_at_least_one_not_none(*args, **kwargs):
    """
    Checks whether at least one of the arguments is not `None`.
    
    If the check succeeds (at least one of the arguments is not `None`), the function returns `True`. If the check
    fails, the function raises an `AssertionError` with a given `message`.
    
    The `message` and `level`, if they are specified, must be passed in as keyword arguments. The other arguments must
    be passed in as non-keyword arguments.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    bool
        `True` if the check succeeds.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_at_least_one_not_none(1, 2, 3)
    True
    >>> check_at_least_one_not_none(None, 2, 3)
    True
    >>> check_at_least_one_not_none(1, None, 3)
    True
    >>> check_at_least_one_not_none(1, 2, None)
    True
    >>> check_at_least_one_not_none(1, None, None)
    True
    >>> check_at_least_one_not_none(None, 2, None)
    True
    >>> check_at_least_one_not_none(None, None, 3)
    True
    
    >>> check_at_least_one_not_none(1, 2, 3, 'hi')
    True
    >>> check_at_least_one_not_none(None, 2, 3, 'hi')
    True
    >>> check_at_least_one_not_none(1, None, 3, 'hi')
    True
    >>> check_at_least_one_not_none(1, 2, None, 'hi')
    True
    >>> check_at_least_one_not_none(1, None, None, 'hi')
    True
    >>> check_at_least_one_not_none(None, 2, None, 'hi')
    True
    >>> check_at_least_one_not_none(None, None, 3, 'hi')
    True
    
    >>> check_at_least_one_not_none(None, None, None)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is 0
    
    >>> check_at_least_one_not_none(None)    
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is 0
    """
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is 0'
    level = kwargs['level'] if 'level' in kwargs else 1
    return check(is_at_least_one_not_none(*args), message, level)
    
def is_at_most_one_not_none(*args):
    """
    Returns `True` if at most one of the arguments is not `None`, otherwise `False`.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_at_most_one_not_none(1, 2, 3)
    False
    >>> is_at_most_one_not_none(None, 2, 3)
    False
    >>> is_at_most_one_not_none(1, None, 3)
    False
    >>> is_at_most_one_not_none(1, 2, None)
    False
    >>> is_at_most_one_not_none(1, None, None)
    True
    >>> is_at_most_one_not_none(None, 2, None)
    True
    >>> is_at_most_one_not_none(None, None, 3)
    True
    
    >>> is_at_most_one_not_none(1, 2, 3, 'hi')
    False
    >>> is_at_most_one_not_none(None, 2, 3, 'hi')
    False
    >>> is_at_most_one_not_none(1, None, 3, 'hi')
    False
    >>> is_at_most_one_not_none(1, 2, None, 'hi')
    False
    >>> is_at_most_one_not_none(1, None, None, 'hi')
    False
    >>> is_at_most_one_not_none(None, 2, None, 'hi')
    False
    >>> is_at_most_one_not_none(None, None, 3, 'hi')
    False
    
    >>> is_at_most_one_not_none(None, None, None)
    True
    
    >>> is_at_most_one_not_none(None)
    True
    """
    return args.count(None) >= len(args) - 1

def check_at_most_one_not_none(*args, **kwargs):
    """
    Checks whether at most one of the arguments is not `None`.
    
    If the check succeeds (at most one of the arguments is not `None`), the function returns `True`. If the check fails,
    the function raises an `AssertionError` with a given `message`.
    
    The `message` and `level`, if they are specified, must be passed in as keyword arguments. The other arguments must
    be passed in as non-keyword arguments.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    bool
        `True` if the check succeeds.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_at_most_one_not_none(1, 2, 3)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(None, 2, 3)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(1, None, 3)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(1, 2, None)
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(1, None, None)
    True
    >>> check_at_most_one_not_none(None, 2, None)
    True
    >>> check_at_most_one_not_none(None, None, 3)
    True
    
    >>> check_at_most_one_not_none(1, 2, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(None, 2, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(1, None, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(1, 2, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(1, None, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(None, 2, None, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(None, None, 3, 'hi')
    Traceback (most recent call last):
        ...
    AssertionError: The number of non-None arguments is neither 0 nor 1
    >>> check_at_most_one_not_none(None, None, None)
    True
    >>> check_at_most_one_not_none(None)
    True
    """
    message = kwargs['message'] if 'message' in kwargs else 'The number of non-None arguments is neither 0 nor 1'
    level = kwargs['level'] if 'level' in kwargs else 1
    return check(is_at_most_one_not_none(*args), message, level)
    
def is_same_len(*args):
    """
    Returns `True` if all the arguments are of the same length, otherwise `False`.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_same_len(1, 'aaa')
    Traceback (most recent call last):
        ...
    TypeError: object of type 'int' has no len()

    >>> is_same_len([1], ['aaa'])
    True
    >>> is_same_len([1, 'b'], ['aaa', 222])
    True
    >>> is_same_len([1, 'b', 3], ['aaa', 222, 'ccc'])
    True

    >>> is_same_len([], ['aaa'])
    False
    >>> is_same_len([1], ['aaa', 222])
    False
    >>> is_same_len([1, 'b'], ['aaa'])
    False

    >>> is_same_len([1], ['aaa'], [111])
    True
    >>> is_same_len([1, 'b'], ['aaa', 222], [111, 'BBB'])
    True
    >>> is_same_len([1, 'b', 3], ['aaa', 222, 'ccc'], [111, 'BBB', 333])
    True

    >>> is_same_len([], ['aaa'], [111])
    False
    >>> is_same_len([1], ['aaa', 222], [111, 'BBB'])
    False
    >>> is_same_len([1, 'b'], ['aaa'], [111, 'BBB'])
    False

    >>> is_same_len([1, 'b'], None)
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> is_same_len(None, ['aaa'])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> is_same_len(None, None)
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()

    >>> is_same_len([1, 'b'], None, ['aaa', 222])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> is_same_len(None, ['aaa'], [111])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> is_same_len(None, None, [111, 'BBB'])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> is_same_len(None, None, None)
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()

    >>> is_same_len([1], None, ['aaa', 222])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> is_same_len(None, ['aaa'], [])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> is_same_len(None, ['aaa'], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    """
    if len(args) == 0: return True
    len0 = len(args[0])
    return all([len(x) == len0 for x in args])

def check_same_len(*args, **kwargs):
    """
    Checks whether all the arguments are of the same length.
    
    If the check succeeds (all the arguments are of the same length), the function returns `True`. If the check fails,
    the function raises an `AssertionError` with a given `message`.
    
    The `message` and `level`, if they are specified, must be passed in as keyword arguments. The other arguments must
    be passed in as non-keyword arguments.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    bool
        `True` if the check succeeds.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_same_len(1, 'aaa')
    Traceback (most recent call last):
        ...
    TypeError: object of type 'int' has no len()

    >>> check_same_len([1], ['aaa'])
    True
    >>> check_same_len([1, 'b'], ['aaa', 222])
    True
    >>> check_same_len([1, 'b', 3], ['aaa', 222, 'ccc'])
    True

    >>> check_same_len([], ['aaa'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are not of the same length
    >>> check_same_len([1], ['aaa', 222])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are not of the same length
    >>> check_same_len([1, 'b'], ['aaa'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are not of the same length

    >>> check_same_len([1], ['aaa'], [111])
    True
    >>> check_same_len([1, 'b'], ['aaa', 222], [111, 'BBB'])
    True
    >>> check_same_len([1, 'b', 3], ['aaa', 222, 'ccc'], [111, 'BBB', 333])
    True

    >>> check_same_len([], ['aaa'], [111])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are not of the same length
    >>> check_same_len([1], ['aaa', 222], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are not of the same length
    >>> check_same_len([1, 'b'], ['aaa'], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are not of the same length

    >>> check_same_len([1, 'b'], None)
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> check_same_len(None, ['aaa'])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> check_same_len(None, None)
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()

    >>> check_same_len([1, 'b'], None, ['aaa', 222])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> check_same_len(None, ['aaa'], [111])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> check_same_len(None, None, [111, 'BBB'])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> check_same_len(None, None, None)
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()

    >>> check_same_len([1], None, ['aaa', 222])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> check_same_len(None, ['aaa'], [])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    >>> check_same_len(None, ['aaa'], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    TypeError: object of type 'NoneType' has no len()
    """
    message = kwargs['message'] if 'message' in kwargs else 'The arguments are not of the same length'
    level = kwargs['level'] if 'level' in kwargs else 1
    return check(is_same_len(*args), message, level)

def is_same_len_or_none(*args):
    """
    Returns `True` if all the arguments are of the same length, otherwise `False`.
    
    Arguments that are `None` are ignored and excluded from the comparison.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_same_len_or_none(1, 'aaa')
    Traceback (most recent call last):
        ...
    TypeError: object of type 'int' has no len()

    >>> is_same_len_or_none([1], ['aaa'])
    True
    >>> is_same_len_or_none([1, 'b'], ['aaa', 222])
    True
    >>> is_same_len_or_none([1, 'b', 3], ['aaa', 222, 'ccc'])
    True

    >>> is_same_len_or_none([], ['aaa'])
    False
    >>> is_same_len_or_none([1], ['aaa', 222])
    False
    >>> is_same_len_or_none([1, 'b'], ['aaa'])
    False

    >>> is_same_len_or_none([1], ['aaa'], [111])
    True
    >>> is_same_len_or_none([1, 'b'], ['aaa', 222], [111, 'BBB'])
    True
    >>> is_same_len_or_none([1, 'b', 3], ['aaa', 222, 'ccc'], [111, 'BBB', 333])
    True

    >>> is_same_len_or_none([], ['aaa'], [111])
    False
    >>> is_same_len_or_none([1], ['aaa', 222], [111, 'BBB'])
    False
    >>> is_same_len_or_none([1, 'b'], ['aaa'], [111, 'BBB'])
    False

    >>> is_same_len_or_none([1, 'b'], None)
    True
    >>> is_same_len_or_none(None, ['aaa'])
    True
    >>> is_same_len_or_none(None, None)
    True

    >>> is_same_len_or_none([1, 'b'], None, ['aaa', 222])
    True
    >>> is_same_len_or_none(None, ['aaa'], [111])
    True
    >>> is_same_len_or_none(None, None, [111, 'BBB'])
    True
    >>> is_same_len_or_none(None, None, None)
    True

    >>> is_same_len_or_none([1], None, ['aaa', 222])
    False
    >>> is_same_len_or_none(None, ['aaa'], [])
    False
    >>> is_same_len_or_none(None, ['aaa'], [111, 'BBB'])
    False
    """
    the_len = None
    for x in args:
        if x is not None:
            if the_len is None: the_len = len(x)
            elif the_len != len(x): return False
    return True

def check_same_len_or_none(*args, **kwargs):
    """
    Checks whether all the arguments are of the same length.
    
    Arguments that are `None` are ignored and excluded from the comparison.
    
    If the check succeeds (all the arguments are of the same length), the function returns `True`. If the check fails,
    the function raises an `AssertionError` with a given `message`.
    
    The `message` and `level`, if they are specified, must be passed in as keyword arguments. The other arguments must
    be passed in as non-keyword arguments.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    bool
        `True` if the check succeeds.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_same_len_or_none(1, 'aaa')
    Traceback (most recent call last):
        ...
    TypeError: object of type 'int' has no len()

    >>> check_same_len_or_none([1], ['aaa'])
    True
    >>> check_same_len_or_none([1, 'b'], ['aaa', 222])
    True
    >>> check_same_len_or_none([1, 'b', 3], ['aaa', 222, 'ccc'])
    True

    >>> check_same_len_or_none([], ['aaa'])
    Traceback (most recent call last):
        ...
    AssertionError: The non-None arguments are not of the same length
    >>> check_same_len_or_none([1], ['aaa', 222])
    Traceback (most recent call last):
        ...
    AssertionError: The non-None arguments are not of the same length
    >>> check_same_len_or_none([1, 'b'], ['aaa'])
    Traceback (most recent call last):
        ...
    AssertionError: The non-None arguments are not of the same length

    >>> check_same_len_or_none([1], ['aaa'], [111])
    True
    >>> check_same_len_or_none([1, 'b'], ['aaa', 222], [111, 'BBB'])
    True
    >>> check_same_len_or_none([1, 'b', 3], ['aaa', 222, 'ccc'], [111, 'BBB', 333])
    True

    >>> check_same_len_or_none([], ['aaa'], [111])
    Traceback (most recent call last):
        ...
    AssertionError: The non-None arguments are not of the same length
    >>> check_same_len_or_none([1], ['aaa', 222], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    AssertionError: The non-None arguments are not of the same length
    >>> check_same_len_or_none([1, 'b'], ['aaa'], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    AssertionError: The non-None arguments are not of the same length

    >>> check_same_len_or_none([1, 'b'], None)
    True
    >>> check_same_len_or_none(None, ['aaa'])
    True
    >>> check_same_len_or_none(None, None)
    True

    >>> check_same_len_or_none([1, 'b'], None, ['aaa', 222])
    True
    >>> check_same_len_or_none(None, ['aaa'], [111])
    True
    >>> check_same_len_or_none(None, None, [111, 'BBB'])
    True
    >>> check_same_len_or_none(None, None, None)
    True

    >>> check_same_len_or_none([1], None, ['aaa', 222])
    Traceback (most recent call last):
        ...
    AssertionError: The non-None arguments are not of the same length
    >>> check_same_len_or_none(None, ['aaa'], [])
    Traceback (most recent call last):
        ...
    AssertionError: The non-None arguments are not of the same length
    >>> check_same_len_or_none(None, ['aaa'], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    AssertionError: The non-None arguments are not of the same length
    """
    message = kwargs['message'] if 'message' in kwargs else 'The non-None arguments are not of the same length'
    level = kwargs['level'] if 'level' in kwargs else 1
    return check(is_same_len_or_none(*args), message, level)

def is_same_len_or_all_none(*args):
    """
    Returns `True` if either all the arguments are of the same length, or all the arguments are None, otherwise `False`.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_same_len_or_all_none(1, 'aaa')
    Traceback (most recent call last):
        ...
    TypeError: object of type 'int' has no len()

    >>> is_same_len_or_all_none([1], ['aaa'])
    True
    >>> is_same_len_or_all_none([1, 'b'], ['aaa', 222])
    True
    >>> is_same_len_or_all_none([1, 'b', 3], ['aaa', 222, 'ccc'])
    True

    >>> is_same_len_or_all_none([], ['aaa'])
    False
    >>> is_same_len_or_all_none([1], ['aaa', 222])
    False
    >>> is_same_len_or_all_none([1, 'b'], ['aaa'])
    False

    >>> is_same_len_or_all_none([1], ['aaa'], [111])
    True
    >>> is_same_len_or_all_none([1, 'b'], ['aaa', 222], [111, 'BBB'])
    True
    >>> is_same_len_or_all_none([1, 'b', 3], ['aaa', 222, 'ccc'], [111, 'BBB', 333])
    True

    >>> is_same_len_or_all_none([], ['aaa'], [111])
    False
    >>> is_same_len_or_all_none([1], ['aaa', 222], [111, 'BBB'])
    False
    >>> is_same_len_or_all_none([1, 'b'], ['aaa'], [111, 'BBB'])
    False

    >>> is_same_len_or_all_none([1, 'b'], None)
    False
    >>> is_same_len_or_all_none(None, ['aaa'])
    False
    >>> is_same_len_or_all_none(None, None)
    True

    >>> is_same_len_or_all_none([1, 'b'], None, ['aaa', 222])
    False
    >>> is_same_len_or_all_none(None, ['aaa'], [111])
    False
    >>> is_same_len_or_all_none(None, None, [111, 'BBB'])
    False
    >>> is_same_len_or_all_none(None, None, None)
    True

    >>> is_same_len_or_all_none([1], None, ['aaa', 222])
    False
    >>> is_same_len_or_all_none(None, ['aaa'], [])
    False
    >>> is_same_len_or_all_none(None, ['aaa'], [111, 'BBB'])
    False
    """
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

def check_same_len_or_all_none(*args, **kwargs):
    """
    Checks whether either all the arguments are of the same length or all are None.
    
    If the check succeeds (all the arguments are of the same length or all are None), the function returns `True`. If
    the check fails, the function raises an `AssertionError` with a given `message`.
    
    The `message` and `level`, if they are specified, must be passed in as keyword arguments. The other arguments must
    be passed in as non-keyword arguments.

    Parameters
    ----------
    *args : miscellaneous
        The argument(s) to be checked.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    bool
        `True` if the check succeeds.
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_same_len_or_all_none(1, 'aaa')
    Traceback (most recent call last):
        ...
    TypeError: object of type 'int' has no len()

    >>> check_same_len_or_all_none([1], ['aaa'])
    True
    >>> check_same_len_or_all_none([1, 'b'], ['aaa', 222])
    True
    >>> check_same_len_or_all_none([1, 'b', 3], ['aaa', 222, 'ccc'])
    True

    >>> check_same_len_or_all_none([], ['aaa'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none([1], ['aaa', 222])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none([1, 'b'], ['aaa'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None

    >>> check_same_len_or_all_none([1], ['aaa'], [111])
    True
    >>> check_same_len_or_all_none([1, 'b'], ['aaa', 222], [111, 'BBB'])
    True
    >>> check_same_len_or_all_none([1, 'b', 3], ['aaa', 222, 'ccc'], [111, 'BBB', 333])
    True

    >>> check_same_len_or_all_none([], ['aaa'], [111])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none([1], ['aaa', 222], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none([1, 'b'], ['aaa'], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None

    >>> check_same_len_or_all_none([1, 'b'], None)
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none(None, ['aaa'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none(None, None)
    True

    >>> check_same_len_or_all_none([1, 'b'], None, ['aaa', 222])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none(None, ['aaa'], [111])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none(None, None, [111, 'BBB'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none(None, None, None)
    True

    >>> check_same_len_or_all_none([1], None, ['aaa', 222])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none(None, ['aaa'], [])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    >>> check_same_len_or_all_none(None, ['aaa'], [111, 'BBB'])
    Traceback (most recent call last):
        ...
    AssertionError: The arguments are neither of the same length nor all None
    """
    message = kwargs['message'] if 'message' in kwargs else 'The arguments are neither of the same length nor all None'
    level = kwargs['level'] if 'level' in kwargs else 1
    return check(is_same_len_or_all_none(*args), message, level)

def is_instance(arg, types, allow_none=False):
    """
    Returns `True` if `arg` is of one of the given `types`, otherwise `False`.
    
    If `allow_none` is `True`, and `arg` is `None`, will return `True` irrespective of the `types`.

    Parameters
    ----------
    arg :
        The argument to be checked.
    types : a type or an iterable of types
        The type or types.
    allow_none : bool
        Allow `None` `arg`.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_instance(1, int)
    True
    >>> is_instance(3.5, float)
    True
    >>> is_instance('hello', str)
    True
    >>> is_instance([1, 2, 3], list)
    True

    >>> is_instance(1, (int, float))
    True
    >>> is_instance(3.5, (int, float))
    True
    >>> is_instance('hello', (str, list))
    True
    >>> is_instance([1, 2, 3], (str, list))
    True

    >>> is_instance(1, float)
    False
    >>> is_instance(3.5, int)
    False
    >>> is_instance('hello', list)
    False
    >>> is_instance([1, 2, 3], str)
    False

    >>> is_instance(1, (list, str))
    False
    >>> is_instance(3.5, (list, str))
    False
    >>> is_instance('hello', (int, float))
    False
    >>> is_instance([1, 2, 3], (int, float))
    False

    >>> is_instance(None, int)
    False
    >>> is_instance(None, float)
    False
    >>> is_instance(None, str)
    False
    >>> is_instance(None, list)
    False

    >>> is_instance(None, (int, float))
    False
    >>> is_instance(None, (int, float))
    False
    >>> is_instance(None, (str, list))
    False
    >>> is_instance(None, (str, list))
    False

    >>> is_instance(1, int, allow_none=True)
    True
    >>> is_instance(3.5, float, allow_none=True)
    True
    >>> is_instance('hello', str, allow_none=True)
    True
    >>> is_instance([1, 2, 3], list, allow_none=True)
    True

    >>> is_instance(1, (int, float), allow_none=True)
    True
    >>> is_instance(3.5, (int, float), allow_none=True)
    True
    >>> is_instance('hello', (str, list), allow_none=True)
    True
    >>> is_instance([1, 2, 3], (str, list), allow_none=True)
    True

    >>> is_instance(1, float, allow_none=True)
    False
    >>> is_instance(3.5, int, allow_none=True)
    False
    >>> is_instance('hello', list, allow_none=True)
    False
    >>> is_instance([1, 2, 3], str, allow_none=True)
    False

    >>> is_instance(1, (list, str), allow_none=True)
    False
    >>> is_instance(3.5, (list, str), allow_none=True)
    False
    >>> is_instance('hello', (int, float), allow_none=True)
    False
    >>> is_instance([1, 2, 3], (int, float), allow_none=True)
    False

    >>> is_instance(None, int, allow_none=True)
    True
    >>> is_instance(None, float, allow_none=True)
    True
    >>> is_instance(None, str, allow_none=True)
    True
    >>> is_instance(None, list, allow_none=True)
    True

    >>> is_instance(None, (int, float), allow_none=True)
    True
    >>> is_instance(None, (int, float), allow_none=True)
    True
    >>> is_instance(None, (str, list), allow_none=True)
    True
    >>> is_instance(None, (str, list), allow_none=True)
    True
    """
    return (allow_none and arg is None) or isinstance(arg, types)
    
def check_instance(arg, types, allow_none=False, message='Argument "%(string)s" is not of type %(expected)s, but of type %(actual)s', level=1):
    """
    Checks whether `arg` is of one of the given `types`.
    
    If `allow_none` is `True`, and `arg` is `None`, the check will succeed irrespective of the `types`.

    If the check succeeds, the function returns `arg`. If the check fails, the function raises an `AssertionError` with
    a given `message`.
    
    In `message`, `%(string)s`, if present, will be replaced with a string representation of `arg`; `%(expected)s`, if
    present, will be replaced with the expected type(s); `%(actual)s`, if present, will be replaced with the actual type
    of `arg`. 
    
    Parameters
    ----------
    arg :
        The argument to be checked.
    types : a type or an iterable of types
        The type or types.
    allow_none : bool
        Allow `None` `arg`.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    object
        The argument is returned to facilitate the fluent pattern (function call chaining).
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_instance(1, int)
    1
    >>> check_instance(3.5, float)
    3.5
    >>> check_instance('hello', str)
    'hello'
    >>> check_instance([1, 2, 3], list)
    [1, 2, 3]

    >>> check_instance(1, (int, float))
    1
    >>> check_instance(3.5, (int, float))
    3.5
    >>> check_instance('hello', (str, list))
    'hello'
    >>> check_instance([1, 2, 3], (str, list))
    [1, 2, 3]

    >>> check_instance(1, float)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "1" is not of type <class 'float'>, but of type <class 'int'>
    >>> check_instance(3.5, int)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not of type <class 'int'>, but of type <class 'float'>
    >>> check_instance('hello', list)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hello" is not of type <class 'list'>, but of type <class 'str'>
    >>> check_instance([1, 2, 3], str)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" is not of type <class 'str'>, but of type <class 'list'>

    >>> check_instance(1, (list, str))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "1" is not of type (<class 'list'>, <class 'str'>), but of type <class 'int'>
    >>> check_instance(3.5, (list, str))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not of type (<class 'list'>, <class 'str'>), but of type <class 'float'>
    >>> check_instance('hello', (int, float))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hello" is not of type (<class 'int'>, <class 'float'>), but of type <class 'str'>
    >>> check_instance([1, 2, 3], (int, float))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" is not of type (<class 'int'>, <class 'float'>), but of type <class 'list'>

    >>> check_instance(None, int)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not of type <class 'int'>, but of type <class 'NoneType'>
    >>> check_instance(None, float)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not of type <class 'float'>, but of type <class 'NoneType'>
    >>> check_instance(None, str)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not of type <class 'str'>, but of type <class 'NoneType'>
    >>> check_instance(None, list)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not of type <class 'list'>, but of type <class 'NoneType'>

    >>> check_instance(None, (int, float))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not of type (<class 'int'>, <class 'float'>), but of type <class 'NoneType'>
    >>> check_instance(None, (str, list))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not of type (<class 'str'>, <class 'list'>), but of type <class 'NoneType'>

    >>> check_instance(1, int, allow_none=True)
    1
    >>> check_instance(3.5, float, allow_none=True)
    3.5
    >>> check_instance('hello', str, allow_none=True)
    'hello'
    >>> check_instance([1, 2, 3], list, allow_none=True)
    [1, 2, 3]

    >>> check_instance(1, (int, float), allow_none=True)
    1
    >>> check_instance(3.5, (int, float), allow_none=True)
    3.5
    >>> check_instance('hello', (str, list), allow_none=True)
    'hello'
    >>> check_instance([1, 2, 3], (str, list), allow_none=True)
    [1, 2, 3]

    >>> check_instance(1, float, allow_none=True)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "1" is not of type <class 'float'>, but of type <class 'int'>
    >>> check_instance(3.5, int, allow_none=True)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not of type <class 'int'>, but of type <class 'float'>
    >>> check_instance('hello', list, allow_none=True)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hello" is not of type <class 'list'>, but of type <class 'str'>
    >>> check_instance([1, 2, 3], str, allow_none=True)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" is not of type <class 'str'>, but of type <class 'list'>

    >>> check_instance(1, (list, str), allow_none=True)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "1" is not of type (<class 'list'>, <class 'str'>), but of type <class 'int'>
    >>> check_instance(3.5, (list, str), allow_none=True)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not of type (<class 'list'>, <class 'str'>), but of type <class 'float'>
    >>> check_instance('hello', (int, float), allow_none=True)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hello" is not of type (<class 'int'>, <class 'float'>), but of type <class 'str'>
    >>> check_instance([1, 2, 3], (int, float), allow_none=True)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" is not of type (<class 'int'>, <class 'float'>), but of type <class 'list'>

    >>> check_instance(None, int, allow_none=True)
    >>> check_instance(None, float, allow_none=True)
    >>> check_instance(None, str, allow_none=True)
    >>> check_instance(None, list, allow_none=True)

    >>> check_instance(None, (int, float), allow_none=True)
    >>> check_instance(None, (int, float), allow_none=True)
    >>> check_instance(None, (str, list), allow_none=True)
    >>> check_instance(None, (str, list), allow_none=True)
    """
    check(is_instance(arg, types, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg), 'expected': types}, level)
    return arg

def is_int(arg, allow_none=False):
    """
    Returns `True` if `arg` is of type `int`, otherwise `False`.
    
    If `allow_none` is `True`, and `arg` is `None`, will return `True`. If `allow_none` is `False`, and `arg` is `None`,
    will return `False`.

    Parameters
    ----------
    arg :
        The argument to be checked.
    allow_none : bool
        Allow `None` `arg`.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_int(3)
    True
    >>> is_int(3.5)
    False
    >>> import numpy as np
    >>> is_int(np.int64(3))
    False
    >>> is_int(None)
    False
    >>> is_int(None, allow_none=True)
    True
    >>> is_int('hi')
    False
    """
    return is_instance(arg, int, allow_none)

def check_int(arg, allow_none=False, message='Argument "%(string)s" is not an integer, but of type %(actual)s', level=1):
    """
    Checks whether `arg` is of type int.
    
    If `allow_none` is `True`, and `arg` is `None`, the check will succeed. If `allow_none` is `False`, and `arg` is
    `None`, the check will fail.

    If the check succeeds, the function returns `arg`. If the check fails, the function raises an `AssertionError` with
    a given `message`.
    
    In `message`, `%(string)s`, if present, will be replaced with a string representation of `arg`; `%(actual)s`, if
    present, will be replaced with the actual type of `arg`. 

    Parameters
    ----------
    arg :
        The argument to be checked.
    allow_none : bool
        Allow `None` `arg`.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    object
        The argument is returned to facilitate the fluent pattern (function call chaining).
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_int(3)
    3
    >>> check_int(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not an integer, but of type <class 'float'>
    >>> import numpy as np
    >>> check_int(np.int64(3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" is not an integer, but of type <class 'numpy.int64'>
    >>> check_int(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not an integer, but of type <class 'NoneType'>
    >>> check_int(None, allow_none=True)
    >>> check_int('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not an integer, but of type <class 'str'>
    """
    check(is_int(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_numpy_int(arg, allow_none=False):
    """
    Returns `True` if `arg` is of one of the NumPy integral types, otherwise `False`.
    
    If `allow_none` is `True`, and `arg` is `None`, will return `True`. If `allow_none` is `False`, and `arg` is `None`,
    will return `False`.

    Parameters
    ----------
    arg :
        The argument to be checked.
    allow_none : bool
        Allow `None` `arg`.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_some_numpy_int(3)
    False
    >>> is_some_numpy_int(3.5)
    False
    >>> import numpy as np
    >>> is_some_numpy_int(np.int64(3))
    True
    >>> is_some_numpy_int(None)
    False
    >>> is_some_numpy_int(None, allow_none=True)
    True
    >>> is_some_numpy_int('hi')
    False
    """
    import numpy as np
    return is_instance(arg, (np.int0, np.int8, np.int16, np.int32, np.int64), allow_none)

def check_some_numpy_int(arg, allow_none=False, message='Argument "%(string)s" is not a NumPy int*, but of type %(actual)s', level=1):
    """
    Checks whether `arg` is of one of the NumPy integral types.
    
    If `allow_none` is `True`, and `arg` is `None`, the check will succeed. If `allow_none` is `False`, and `arg` is
    `None`, the check will fail.

    If the check succeeds, the function returns `arg`. If the check fails, the function raises an `AssertionError` with
    a given `message`.
    
    In `message`, `%(string)s`, if present, will be replaced with a string representation of `arg`; `%(actual)s`, if
    present, will be replaced with the actual type of `arg`. 

    Parameters
    ----------
    arg :
        The argument to be checked.
    allow_none : bool
        Allow `None` `arg`.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    object
        The argument is returned to facilitate the fluent pattern (function call chaining).
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_some_numpy_int(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" is not a NumPy int*, but of type <class 'int'>
    >>> check_some_numpy_int(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not a NumPy int*, but of type <class 'float'>
    >>> import numpy as np
    >>> check_some_numpy_int(np.int64(3))
    3
    >>> check_some_numpy_int(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not a NumPy int*, but of type <class 'NoneType'>
    >>> check_some_numpy_int(None, allow_none=True)
    >>> check_some_numpy_int('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not a NumPy int*, but of type <class 'str'>
    """
    check(is_some_numpy_int(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_numpy_uint(arg, allow_none=False):
    """
    Returns `True` if `arg` is of one of the NumPy unsigned integral types, otherwise `False`.
    
    If `allow_none` is `True`, and `arg` is `None`, will return `True`. If `allow_none` is `False`, and `arg` is `None`,
    will return `False`.

    Parameters
    ----------
    arg :
        The argument to be checked.
    allow_none : bool
        Allow `None` `arg`.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_some_numpy_uint(3)
    False
    >>> is_some_numpy_uint(3.5)
    False
    >>> import numpy as np
    >>> is_some_numpy_uint(np.uint64(3))
    True
    >>> is_some_numpy_uint(None)
    False
    >>> is_some_numpy_uint(None, allow_none=True)
    True
    >>> is_some_numpy_uint('hi')
    False
    """
    import numpy as np
    return is_instance(arg, (np.uint, np.uint0, np.uint8, np.uint16, np.uint32, np.uint64), allow_none)

def check_some_numpy_uint(arg, allow_none=False, message='Argument "%(string)s" is not a NumPy uint*, but of type %(actual)s', level=1):
    """
    Checks whether `arg` is of one of the NumPy unsigned integral types.
    
    If `allow_none` is `True`, and `arg` is `None`, the check will succeed. If `allow_none` is `False`, and `arg` is
    `None`, the check will fail.

    If the check succeeds, the function returns `arg`. If the check fails, the function raises an `AssertionError` with
    a given `message`.
    
    In `message`, `%(string)s`, if present, will be replaced with a string representation of `arg`; `%(actual)s`, if
    present, will be replaced with the actual type of `arg`. 

    Parameters
    ----------
    arg :
        The argument to be checked.
    allow_none : bool
        Allow `None` `arg`.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    object
        The argument is returned to facilitate the fluent pattern (function call chaining).
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_some_numpy_uint(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" is not a NumPy uint*, but of type <class 'int'>
    >>> check_some_numpy_uint(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not a NumPy uint*, but of type <class 'float'>
    >>> import numpy as np
    >>> check_some_numpy_uint(np.uint64(3))
    3
    >>> check_some_numpy_uint(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not a NumPy uint*, but of type <class 'NoneType'>
    >>> check_some_numpy_uint(None, allow_none=True)
    >>> check_some_numpy_uint('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not a NumPy uint*, but of type <class 'str'>
    """
    check(is_some_numpy_uint(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_int(arg, allow_none=False):
    """
    Returns `True` if `arg` is either a native Python `int` or of one of the NumPy signed or unsigned integral types,
    otherwise `False`.
    
    If `allow_none` is `True`, and `arg` is `None`, will return `True`. If `allow_none` is `False`, and `arg` is `None`,
    will return `False`.

    Parameters
    ----------
    arg :
        The argument to be checked.
    allow_none : bool
        Allow `None` `arg`.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_some_int(3)
    True
    >>> is_some_int(3.5)
    False
    >>> import numpy as np
    >>> is_some_int(np.uint64(3))
    True
    >>> is_some_int(None)
    False
    >>> is_some_int(None, allow_none=True)
    True
    >>> is_some_int('hi')
    False
    """
    return is_int(arg, allow_none) or is_some_numpy_int(arg, allow_none) or is_some_numpy_uint(arg, allow_none)

def check_some_int(arg, allow_none=False, message='Argument "%(string)s" is not some (u)int*, but of type %(actual)s', level=1):
    """
    Checks whether `arg` is either a native Python `int` or of one of the NumPy signed or unsigned integral types.
    
    If `allow_none` is `True`, and `arg` is `None`, the check will succeed. If `allow_none` is `False`, and `arg` is
    `None`, the check will fail.

    If the check succeeds, the function returns `arg`. If the check fails, the function raises an `AssertionError` with
    a given `message`.
    
    In `message`, `%(string)s`, if present, will be replaced with a string representation of `arg`; `%(actual)s`, if
    present, will be replaced with the actual type of `arg`.

    Parameters
    ----------
    arg :
        The argument to be checked.
    allow_none : bool
        Allow `None` `arg`.
    message : str, callable
        The message for the `AssertionError` in case the check has failed. If `message` is callable, then it will be
        called with no arguments to obtain the message. If unspecified, the default message will be used.
    level : int
        The level of this check. The check will only be carried out if `tsa_settings.MIN_CHECK_LEVEL` is less than or
        equal to `level`. Otherwise the check will succeed regardless of the `arg`. If unspecified, defaults to 1.

    Returns
    -------
    object
        The argument is returned to facilitate the fluent pattern (function call chaining).
    
    Raises
    ------
    AssertionError
        The check has failed.
    
    Examples
    --------
    >>> check_some_int(3)
    3
    >>> check_some_int(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not some (u)int*, but of type <class 'float'>
    >>> import numpy as np
    >>> check_some_int(np.int64(3))
    3
    >>> check_some_int(np.uint64(3))
    3
    >>> check_some_int(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not some (u)int*, but of type <class 'NoneType'>
    >>> check_some_int(None, allow_none=True)
    >>> check_some_int('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not some (u)int*, but of type <class 'str'>
    """
    check(is_some_int(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_float(arg, allow_none=False):
    """
    Returns `True` if `arg` is of type `float`, otherwise `False`.
    
    If `allow_none` is `True`, and `arg` is `None`, will return `True`. If `allow_none` is `False`, and `arg` is `None`,
    will return `False`.

    Parameters
    ----------
    arg :
        The argument to be checked.
    allow_none : bool
        Allow `None` `arg`.

    Returns
    -------
    bool
        `True` or `False`.
    
    Examples
    --------
    >>> is_float(3)
    False
    >>> is_float(3.5)
    True
    
    >>> import numpy as np

    NB! The following is true (is that right?):

    >>> is_float(np.float64(3.5))
    True

    NB! The following is true (is that right?):

    >>> is_float(np.double(3.5))
    True

    >>> is_float(None)
    False

    >>> is_float(None, allow_none=True)
    True

    >>> is_float('hi')
    False
    """
    return is_instance(arg, float, allow_none)

def check_float(arg, allow_none=False, message='Argument "%(string)s" is not a float, but of type %(actual)s', level=1):
    """
    >>> check_float(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" is not a float, but of type <class 'int'>
    >>> check_float(3.5)
    3.5
    >>> import numpy as np
    >>> check_float(np.float64(3.5))
    3.5
    >>> check_float(np.double(3.5))
    3.5
    >>> check_float(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not a float, but of type <class 'NoneType'>
    >>> check_float(None, allow_none=True)
    >>> check_float('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not a float, but of type <class 'str'>
    """
    check(is_float(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_numpy_float(arg, allow_none=False):
    """
    >>> is_some_numpy_float(3)
    False
    
    >>> is_some_numpy_float(3.5)
    False
    
    >>> import numpy as np
    >>> is_some_numpy_float(np.float64(3.5))
    True
    
    NB! The following is true (is that right?):

    >>> is_some_numpy_float(np.double(3.5))
    True

    >>> is_some_numpy_float(None)
    False

    >>> is_some_numpy_float(None, allow_none=True)
    True

    >>> is_some_numpy_float('hi')
    False
    """
    import numpy as np
    return is_instance(arg, (np.float16, np.float32, np.float64), allow_none)

def check_some_numpy_float(arg, allow_none=False, message='Argument "%(string)s" is not a NumPy float*, but of type %(actual)s', level=1):
    """
    >>> check_some_numpy_float(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" is not a NumPy float*, but of type <class 'int'>
    >>> check_some_numpy_float(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not a NumPy float*, but of type <class 'float'>
    >>> import numpy as np
    >>> check_some_numpy_float(np.float64(3.5))
    3.5
    >>> check_some_numpy_float(np.double(3.5))
    3.5
    >>> check_some_numpy_float(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not a NumPy float*, but of type <class 'NoneType'>
    >>> check_some_numpy_float(None, allow_none=True)
    >>> check_some_numpy_float('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not a NumPy float*, but of type <class 'str'>
    """
    check(is_some_numpy_float(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_numpy_double(arg, allow_none=False):
    """
    >>> is_some_numpy_double(3)
    False

    >>> is_some_numpy_double(3.5)
    False

    >>> import numpy as np
    
    NB! The following is true (is that right?):

    >>> is_some_numpy_double(np.float64(3.5))
    True
    
    >>> is_some_numpy_double(np.double(3.5))
    True
    
    >>> is_some_numpy_double(None)
    False
    
    >>> is_some_numpy_double(None, allow_none=True)
    True
    
    >>> is_some_numpy_double('hi')
    False
    """
    import numpy as np
    return is_instance(arg, (np.double, np.longdouble), allow_none)

def check_some_numpy_double(arg, allow_none=False, message='Argument "%(string)s" is not a NumPy double/longdouble, but of type %(actual)s', level=1):
    """
    >>> check_some_numpy_double(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" is not a NumPy double/longdouble, but of type <class 'int'>
    >>> check_some_numpy_double(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not a NumPy double/longdouble, but of type <class 'float'>
    >>> import numpy as np
    >>> check_some_numpy_double(np.float64(3.5))
    3.5
    >>> check_some_numpy_double(np.double(3.5))
    3.5
    >>> check_some_numpy_double(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not a NumPy double/longdouble, but of type <class 'NoneType'>
    >>> check_some_numpy_double(None, allow_none=True)
    >>> check_some_numpy_double('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not a NumPy double/longdouble, but of type <class 'str'>
    """
    check(is_some_numpy_double(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_float(arg, allow_none=False):
    """
    >>> is_some_float(3)
    False
    >>> is_some_float(3.5)
    True
    >>> import numpy as np
    >>> is_some_float(np.float64(3.5))
    True
    >>> is_some_float(np.double(3.5))
    True
    >>> is_some_float(None)
    False
    >>> is_some_float(None, allow_none=True)
    True
    >>> is_some_float('hi')
    False
    """
    return is_float(arg, allow_none) or is_some_numpy_float(arg, allow_none) or is_some_numpy_double(arg, allow_none)

def check_some_float(arg, allow_none=False, message='Argument "%(string)s" is not some float*/double/longdouble, but of type %(actual)s', level=1):
    """
    >>> check_some_float(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" is not some float*/double/longdouble, but of type <class 'int'>
    >>> check_some_float(3.5)
    3.5
    >>> import numpy as np
    >>> check_some_float(np.float64(3.5))
    3.5
    >>> check_some_float(np.double(3.5))
    3.5
    >>> check_some_float(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not some float*/double/longdouble, but of type <class 'NoneType'>
    >>> check_some_float(None, allow_none=True)
    >>> check_some_float('hi')        
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not some float*/double/longdouble, but of type <class 'str'>
    """
    check(is_some_float(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_number(arg, allow_none=False):
    """
    >>> is_some_number(3)
    True
    >>> is_some_number(3.5)
    True
    >>> import numpy as np
    >>> is_some_number(np.int64(3))
    True
    >>> is_some_number(np.float64(3.5))
    True
    >>> is_some_number(np.double(3.5))
    True
    >>> is_some_number(None)
    False
    >>> is_some_number(None, allow_none=True)
    True
    >>> is_some_number('hi')
    False
    """
    return is_some_int(arg, allow_none) or is_some_float(arg, allow_none)

def check_some_number(arg, allow_none=False, message='Argument "%(string)s" is not some number, but of type %(actual)s', level=1):
    """
    >>> check_some_number(3)
    3
    >>> check_some_number(3.5)
    3.5
    >>> import numpy as np
    >>> check_some_number(np.float64(3.5))
    3.5
    >>> check_some_number(np.double(3.5))
    3.5
    >>> check_some_number(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not some number, but of type <class 'NoneType'>
    >>> check_some_number(None, allow_none=True)
    >>> check_some_number('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not some number, but of type <class 'str'>
    """
    check(is_some_number(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_numpy_array(arg, allow_none=False):
    """
    >>> import numpy as np
    >>> is_numpy_array(np.array([1, 2, 3]))
    True
    >>> is_numpy_array(np.array([[1, 2, 3], [1, 2, 3]]))
    True
    >>> is_numpy_array(np.array(3))
    True
    >>> is_numpy_array([1, 2, 3])
    False
    >>> is_numpy_array(3)
    False
    >>> is_numpy_array(np.int64(3))
    False
    >>> is_numpy_array(3.5)
    False
    >>> is_numpy_array(np.float64(3.5))
    False
    >>> is_numpy_array('hi')
    False
    >>> is_numpy_array(None)
    False
    >>> is_numpy_array(None, allow_none=True)
    True
    """
    import numpy as np
    return is_instance(arg, np.ndarray, allow_none)

def check_numpy_array(arg, allow_none=False, message='Argument "%(string)s" is not a NumPy array, but of type %(actual)s', level=1):
    """
    >>> import numpy as np
    >>> check_numpy_array(np.array([1, 2, 3]))
    array([1, 2, 3])
    >>> check_numpy_array(np.array([[1, 2, 3], [1, 2, 3]]))
    array([[1, 2, 3],
           [1, 2, 3]])
    >>> check_numpy_array(np.array(3))
    array(3)
    >>> check_numpy_array([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" is not a NumPy array, but of type <class 'list'>
    >>> check_numpy_array(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" is not a NumPy array, but of type <class 'int'>
    >>> check_numpy_array(np.int64(3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" is not a NumPy array, but of type <class 'numpy.int64'>
    >>> check_numpy_array(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not a NumPy array, but of type <class 'float'>
    >>> check_numpy_array(np.float64(3.5))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" is not a NumPy array, but of type <class 'numpy.float64'>
    >>> check_numpy_array('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" is not a NumPy array, but of type <class 'str'>
    >>> check_numpy_array(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" is not a NumPy array, but of type <class 'NoneType'>
    >>> check_numpy_array(None, allow_none=True)
    """
    check(is_numpy_array(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_string(arg, allow_none=False):
    """
    >>> is_string([1, 2, 3])
    False
    >>> is_string(3)
    False
    >>> is_string(3.5)
    False
    >>> is_string('hi')
    True
    >>> is_string("hi")
    True
    >>> is_string(None)
    False
    >>> is_string(None, allow_none=True)
    True
    """
    return is_instance(arg, str, allow_none)

def check_string(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a string', level=1):
    """
    >>> check_string([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a string
    >>> check_string(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a string
    >>> check_string(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not a string
    >>> check_string('hi')
    'hi'
    >>> check_string("hi")
    'hi'
    >>> check_string(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a string
    >>> check_string(None, allow_none=True)
    """
    check(is_string(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_date(arg, allow_none=False):
    """
    >>> is_date([1, 2, 3])
    False
    >>> is_date(3)
    False
    >>> is_date(3.5)
    False
    >>> is_date('hi')
    False
    >>> is_date("hi")
    False
    >>> import datetime as dt
    >>> is_date(dt.date(2019, 9, 10))
    True
    >>> is_date(dt.time(12, 3))
    False
    >>> is_date(dt.datetime(2019, 9, 10, 12, 3))
    False
    >>> is_date(dt.timedelta(seconds=5))
    False
    >>> import numpy as np
    >>> is_date(np.timedelta64(5, 's'))
    False
    >>> import pandas as pd
    >>> is_date(pd.Timedelta(5, 's'))
    False
    >>> is_date(None)
    False
    >>> is_date(None, allow_none=True)
    True
    """
    import datetime as dt
    if is_instance(arg, dt.datetime, allow_none=False): return False
    return is_instance(arg, dt.date, allow_none)

def check_date(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a date', level=1):
    """
    >>> check_date([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a date
    >>> check_date(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a date
    >>> check_date(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not a date
    >>> check_date('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a date
    >>> check_date("hi")
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a date
    >>> import datetime as dt
    >>> check_date(dt.date(2019, 9, 10))
    datetime.date(2019, 9, 10)
    >>> check_date(dt.time(12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "12:03:00" of type <class 'datetime.time'> is not a date
    >>> check_date(dt.datetime(2019, 9, 10, 12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10 12:03:00" of type <class 'datetime.datetime'> is not a date
    >>> check_date(dt.timedelta(seconds=5))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0:00:05" of type <class 'datetime.timedelta'> is not a date
    >>> import numpy as np
    >>> check_date(np.timedelta64(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "5 seconds" of type <class 'numpy.timedelta64'> is not a date
    >>> import pandas as pd
    >>> check_date(pd.Timedelta(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0 days 00:00:05" of type <class 'pandas._libs.tslibs.timedeltas.Timedelta'> is not a date
    >>> check_date(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a date
    >>> check_date(None, allow_none=True)
    """
    check(is_date(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_date(arg, allow_none=False):
    """
    >>> is_some_date([1, 2, 3])
    False
    >>> is_some_date(3)
    False
    >>> is_some_date(3.5)
    False
    >>> is_some_date('hi')
    False
    >>> is_some_date("hi")
    False
    >>> import datetime as dt
    >>> is_some_date(dt.date(2019, 9, 10))
    True
    >>> is_some_date(dt.time(12, 3))
    False
    >>> is_some_date(dt.datetime(2019, 9, 10, 12, 3))
    False
    >>> is_some_date(dt.timedelta(seconds=5))
    False
    >>> import numpy as np
    >>> is_some_date(np.timedelta64(5, 's'))
    False
    >>> import pandas as pd
    >>> is_some_date(pd.Timedelta(5, 's'))
    False
    >>> is_some_date(None)
    False
    >>> is_some_date(None, allow_none=True)
    True
    """
    return is_date(arg, allow_none)

def check_some_date(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a date', level=1):
    """
    >>> check_some_date([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a date
    >>> check_some_date(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a date
    >>> check_some_date(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not a date
    >>> check_some_date('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a date
    >>> check_some_date("hi")
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a date
    >>> import datetime as dt
    >>> check_some_date(dt.date(2019, 9, 10))
    datetime.date(2019, 9, 10)
    >>> check_some_date(dt.time(12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "12:03:00" of type <class 'datetime.time'> is not a date
    >>> check_some_date(dt.datetime(2019, 9, 10, 12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10 12:03:00" of type <class 'datetime.datetime'> is not a date
    >>> check_some_date(dt.timedelta(seconds=5))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0:00:05" of type <class 'datetime.timedelta'> is not a date
    >>> import numpy as np
    >>> check_some_date(np.timedelta64(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "5 seconds" of type <class 'numpy.timedelta64'> is not a date
    >>> import pandas as pd
    >>> check_some_date(pd.Timedelta(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0 days 00:00:05" of type <class 'pandas._libs.tslibs.timedeltas.Timedelta'> is not a date
    >>> check_some_date(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a date
    >>> check_some_date(None, allow_none=True)
    """
    check(is_some_date(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_time(arg, allow_none=False):
    """
    >>> is_time([1, 2, 3])
    False
    >>> is_time(3)
    False
    >>> is_time(3.5)
    False
    >>> is_time('hi')
    False
    >>> is_time("hi")
    False
    >>> import datetime as dt
    >>> is_time(dt.date(2019, 9, 10))
    False
    >>> is_time(dt.time(12, 3))
    True
    >>> is_time(dt.datetime(2019, 9, 10, 12, 3))
    False
    >>> is_time(dt.timedelta(seconds=5))
    False
    >>> import numpy as np
    >>> is_time(np.timedelta64(5, 's'))
    False
    >>> import pandas as pd
    >>> is_time(pd.Timedelta(5, 's'))
    False
    >>> is_time(None)
    False
    >>> is_time(None, allow_none=True)
    True
    """
    import datetime as dt
    return is_instance(arg, dt.time, allow_none)

def check_time(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a time', level=1):
    """
    >>> check_time([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a time
    >>> check_time(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a time
    >>> check_time(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not a time
    >>> check_time('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a time
    >>> check_time("hi")
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a time
    >>> import datetime as dt
    >>> check_time(dt.date(2019, 9, 10))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10" of type <class 'datetime.date'> is not a time
    >>> check_time(dt.time(12, 3))
    datetime.time(12, 3)
    >>> check_time(dt.datetime(2019, 9, 10, 12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10 12:03:00" of type <class 'datetime.datetime'> is not a time
    >>> check_time(dt.timedelta(seconds=5))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0:00:05" of type <class 'datetime.timedelta'> is not a time
    >>> import numpy as np
    >>> check_time(np.timedelta64(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "5 seconds" of type <class 'numpy.timedelta64'> is not a time
    >>> import pandas as pd
    >>> check_time(pd.Timedelta(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0 days 00:00:05" of type <class 'pandas._libs.tslibs.timedeltas.Timedelta'> is not a time
    >>> check_time(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a time
    >>> check_time(None, allow_none=True)
    """
    check(is_time(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_time(arg, allow_none=False):
    """
    >>> is_some_time([1, 2, 3])
    False
    >>> is_some_time(3)
    False
    >>> is_some_time(3.5)
    False
    >>> is_some_time('hi')
    False
    >>> is_some_time("hi")
    False
    >>> import datetime as dt
    >>> is_some_time(dt.date(2019, 9, 10))
    False
    >>> is_some_time(dt.time(12, 3))
    True
    >>> is_some_time(dt.datetime(2019, 9, 10, 12, 3))
    False
    >>> is_some_time(dt.timedelta(seconds=5))
    False
    >>> is_some_time(None)
    False
    >>> is_some_time(None, allow_none=True)
    True
    """
    return is_time(arg, allow_none)

def check_some_time(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a time', level=1):
    """
    >>> check_some_time([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a time
    >>> check_some_time(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a time
    >>> check_some_time(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not a time
    >>> check_some_time('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a time
    >>> check_some_time("hi")
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a time
    >>> import datetime as dt
    >>> check_some_time(dt.date(2019, 9, 10))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10" of type <class 'datetime.date'> is not a time
    >>> check_some_time(dt.time(12, 3))
    datetime.time(12, 3)
    >>> check_some_time(dt.datetime(2019, 9, 10, 12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10 12:03:00" of type <class 'datetime.datetime'> is not a time
    >>> check_some_time(dt.timedelta(seconds=5))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0:00:05" of type <class 'datetime.timedelta'> is not a time
    >>> import numpy as np
    >>> check_some_time(np.timedelta64(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "5 seconds" of type <class 'numpy.timedelta64'> is not a time
    >>> import pandas as pd
    >>> check_some_time(pd.Timedelta(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0 days 00:00:05" of type <class 'pandas._libs.tslibs.timedeltas.Timedelta'> is not a time
    >>> check_some_time(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a time
    >>> check_some_time(None, allow_none=True)
    """
    check(is_some_time(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_datetime(arg, allow_none=False):
    """
    >>> is_datetime([1, 2, 3])
    False
    >>> is_datetime(3)
    False
    >>> is_datetime(3.5)
    False
    >>> is_datetime('hi')
    False
    >>> is_datetime("hi")
    False
    >>> import datetime as dt
    >>> is_datetime(dt.date(2019, 9, 10))
    False
    >>> is_datetime(dt.time(12, 3))
    False
    >>> is_datetime(dt.datetime(2019, 9, 10, 12, 3))
    True
    >>> is_datetime(dt.timedelta(seconds=5))
    False
    >>> import numpy as np
    >>> is_datetime(np.timedelta64(5, 's'))
    False
    >>> import pandas as pd
    >>> is_datetime(pd.Timedelta(5, 's'))
    False
    >>> is_datetime(None)
    False
    >>> is_datetime(None, allow_none=True)
    True
    """
    import datetime as dt
    return is_instance(arg, dt.datetime, allow_none)

def check_datetime(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a datetime', level=1):
    """
    >>> check_datetime([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a datetime
    >>> check_datetime(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a datetime
    >>> check_datetime(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not a datetime
    >>> check_datetime('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a datetime
    >>> check_datetime("hi")
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a datetime
    >>> import datetime as dt
    >>> check_datetime(dt.date(2019, 9, 10))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10" of type <class 'datetime.date'> is not a datetime
    >>> import datetime as dt
    >>> check_datetime(dt.time(12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "12:03:00" of type <class 'datetime.time'> is not a datetime
    >>> check_datetime(dt.datetime(2019, 9, 10, 12, 3))
    datetime.datetime(2019, 9, 10, 12, 3)
    >>> check_datetime(dt.timedelta(seconds=5))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0:00:05" of type <class 'datetime.timedelta'> is not a datetime
    >>> import numpy as np
    >>> check_datetime(np.timedelta64(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "5 seconds" of type <class 'numpy.timedelta64'> is not a datetime
    >>> import pandas as pd
    >>> check_datetime(pd.Timedelta(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0 days 00:00:05" of type <class 'pandas._libs.tslibs.timedeltas.Timedelta'> is not a datetime
    >>> check_datetime(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a datetime
    >>> check_datetime(None, allow_none=True)
    """
    check(is_datetime(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_datetime(arg, allow_none=False):
    """
    >>> is_some_datetime([1, 2, 3])
    False
    >>> is_some_datetime(3)
    False
    >>> is_some_datetime(3.5)
    False
    >>> is_some_datetime('hi')
    False
    >>> is_some_datetime("hi")
    False
    >>> import datetime as dt
    >>> is_some_datetime(dt.date(2019, 9, 10))
    False
    >>> is_some_datetime(dt.time(12, 3))
    False
    >>> is_some_datetime(dt.datetime(2019, 9, 10, 12, 3))
    True
    >>> is_some_datetime(dt.timedelta(seconds=5))
    False
    >>> is_some_datetime(None)
    False
    >>> is_some_datetime(None, allow_none=True)
    True
    """
    import datetime as dt
    import numpy as np
    import pandas as pd
    return is_instance(arg, (dt.datetime, np.datetime64, pd.Timestamp), allow_none)

def check_some_datetime(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not some datetime', level=1):
    """
    >>> check_some_datetime([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not some datetime
    >>> check_some_datetime(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not some datetime
    >>> check_some_datetime(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not some datetime
    >>> check_some_datetime('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not some datetime
    >>> check_some_datetime("hi")
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not some datetime
    >>> import datetime as dt
    >>> check_some_datetime(dt.date(2019, 9, 10))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10" of type <class 'datetime.date'> is not some datetime
    >>> check_some_datetime(dt.time(12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "12:03:00" of type <class 'datetime.time'> is not some datetime
    >>> check_some_datetime(dt.datetime(2019, 9, 10, 12, 3))
    datetime.datetime(2019, 9, 10, 12, 3)
    >>> check_some_datetime(dt.timedelta(seconds=5))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0:00:05" of type <class 'datetime.timedelta'> is not some datetime
    >>> import numpy as np
    >>> check_some_datetime(np.timedelta64(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "5 seconds" of type <class 'numpy.timedelta64'> is not some datetime
    >>> import pandas as pd
    >>> check_some_datetime(pd.Timedelta(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "0 days 00:00:05" of type <class 'pandas._libs.tslibs.timedeltas.Timedelta'> is not some datetime
    >>> check_some_datetime(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not some datetime
    >>> check_some_datetime(None, allow_none=True)
    """
    check(is_some_datetime(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_timedelta(arg, allow_none=False):
    """
    >>> is_timedelta([1, 2, 3])
    False

    >>> is_timedelta(3)
    False
    
    >>> is_timedelta(3.5)
    False
    
    >>> is_timedelta('hi')
    False
    
    >>> is_timedelta("hi")
    False
    
    >>> import datetime as dt
    
    >>> is_timedelta(dt.date(2019, 9, 10))
    False
    
    >>> is_timedelta(dt.time(12, 3))
    False
    
    >>> is_timedelta(dt.datetime(2019, 9, 10, 12, 3))
    False
    
    >>> is_timedelta(dt.timedelta(seconds=5))
    True
    
    >>> import numpy as np
    
    >>> is_timedelta(np.timedelta64(5, 's'))
    False
    
    >>> import pandas as pd
    
    NB! Note that the following is true:

    >>> is_timedelta(pd.Timedelta(5, 's'))
    True
    
    >>> is_timedelta(None)
    False
    
    >>> is_timedelta(None, allow_none=True)
    True
    """
    import datetime as dt
    return is_instance(arg, dt.timedelta, allow_none)

def check_timedelta(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a timedelta', level=1):
    """
    >>> check_timedelta([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a timedelta

    >>> check_timedelta(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a timedelta

    >>> check_timedelta(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not a timedelta

    >>> check_timedelta('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a timedelta

    >>> check_timedelta("hi")
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a timedelta

    >>> import datetime as dt

    >>> check_timedelta(dt.date(2019, 9, 10))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10" of type <class 'datetime.date'> is not a timedelta

    >>> check_timedelta(dt.time(12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "12:03:00" of type <class 'datetime.time'> is not a timedelta

    >>> check_timedelta(dt.datetime(2019, 9, 10, 12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10 12:03:00" of type <class 'datetime.datetime'> is not a timedelta

    >>> check_timedelta(dt.timedelta(seconds=5))    #doctest: +ELLIPSIS
    datetime.timedelta(...)
    
    >>> import numpy as np
    
    >>> check_timedelta(np.timedelta64(5, 's'))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "5 seconds" of type <class 'numpy.timedelta64'> is not a timedelta
    
    >>> import pandas as pd
    
    NB! Note that the following holds:
    
    >>> check_timedelta(pd.Timedelta(5, 's'))
    Timedelta('0 days 00:00:05')
    
    >>> check_timedelta(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a timedelta
    
    >>> check_timedelta(None, allow_none=True)
    """
    check(is_timedelta(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_timedelta(arg, allow_none=False):
    """
    >>> is_some_timedelta([1, 2, 3])
    False
    >>> is_some_timedelta(3)
    False
    >>> is_some_timedelta(3.5)
    False
    >>> is_some_timedelta('hi')
    False
    >>> is_some_timedelta("hi")
    False
    >>> import datetime as dt
    >>> is_some_timedelta(dt.date(2019, 9, 10))
    False
    >>> is_some_timedelta(dt.time(12, 3))
    False
    >>> is_some_timedelta(dt.datetime(2019, 9, 10, 12, 3))
    False
    >>> is_some_timedelta(dt.timedelta(seconds=5))
    True
    >>> import numpy as np
    >>> is_some_timedelta(np.timedelta64(5, 's'))
    True
    >>> import pandas as pd
    >>> is_some_timedelta(pd.Timedelta(5, 's'))
    True
    >>> is_some_timedelta(None)
    False
    >>> is_some_timedelta(None, allow_none=True)
    True
    """
    import datetime as dt
    import numpy as np
    import pandas as pd
    return is_instance(arg, (dt.timedelta, np.timedelta64, pd.Timedelta), allow_none)

def check_some_timedelta(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not some timedelta', level=1):
    """
    >>> check_some_timedelta([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not some timedelta
    >>> check_some_timedelta(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not some timedelta
    >>> check_some_timedelta(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not some timedelta
    >>> check_some_timedelta('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not some timedelta
    >>> check_some_timedelta("hi")
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not some timedelta
    >>> import datetime as dt
    >>> check_some_timedelta(dt.date(2019, 9, 10))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10" of type <class 'datetime.date'> is not some timedelta
    >>> check_some_timedelta(dt.time(12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "12:03:00" of type <class 'datetime.time'> is not some timedelta
    >>> check_some_timedelta(dt.datetime(2019, 9, 10, 12, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "2019-09-10 12:03:00" of type <class 'datetime.datetime'> is not some timedelta
    >>> check_some_timedelta(dt.timedelta(seconds=5))    #doctest: +ELLIPSIS
    datetime.timedelta(...)
    >>> import numpy as np
    >>> check_some_timedelta(np.timedelta64(5, 's'))
    numpy.timedelta64(5,'s')
    >>> import pandas as pd
    >>> check_some_timedelta(pd.Timedelta(5, 's'))
    Timedelta('0 days 00:00:05')
    >>> check_some_timedelta(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not some timedelta
    >>> check_some_timedelta(None, allow_none=True)
    """
    check(is_some_timedelta(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_iterable(arg, allow_none=False):
    """
    >>> is_iterable(3)
    False
    >>> is_iterable(3.5)
    False
    >>> is_iterable('hi')
    True
    >>> is_iterable([1, 2, 3])
    True
    >>> is_iterable([[1, 2, 3], [1, 2, 3]])
    True
    >>> import numpy as np
    >>> is_iterable(np.array([1, 2, 3]))
    True
    >>> is_iterable(np.array([[1, 2, 3], [1, 2, 3]]))
    True
    >>> is_iterable({'name': 'Paul', 'surname': 'Bilokon'})
    True
    >>> is_iterable(None)
    False
    >>> is_iterable(None, allow_none=True)
    True
    """
    return is_instance(arg, collections.abc.Iterable, allow_none)

def check_iterable(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not iterable', level=1):
    """
    >>> check_iterable(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not iterable
    >>> check_iterable(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not iterable
    >>> check_iterable('hi')
    'hi'
    >>> check_iterable([1, 2, 3])
    [1, 2, 3]
    >>> check_iterable([[1, 2, 3], [1, 2, 3]])
    [[1, 2, 3], [1, 2, 3]]
    >>> import numpy as np
    >>> check_iterable(np.array([1, 2, 3]))
    array([1, 2, 3])
    >>> check_iterable(np.array([[1, 2, 3], [1, 2, 3]]))
    array([[1, 2, 3],
           [1, 2, 3]])
    >>> check_iterable({'name': 'Paul', 'surname': 'Bilokon'})
    {'name': 'Paul', 'surname': 'Bilokon'}
    >>> check_iterable(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not iterable
    >>> check_iterable(None, allow_none=True)
    """
    check(is_iterable(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_iterable_not_string(arg, allow_none=False):
    """
    >>> is_iterable_not_string(3)
    False
    >>> is_iterable_not_string(3.5)
    False
    >>> is_iterable_not_string('hi')
    False
    >>> is_iterable_not_string([1, 2, 3])
    True
    >>> is_iterable_not_string([[1, 2, 3], [1, 2, 3]])
    True
    >>> import numpy as np
    >>> is_iterable_not_string(np.array([1, 2, 3]))
    True
    >>> is_iterable_not_string(np.array([[1, 2, 3], [1, 2, 3]]))
    True
    >>> is_iterable_not_string({'name': 'Paul', 'surname': 'Bilokon'})
    True
    >>> is_iterable_not_string(None)
    False
    >>> is_iterable_not_string(None, allow_none=True)
    True
    """
    return (allow_none and arg is None) or ((not is_string(arg)) and is_iterable(arg))

def check_iterable_not_string(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is either not iterable or a string', level=1):
    """
    >>> check_iterable_not_string(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is either not iterable or a string
    >>> check_iterable_not_string(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is either not iterable or a string
    >>> check_iterable_not_string('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is either not iterable or a string
    >>> check_iterable_not_string([1, 2, 3])
    [1, 2, 3]
    >>> check_iterable_not_string([[1, 2, 3], [1, 2, 3]])
    [[1, 2, 3], [1, 2, 3]]
    >>> import numpy as np
    >>> check_iterable_not_string(np.array([1, 2, 3]))
    array([1, 2, 3])
    >>> check_iterable_not_string(np.array([[1, 2, 3], [1, 2, 3]]))
    array([[1, 2, 3],
           [1, 2, 3]])
    >>> check_iterable_not_string({'name': 'Paul', 'surname': 'Bilokon'})
    {'name': 'Paul', 'surname': 'Bilokon'}
    >>> check_iterable_not_string(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is either not iterable or a string
    >>> check_iterable_not_string(None, allow_none=True)
    """
    check(is_iterable_not_string(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_iterable_over_instances(arg, types, allow_none=False, allow_empty=False):
    """
    >>> result, iterable = is_iterable_over_instances(3, int)
    >>> result
    False
    >>> iterable
    3

    >>> result, iterable = is_iterable_over_instances(3.5, float)
    >>> result
    False
    >>> iterable
    3.5

    >>> result, iterable = is_iterable_over_instances('hi', str)
    >>> result
    True
    >>> list(iterable)
    ['h', 'i']

    >>> result, iterable = is_iterable_over_instances([1, 2, 3], int)
    >>> result
    True
    >>> list(iterable)
    [1, 2, 3]

    >>> result, iterable = is_iterable_over_instances([[1, 2, 3], [1, 2, 3]], list)
    >>> result
    True
    >>> list(iterable)
    [[1, 2, 3], [1, 2, 3]]

    >>> import numpy as np

    >>> result, iterable = is_iterable_over_instances(np.array([1, 2, 3]), np.int32)
    >>> result
    True
    >>> list(iterable)
    [1, 2, 3]

    NB! In this case the iterable that was passed in does not quite match the returned iterable:

    >>> result, _ = is_iterable_over_instances(np.array([[1, 2, 3], [1, 2, 3]]), np.ndarray)
    >>> result
    True
    
    >>> result, iterable = is_iterable_over_instances({'name': 'Paul', 'surname': 'Bilokon'}, str)
    >>> result
    True
    >>> list(iterable)
    ['name', 'surname']

    >>> result, iterable = is_iterable_over_instances([], int)
    >>> result
    False
    
    >>> result, iterable = is_iterable_over_instances([], int, allow_empty=True)
    >>> result
    True
    
    >>> result, iterable = is_iterable_over_instances(None, int)
    >>> result
    False
    >>> iterable is None
    True
    
    >>> result, iterable = is_iterable_over_instances(None, int, allow_none=True)
    >>> result
    True
    >>> iterable is None
    True
    """
    if (allow_none and arg is None): return True, arg
    if is_iterable(arg):
        objs, iterable = utils.peek(iter(arg))
        if (len(objs) == 0): return allow_empty, iterable
        return isinstance(objs[0], types), iterable
    return False, arg
    
def check_iterable_over_instances(arg, types, allow_none=False, allow_empty=False, message='Argument is not an iterable over type %(expected)s', level=1):
    """
    >>> check_iterable_over_instances(3, int)
    Traceback (most recent call last):
        ...
    AssertionError: Argument is not an iterable over type <class 'int'>

    >>> check_iterable_over_instances(3.5, float)
    Traceback (most recent call last):
        ...
    AssertionError: Argument is not an iterable over type <class 'float'>

    >>> iterable = check_iterable_over_instances('hi', str)
    >>> list(iterable)
    ['h', 'i']

    >>> iterable = check_iterable_over_instances([1, 2, 3], int)
    >>> list(iterable)
    [1, 2, 3]

    >>> iterable = check_iterable_over_instances([[1, 2, 3], [1, 2, 3]], list)
    >>> list(iterable)
    [[1, 2, 3], [1, 2, 3]]

    >>> import numpy as np

    >>> iterable = check_iterable_over_instances(np.array([1, 2, 3]), np.int32)
    >>> list(iterable)
    [1, 2, 3]

    NB! In this case the iterable that was passed in does not quite match the returned iterable:

    >>> _ = check_iterable_over_instances(np.array([[1, 2, 3], [1, 2, 3]]), np.ndarray)

    >>> iterable = check_iterable_over_instances({'name': 'Paul', 'surname': 'Bilokon'}, str)
    >>> list(iterable)
    ['name', 'surname']

    >>> check_iterable_over_instances([], int)
    Traceback (most recent call last):
        ...
    AssertionError: Argument is not an iterable over type <class 'int'>

    >>> iterable = check_iterable_over_instances([], int, allow_empty=True)
    >>> check_iterable_over_instances(None, int)
    Traceback (most recent call last):
        ...
    AssertionError: Argument is not an iterable over type <class 'int'>

    >>> iterable = check_iterable_over_instances(None, int, allow_none=True)
    >>> iterable is None
    True
    """
    result, iterable = is_iterable_over_instances(arg, types, allow_none, allow_empty)
    check(result, lambda: message % {'expected': types}, level)
    return iterable

def is_dict(arg, allow_none=False):
    """
    >>> is_dict(3)
    False
    >>> is_dict(3.5)
    False
    >>> is_dict('hi')
    False
    >>> is_dict([1, 2, 3])
    False
    >>> is_dict([[1, 2, 3], [1, 2, 3]])
    False
    >>> import numpy as np
    >>> is_dict(np.array([1, 2, 3]))
    False
    >>> is_dict(np.array([[1, 2, 3], [1, 2, 3]]))
    False
    >>> is_dict({'name': 'Paul', 'surname': 'Bilokon'})
    True
    >>> import collections as col
    >>> is_dict(col.OrderedDict((('name', 'Paul'), ('surname', 'Bilokon'))))
    True
    >>> is_dict(None)
    False
    >>> is_dict(None, allow_none=True)
    True
    """
    return is_instance(arg, dict, allow_none)

def check_dict(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a dict', level=1):
    """
    >>> check_dict(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a dict
    >>> check_dict(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not a dict
    >>> check_dict('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a dict
    >>> check_dict([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a dict
    >>> check_dict([[1, 2, 3], [1, 2, 3]])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[[1, 2, 3], [1, 2, 3]]" of type <class 'list'> is not a dict
    >>> import numpy as np
    >>> check_dict(np.array([1, 2, 3]))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1 2 3]" of type <class 'numpy.ndarray'> is not a dict
    >>> check_dict(np.array([[1, 2, 3], [1, 2, 3]]))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[[1 2 3]
     [1 2 3]]" of type <class 'numpy.ndarray'> is not a dict
    >>> check_dict({'name': 'Paul', 'surname': 'Bilokon'})
    {'name': 'Paul', 'surname': 'Bilokon'}
    >>> import collections as col
    >>> check_dict(col.OrderedDict((('name', 'Paul'), ('surname', 'Bilokon'))))
    OrderedDict([('name', 'Paul'), ('surname', 'Bilokon')])
    >>> check_dict(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a dict
    >>> check_dict(None, allow_none=True)
    """
    check(is_dict(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_some_dict(arg, allow_none=False):
    """
    >>> is_some_dict(3)
    False
    >>> is_some_dict(3.5)
    False
    >>> is_some_dict('hi')
    False
    >>> is_some_dict([1, 2, 3])
    False
    >>> is_some_dict([[1, 2, 3], [1, 2, 3]])
    False
    >>> import numpy as np
    >>> is_some_dict(np.array([1, 2, 3]))
    False
    >>> is_some_dict(np.array([[1, 2, 3], [1, 2, 3]]))
    False
    >>> is_some_dict({'name': 'Paul', 'surname': 'Bilokon'})
    True
    >>> import collections as col
    >>> is_some_dict(col.OrderedDict((('name', 'Paul'), ('surname', 'Bilokon'))))
    True
    >>> is_some_dict(None)
    False
    >>> is_some_dict(None, allow_none=True)
    True
    """
    return (allow_none and arg is None) or hasattr(arg, 'keys')

def check_some_dict(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a dictionary', level=1):
    """
    >>> check_some_dict(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a dictionary
    >>> check_some_dict(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not a dictionary
    >>> check_some_dict('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a dictionary
    >>> check_some_dict([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a dictionary
    >>> check_some_dict([[1, 2, 3], [1, 2, 3]])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[[1, 2, 3], [1, 2, 3]]" of type <class 'list'> is not a dictionary
    >>> import numpy as np
    >>> check_some_dict(np.array([1, 2, 3]))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1 2 3]" of type <class 'numpy.ndarray'> is not a dictionary
    >>> check_some_dict(np.array([[1, 2, 3], [1, 2, 3]]))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[[1 2 3]
     [1 2 3]]" of type <class 'numpy.ndarray'> is not a dictionary
    >>> check_some_dict({'name': 'Paul', 'surname': 'Bilokon'})
    {'name': 'Paul', 'surname': 'Bilokon'}
    >>> import collections as col
    >>> check_some_dict(col.OrderedDict((('name', 'Paul'), ('surname', 'Bilokon'))))
    OrderedDict([('name', 'Paul'), ('surname', 'Bilokon')])
    >>> check_some_dict(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a dictionary
    >>> check_some_dict(None, allow_none=True)
    """
    check(is_some_dict(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_callable(arg, allow_none=False):
    """
    >>> is_callable(3)
    False
    >>> is_callable(3.5)
    False
    >>> is_callable('hi')
    False
    >>> is_callable([1, 2, 3])
    False
    >>> is_callable([[1, 2, 3], [1, 2, 3]])
    False
    >>> import numpy as np
    >>> is_callable(np.array([1, 2, 3]))
    False
    >>> is_callable(np.array([[1, 2, 3], [1, 2, 3]]))
    False
    >>> is_callable({'name': 'Paul', 'surname': 'Bilokon'})
    False
    >>> def my_func():
    ...     return 123
    >>> is_callable(my_func)
    True
    >>> is_callable(lambda x, y: x + y)
    True
    >>> is_callable(None)
    False
    >>> is_callable(None, allow_none=True)
    True
    """
    return (allow_none and arg is None) or (hasattr(arg, '__call__') or isinstance(arg, collections.abc.Callable))

def check_callable(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not callable', level=1):
    """
    >>> check_callable(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not callable
    >>> check_callable(3.5)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3.5" of type <class 'float'> is not callable
    >>> check_callable('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not callable
    >>> check_callable([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not callable
    >>> check_callable([[1, 2, 3], [1, 2, 3]])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[[1, 2, 3], [1, 2, 3]]" of type <class 'list'> is not callable
    >>> import numpy as np
    >>> check_callable(np.array([1, 2, 3]))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1 2 3]" of type <class 'numpy.ndarray'> is not callable
    >>> check_callable(np.array([[1, 2, 3], [1, 2, 3]]))
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[[1 2 3]
     [1 2 3]]" of type <class 'numpy.ndarray'> is not callable
    >>> check_callable({'name': 'Paul', 'surname': 'Bilokon'})
    Traceback (most recent call last):
        ...
    AssertionError: Argument "{'name': 'Paul', 'surname': 'Bilokon'}" of type <class 'dict'> is not callable
    >>> def my_func1():
    ...     return 123
    >>> check_callable(my_func1)    #doctest: +ELLIPSIS
    <function my_func1 at 0x...
    >>> check_callable(lambda x, y: x + y)    #doctest: +ELLIPSIS
    <function <lambda> at 0x...
    >>> check_callable(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not callable
    >>> check_callable(None, allow_none=True)
    """
    check(is_callable(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def is_type(arg, allow_none=False):
    """
    >>> is_type(3)
    False
    >>> is_type('hi')
    False
    >>> is_type([1, 2, 3])
    False
    >>> is_type(int)
    True
    >>> import numpy as np
    >>> is_type(np.ndarray)
    True
    >>> is_type(None)
    False
    >>> is_type(None, allow_none=True)
    True
    """
    return is_instance(arg, type, allow_none)

def check_type(arg, allow_none=False, message='Argument "%(string)s" of type %(actual)s is not a type', level=1):
    """
    >>> check_type(3)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "3" of type <class 'int'> is not a type
    >>> check_type('hi')
    Traceback (most recent call last):
        ...
    AssertionError: Argument "hi" of type <class 'str'> is not a type
    >>> check_type([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError: Argument "[1, 2, 3]" of type <class 'list'> is not a type
    >>> check_type(int)
    <class 'int'>
    >>> import numpy as np
    >>> check_type(np.ndarray)
    <class 'numpy.ndarray'>
    >>> check_type(None)
    Traceback (most recent call last):
        ...
    AssertionError: Argument "None" of type <class 'NoneType'> is not a type
    >>> check_type(None, allow_none=True)
    """
    check(is_type(arg, allow_none), lambda: message % {'string': str(arg), 'actual': type(arg)}, level)
    return arg

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
