import numpy as np

import thalesians.tsa.numpyutils as npu
import thalesians.tsa.utils as utils

def make_cov_2d(sd1, sd2, cor):
    offdiag = cor*sd1*sd2
    return np.array([[sd1*sd1, offdiag], [offdiag, sd2*sd2]])

def make_vol_2d(sd1, sd2, cor):
    return np.array([[sd1, 0.], [cor*sd2, np.sqrt(1. - cor*cor)*sd2]])

def cov_to_vol(cov):
    cov = npu.to_ndim_2(cov, ndim_1_to_col=True, copy=False)
    return np.linalg.cholesky(cov)
    
def cor_to_cov(cors, vars=None, sds=None, copy=True):  # @ReservedAssignment
    assert (vars is None and sds is not None) or (vars is not None and sds is None)
    sds = np.sqrt(vars) if vars is not None else sds
    if isinstance(cors, (utils.DiagonalArray, utils.SubdiagonalArray)):
        cors = cors.tonumpyarray()
    cors = npu.to_ndim_2(cors, copy=copy)
    dim = len(vars)
    assert dim == np.shape(cors)[0] and dim == np.shape(cors)[1]
    np.fill_diagonal(cors, 1.)
    for i in range(dim):
        cors[i,:] = sds[i] * cors[i,:]
        cors[:,i] = sds[i] * cors[:,i]
    npu.lower_to_symmetric(cors, copy=False)
    return cors

def cholesky_sqrt_2d(sd1, sd2, cor):
    return np.array(((sd1, 0.), (sd2 * cor, sd2 * np.sqrt(1. - cor * cor))))

class OnlineStatsCalculator(object):
    def __init__(self, zero=0.0):
        self.reset(zero)
        
    def reset(self, zero):
        self.__n = 0
        self.__sum = zero
        self.__mean = zero
        self.__mean_sq = zero
        self.__M2 = zero
    
    @property
    def count(self):
        return self.__n
    
    @property
    def sum(self):
        return self.__sum

    @property    
    def mean(self):
        return self.__mean

    @property
    def mean_sq(self):
        return self.__mean_sq
    
    @property
    def rms(self):
        return np.sqrt(self.mean_sq)

    @property    
    def var_n(self):
        return self.__M2 / self.__n
    
    @property
    def var(self):
        return self.__M2 / (self.__n - 1)

    @property    
    def sd(self):
        return np.sqrt(self.var)

    @property    
    def sd_n(self):
        return np.sqrt(self.var_n)
    
    def add(self, x):
        self.__n += 1
        self.__sum += x
        delta = x - self.__mean
        self.__mean += delta / self.__n
        deltasq = x * x - self.__mean_sq
        self.__mean_sq += deltasq / self.__n
        if self.__n > 1:
            self.__M2 += delta * (x - self.__mean)

    def add_all(self, xs):
        for x in xs: self.add(x)
        