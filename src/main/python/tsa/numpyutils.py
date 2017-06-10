import numpy as np

import tsa.checks as checks
import tsa.utils as utils

def isviewof(arg1, arg2):
    if not isinstance(arg1, np.ndarray) or not isinstance(arg2, np.ndarray):
        return False
    return arg1.base is arg2

def areviewsofsame(arg1, arg2):
    if not isinstance(arg1, np.ndarray) or not isinstance(arg2, np.ndarray):
        return False
    return (arg1.base is arg2) or (arg2.base is arg1) or ((arg1.base is arg2.base) and arg1.base is not None)
    
def nrow(arg):
    return np.shape(arg)[0]

def ncol(arg):
    return np.shape(arg)[1]

def toscalar(arg):
    if isinstance(arg, float): return arg
    elif isinstance(arg, np.ndarray): return np.asscalar(arg)
    else: return np.asscalar(np.array(arg))

def tondim1(arg, copy=False):
    r = np.reshape(arg, (np.size(arg),))
    if r.base is arg and copy: r = np.copy(r)
    return r

def tondim2(arg, ndim1tocol=False, copy=False):
    r = np.ndim(arg)
    if r == 0: arg = np.array(((arg,),))
    elif r == 1:
        arg = np.array((arg,))
        if ndim1tocol: arg = arg.T
    return np.array(arg, copy=copy)

def row(*args):
    return tondim2(args, ndim1tocol=False)

def col(*args):
    return tondim2(args, ndim1tocol=True)

def matrix(ncol, *args):
    return np.array(utils.batch(ncol, args))

def matrixof(nrow, ncol, val):
    r = np.empty((nrow, ncol))
    r.fill(val)
    return r

def rowof(n, val):
    return matrixof(1, n, val)

def colof(n, val):
    return matrixof(n, 1, val)

def ndim1of(n, val):
    r = np.empty((n,))
    r.fill(val)
    return r

def makeimmutable(arg):
    checks.checkisinstance(arg, np.ndarray)
    arg.flags.writeable = False
    return arg

def immutablecopyof(arg):
    if isinstance(arg, np.ndarray):
        result = np.copy(arg) if arg.flags.writeable else arg
    else:
        result = np.array(arg)
    result.flags.writeable = False
    return result
        
def lowertosymmetric(a, copy=False):
    a = np.copy(a) if copy else a
    idxs = np.triu_indices_from(a)
    a[idxs] = a[(idxs[1], idxs[0])]
    return a

def uppertosymmetric(a, copy=False):
    a = np.copy(a) if copy else a
    idxs = np.triu_indices_from(a)
    a[(idxs[1], idxs[0])] = a[idxs]
    return a

def vectorised(func):
    func.__dict__['vectorised'] = True
    return func

def isvectorised(func):
    res = False
    if hasattr(func, '__call__'):
        if hasattr(func.__call__, '__dict__'):
            res |= func.__call__.__getattribute__('__dict__').get('vectorised', False)
    if not res and hasattr(func, '__dict__'):
        res = func.__getattribute__('__dict__').get('vectorised', False)
    return res

class NumericError(Exception):
    def __init__(self, message):
        super(NumericError, self).__init__(message)
