import numpy as np
from scipy.linalg import block_diag

import thalesians.tsa.checks as checks
from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.filtering as filtering
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.objects as objects
import thalesians.tsa.processes as proc

class KalmanObsResult(filtering.ObsResult):
    def __init__(self, accepted, obs, predicted_obs, innov_distr, log_likelihood, gain):
        super().__init__(accepted, obs, predicted_obs, innov_distr, log_likelihood)
        ##self._gain = gain
        self._to_string_helper_KalmanObsResult = None
        self._str_KalmanObsResult = None
        
    @property
    def gain(self):
        return self._gain
    
    def to_string_helper(self):
        if self._to_string_helper_KalmanObsResult is None:
            self._to_string_helper_KalmanObsResult = super().to_string_helper() \
                    .set_type(self) ##\
                    ##.add('gain', self._gain)
            return self._to_string_helper_KalmanObsResult
        
    def __str__(self):
        if self._str_KalmanObsResult is None: self._str_KalmanObsResult = self.to_string_helper().to_string()
        return self._str_KalmanObsResult
    
    def __repr__(self):
        return str(self)
    
class KalmanFilterObsModel(filtering.ObsModel):
    def __init__(self, obs_matrix, name=None):
        super().__init__(name)
        if not checks.is_numpy_array(obs_matrix) and not checks.is_iterable(obs_matrix):
            obs_matrix = (obs_matrix,)
        self._obs_matrix = npu.make_immutable(
                block_diag(
                        *[npu.to_ndim_2(om, ndim_1_to_col=False, copy=False) for om in obs_matrix]))
        self._to_string_helper_KalmanFilterObsModel = None
        self._str_KalmanFilterObsModel = None
        
    @staticmethod
    def create(*args):
        return KalmanFilterObsModel(args)
    
    @property
    def obs_matrix(self):
        return self._obs_matrix
    
    def predict_obs(self, time, state_distr, observable=None):
        obs_mean = np.dot(self._obs_matrix, state_distr.mean)
        cross_cov = np.dot(self._obs_matrix, state_distr.cov)
        obs_cov = np.dot(cross_cov, self._obs_matrix.T)
        return filtering.PredictedObs(observable, time, N(mean=obs_mean, cov=obs_cov), cross_cov)
    
    def to_string_helper(self):
        if self._to_string_helper_KalmanFilterObsModel is None:
            self._to_string_helper_KalmanFilterObsModel = super().to_string_helper() \
                    .set_type(self) \
                    .add('obs_matrix', self._obs_matrix)
        return self._to_string_helper_KalmanFilterObsModel
    
    def __str__(self):
        if self._str_KalmanFilterObsModel is None: self._str_KalmanFilterObsModel = self.to_string_helper().to_string()
        return self._str_KalmanFilterObsModel
    
    def __repr__(self):
        return str(self)

class KalmanFilterState(filtering.FilterState):
    def __init__(self, filter, time, is_posterior, state_distr):  # @ReservedAssignment
        super().__init__(filter, time, is_posterior)
        self._state_distr = state_distr
        self._to_string_helper_KalmanFilterState = None
        self._str_KalmanFilterState = None
    
    def __getstate__(self):
        state = {
                '_state_distr': self._state_distr,
                '_to_string_helper_KalmanFilterState': None,
                '_str_KalmanFilterState': None
            }
        state.update(super().__getstate__())
        return state
        
    @property
    def state_distr(self):
        return self._state_distr
    
    def to_string_helper(self):
        if self._to_string_helper_KalmanFilterState is None:
            self._to_string_helper_KalmanFilterState = super().to_string_helper() \
                    .set_type(self) \
                    .add('state_distr', self._state_distr)
        return self._to_string_helper_KalmanFilterState
    
    def __str__(self):
        if self._str_KalmanFilterState is None: self._str_KalmanFilterState = self.to_string_helper().to_string()
        return self._str_KalmanFilterState
    
    def __repr__(self):
        return str(self)

