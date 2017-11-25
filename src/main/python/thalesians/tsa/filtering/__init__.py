import enum
import warnings

import numpy as np
from scipy.linalg import block_diag

import thalesians.tsa.checks as checks
from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.objects as objects
import thalesians.tsa.processes as proc
from thalesians.tsa.strings import ToStringHelper
import thalesians.tsa.utils as utils
from docutils.writers.odf_odt import ToString

class Obs(object):
    def __init__(self, observable, time, distr):
        self._observable = observable
        self._observable_name = observable.name
        self._filter = observable.filter
        self._filter_name = self._filter.name
        self._time = time
        self._distr = distr
        self._to_string_helper_Obs = None
        self._str_Obs = None
    
    def __getstate__(self):
        return {
                '_observable': None,
                '_observable_name': self._observable_name,
                '_filter': None,
                '_filter_name': self._filter_name,
                '_time': self._time,
                '_distr': self._distr,
                '_to_string_helper_Obs': None,
                '_str_Obs': None
            }
    
    @property
    def observable(self):
        return self._observable
    
    @property
    def observable_name(self):
        return self._observable_name
    
    @property
    def filter(self):
        return self._filter
    
    @property
    def filter_name(self):
        return self._filter_name
    
    @property
    def time(self):
        return self._time
    
    @property
    def distr(self):
        return self._distr
    
    def to_string_helper(self):
        if self._to_string_helper_Obs is None:
            self._to_string_helper_Obs = ToStringHelper(self) \
                    .add('time', self._time) \
                    .add('distr', self._distr) ##\
                    ##.add('observable', self._observable)
        return self._to_string_helper_Obs 
    
    def __str__(self):
        if self._str_Obs is None: self._str_Obs = self.to_string_helper().to_string()
        return self._str_Obs
    
    def __repr__(self):
        return str(self)    

class PredictedObs(Obs):
    def __init__(self, obs_model, time, distr, cross_cov):
        super().__init__(obs_model, time, distr)
        self._cross_cov = cross_cov
        self._to_string_helper_PredictedObs = None
        self._str_PredictedObs = None
    
    def __getstate__(self):
        state = {
                '_cross_cov': self._cross_cov,
                '_to_string_helper_PredictedObs': None,
                '_str_PredictedObs': None
            }
        state.update(super().__getstate__())
        return state
    
    @property
    def cross_cov(self):
        return self._cross_cov
    
    def to_string_helper(self):
        if self._to_string_helper_PredictedObs is None:
            self._to_string_helper_PredictedObs = super().to_string_helper() \
                    .set_type(self) \
                    .add('cross_cov', self._cross_cov)
        return self._to_string_helper_PredictedObs 
    
    def __str__(self):
        if self._str_PredictedObs is None: self._str_PredictedObs = self.to_string_helper().to_string()
        return self._str_PredictedObs
    
    def __repr__(self):
        return str(self)
    
class ObsResult(object):
    def __init__(self, accepted, obs, predicted_obs, innov_distr, log_likelihood):
        self._accepted = accepted
        self._obs = obs
        self._predicted_obs = predicted_obs        
        self._innov_distr = innov_distr
        self._log_likelihood = log_likelihood
        self._to_string_helper_ObsResult = None
        self._str_ObsResult = None
    
    @property
    def accepted(self):
        return self._accepted
    
    @property
    def obs(self):
        return self._obs
    
    @property
    def predicted_obs(self):
        return self._predicted_obs
    
    @property
    def innov_distr(self):
        return self._innov_distr
    
    @property
    def log_likelihood(self):
        return self._log_likelihood
    
    def to_string_helper(self):
        if self._to_string_helper_ObsResult is None:
            self._to_string_helper_ObsResult = ToStringHelper(self) ##\
                    ##.add('accepted', self._accepted) \
                    ##.add('obs', self._obs) \
                    ##.add('predicted_obs', self._predicted_obs) \
                    ##.add('innov_distr', self._innov_distr) \
                    ##.add('log_likelihood', self._log_likelihood)
            return self._to_string_helper_ObsResult
        
    def __str__(self):
        if self._str_ObsResult is None: self._str_ObsResult = self.to_string_helper().to_string()
        return self._str_ObsResult
    
    def __repr__(self):
        return str(self)
    
