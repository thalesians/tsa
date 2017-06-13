import warnings

import numpy as np

import tsa.numpyutils as npu

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

    def __init__(self, x=None, P=None, Q=None, R=None, F=None, H=None, a=None, b=None, W=None, V=None):
        self.n = None
        self.q = None

        # The n-dimensional state of the system.
        self.x = x
        self.P = P
        self.__priorx = None
        self.__priorP = None
        self.Q = Q
        self.R = R
        self.F = F
        self.H = H
        self.a = a
        self.b = b
        self.W = W
        self.V = V

        # We shall be storing the latest innovation and its variance.
        self.predictedobservation = None
        self.lastobservation = None
        self.innovation = None
        self.innovationvar = None
        self.gain = None

        self.loglikelihood = 0.0

# ------------------------------------------------------------------------------
# Predict and observe
# ------------------------------------------------------------------------------
# The core of the implementation.
# ------------------------------------------------------------------------------

    def predict(self, **kwargs):
        assert not self.Q is None, 'The covariance matrix Q is not set'

        # By default, our transition matrix is the n-by-n-dimensional identity
        # matrix: the state stays the same as time passes.
        if self.F is None:
            if not self.n is None:
                warnings.warn('The transition matrix F is not set. Defaulting to n-by-n-dimensional identity')
                self.F = np.eye(self.n)

        assert not self.F is None, 'The transition matrix F is not set'
        
        if self.W is None:
            self.W = np.eye(self.n)
            
        if self.W is None:
            if not self.n is None:
                warnings.warn('The matrix W is not set. Defaulting to n-by-n-dimensional identity')
                self.W = np.eye(self.n)

        assert not self.W is None, 'The matrix W is not set'

        # Here we shall refer to the steps given in [Haykin-2001]_.

        # State estimate propagation (step 1):
        self.x = np.dot(self.F, self.x)
        if self.a is not None:
            self.x += self.a

        # Error covariance propagation (step 2):
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + np.dot(np.dot(self.W, self.Q), self.W.T)

        self.__priorx = self.x
        self.__priorP = self.P

        return self.x

    def observe(self, observation, **kwargs):
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

        observation = npu.tondim2(observation, ndim1tocol=True, copy=False)

        # Here we shall refer to the steps given in [Haykin-2001]_.

        # Kalman gain matrix (step 3):
        self.innovationvar = np.dot(np.dot(self.H, self.P), self.H.T) + np.dot(np.dot(self.V, R), self.V.T)

        self.gain = np.dot(np.dot(self.P, self.H.T), np.linalg.pinv(self.innovationvar))
        
        self.predictedobservation = np.dot(self.H, self.x)
        if self.b is not None:
            self.predictedobservation += self.b

        # State estimate update (step 4):
        self.innovation = observation - self.predictedobservation
        self.x = self.x + np.dot(self.gain, self.innovation)
        self.P = np.dot(np.identity(self.n) - np.dot(self.gain, self.H), self.P)

        self.loglikelihood += KalmanFilter.MINUS_HALF_LN_2PI - .5 * (np.log(self.innovationvar) + self.innovation * self.innovation / self.innovationvar)
        
        self._lastobservation = observation

        return self.x

    def predictAndObserve(self, observation, **kwargs):
        self.predict(**kwargs)
        return self.observe(observation, **kwargs)

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

    def __get_priorx(self):
        return self.__priorx

    priorx = property(fget=__get_priorx, doc='The n-dimensional predicted state of the system')

    def __get_priorP(self):
        return self.__priorP

    priorP = property(fget=__get_priorP, doc='The n-by-n-dimensional a priori error covariance matrix (a measure of the estimated accuracy of the state estimate)')

    def __get_Q(self):
        return self.__Q

    def __set_Q(self, value):
        if value is not None:
            self.__Q = npu.tondim2(value, copy=True)
            shape = np.shape(self.__Q)
            assert shape[0] == shape[1], 'The covariance matrix Q must be square'
            assert (self.n is None) or (self.n == shape[0]), 'The covariance matrix Q must be n-by-n-dimensional'
            self.n = shape[0]
        else:
            self.__Q = None

    Q = property(fget=__get_Q, fset=__set_Q, doc='The n-by-n-dimensional covariance matrix of the state noise process due to disturbances and modelling errors')

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

    def __get_F(self):
        return self.__F

    def __set_F(self, value):
        if value is not None:
            self.__F = npu.tondim2(value, copy=True)
            shape = np.shape(self.__F)
            assert shape[0] == shape[1], 'The transition matrix F must be square'
            assert (self.n is None) or (self.n == shape[0]), 'The transition matrix F must be n-by-n-dimensional'
            self.n = shape[0]
        else:
            self.__F = None

    F = property(fget=__get_F, fset=__set_F, doc='The n-by-n-dimensional transition matrix taking the state x from time k to time k+1')

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
    
    def __get_a(self):
        return self.__a
    
    def __set_a(self, value):
        if value is not None:
            self.__a = npu.tondim2(value, ndim1tocol=True, copy=True)
        else:
            self.__a = None
    
    a = property(fget=__get_a, fset=__set_a)

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

# ------------------------------------------------------------------------------
# Special methods
# ------------------------------------------------------------------------------

    def __str__(self):
        return 'KalmanFilter(n=%s, q=%s, x=%s, P=%s, Q=%s, R=%s, F=%s, H=%s, innovation=%s, innovationvar=%s)' % (
            self.n, self.q, self.x, self.P, self.Q, self.R, self.F, self.H, self.innovation, self.innovationvar)
