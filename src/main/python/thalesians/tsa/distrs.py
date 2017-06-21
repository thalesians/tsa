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
            self.__dim = 1 if dim is None else dim
            mean = npu.colof(self.__dim, 0.)
            cov = np.eye(self.__dim)
            vol = np.eye(self.__dim)
            
        self.__dim, self.__mean, self.__vol, self.__cov = None, None, None, None
        
        # TODO We don't currently check whether cov and vol are consistent, i.e. that cov = np.dot(vol, vol.T) -- should we?
        
        if mean is not None:
            self.__mean = npu.tondim2(mean, ndim1tocol=True, copy=copy)
            self.__dim = npu.nrow(self.__mean)
        if cov is not None:
            self.__cov = npu.tondim2(cov, ndim1tocol=True, copy=copy)
            self.__dim = npu.nrow(self.__cov)
        if vol is not None:
            self.__vol = npu.tondim2(vol, ndim1tocol=True, copy=copy)
            self.__dim = npu.nrow(self.__vol)
            
        if self.__mean is None: self.__mean = npu.colof(self.__dim, 0.)
        if self.__cov is None and self.__vol is None:
            self.__cov = np.eye(self.__dim)
            self.__vol = np.eye(self.__dim)
            
        npc.checkcol(self.__mean)
        npc.checknrow(self.__mean, self.__dim)
        if self.__cov is not None:
            npc.checknrow(self.__cov, self.__dim)
            npc.checksquare(self.__cov)
        if self.__vol is not None:
            npc.checknrow(self.__vol, self.__dim)
            
        npu.makeimmutable(self.__mean)
        if self.__cov is not None: npu.makeimmutable(self.__cov)
        if self.__vol is not None: npu.makeimmutable(self.__vol)
        
        super(NormalDistr, self).__init__()
        
    @staticmethod
    def creatediracdelta(value):
        dim = np.size(value)
        return NormalDistr(mean=value, cov=np.zeros((dim, dim)))

    @staticmethod
    def makecov2d(sd1, sd2, cor):
        offdiag = cor*sd1*sd2
        return np.array([[sd1*sd1, offdiag], [offdiag, sd2*sd2]])
    
    @staticmethod
    def makevol2d(sd1, sd2, cor):
        return np.array([[sd1, 0.], [cor*sd2, np.sqrt(1. - cor*cor)*sd2]])
    
    @staticmethod
    def makevolfromcov(cov):
        cov = npu.tondim2(cov, ndim1tocol=True, copy=False)
        return np.linalg.cholesky(cov)
    
    @property
    def dim(self):
        return self.__dim
    
    @property
    def mean(self):
        return self.__mean
    
    @property
    def cov(self):
        if self.__cov is None:
            self.__cov = np.dot(self.__vol, self.__vol.T)
        return self.__cov
    
    @property
    def vol(self):
        if self.__vol is None:
            self.__vol = NormalDistr.makevolfromcov(self.__cov)
        return self.__vol
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.__mean != other.__mean: return False
            if self.__cov is None:
                return self.__vol == other.vol
            else:
                return self.__cov == other.cov
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return 'Normal(mean=%s, cov=%s)' % (str(self.__mean), str(self.__cov))
    