import numpy as np

from thalesians.tsa.checks import check
import thalesians.tsa.numpyutils as npu

def is_size(arg, size):
    return np.size(arg) == size

def check_size(arg, size, message='Unexpected size: actual=%(actual)d, expected=%(expected)d', level=1):
    n = np.size(arg)
    check(n == size, message=lambda: message % {'actual': n, 'expected': size}, level=level)
    return arg

def is_shape(arg, shape):
    return np.shape(arg) == shape

def check_shape(arg, shape, message='Unexpected shape: actual=%(actual)s, expected=%(expected)s', level=1):
    s = np.shape(arg)
    check(s == shape, message=lambda: message % {'actual': s, 'expected': shape}, level=level)
    return arg

def is_same_shape(arg1, arg2):
    return np.shape(arg1) == np.shape(arg2)

def check_same_shape(arg1, arg2, message='Shapes differ: %(shape1)s vs %(shape2)s', level=1):
    s1 = np.shape(arg1); s2 = np.shape(arg2)
    check(s1 == s2, message=lambda: message % {'shape1': s1, 'shape2': s2}, level=level)
    return s1

def is_ndim_1(arg):
    return len(np.shape(arg)) == 1

def check_ndim_1(arg, message='Not a one-dimensional array; number of dimensions: %(actual)d', level=1):
    n = np.ndim(arg)
    check(n == 1, message=lambda: message % {'actual': n}, level=level)
    return arg

def is_square(arg):
    if np.size(arg) == 1: return True
    s = np.shape(arg)
    return len(s) == 2 and s[0] == s[1]

def check_square(arg, message='Matrix is not square: %(actual)s', level=1):
    if np.size(arg) > 1:
        s = np.shape(arg)
        check(len(s) == 2 and s[0] == s[1], message=lambda: message % {'actual': s}, level=level)
    return arg

def is_row(arg):
    s = np.shape(arg)
    return len(s) == 2 and s[0] == 1

def check_row(arg, message='Matrix is not a row: %(actual)s', level=1):
    s = np.shape(arg)
    check(len(s) == 2 and s[0] == 1, message=lambda: message % {'actual': s}, level=level)
    return arg

def is_col(arg):
    s = np.shape(arg)
    return len(s) == 2 and s[1] == 1
    
def check_col(arg, message='Matrix is not a column: %(actual)s', level=1):
    s = np.shape(arg)
    check(len(s) == 2 and s[1] == 1, message=lambda: message % {'actual': s}, level=level)
    return arg

def is_nrow(arg, nrow):
    return npu.nrow(arg) == nrow

def check_nrow(arg, nrow, message='Unexpected number of rows: actual=%(actual)d, expected=%(expected)d', level=1):
    n = npu.nrow(arg)
    check(n == nrow, message=lambda: message % {'actual': n, 'expected': nrow}, level=level)
    return arg

def is_ncol(arg, ncol):
    return npu.ncol(arg) == ncol

def check_ncol(arg, ncol, message='Unexpected number of columns: actual=%(actual)d, expected=%(expected)d', level=1):
    n = npu.ncol(arg)
    check(n == ncol, message=lambda: message % {'actual': n, 'expected': ncol}, level=level)
    return arg
