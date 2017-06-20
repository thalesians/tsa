import warnings

import numpy as np
from scipy.linalg import block_diag

import thalesians.tsa.checks as checks
import thalesians.tsa.distrs as distrs
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.processes as proc

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
    def __init__(self, time, obs, accepted, predictedobs, innov, loglikelihood):
        self.__time = time
        self.__obs = obs
        self.__accepted = accepted
        self.__predictedobs = predictedobs
        self.__innov = innov
        self.__loglikelihood = loglikelihood
        
    @property
    def time(self):
        return self.__time
    
    @property
    def obs(self):
        return self.__obs
    
    @property
    def accepted(self):
        return self.__accepted
    
    @property
    def predictedobs(self):
        return self.__predictedobs
    
    @property
    def innov(self):
        return self.__innov
    
    @property
    def loglikelihood(self):
        return self.__loglikelihood
    
    def __str__(self):
        return 'ObsResult(time=%s, obs=%s, accepted=%s, predictedobs=%s, innov=%s, loglikelihood=%f)' % (self.__time, self.__obs, self.__accepted, self.__predictedobs, self.__innov, self.__loglikelihood)
    
class Observable(object):
    def predict(self, time):
        raise NotImplementedError()
        
    def observe(self, time, obs, obscov):
        raise NotImplementedError()
    
class KalmanFilter(object):
    r"""
The Kalman filter.

:param x: The initial n-dimensional estimate of the state of the system
:param P: The n-by-n-dimensional a posteriori error covariance matrix (a measure
    of the estimated accuracy of the state estimate)
:param Q: The n-by-n-dimensional covariance matrix of the state noise process
    due to disturbances and modelling errors
:param R: The q-by-q-dimensional covariance matrix of the measurement noise
    process
:param F: The n-by-n-dimensional transition matrix taking the state x from time
    k to time k+1
:param H: The q-by-n-dimensional measurement matrix. Applied to a state, it
    produces the corresponding observable
    """

    MINUS_HALF_LN_2PI = -.5 * np.log(2. * np.pi)
    
# ------------------------------------------------------------------------------
# Constructor
# ------------------------------------------------------------------------------

    def __init__(self, time, distr, process):
        checks.checkisinstance(distr, distrs.NormalDistr)
        # TODO process may also be an iterable of MarkovProcesses
        checks.checkisinstance(process, proc.MarkovProcess)
        self.__time = time
        self.__distr = distr
        self.__processes = process
        
        self.R = R
        self.H = H
        self.b = b
        self.V = V

        self.gain = None

    class KalmanObservable(Observable):
        def __init__(self, filter, allprocesses, observedprocesses):
            self.__filter = filter
            self.__staterects = []
            self.__statecovrects = []
            for op in observedprocesses:
                matched = False
                row = 0
                for ap in allprocesses:
                    processdim = ap.processdim
                    if op is ap:
                        matched = True
                        self.__staterects.append(np.s_[row:row+processdim, 0:1])
                        self.__statecovrects.append(np.s_[row:row+processdim, row:row+processdim])
                    row += processdim
                if not matched: raise ValueError('Each observed process must match a Kalman filter\'s process')
                
        def __substate(self, state):
            return np.vstack([state[r] for r in self.__staterects])
        
        def __substatecov(self, statecov):
            return block_diag(*[statecov[r] for r in self.__statecovrects])
        
        def predict(self, time):
            self.__filter.predict()
        
        def observe(self, time, obs, obscov):
            pass
        
    def createobservable(self, process):
        pass
    
    def predict(self, time):
        if time < self.__time: raise ValueError('Predicting the past (current time=%s, prediction time=%s)' % (self.__time, time))
        if time == self.__time: return
        distrs = []
        row = 0
        for p in self.__processes:
            processdim = p.processdim
            m = self.__state[row:row+processdim, 0:1]
            c = self.__statecov[row:row+processdim, row:row+processdim]
            distrs.append(p.propagatedistr(time, self.__time, distrs.NormalDistr(mean=m, cov=c)))
            row += processdim
        self.__state = np.vstack([d.mean for d in distrs])
        self.__statecov = block_diag(*[d.cov for d in distrs])
        self.__time = time

