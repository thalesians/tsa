import warnings

import numpy as np
from scipy.linalg import block_diag

import thalesians.tsa.checks as checks
from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.processes as proc
import thalesians.tsa.utils as utils

class PredictedObs(object):
    def __init__(self, time, distr, cross_cov):
        self._time = time
        self._distr = distr
        self._cross_cov = cross_cov
    
    @property
    def time(self):
        return self._time
    
    @property
    def distr(self):
        return self._distr
    
    @property
    def cross_cov(self):
        return self._cross_cov
    
    def __str__(self):
        return 'PredictedObs(time=%s, distr=%s, cross_cov=%s)' % (self._time, self._distr, self._cross_cov)
    
    def __repr__(self):
        return str(self)
    
class ObsResult(object):
    def __init__(self, time, obs_distr, accepted, predicted_obs, innov_distr, log_likelihood):
        self._time = time
        self._obs_distr = obs_distr
        self._accepted = accepted
        self._predicted_obs = predicted_obs
        self._innov_distr = innov_distr
        self._log_likelihood = log_likelihood
        
    @property
    def time(self):
        return self._time
    
    @property
    def obs_distr(self):
        return self._obs_distr
    
    @property
    def accepted(self):
        return self._accepted
    
    @property
    def predicted_obs(self):
        return self._predicted_obs
    
    @property
    def innov_distr(self):
        return self._innov_distr
    
    @property
    def log_likelihood(self):
        return self._log_likelihood
    
    def __str__(self):
        return 'ObsResult(time=%s, obs_distr=%s, accepted=%s, predicted_obs=%s, innov_distr=%s, log_likelihood=%f)' % (self._time, self._obs_distr, self._accepted, self._predicted_obs, self._innov_distr, self._log_likelihood)
    
    def __repr__(self):
        return str(self)
    
class ObsModel(object):
    def predict_obs(self, time, state_distr):
        pass
    
class KalmanFilterObsModel(ObsModel):
    def __init__(self, obs_matrix):
        if not isinstance(obs_matrix, np.ndarray) and not checks.is_iterable(obs_matrix):
            obs_matrix = (obs_matrix,)
        self._obs_matrix = block_diag(*[npu.to_ndim_2(om, ndim_1_to_col=False, copy=False) for om in obs_matrix])
        
    @staticmethod
    def create(*args):
        return KalmanFilterObsModel(args)
    
    def predict_obs(self, time, state_distr):
        obs_mean = np.dot(self._obs_matrix, state_distr.mean)
        cross_cov = np.dot(self._obs_matrix, state_distr.cov)
        obs_cov = np.dot(cross_cov, self._obs_matrix.T)
        return PredictedObs(time, N(mean=obs_mean, cov=obs_cov), cross_cov)

class Observable(object):
    def predict(self, time):
        raise NotImplementedError()
        
    def observe(self, time, obs, obs_cov):
        raise NotImplementedError()
    
class KalmanFilter(object):
    LN_2PI = np.log(2. * np.pi)
    
    def __init__(self, time, state_distr, process):
        if not checks.is_iterable(process): process = (process,)
        checks.check_instance(state_distr, N)
        process = checks.check_iterable_over_instances(process, proc.MarkovProcess)
        self._time = time
        self._state_distr = state_distr
        self._processes = tuple(process)

    class KalmanObservable(Observable):
        def __init__(self, filter, obs_model, observed_processes):
            if not checks.is_iterable(observed_processes): observed_processes = [observed_processes]
            observed_processes = checks.check_iterable_over_instances(observed_processes, proc.MarkovProcess)
            self._filter = filter
            self._obs_model = obs_model
            self._state_mean_rects = []
            self._state_cov_diag_rects = []
            for op in observed_processes:
                matched = False
                row = 0
                for ap in self._filter._processes:
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
            self._filter.predict(time)
            predicted_obs = self._obs_model.predict_obs(time, self._sub_state_distr(self._filter._state_distr))
            
            cc = predicted_obs.cross_cov
            
            # While cc is the cross-covariance between the "observed" processes and the observation, we need the cross-covariance between the full compound
            # process and the observation. Therefore we enlarge this matrix by inserting columns of zeros at appropriate indices
            cc_nrow = npu.nrow(cc)
            cross_cov = np.zeros((cc_nrow, self._filter._state_distr.dim))
            col = 0
            for r in self._state_mean_rects:
                size = r[0].stop - r[0].start
                cross_cov[0:cc_nrow, r[0].start:r[0].start+size] = cc[0:cc_nrow, col:col+size]
                col += size
            
            return PredictedObs(time, predicted_obs.distr, cross_cov)
        
        def observe(self, time, obs_distr):
            predicted_obs = self.predict(time)
            return self._filter.observe(obs_distr, predicted_obs)
        
    def create_observable(self, obs_model, *args):
        return KalmanFilter.KalmanObservable(self, obs_model, args)
    
    def predict(self, time):
        if time < self._time: raise ValueError('Predicting the past (current time=%s, prediction time=%s)' % (self._time, time))
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
        self._time = time
        
    def observe(self, obs_distr, predicted_obs):
        innov = obs_distr.mean - predicted_obs.distr.mean
        innov_cov = predicted_obs.distr.cov + obs_distr.cov
        innov_cov_inv = np.linalg.inv(innov_cov)
        gain = np.dot(predicted_obs.cross_cov.T, innov_cov_inv)
        m = self._state_distr.mean + np.dot(gain, innov)
        c = self._state_distr.cov - np.dot(gain, predicted_obs.cross_cov)
        self._state_distr = N(mean=m, cov=c, copy=False)
        log_likelihood = -.5 * (obs_distr.dim * KalmanFilter.LN_2PI + np.log(np.linalg.det(innov_cov)) + np.dot(np.dot(innov.T, innov_cov_inv), innov))
        return ObsResult(predicted_obs.time, obs_distr, True, predicted_obs, N(mean=innov, cov=innov_cov, copy=False), log_likelihood)
    
    def __str__(self):
        return 'KalmanFilter(time=%s, state=%s)' % (self._time, self._state_distr)
    
    def __repr__(self):
        return str(self)
    