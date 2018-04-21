import numpy as np

import thalesians.tsa.numpychecks as npc
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.stats as stats
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
    
class WideSenseDistr(Distr):
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
        
        self._to_string_helper_WideSenseDistr = None
        self._str_WideSenseDistr = None
        
        super(WideSenseDistr, self).__init__()
        
    @property
    def dim(self):
        return self._dim
    
    @property
    def mean(self):
        return self._mean
    
    @property
    def cov(self):
        if self._cov is None:
            self._cov = stats.vol_to_cov(self._vol)
        return self._cov
    
    @property
    def vol(self):
        if self._vol is None:
            self._vol = stats.cov_to_vol(self._cov)
        return self._vol
    
    def __eq__(self, other):
        if isinstance(other, WideSenseDistr):
            if self.dim != other.dim: return False
            if not np.array_equal(self.mean, other.mean): return False
            return np.array_equal(self.cov, other.cov)
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def to_string_helper(self):
        if self._to_string_helper_WideSenseDistr is None:
            self._to_string_helper_WideSenseDistr = super().to_string_helper() \
                    .set_type(self) \
                    .add('mean', self._mean) \
                    .add('cov', self._cov)
        return self._to_string_helper_WideSenseDistr 
    
    def __str__(self):
        if self._str_WideSenseDistr is None: self._str_WideSenseDistr = self.to_string_helper().to_string()
        return self._str_WideSenseDistr
    
    def __repr__(self):
        return str(self)

class NormalDistr(WideSenseDistr):
    def __init__(self, mean=None, cov=None, vol=None, dim=None, copy=True):
        super(NormalDistr, self).__init__(mean, cov, vol, dim, copy)

    @staticmethod
    def approximate(distr, copy=True):
        if isinstance(distr, NormalDistr) and not copy: return distr
        return NormalDistr(distr.mean, distr.cov, None, distr.dim, copy)

    def __eq__(self, other):
        if isinstance(other, NormalDistr):
            if self.dim != other.dim: return False
            if not np.array_equal(self.mean, other.mean): return False
            return np.array_equal(self.cov, other.cov)
        return False

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

class LogNormalDistr(WideSenseDistr):
    def __init__(self, mean_of_log=None, cov_of_log=None, vol_of_log=None, dim=None, copy=True):
        if mean_of_log is not None and dim is not None and np.size(mean_of_log) == 1:
            mean_of_log = npu.col_of(dim, npu.to_scalar(mean_of_log))
        
        if mean_of_log is None and vol_of_log is None and cov_of_log is None:
            self._dim = 1 if dim is None else dim
            mean_of_log = npu.col_of(self._dim, 0.)
            cov_of_log = np.eye(self._dim)
            vol_of_log = np.eye(self._dim)
            
        self._dim, self._mean_of_log, self._vol_of_log, self._cov_of_log = None, None, None, None
        
        # TODO We don't currently check whether cov_of_log and vol_of_log are consistent, i.e. that cov_of_log = np.dot(vol_of_log, vol_of_log.T) -- should we?
        
        if mean_of_log is not None:
            self._mean_of_log = npu.to_ndim_2(mean_of_log, ndim_1_to_col=True, copy=copy)
            self._dim = npu.nrow(self._mean_of_log)
        if cov_of_log is not None:
            self._cov_of_log = npu.to_ndim_2(cov_of_log, ndim_1_to_col=True, copy=copy)
            self._dim = npu.nrow(self._cov_of_log)
        if vol_of_log is not None:
            self._vol_of_log = npu.to_ndim_2(vol_of_log, ndim_1_to_col=True, copy=copy)
            self._dim = npu.nrow(self._vol_of_log)
        
        if self._mean_of_log is None: self._mean_of_log = npu.col_of(self._dim, 0.)
        if self._cov_of_log is None and self._vol_of_log is None:
            self._cov_of_log = np.eye(self._dim)
            self._vol_of_log = np.eye(self._dim)
        npc.check_col(self._mean_of_log)
        npc.check_nrow(self._mean_of_log, self._dim)
        if self._cov_of_log is not None:
            npc.check_nrow(self._cov_of_log, self._dim)
            npc.check_square(self._cov_of_log)
        if self._vol_of_log is not None:
            npc.check_nrow(self._vol_of_log, self._dim)

        if self._cov_of_log is None: self._cov_of_log = stats.vol_to_cov(self._vol)
        if self._vol_of_log is None: self._vol_of_log = stats.cov_to_vol(self._cov)
            
        npu.make_immutable(self._mean_of_log)
        npu.make_immutable(self._cov_of_log)
        npu.make_immutable(self._vol_of_log)

        mean = np.exp(self._mean_of_log + .5 * npu.col(*[self._cov_of_log[i,i] for i in range(dim)]))
        cov = np.array([[np.exp(self._mean_of_log[i] + self._mean_of_log[j] + .5 * (self._cov_of_log[i,i] + self._cov_of_log[j,j])) * (np.exp(self._cov_of_log[i,j]) - 1.) for j in range(dim)] for i in range(dim)])
        
        self._to_string_helper_LogNormalDistr = None
        self._str_LogNormalDistr = None
        
        super(LogNormalDistr, self).__init__(mean, cov, vol, dim, copy)

    @property
    def mean_of_log(self):
        return self._mean_of_log
    
    @property
    def vol_of_log(self):
        return self._vol_of_log

    @property
    def cov_of_log(self):
        return self._cov_of_log

    def __eq__(self, other):
        if isinstance(other, LogNormalDistr):
            if self.dim != other.dim: return False
            if not np.array_equal(self.mean_of_log, other.mean_of_log): return False
            return np.array_equal(self.cov_of_log, other.cov_of_log)
        return False
    
    def to_string_helper(self):
        if self._to_string_helper_LogNormalDistr is None:
            self._to_string_helper_LogNormalDistr = super().to_string_helper() \
                    .set_type(self) \
                    .add('mean_of_log', self._mean_of_log) \
                    .add('cov_of_log', self._cov_of_log)
        return self._to_string_helper_LogNormalDistr
    
    def __str__(self):
        if self._str_LogNormalDistr is None: self._str_LogNormalDistr = self.to_string_helper().to_string()
        return self._str_LogNormalDistr
