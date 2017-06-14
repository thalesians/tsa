import numpy as np
import scipy.linalg as la

import tsa.numpyutils as npu
import tsa.numpychecks as npc

class ItoProcess(object):
    def __init__(self, processdim=1, noisedim=1, drift=None, diffusion=None):
        self.__processdim = processdim
        self.__noisedim = noisedim
        # Note: the brackets around the lambdas below are essential, otherwise the result of the parsing will not be what we need:
        self.__drift = (lambda t, x: npu.rowof(self.__processdim, 0.)) if drift is None else drift
        self.__diffusion = (lambda t, x: npu.matrixof(self.__processdim, self.__noisedim, 0.)) if diffusion is None else diffusion
        
    @property
    def processdim(self):
        return self.__processdim
    
    @property
    def noisedim(self):
        return self.__noisedim
    
    @property
    def drift(self):
        return self.__drift
    
    @property
    def diffusion(self):
        return self.__diffusion
    
    def __str__(self):
        return 'ItoProcess(processdim=%d, noisedim=%d)' % (self.__processdim, self.__noisedim)
    
class SolvedItoProcess(ItoProcess):
    def __init__(self, processdim=1, noisedim=1, drift=None, diffusion=None):
        super(SolvedItoProcess, self).__init__(processdim, noisedim, drift, diffusion)
        
    def propagate(self, time, variate, time0, value0, state0=None):
        raise NotImplementedError()
    
    def __str__(self):
        return 'SolvedItoProcess(processdim=%d, noisedim=%d)' % (self.__processdim, self.__noisedim)

# TODO To be implemented
class MarkovProcess(object):
    def __init__(self, processdim, noisedim):
        self.__processdim = processdim
        self.__noisedim = noisedim
        
    def propagatevalue(self, time, value, timedelta, variatedelta):
        raise NotImplementedError()
    
    def propagatedistribution(self):
        pass
    
# TODO To be implemented
class KalmanProcess(object):
    def __init__(self):
        pass
    
class WienerProcess(SolvedItoProcess):
    def __init__(self, mean=None, vol=None):
        if mean is None and vol is None:
            mean = 0.; vol = 1.
            
        self.__mean, self.__vol = None, None
            
        if mean is not None:
            self.__mean = npu.tondim2(mean, ndim1tocol=True, copy=True)
            processdim = npu.nrow(self.__mean)
        if vol is not None:
            self.__vol = npu.tondim2(vol, ndim1tocol=True, copy=True)
            processdim = npu.nrow(self.__vol)
            
        if self.__mean is None: self.__mean = npu.colof(processdim, 0.)
        if self.__vol is None: self.__vol = np.eye(processdim)
            
        npc.checkcol(self.__mean)
        npc.checknrow(self.__mean, processdim)
        npc.checknrow(self.__vol, processdim)
        
        noisedim = npu.ncol(self.__vol)
        
        npu.makeimmutable(self.__mean)
        npu.makeimmutable(self.__vol)
        
        super(WienerProcess, self).__init__(processdim, noisedim, lambda t, x: self.__mean, lambda t, x: self.__vol)
        
    @staticmethod    
    def makevol2d(sd1, sd2, cor):
        return np.array([[sd1, 0.], [cor*sd2, np.sqrt(1. - cor*cor)*sd2]])
    
    @staticmethod
    def makevolfromcov(cov):
        return np.linalg.cholesky(cov)
    
    @staticmethod
    def create2d(mean1, mean2, sd1, sd2, cor):
        return WienerProcess(npu.col(mean1, mean2), WienerProcess.makevol2d(sd1, sd2, cor))
    
    @staticmethod
    def createfromcov(mean, cov):
        return WienerProcess(mean, WienerProcess.makevolfromcov(cov))
    
    @property
    def mean(self):
        return self.__mean
    
    @property
    def vol(self):
        return self.__vol
    
    def propagate(self, time, variate, time0, value0, state0=None):
        if time == time0: return npu.tondim2(value0, ndim1tocol=True, copy=True)
        value0 = npu.tondim2(value0, ndim1tocol=True, copy=False)
        variate = npu.tondim2(variate, ndim1tocol=True, copy=False)
        timedelta = time - time0
        return value0 + self.__mean * timedelta + np.dot(self.__vol, np.sqrt(timedelta) * variate)

    def __str__(self):
        return 'WienerProcess(processdim=%d, noisedim=%d, mean=%s, vol=%s)' % (self.processdim, self.noisedim, str(self.__mean), str(self.__vol))