class KalmanFilter(objects.Named):
    LN_2PI = np.log(2. * np.pi)
    
    def __init__(self, time, state_distr, process, name=None, pype=None,
                 pype_options=frozenset(filtering.FilterPypeOptions)):
        super().__init__(name)
        self._pype = pype
        self._pype_options = frozenset() if (pype_options is None or pype is None) else frozenset(pype_options)
        if not checks.is_iterable(process): process = (process,)
        checks.check_instance(state_distr, N)
        process = checks.check_iterable_over_instances(process, proc.MarkovProcess)
        self._time = time
        self._state_distr = state_distr
        self._is_posterior = False
        self._processes = tuple(process)
        self._to_string_helper_KalmanFilter = None
        self._str_KalmanFilter = None
        if filtering.FilterPypeOptions.PRIOR_STATE in self._pype_options: self._pype.send(self.state)
    
    @property
    def time(self):
        return self._time
    
    @property
    def state(self):
        return KalmanFilterState(self, self._time, self._is_posterior, self._state_distr)
    
    @state.setter
    def state(self, state):
        self._time = state.time
        self._is_posterior = state.is_posterior
        self._state_distr = state._state_distr

    class KalmanObservable(filtering.Observable):
        def __init__(self, filter, obs_model, observed_processes):  # @ReservedAssignment
            super().__init__(filter)
            if not checks.is_iterable(observed_processes): observed_processes = [observed_processes]
            observed_processes = checks.check_iterable_over_instances(observed_processes, proc.MarkovProcess)
            self._obs_model = obs_model
            self._state_mean_rects = []
            self._state_cov_diag_rects = []
            for op in observed_processes:
                matched = False
                row = 0
                for ap in self.filter._processes:
                    process_dim = ap.process_dim
                    if op is ap:
                        matched = True
                        self._state_mean_rects.append(np.s_[row:row+process_dim, 0:1])
                        self._state_cov_diag_rects.append(np.s_[row:row+process_dim, row:row+process_dim])
                    row += process_dim
                if not matched: raise ValueError('Each observed process must match a Kalman filter\'s process')
            self._state_cov_rects = []
            for r in self._state_cov_diag_rects:
                startrow = r[0].start
                stoprow = r[0].stop
                rects = []
                for r1 in self._state_cov_diag_rects:
                    startcol = r1[1].start
                    stopcol = r1[1].stop
                    rects.append(np.s_[startrow:stoprow, startcol:stopcol])
                self._state_cov_rects.append(rects)
                
        def _sub_state_mean(self, state_mean):
            return np.vstack([state_mean[r] for r in self._state_mean_rects])
        
        def _sub_state_cov(self, state_cov):
            return np.vstack([np.hstack([state_cov[r] for r in rs]) for rs in self._state_cov_rects])
        
        def _sub_state_distr(self, state_distr):
            return N(mean=self._sub_state_mean(state_distr.mean), cov=self._sub_state_cov(state_distr.cov), copy=False)
        
        def predict(self, time):
            self.filter.predict(time)
            predicted_obs = self._obs_model.predict_obs(time, self._sub_state_distr(self.filter._state_distr), self)
            
            cc = predicted_obs.cross_cov
            
            # While cc is the cross-covariance between the "observed" processes and the observation, we need the
            # cross-covariance between the full compound process and the observation. Therefore we enlarge this matrix
            # by inserting columns of zeros at appropriate indices
            cc_nrow = npu.nrow(cc)
            cross_cov = np.zeros((cc_nrow, self.filter._state_distr.dim))
            col = 0
            for r in self._state_mean_rects:
                size = r[0].stop - r[0].start
                cross_cov[0:cc_nrow, r[0].start:r[0].start+size] = cc[0:cc_nrow, col:col+size]
                col += size
            
            return filtering.PredictedObs(self, time, predicted_obs.distr, cross_cov)
        
        def observe(self, time, obs_distr, true_value=None):
            if true_value is not None: true_value = npu.to_ndim_2(true_value)
            predicted_obs = self.predict(time)
            return self.filter.observe(obs_distr, predicted_obs, true_value)
    
    def create_observable(self, obs_model, *args):
        return KalmanFilter.KalmanObservable(self, obs_model, args)
    
    def predict(self, time):
        if time < self._time:
            raise ValueError('Predicting the past (current time=%s, prediction time=%s)' % (self._time, time))
        if time == self._time: return
        state_distrs = []
        row = 0
        for p in self._processes:
            process_dim = p.process_dim
            m = self._state_distr.mean[row:row+process_dim, 0:1]
            c = self._state_distr.cov[row:row+process_dim, row:row+process_dim]
            state_distrs.append(p.propagate_distr(time, self._time, N(mean=m, cov=c)))
            row += process_dim
        state_mean = np.vstack([d.mean for d in state_distrs])
        state_cov = block_diag(*[d.cov for d in state_distrs])
        self._state_distr = N(mean=state_mean, cov=state_cov, copy=False)
        self._is_posterior = False
        self._time = time
        if filtering.FilterPypeOptions.PRIOR_STATE in self._pype_options: self._pype.send(self.state)
        
    def observe(self, obs_distr, predicted_obs, true_value):
        innov = obs_distr.mean - predicted_obs.distr.mean
        innov_cov = predicted_obs.distr.cov + obs_distr.cov
        innov_cov_inv = np.linalg.inv(innov_cov)
        gain = np.dot(predicted_obs.cross_cov.T, innov_cov_inv)
        m = self._state_distr.mean + np.dot(gain, innov)
        c = self._state_distr.cov - np.dot(gain, predicted_obs.cross_cov)
        self._state_distr = N(mean=m, cov=c, copy=False)
        self._is_posterior = True
        if filtering.FilterPypeOptions.POSTERIOR_STATE in self._pype_options: self._pype.send(self.state)
        if filtering.FilterPypeOptions.TRUE_VALUE in self._pype_options:
            if true_value is not None: self._pype.send(filtering.TrueValue(self, self._time, true_value))
        log_likelihood = -.5 * (obs_distr.dim * KalmanFilter.LN_2PI + np.log(np.linalg.det(innov_cov)) + \
                np.dot(np.dot(innov.T, innov_cov_inv), innov))
        obs = filtering.Obs(predicted_obs.observable, self._time, obs_distr)
        obs_result = KalmanObsResult(True, obs, predicted_obs, N(mean=innov, cov=innov_cov, copy=False), log_likelihood, gain)
        if filtering.FilterPypeOptions.OBS_RESULT in self._pype_options: self._pype.send(obs_result)
        return obs_result
        
    def to_string_helper(self):
        if self._to_string_helper_KalmanFilter is None:
            self._to_string_helper_KalmanFilter = super().to_string_helper() \
                    .set_type(self) \
                    .add('time', self._time) \
                    .add('state_distr', self._state_distr)
        return self._to_string_helper_KalmanFilter
    
    def __str__(self):
        if self._str_KalmanFilter is None: self._str_KalmanFilter = self.to_string_helper().to_string()
        return self._str_KalmanFilter
    
    def __repr__(self):
        return str(self)
