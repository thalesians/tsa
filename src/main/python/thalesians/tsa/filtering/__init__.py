import enum

import numpy as np
import pandas as pd
from scipy.linalg import block_diag

import thalesians.tsa.checks as checks
import thalesians.tsa.distrs as distrs
from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.objects as objects
import thalesians.tsa.processes as proc
import thalesians.tsa.simulation as sim
from thalesians.tsa.strings import ToStringHelper
import thalesians.tsa.utils as utils
from docutils.writers.odf_odt import ToString

class Obs(object):
    def __init__(self, observable, time, distr, observable_name=None):
        self._observable = observable
        if observable_name is None:
            self._observable_name = None if observable is None else observable.name
        else:
            self._observable_name = observable_name
        self._filter = None if observable is None else observable.filter
        self._filter_name = None if self._filter is None else self._filter.name
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
                    .add('distr', self._distr) \
                    .add('observable_name', self._observable_name)
        return self._to_string_helper_Obs 
    
    def __str__(self):
        if self._str_Obs is None: self._str_Obs = self.to_string_helper().to_string()
        return self._str_Obs
    
    def __repr__(self):
        return str(self)    

def _time_and_obs_distr(obs, time=None, filter_time=None):
    if isinstance(obs, Obs):
        obs_distr = obs.distr
        if time is None: time = obs.time
    elif isinstance(obs, distrs.Distr):
        obs_distr = obs
    else:
        obs_distr = distrs.DiracDeltaDistr(obs)
        
    if time is None: time = filter_time + 1

    return time, obs_distr

class PredictedObs(Obs):
    def __init__(self, obs_model, time, distr, cross_cov, observable_name=None):
        super().__init__(obs_model, time, distr, observable_name)
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
            self._to_string_helper_ObsResult = ToStringHelper(self) \
                    .add('accepted', self._accepted) \
                    .add('obs', self._obs) \
                    .add('predicted_obs', self._predicted_obs) \
                    .add('innov_distr', self._innov_distr) \
                    .add('log_likelihood', self._log_likelihood)
            return self._to_string_helper_ObsResult
        
    def __str__(self):
        if self._str_ObsResult is None: self._str_ObsResult = self.to_string_helper().to_string()
        return self._str_ObsResult
    
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
        
    def observe(self, obs, time=None, true_value=None, predicted_obs=None):
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
    
class FilterState(object):
    def __init__(self, filter, time, is_posterior, filter_name=None):  # @ReservedAssignment
        self._filter = filter
        if filter_name is None:
            self._filter_name = None if filter is None else filter.name
        else:
            self._filter_name = filter_name
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
    def __init__(self, filter, time, value, filter_name=None):  # @ReservedAssignment
        self._filter = filter
        if filter_name is not None:
            self._filter_name = None if filter is None else filter.name
        else:
            self._filter_name = filter_name
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

class FilterRunResult(object):
    def __init__(self, last_obs_result, cumulative_log_likelihood, df):
        self._last_obs_result = last_obs_result
        self._cumulative_log_likelihood = cumulative_log_likelihood
        self._df = df
        self._to_string_helper_FilterRunResult = None
        self._str_FilterRunResult = None

    @property
    def last_obs_result(self):
        return self._last_obs_result

    @property
    def cumulative_log_likelihood(self):
        return self._cumulative_log_likelihood

    @property
    def df(self):
        return self._df

    def to_string_helper(self):
        if self._to_string_helper_FilterRunResult is None:
            self._to_string_helper_FilterRunResult = ToStringHelper(self) \
                    .add('last_obs_result', self._last_obs_result) \
                    .add('cumulative_log_likelihood', self._cumulative_log_likelihood) \
                    .add('df', self._df)
        return self._to_string_helper_FilterRunResult
    
    def __str__(self):
        if self._str_FilterRunResult is None: self._str_FilterRunResult = self.to_string_helper().to_string()
        return self._str_FilterRunResult
    
    def __repr__(self):
        return str(self)

