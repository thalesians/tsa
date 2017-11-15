import numpy as np

import thalesians.tsa.numpychecks as npc
import thalesians.tsa.numpyutils as npu

class Distr(object):
    def __init__(self):
        pass

    @property
    def dim(self):
        raise NotImplementedError()
    
    @property
    def mean(self):
        raise NotImplementedError()
    
    @property
    def cov(self):
        raise NotImplementedError()
    
class NormalDistr(Distr):
    def __init__(self, mean=None, cov=None, vol=None, dim=None, copy=True):
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
        
        super(NormalDistr, self).__init__()
        
    @staticmethod
    def create_dirac_delta(value):
        dim = np.size(value)
        return NormalDistr(mean=value, cov=np.zeros((dim, dim)))

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
        if isinstance(other, self.__class__):
            if self._mean != other._mean: return False
            if self._cov is None:
                return self._vol == other.vol
            else:
                return self._cov == other.cov
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return 'Normal(mean=%s, cov=%s)' % (str(self._mean), str(self._cov))
    