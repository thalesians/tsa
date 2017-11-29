import numpy as np

import thalesians.tsa.numpychecks as npc
import thalesians.tsa.numpyutils as npu
from thalesians.tsa.strings import ToStringHelper

class Distr(object):
    def __init__(self):
        self._to_string_helper_Distr = None
        self._str_Distr = None

    @property
    def dim(self):
        raise NotImplementedError()
    
    @property
    def mean(self):
        raise NotImplementedError()
    
    @property
    def cov(self):
        raise NotImplementedError()
    
    def to_string_helper(self):
        if self._to_string_helper_Distr is None:
            self._to_string_helper_Distr = ToStringHelper(self)
        return self._to_string_helper_Distr
    
    def __str__(self):
        if self._str_Distr is None: self._str_Distr = self.to_string_helper().to_string()
        return self._str_Distr
    
class NormalDistr(Distr):
    def __init__(self, mean=None, cov=None, vol=None, dim=None, copy=True):
        if mean is not None and dim is not None and np.size(mean) == 1:
            mean = npu.col_of(dim, npu.to_scalar(mean))
        
        if mean is None and vol is None and cov is None:
            self._dim = 1 if dim is None else dim
            mean = npu.col_of(self._dim, 0.)
            cov = np.eye(self._dim)
            vol = np.eye(self._dim)
            
        self._dim, self._mean, self._vol, self._cov = None, None, None, None
        
        # TODO We don't currently check whether cov and vol are consistent, i.e. that cov = np.dot(vol, vol.T) -- should we?
        
        if mean is not None:
            self._mean = npu.to_ndim_2(mean, ndim_1_to_col=True, copy=copy)
            self._dim = npu.nrow(self._mean)
        if cov is not None:
            self._cov = npu.to_ndim_2(cov, ndim_1_to_col=True, copy=copy)
            self._dim = npu.nrow(self._cov)
        if vol is not None:
            self._vol = npu.to_ndim_2(vol, ndim_1_to_col=True, copy=copy)
            self._dim = npu.nrow(self._vol)
            
        if self._mean is None: self._mean = npu.col_of(self._dim, 0.)
        if self._cov is None and self._vol is None:
            self._cov = np.eye(self._dim)
            self._vol = np.eye(self._dim)
            
        npc.check_col(self._mean)
        npc.check_nrow(self._mean, self._dim)
        if self._cov is not None:
            npc.check_nrow(self._cov, self._dim)
            npc.check_square(self._cov)
        if self._vol is not None:
            npc.check_nrow(self._vol, self._dim)
            
        npu.make_immutable(self._mean)
        if self._cov is not None: npu.make_immutable(self._cov)
        if self._vol is not None: npu.make_immutable(self._vol)
        
        self._to_string_helper_NormalDistr = None
        self._str_NormalDistr = None
        
        super(NormalDistr, self).__init__()
        
    @staticmethod
    def make_cov_2d(sd1, sd2, cor):
        offdiag = cor*sd1*sd2
        return np.array([[sd1*sd1, offdiag], [offdiag, sd2*sd2]])
    
    @staticmethod
    def make_vol_2d(sd1, sd2, cor):
        return np.array([[sd1, 0.], [cor*sd2, np.sqrt(1. - cor*cor)*sd2]])
    
    @staticmethod
    def make_vol_from_cov(cov):
        cov = npu.to_ndim_2(cov, ndim_1_to_col=True, copy=False)
        return np.linalg.cholesky(cov)
    
    @property
    def dim(self):
        return self._dim
    
    @property
    def mean(self):
        return self._mean
    
    @property
    def cov(self):
        if self._cov is None:
            self._cov = np.dot(self._vol, self._vol.T)
        return self._cov
    
    @property
    def vol(self):
        if self._vol is None:
            self._vol = NormalDistr.make_vol_from_cov(self._cov)
        return self._vol
    
    def __eq__(self, other):
        if isinstance(other, NormalDistr):
            if self.dim != other.dim: return False
            if not np.array_equal(self.mean, other.mean): return False
            return np.array_equal(self.cov, other.cov)
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def to_string_helper(self):
        if self._to_string_helper_NormalDistr is None:
            self._to_string_helper_NormalDistr = super().to_string_helper() \
                    .set_type(self) \
                    .add('mean', self._mean) \
                    .add('cov', self._cov)
        return self._to_string_helper_NormalDistr 
    
    def __str__(self):
        if self._str_NormalDistr is None: self._str_NormalDistr = self.to_string_helper().to_string()
        return self._str_NormalDistr
    
    def __repr__(self):
        return str(self)

class DiracDelta(NormalDistr):
    def __init__(self, mean=None, dim=None, copy=True):
        if mean is not None and dim is not None and np.size(mean) == 1:
            mean = npu.col_of(dim, npu.to_scalar(mean))
        
        if mean is None:
            dim = 1 if dim is None else dim
            mean = npu.col_of(dim, 0.)
            

        self._mean = npu.to_ndim_2(mean, ndim_1_to_col=True, copy=copy)
        if dim is None: dim = npu.nrow(self._mean)
        self._dim = dim

        npc.check_col(self._mean)
        npc.check_nrow(self._mean, self._dim)
            
        npu.make_immutable(self._mean)
        
        self._zero_cov = None
        
        self._to_string_helper_DiracDelta = None
        self._str_DiracDelta = None
        
    @staticmethod
    def create(value=None, dim=None):
        return DiracDelta(value, dim)

    @property
    def cov(self):
        if self._zero_cov is None:
            self._zero_cov = np.zeros((self._dim, self._dim))
        return self._zero_cov
    
    @property
    def vol(self):
        return self.cov
    
    def to_string_helper(self):
        if self._to_string_helper_DiracDelta is None:
            self._to_string_helper_DiracDelta = ToStringHelper(self).add('mean', self._mean)
        return self._to_string_helper_DiracDelta 
    
    def __str__(self):
        if self._str_DiracDelta is None: self._str_DiracDelta = self.to_string_helper().to_string()
        return self._str_DiracDelta
    
    def __repr__(self):
        return str(self)
