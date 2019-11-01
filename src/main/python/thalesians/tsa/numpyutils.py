import datetime as dt
import warnings

import numpy as np

import thalesians.tsa.checks as checks
import thalesians.tsa.utils as utils

def init_warnings():
    np.warnings.filterwarnings('ignore', message='Mean of empty slice')
    np.warnings.filterwarnings('ignore', message='All-NaN axis encountered')
    warnings.filterwarnings('ignore', message='Warning: converting a masked element to nan.')

def apply(func, arg, dtype='float64'):
    result = np.empty(np.shape(arg), dtype=dtype)
    result.flat[:] = [func(x) for x in arg.flat[:]]
    return result

def sign(arg):
    if isinstance(arg, dt.timedelta):
        arg = arg.total_seconds()
    elif checks.is_numpy_array(arg) and arg.dtype == object and np.size(arg) > 0 and isinstance(arg.item(0), dt.timedelta):
        arg = np.vectorize(lambda x: x.total_seconds())(arg)
    return np.sign(arg)

def is_view_of(arg1, arg2):
    if not checks.is_numpy_array(arg1) or not checks.is_numpy_array(arg2):
        return False
    return arg1.base is arg2

def are_views_of_same(arg1, arg2):
    if not checks.is_numpy_array(arg1) or not checks.is_numpy_array(arg2):
        return False
    return (arg1.base is arg2) or (arg2.base is arg1) or ((arg1.base is arg2.base) and arg1.base is not None)
    
def nrow(arg):
    return np.shape(arg)[0]

def ncol(arg):
    return np.shape(arg)[1]

def to_scalar(arg, raise_value_error=True):
    try:
        if checks.is_float(arg): return arg
        elif checks.is_numpy_array(arg): return np.asscalar(arg)
        else: return np.asscalar(np.array(arg))
    except:
        if raise_value_error: raise
        return arg

def to_ndim_1(arg, copy=False):
    r = np.reshape(arg, (np.size(arg),))
    if r.base is arg and copy: r = np.copy(r)
    return r

def to_ndim_2(arg, ndim_1_to_col=False, copy=False):
    r = np.ndim(arg)
    if r == 0: arg = np.array(((arg,),))
    elif r == 1:
        arg = np.array((arg,))
        if ndim_1_to_col: arg = arg.T
    return np.array(arg, copy=copy)

def row(*args):
    return to_ndim_2(args, ndim_1_to_col=False)

def col(*args):
    return to_ndim_2(args, ndim_1_to_col=True)

def matrix(ncol, *args):
    return np.array(utils.batch(ncol, args))

def matrix_of(nrow, ncol, val):
    r = np.empty((nrow, ncol))
    r.fill(val)
    return r

def row_of(n, val):
    return matrix_of(1, n, val)

def col_of(n, val):
    return matrix_of(n, 1, val)

def ndim_1_of(n, val):
    r = np.empty((n,))
    r.fill(val)
    return r

def make_immutable(arg, allow_none=False):
    if allow_none and arg is None: return None
    checks.check_numpy_array(arg)
    arg.flags.writeable = False
    return arg

def immutable_copy_of(arg):
    if checks.is_numpy_array(arg):
        result = np.copy(arg) if arg.flags.writeable else arg
    else:
        result = np.array(arg)
    result.flags.writeable = False
    return result
        
def lower_to_symmetric(a, copy=False):
    a = np.copy(a) if copy else a
    idxs = np.triu_indices_from(a)
    a[idxs] = a[(idxs[1], idxs[0])]
    return a

def upper_to_symmetric(a, copy=False):
    a = np.copy(a) if copy else a
    idxs = np.triu_indices_from(a)
    a[(idxs[1], idxs[0])] = a[idxs]
    return a

def kron_sum(arg1, arg2):
    return np.kron(arg1, np.eye(nrow(arg2))) + np.kron(np.eye(nrow(arg1)), arg2)

def vec(arg):
    return np.resize(to_ndim_2(arg, ndim_1_to_col=True, copy=False).T, (np.size(arg), 1))

def unvec(arg, nrow):
    return np.resize(to_ndim_1(arg, copy=False), (np.size(arg) // nrow, nrow)).T

def vectorised(func):
    func.__dict__['vectorised'] = True
    return func

def is_vectorised(func):
    res = False
    if hasattr(func, '__call__'):
        if hasattr(func.__call__, '__dict__'):
            res |= func.__call__.__getattribute__('__dict__').get('vectorised', False)
    if not res and hasattr(func, '__dict__'):
        res = func.__getattribute__('__dict__').get('vectorised', False)
    return res