# ------------------------------------------------------------------------------
# Predict and observe
# ------------------------------------------------------------------------------
# The core of the implementation.
# ------------------------------------------------------------------------------

    def predict(self, time):
        distr = self.__process.propagatedistr(time, self.__time, distrs.NormalDistr(mean=self.x, cov=self.P))
        self.x, self.P = distr.mean, distr.cov        
        return self.x, self.P

    def observe(self, obs, **kwargs):
        if 'R' in kwargs:
            R = kwargs['R']
        else:
            R = self.R

        assert not R is None, 'The covariance matrix R is not set'

        # By default, our measurement matrix is the n-by-n-dimensional identity
        # matrix: we are observing the state directly. This only makes sense if
        # n == q.
        if self.H is None:
            if (not self.n is None) and (self.n == self.q):
                warnings.warn('The measurement matrix H is not set. Defaulting to n-by-n-dimensional identity')
                self.H = np.eye(self.n)

        assert not self.H is None, 'The measurement matrix H is not set'
        
        if self.V is None:
            if self.q is not None:
                warnings.warn('The matrix V is not set. Defaulting to q-by-q-dimensional identity')
                self.V = np.eye(self.q)

        assert not self.V is None, 'The matrix V is not set'

        obs = npu.tondim2(obs, ndim1tocol=True, copy=False)

        # Here we shall refer to the steps given in [Haykin-2001]_.

        # Kalman gain matrix (step 3):
        innovcov = np.dot(np.dot(self.H, self.P), self.H.T) + np.dot(np.dot(self.V, R), self.V.T)

        self.gain = np.dot(np.dot(self.P, self.H.T), np.linalg.pinv(innovcov))
        
        predictedobs = np.dot(self.H, self.x)
        if self.b is not None:
            predictedobs += self.b

        # State estimate update (step 4):
        self.innov = obs - predictedobs
        self.x = self.x + np.dot(self.gain, innov)
        self.P = np.dot(np.identity(self.n) - np.dot(self.gain, self.H), self.P)

        loglikelihood = KalmanFilter.MINUS_HALF_LN_2PI - .5 * (np.log(innovcov) + innov * innov / innovcov)
        
        return ObsResult(accepted=True, loglikelihood=loglikelihood)
    
        
        (accepted, predictedobs=distrs.NormalDistr(mean=predictedobs, innovcov), innov, loglikelihood)

    def predictAndObserve(self, obs, **kwargs):
        self.predict(**kwargs)
        return self.observe(obs, **kwargs)

# ------------------------------------------------------------------------------
# Properties
# ------------------------------------------------------------------------------
# This code is mostly wrappers and glue. The reason it is here is to ensure that
# we are dealing with numpy arrays of the right rank and shape. We are coercing
# inputs to (two-dimensional) matrices. This helps us avoid subtle
# bugs.
# ------------------------------------------------------------------------------

    def __get_x(self):
        return self.__x

    def __set_x(self, value):
        if value is not None:
            self.__x = npu.tondim2(value, ndim1tocol=True, copy=True)
            shape = np.shape(self.__x)
            assert (self.n is None) or (self.n == shape[0]), 'The state estimate x must be n-dimensional'
            self.n = shape[0]
        else:
            self.__x = None

    x = property(fget=__get_x, fset=__set_x, doc='The n-dimensional estimate of the state of the system')

    def __get_P(self):
        return self.__P

    def __set_P(self, value):
        if value is not None:
            self.__P = npu.tondim2(value, copy=True)
            shape = np.shape(self.__P)
            assert shape[0] == shape[1], 'The covariance matrix P must be square'
            assert (self.n is None) or (self.n == shape[0]), 'The covariance matrix P must be n-by-n-dimensional'
            self.n = shape[0]
        else:
            self.__P = None

    P = property(fget=__get_P, fset=__set_P, doc='The n-by-n-dimensional a posteriori error covariance matrix (a measure of the estimated accuracy of the state estimate)')

    def __get_R(self):
        return self.__R

    def __set_R(self, value):
        if value is not None:
            self.__R = npu.tondim2(value, copy=True)
            shape = np.shape(self.__R)
            assert shape[0] == shape[1], 'The covariance matrix R must be square'
            assert (self.q is None) or (self.q == shape[0]), 'The covariance matrix R must be q-by-q-dimensional'
            self.q = shape[0]
        else:
            self.__R = None

    R = property(fget=__get_R, fset=__set_R, doc='The q-by-q-dimensional covariance matrix of the measurement noise process')

    def __get_H(self):
        return self.__H

    def __set_H(self, value):
        if value is not None:
            self.__H = npu.tondim2(value, copy=True)
            shape = np.shape(self.__H)
            assert (self.q is None) or (self.q == shape[0]), 'The measurement matrix H must have q (%d) rows; it has %d rows' % (self.q, shape[0])
            assert (self.n is None) or (self.n == shape[1]), 'The measurement matrix H must have n (%d) columns; it has %d columns' % (self.n, shape[1])
            self.q = shape[0]
            self.n = shape[1]
        else:
            self.__H = None

    H = property(fget=__get_H, fset=__set_H, doc='The q-by-n-dimensional measurement matrix. Applied to a state, it produces the corresponding observable')
    
    def __get_b(self):
        return self.__b
    
    def __set_b(self, value):
        if value is not None:
            self.__b = npu.tondim2(value, ndim1tocol=True, copy=True)
        else:
            self.__b = None
    
    b = property(fget=__get_b, fset=__set_b)
    
    @property
    def mean(self): return self.x
    
    @property
    def var(self): return self.P

    def __str__(self):
        return 'KalmanFilter(x=%s, P=%s, R=%s, H=%s)' % (self.x, self.P, self.R, self.H)