def run(observable, obss=None, times=None, obs_covs=None, true_values=None, df=None, fun=None, return_df=False):
    if df is not None:
        if obss is not None and (checks.is_string(obss) or checks.is_int(obss)):
            obss = df[obss]

        if times is None:
            if isinstance(obss, pd.Series): times = obss.index.values
        elif (checks.is_string(times) or checks.is_int(times)):
            times = df[times].values

        if isinstance(obss, pd.Series): obss = obss.values

        if obs_covs is not None and (checks.is_string(obs_covs) or checks.is_int(obs_covs)):
            obs_covs = df[obs_covs].values

        if true_values is not None and (checks.is_string(true_values) or checks.is_int(true_values)):
            true_values = df[true_values].values
            
    checks.check_not_none(obss)

    if not checks.is_iterable_not_string(observable): observable = utils.xconst(observable)
    if not checks.is_iterable_not_string(obss): obss = [obss]
    if not checks.is_iterable_not_string(times): times = utils.xconst(times)
    if not checks.is_iterable_not_string(obs_covs): obs_covs = utils.xconst(obs_covs)    
    if not checks.is_iterable_not_string(true_values): true_values = utils.xconst(true_values)
    
    obs_result = None
    cumulative_log_likelihood = 0.
    
    if return_df:
        time = []
        filter_name = []
        filter_type = []
        observable_name = []
        accepted = []
        obs_mean = []
        obs_cov = []
        predicted_obs_mean = []
        predicted_obs_cov = []
        cross_cov = []
        innov_mean = []
        innov_cov = []
        prior_state_mean = []
        prior_state_cov = []
        posterior_state_mean = []
        posterior_state_cov = []
        true_value = []
        log_likelihood = []
        gain = []

    last_time = None
        
    for an_observable, an_obs, a_time, an_obs_cov, a_true_value in zip(observable, obss, times, obs_covs, true_values):
        if a_time is None:
            if last_time is None: a_time = 0
            else: a_time = last_time + 1
        last_time = a_time

        if checks.is_callable(an_observable): an_observable = an_observable(an_obs)
        if fun is not None: an_obs = fun(an_obs)
        if an_obs_cov is not None:
            if isinstance(an_obs, (Obs, distrs.Distr)):
                raise ValueError('An observation covariance is provided while the observation is given by a distribution --- conflicting arguments')
            an_obs = distrs.NormalDistr(an_obs, an_obs_cov)
        
        if return_df and len(time) == 0:
            an_initial_state_mean = an_observable.filter.state.state_distr.mean
            an_initial_state_cov = an_observable.filter.state.state_distr.cov
            time.append(an_observable.filter.time)
            filter_name.append(an_observable.filter.name)
            filter_type.append(type(an_observable.filter))
            observable_name.append(None)
            accepted.append(None)
            obs_mean.append(None)
            obs_cov.append(None)
            predicted_obs_mean.append(None)
            predicted_obs_cov.append(None)
            cross_cov.append(None)
            innov_mean.append(None)
            innov_cov.append(None)
            prior_state_mean.append(npu.to_scalar(an_initial_state_mean, raise_value_error=False))
            prior_state_cov.append(npu.to_scalar(an_initial_state_cov, raise_value_error=False))
            posterior_state_mean.append(npu.to_scalar(an_initial_state_mean, raise_value_error=False))
            posterior_state_cov.append(npu.to_scalar(an_initial_state_cov, raise_value_error=False))
            true_value.append(None)
            log_likelihood.append(None)
            gain.append(None)
        
        if isinstance(an_obs, Obs):
            a_time, _ = _time_and_obs_distr(an_obs, a_time, an_observable.filter.time)
            
        predicted_obs = an_observable.predict(time=a_time, true_value=a_true_value)
        a_prior_state_mean = an_observable.filter.state.state_distr.mean
        a_prior_state_cov = an_observable.filter.state.state_distr.cov
        obs_result = an_observable.observe(obs=an_obs, time=a_time, true_value=a_true_value, predicted_obs=predicted_obs)
        if obs_result.accepted: cumulative_log_likelihood += obs_result.log_likelihood
        a_posterior_state_mean = an_observable.filter.state.state_distr.mean
        a_posterior_state_cov = an_observable.filter.state.state_distr.cov
        
        if return_df:
            time.append(obs_result.obs.time)
            filter_name.append(an_observable.filter.name)
            filter_type.append(type(an_observable.filter))
            observable_name.append(an_observable.name)
            accepted.append(obs_result.accepted)
            obs_mean.append(npu.to_scalar(obs_result.obs.distr.mean, raise_value_error=False))
            obs_cov.append(npu.to_scalar(obs_result.obs.distr.cov, raise_value_error=False))
            predicted_obs_mean.append(npu.to_scalar(obs_result.predicted_obs.distr.mean, raise_value_error=False))
            predicted_obs_cov.append(npu.to_scalar(obs_result.predicted_obs.distr.cov, raise_value_error=False))
            cross_cov.append(npu.to_scalar(obs_result.predicted_obs.cross_cov, raise_value_error=False))
            innov_mean.append(npu.to_scalar(obs_result.innov_distr.mean, raise_value_error=False))
            innov_cov.append(npu.to_scalar(obs_result.innov_distr.cov, raise_value_error=False))
            prior_state_mean.append(npu.to_scalar(a_prior_state_mean, raise_value_error=False))
            prior_state_cov.append(npu.to_scalar(a_prior_state_cov, raise_value_error=False))
            posterior_state_mean.append(npu.to_scalar(a_posterior_state_mean, raise_value_error=False))
            posterior_state_cov.append(npu.to_scalar(a_posterior_state_cov, raise_value_error=False))
            true_value.append(npu.to_scalar(a_true_value, raise_value_error=False))
            log_likelihood.append(npu.to_scalar(obs_result.log_likelihood, raise_value_error=False))
            gain.append(obs_result.gain if hasattr(obs_result, 'gain') else None)
    
    df = None
    if return_df:
        df = pd.DataFrame({
            'time': time,
            'filter_name': filter_name,
            'filter_type': filter_type,
            'observable_name': observable_name,
            'accepted': accepted,
            'obs_mean': obs_mean,
            'obs_cov': obs_cov,
            'predicted_obs_mean': predicted_obs_mean,
            'predicted_obs_cov': predicted_obs_cov,
            'cross_cov': cross_cov,
            'innov_mean': innov_mean,
            'innov_cov': innov_cov,
            'prior_state_mean': prior_state_mean,
            'prior_state_cov': prior_state_cov,
            'posterior_state_mean': prior_state_mean,
            'posterior_state_cov': prior_state_cov,
            'true_value': true_value,
            'log_likelihood': log_likelihood,
            'gain': gain},
            columns=('time', 'filter_name', 'filter_type', 'observable_name',
                     'accepted', 'obs_mean', 'obs_cov', 'predicted_obs_mean', 'predicted_obs_cov', 'cross_cov',
                     'innov_mean', 'innov_cov',
                     'prior_state_mean', 'prior_state_cov', 'posterior_state_mean', 'posterior_state_cov',
                     'true_value', 'log_likelihood', 'gain'))

    return FilterRunResult(obs_result, cumulative_log_likelihood, df)
