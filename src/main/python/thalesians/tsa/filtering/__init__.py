import warnings

import numpy as np
from scipy.linalg import block_diag

import thalesians.tsa.checks as checks
from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.processes as proc
import thalesians.tsa.utils as utils

class PredictedObs(object):
    def __init__(self, time, distr, crosscov):
        self.__time = time
        self.__distr = distr
        self.__crosscov = crosscov
    
    @property
    def time(self):
        return self.__time
    
    @property
    def distr(self):
        return self.__distr
    
    @property
    def crosscov(self):
        return self.__crosscov
    
    def __str__(self):
        return 'PredictedObs(time=%s, distr=%s, crosscov=%s)' % (self.__time, self.__distr, self.__crosscov)
    
class ObsResult(object):
    def __init__(self, time, obsdistr, accepted, predictedobs, innovdistr, loglikelihood):
        self.__time = time
        self.__obsdistr = obsdistr
        self.__accepted = accepted
        self.__predictedobs = predictedobs
        self.__innovdistr = innovdistr
        self.__loglikelihood = loglikelihood
        
    @property
    def time(self):
        return self.__time
    
    @property
    def obsdistr(self):
        return self.__obsdistr
    
    @property
    def accepted(self):
        return self.__accepted
    
    @property
    def predictedobs(self):
        return self.__predictedobs
    
    @property
    def innovdistr(self):
        return self.__innovdistr
    
    @property
    def loglikelihood(self):
        return self.__loglikelihood
    
    def __str__(self):
        return 'ObsResult(time=%s, obsdistr=%s, accepted=%s, predictedobs=%s, innovdistr=%s, loglikelihood=%f)' % (self.__time, self.__obsdistr, self.__accepted, self.__predictedobs, self.__innovdistr, self.__loglikelihood)
    
class ObsModel(object):
    def predictobs(self, time, statedistr):
        pass
    
class KalmanFilterObsModel(ObsModel):
    def __init__(self, obsmatrix):
        self.__obsmatrix = obsmatrix
    
    @staticmethod
    def createfromcompoundobsmatrix(obsmatrix):
        obsmatrix = npu.tondim2(obsmatrix, ndim1tocol=False, copy=True)
        return KalmanFilterObsModel(obsmatrix)
    
    def predictobs(self, time, statedistr):
        obsmean = np.dot(self.__obsmatrix, statedistr.mean)
        crosscov = np.dot(self.__obsmatrix, statedistr.cov)
        obscov = np.dot(crosscov, self.__obsmatrix.T)
        return PredictedObs(time, N(mean=obsmean, cov=obscov), crosscov)

class Observable(object):
    def predict(self, time):
        raise NotImplementedError()
        
    def observe(self, time, obs, obscov):
        raise NotImplementedError()
    
class KalmanFilter(object):
    LN_2PI = np.log(2. * np.pi)
    
    def __init__(self, time, statedistr, process):
        if not checks.isiterable(process): process = (process,)
        checks.checkinstance(statedistr, N)
        process = checks.checkiterableoverinstances(process, proc.MarkovProcess)
        self.__time = time
        self._statedistr = statedistr
        self._processes = tuple(process)

    class KalmanObservable(Observable):
        def __init__(self, filter, obsmodel, observedprocesses):
            if not checks.isiterable(observedprocesses): observedprocesses = [observedprocesses]
            observedprocesses = checks.checkiterableoverinstances(observedprocesses, proc.MarkovProcess)
            self.__filter = filter
            self.__obsmodel = obsmodel
            self.__statemeanrects = []
            self.__statecovrects = []
            for op in observedprocesses:
                matched = False
                row = 0
                for ap in self.__filter._processes:
                    processdim = ap.processdim
                    if op is ap:
                        matched = True
                        self.__statemeanrects.append(np.s_[row:row+processdim, 0:1])
                        self.__statecovrects.append(np.s_[row:row+processdim, row:row+processdim])
                    row += processdim
                if not matched: raise ValueError('Each observed process must match a Kalman filter\'s process')
                
        def __substatemean(self, statemean):
            return np.vstack([statemean[r] for r in self.__statemeanrects])
        
        def __substatecov(self, statecov):
            return block_diag(*[statecov[r] for r in self.__statecovrects])
        
        def __substatedistr(self, statedistr):
            return N(mean=self.__substatemean(statedistr.mean), cov=self.__substatecov(statedistr.cov), copy=False)
        
        def predict(self, time):
            self.__filter.predict(time)
            predictedobs = self.__obsmodel.predictobs(time, self.__substatedistr(self.__filter._statedistr))
            
            cc = predictedobs.crosscov
            
            # While cc is the cross-covariance between the "observed" processes and the observation, we need the cross-covariance between the full compound
            # process and the observation. Therefore we enlarge this matrix by inserting columns of zeros at appropriate indices
            crosscov = np.zeros((npu.nrow(cc), self.__filter._statedistr.dim))
            col = 0
            for r in self.__statemeanrects:
                size = r[0].stop - r[0].start
                crosscov[0:size, r[0].start:r[0].stop] = cc[0:size, col:col+size]
                col += size
            
            return PredictedObs(time, predictedobs.distr, crosscov)
        
        def observe(self, time, obsdistr):
            predictedobs = self.predict(time)
            self.__filter.observe(obsdistr, predictedobs)
        
    def createobservable(self, obsmodel, process):
        return KalmanFilter.KalmanObservable(self, obsmodel, process)
    
    def predict(self, time):
        if time < self.__time: raise ValueError('Predicting the past (current time=%s, prediction time=%s)' % (self.__time, time))
        if time == self.__time: return
        statedistrs = []
        row = 0
        for p in self._processes:
            processdim = p.processdim
            m = self._statedistr.mean[row:row+processdim, 0:1]
            c = self._statedistr.cov[row:row+processdim, row:row+processdim]
            statedistrs.append(p.propagatedistr(time, self.__time, N(mean=m, cov=c)))
            row += processdim
        statemean = np.vstack([d.mean for d in statedistrs])
        statecov = block_diag(*[d.cov for d in statedistrs])
        self._statedistr = N(mean=statemean, cov=statecov, copy=False)
        self.__time = time
        
    def observe(self, obsdistr, predictedobs):
        innov = obsdistr.mean - predictedobs.distr.mean
        innovcov = predictedobs.distr.cov + obsdistr.cov
        innovcovinv = np.linalg.inv(innovcov)
        gain = np.dot(predictedobs.crosscov.T, innovcovinv)
        m = self._statedistr.mean + np.dot(gain, innov)
        c = self._statedistr.cov - np.dot(gain, predictedobs.crosscov)
        self._statedistr = N(mean=m, cov=c, copy=False)
        loglikelihood = -.5 * (obsdistr.dim * KalmanFilter.LN_2PI + np.log(np.linalg.det(innovcov)) + np.dot(np.dot(innov.T, innovcovinv), innov))
        return ObsResult(predictedobs.time, obsdistr, True, predictedobs, N(mean=innov, cov=innovcov, copy=False), loglikelihood)