class ObsModel(object):
    def __init__(self):
        self._to_string_helper_ObsModel = None
        self._str_ObsModel = None
    
    def predict_obs(self, time, state_distr, observable=None):
        raise NotImplementedError()
    
    def to_string_helper(self):
        if self._to_string_helper_ObsModel is None: self._to_string_helper_ObsModel = ToStringHelper(self)
        return self._to_string_helper_ObsModel
        
    def __str__(self):
        if self._str_ObsModel is None: self._str_ObsModel = self.to_string_helper().to_string()
        return self._str_ObsModel
    
    def __repr__(self):
        return str(self)

class Observable(objects.Named):
    def __init__(self, filter, name=None):  # @ReservedAssignment
        super().__init__(name)
        self._filter = filter
        self._to_string_helper_Observable = None
        self._str_Observable = None
    
    @property
    def filter(self):
        return self._filter
    
    def predict(self, time):
        raise NotImplementedError()
        
    def observe(self, time, obs_distr):
        raise NotImplementedError()
    
    def to_string_helper(self):
        if self._to_string_helper_Observable is None:
            self._to_string_helper_Observable = super().to_string_helper() \
                    .set_type(self) \
                    .add('filter', self._filter)
        return self._to_string_helper_Observable 
        
    def __str__(self):
        if self._str_Observable is None: self._str_Observable = self.to_string_helper().to_string()
        return self._str_Observable
    
    def __repr__(self):
        return str(self)
    
class FilterState(object):
    def __init__(self, filter, time, is_posterior):  # @ReservedAssignment
        self._filter = filter
        self._filter_name = filter.name
        self._time = time
        self._is_posterior = is_posterior
        self._to_string_helper_FilterState = None
        self._str_FilterState = None
        
    def __getstate__(self):
        return {
                '_filter': None,
                '_filter_name': self._filter_name,
                '_time': self._time,
                '_is_posterior': self._is_posterior,
                '_to_string_helper_FilterState': None,
                '_str_FilterState': None
            }
        
    @property
    def filter(self):
        return self._filter
    
    @property
    def filter_name(self):
        return self._filter_name
    
    @property
    def time(self):
        return self._time
    
    @property
    def is_posterior(self):
        return self._is_posterior
    
    def to_string_helper(self):
        if self._to_string_helper_FilterState is None:
            self._to_string_helper_FilterState = ToStringHelper(self) \
                    .add('filter_name', self._filter_name) \
                    .add('time', self._time) \
                    .add('is_posterior', self._is_posterior)
        return self._to_string_helper_FilterState
    
    def __str__(self):
        if self._str_FilterState is None: self._str_FilterState = self.to_string_helper().to_string()
        return self._str_FilterState
    
    def __repr__(self):
        return str(self)
    
class TrueValue(object):
    def __init__(self, filter, time, value):  # @ReservedAssignment
        self._filter = filter
        self._filter_name = filter.name
        self._time = time
        self._value = value
        self._to_string_helper_TrueValue = None
        self._str_TrueValue = None
        
    def __getstate__(self):
        return {
                '_filter': None,
                '_filter_name': self._filter_name,
                '_time': self._time,
                '_value': self._value,
                '_to_string_helper_TrueValue': None,
                '_str_TrueValue': None
            }
        
    @property
    def filter(self):
        return self._filter
    
    @property
    def filter_name(self):
        return self._filter_name
    
    @property
    def time(self):
        return self._time
    
    @property
    def value(self):
        return self._value

    def to_string_helper(self):
        if self._to_string_helper_TrueValue is None:
            self._to_string_helper_TrueValue = ToStringHelper(self) \
                    .add('filter_name', self._filter_name) \
                    .add('time', self._time) \
                    .add('value', self._value)
        return self._to_string_helper_TrueValue
    
    def __str__(self):
        if self._str_TrueValue is None: self._str_TrueValue = self.to_string_helper().to_string()
        return self._str_TrueValue
    
    def __repr__(self):
        return str(self)

class FilterPypeOptions(enum.Enum):
    PRIOR_STATE = 1
    POSTERIOR_STATE = 2
    OBS_RESULT = 3
    TRUE_VALUE = 4