# TODO Add the propagate method
class OrnsteinUhlenbeckProcess(ItoProcess):
    def __init__(self, transition=None, mean=None, vol=None):
        if transition is None and mean is None and vol is None:
            transition = 1.; mean = 0.; vol = 1.
            
        self.__transition, self.__mean, self.__vol = None, None, None
            
        if transition is not None:
            self.__transition = npu.tondim2(transition, ndim1tocol=True, copy=True)
            processdim = npu.nrow(self.__transition)
        if mean is not None:
            self.__mean = npu.tondim2(mean, ndim1tocol=True, copy=True)
            processdim = npu.nrow(self.__mean)
        if vol is not None:
            self.__vol = npu.tondim2(vol, ndim1tocol=True, copy=True)
            processdim = npu.nrow(self.__vol)
        
        if self.__transition is None: self.__transition = np.eye(processdim)
        if self.__mean is None: self.__mean = npu.colof(processdim, 0.)
        if self.__vol is None: self.__vol = np.eye(processdim)
        
        npc.checksquare(self.__transition)
        npc.checknrow(self.__transition, processdim)
        npc.checkcol(self.__mean)
        npc.checknrow(self.__mean, processdim)
        npc.checknrow(self.__vol, processdim)
        
        noisedim = npu.ncol(self.__vol)
        
        self.__transitionx2 = npu.kronsum(self.__transition, self.__transition)
        self.__transitionx2inverse = np.linalg.inv(self.__transitionx2)
        self.__cov = np.dot(self.__vol, self.__vol.T)
        self.__covvec = npu.vec(self.__cov)
        
        self.__cachedmeanreversionfactor = None
        self.__cachedmeanreversionfactortimedelta = None
        self.__cachedmeanreversionfactorsquared = None
        self.__cachedmeanreversionfactorsquaredtimedelta = None
        
        npu.makeimmutable(self.__transition)
        npu.makeimmutable(self.__transitionx2)
        npu.makeimmutable(self.__transitionx2inverse)
        npu.makeimmutable(self.__mean)
        npu.makeimmutable(self.__vol)
        npu.makeimmutable(self.__cov)
        npu.makeimmutable(self.__covvec)
        
        super(OrnsteinUhlenbeckProcess, self).__init__(processdim, noisedim, lambda t, x: -np.dot(self.__transition, x - self.__mean), lambda t, x: self.__vol)
        
    @property
    def transition(self):
        return self.__transition
        
    @property
    def mean(self):
        return self.__mean
    
    @property
    def vol(self):
        return self.__vol
    
    def meanreversionfactor(self, timedelta):
        if self.__cachedmeanreversionfactorsquaredtimedelta is None or self.__cachedmeanreversionfactortimedelta != timedelta:
            self.__cachedmeanreversionfactorsquaredtimedelta = timedelta
            self.__cachedmeanreversionfactor = la.expm(self.__transition * (-timedelta))
        return self.__cachedmeanreversionfactor
    
    def meanreversionfactorsquared(self, timedelta):
        if self.__cachedmeanreversionfactorsquaredtimedelta is None or self.__cachedmeanreversionfactorsquaredtimedelta != timedelta:
            self.__cachedmeanreversionfactorsquaredtimedelta = timedelta
            self.__cachedmeanreversionfactorsquared = la.expm(self.__transitionratex2 * (-timedelta))
        return self.__cachedmeanreversionfactorsquared
        
    def noisecovariance(self, time, time0):
        timedelta = time - time0
        mrfsquared = self.meanreversionfactorsquared(timedelta)
        eyeminusmrfsquared = np.eye(self.processdim) - mrfsquared
        return npu.unvec(np.dot(np.dot(self.__transitionx2inverse, eyeminusmrfsquared), self.__covvec), self.processdim)
        
    def propagate(self, time, variate, time0, value0, state0=None):
        if time == time0: return npu.tondim2(value0, ndim1tocol=True, copy=True)
        value0 = npu.tondim2(value0, ndim1tocol=True, copy=False)
        variate = npu.tondim2(variate, ndim2tocol=True, copy=False)
        timedelta = time - time0
        mrf = self.meanreversionfactor(timedelta)
        eyeminusmrf = np.eye(self.processdim) - mrf
        m = np.dot(mrf, value0) + np.dot(eyeminusmrf, self.__mean)
        c = self.noisecovariance(time, time0)
        return m + np.dot(np.linalg.cholesky(c), variate)
        
    def __str__(self):
        return 'OrnsteinUhlenbeckProcess(processdim=%d, noisedim=%d, transition=%s, mean=%s, vol=%s)' % (self.processdim, self.noisedim, str(self.__transition), str(self.__mean), str(self.__vol))
    