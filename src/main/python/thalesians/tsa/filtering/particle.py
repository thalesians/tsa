from collections import OrderedDict
import warnings

import numpy as np
import statsmodels.api as sm

import thalesians.tsa.checks as checks
from thalesians.tsa.distrs import EmpiricalDistr
from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.filtering as filtering
import thalesians.tsa.objects as objects
import thalesians.tsa.outliers as outliers
import thalesians.tsa.processes as proc
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.random as rnd

class ParticleObsResult(filtering.ObsResult):
    def __init__(self, accepted, obs, predicted_obs, innov_distr, log_likelihood):
        super().__init__(accepted, obs, predicted_obs, innov_distr, log_likelihood)

    def to_string_helper(self):
        if self._to_string_helper_ParticleObsResult is None:
            self._to_string_helper_ParticleObsResult = super().to_string_helper() \
                    .set_type(self)
            return self._to_string_helper_ParticleObsResult
        
    def __str__(self):
        if self._str_ParticleObsResult is None: self._str_ParticleObsResult = self.to_string_helper().to_string()
        return self._str_ParticleObsResult

class KDEWeightingFunction(object):
    def __init__(self, obs_function=None):
        if obs_function is None: obs_function = lambda x: x
        self._obs_function = obs_function

    def __call__(self, obs, particles):
        obs_particles = [self._obs_function(p) for p in particles]
        obs_particles_kde = sm.nonparametric.KDEMultivariate(obs_particles)
        return obs_particles_kde.pdf(obs)

class ParticleFilterObsModel(object):
    def __init__(self, weighting_function):
        super().__init__()
        self._weighting_function = weighting_function
        self._to_string_helper_ParticleFilterObsModel = None
        self._str_ParticleFilterObsModel = None

    @staticmethod
    def create(weighting_function):
        return ParticleFilterObsModel(weighting_function)

    @property
    def weighting_function(self):
        return self._weighting_function

    def predict_obs(self, time, state_distr, observable=None):
        raise NotImplementedError()

    def to_string_helper(self):
        if self._to_string_helper_ParticleFilterObsModel is None:
            self._to_string_helper_ParticleFilterObsModel = super().to_string_helper() \
                    .set_type(self) \
                    .add('weighting_function', self._weighting_function)
        return self._to_string_helper_ParticleFilterObsModel
    
    def __str__(self):
        if self._str_ParticleFilterObsModel is None: self._str_ParticleFilterObsModel = self.to_string_helper().to_string()
        return self._str_ParticleFilterObsModel

class ParticleFilter(objects.Named):
    MIN_WEIGHT_SUM = np.finfo(float).eps

    # TODO Kalman filter has the following parameters:
    # def __init__(self, time, state_distr, process, name=None, pype=None,
    #              pype_options=frozenset(filtering.FilterPypeOptions)):

    # TODO Use time
    # TODO Replaced transition_distr with process
    # TODO Kalman filter allows process=(process1, process2)

    def __init__(self, time, state_distr, process,
                 weighting_func=None,
                 particle_count=1000, observation_dim=1,
                 random_state=None,
                 predicted_observation_sampler=None, outlier_threshold=None,
                 name=None, pype=None, pype_options=frozenset(filtering.FilterPypeOptions)):
        super().__init__(name)
        self._pype = pype
        self._pype_options = frozenset() if (pype_options is None or pype is None) else frozenset(pype_options)
        if not checks.is_iterable(process): process = (process,)
        process = checks.check_iterable_over_instances(process, proc.SolvedItoProcess)
        if weighting_func is None: weighting_func = KDEWeightingFunction()
        self._time = time
        self._observation_dim = observation_dim
        self._state_distr = state_distr
        self._processes = tuple(process)
        self._state_dim = sum([p.process_dim for p in self._processes])
        self._weighting_func = weighting_func
        self._particle_count = particle_count
        self._current_particle_idx = None
        self._random_state = rnd.random_state() if random_state is None else random_state
        self._predicted_observation_sampler = predicted_observation_sampler
        
        self._prior_particles = np.empty((self._particle_count, self._state_dim))
        self._resampled_particles = np.empty((self._particle_count, self._state_dim))
        self._unnormalised_weights = np.empty((self._particle_count,))
        self._weights = np.empty((self._particle_count,))
        self._resampled_particles_uptodate = False
        
        self._last_observation = None
        
        self._cached_prior_mean = None
        self._cached_prior_var = None
        self._cached_posterior_mean = None
        self._cached_posterior_var = None
        self._cached_resampled_mean = None
        self._cached_resampled_var = None
        
        self.log_likelihood = 0.0
        self.effective_sample_size = np.NaN
        
        if self._predicted_observation_sampler is not None:
            self.predicted_observation_particles = None
            self.predicted_observation_kde = None
            self.predicted_observation = np.NaN
            self.innovation = np.NaN
            self.innovationvar = np.NaN
            
        assert self._predicted_observation_sampler is not None or outlier_threshold is None 
        self._outlier_threshold = outlier_threshold
            
        self._context = OrderedDict()
        
        self._initialise()

    @property
    def time(self):
        return self._time

    # TODO Add @property time, @property state, and @state.setter state, as in KalmanFilter

    class ParticleObservable(filtering.Observable):
        def __init__(self, filter, name, obs_model, observed_processes, *args, **kwargs):
            super().__init__(filter, name)
            if not checks.is_iterable(observed_processes): observed_processes = [observed_processes]
            observed_processes = tuple(checks.check_iterable_over_instances(observed_processes, proc.MarkovProcess))
            if obs_model is None:
                obs_model = ParticleFilterObsModel.create(
                    np.eye(sum([p.process_dim for p in observed_processes])))
            self._obs_model = obs_model
            self._state_mean_rects = []
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
                if not matched: raise ValueError('Each observed process must match a particle filter\'s process')
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
            # TODO Does this even make sense?
            return N(mean=self._sub_state_mean(state_distr.mean), cov=self._sub_state_cov(state_distr.cov), copy=False)
        
        def predict(self, time, true_value=None):
            print('ParticleObservable.predict called')
            self.filter.predict(time, true_value)
            predicted_obs = self._obs_model.predict_obs(time, self._sub_state_distr(self.filter._state_distr), self)
            print('predicted_obs:', predicted_obs)
            
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
        
        def observe(self, obs, time=None, true_value=None, predicted_obs=None):
            time, obs_distr = filtering._time_and_obs_distr(obs, time, self.filter.time)
            if true_value is not None: true_value = npu.to_ndim_2(true_value)
            if predicted_obs is None: predicted_obs = self.predict(time, true_value)
            return self.filter.observe(obs_distr, predicted_obs, true_value)
    
    def create_observable(self, obs_model, *args):
        return ParticleFilter.ParticleObservable(self, None, obs_model, args)
    
    def create_identity_observable(self, *args):
        return ParticleFilter.ParticleObservable(self, None, None, args)
    
    def create_named_observable(self, name, obs_model, *args):
        return ParticleFilter.ParticleObservable(self, name, obs_model, args)
    
    def create_named_identity_observable(self, name, *args):
        return ParticleFilter.ParticleObservable(self, name, None, args)
            
    # An auxiliary method of the constructor. Not called anywhere else.
    def _initialise(self):
        # TODO Vectorise
        for i in range(self._particle_count):
            self._current_particle_idx = i
            self._prior_particles[i,:] = npu.to_ndim_1(self._state_distr.sample())
            self._resampled_particles[i,:] = self._prior_particles[i,:]
        self._current_particle_idx = None
        self._unnormalised_weights[:] = np.NaN
        self._weights[:] = 1./self._particle_count
            
    def predict(self, time, true_value=None):
        # TODO Use true_value
        if time < self._time:
            raise ValueError('Predicting the past (current time=%s, prediction time=%s)' % (self._time, time))
        if time == self.time:
            print('Predicting the present - nothing to do')
            return
        if not self._resampled_particles_uptodate:
            self._resampled_particles[:] = self._prior_particles[:]
        row = 0
        self._prior_particles = np.empty((self._particle_count, self._state_dim))
        for p in self._processes:
            process_dim = p.process_dim
            if npu.is_vectorised(p.propagate):
                self._prior_particles[:, row:row+process_dim] = p.propagate(self._time, self._resampled_particles[:, row:row+process_dim], time)
            else:
                for i in range(self._particle_count):
                    self._current_particle_idx = i
                    self._prior_particles[i, row:row+process_dim] = npu.to_ndim_1(p.propagate(self._time, self._resampled_particles[i, row:row+process_dim], time))
                self._current_particle_idx = None
            row += process_dim

        self._time = time

        self._resampled_particles_uptodate = False
        self._cached_prior_mean = None
        self._cached_prior_var = None
        
        # TODO Vectorise
        # TODO using fft kde - assumes all weights are equal!
        # TODO This only works when self._state_dim == 1
        if self._predicted_observation_sampler is not None:
            if npu.is_vectorised(self._predicted_observation_sampler):
                self.predicted_observation_particles = self._predicted_observation_sampler(self._prior_particles, self)
            else:
                self.predicted_observation_particles = np.empty((self._particle_count, self._observation_dim))
                for i in range(self._particle_count):
                    self._current_particle_idx = i
                    self.predicted_observation_particles[i,:] = self._predicted_observation_sampler(self._prior_particles[i,:], self)
                self._current_particle_idx = None
            self.predicted_observation = np.average(self.predicted_observation_particles, weights=self._weights, axis=0)
            self.predicted_observation_kde = sm.nonparametric.KDEUnivariate(self.predicted_observation_particles)
            #fft=False, weights=self._weights
            self.predicted_observation_kde.fit()
            # import matplotlib.pyplot as plt
            # fig = plt.figure()
            #x_grid = np.linspace(-4.5, 3.5, 1000)
            #plt.plot(x_grid, kde.evaluate(x_grid))
            #plt.show()
            self.innovationvar = np.var(self.predicted_observation_particles) + self.predicted_observation_kde.bw * self.predicted_observation_kde.bw

        self._state_distr = EmpiricalDistr(particles=self._prior_particles)
            
    def _weight(self, observation):
        if self._predicted_observation_sampler is not None:
            self.innovation = observation - self.predicted_observation
        
        weight_sum = 0.

        if npu.is_vectorised(self._weighting_func):
            self._unnormalised_weights = npu.to_ndim_1(self._weighting_func(observation, self._prior_particles, self))
            weight_sum = np.sum(self._unnormalised_weights)
        else:
            for i in range(self._particle_count):
                self._current_particle_idx = i
                self._unnormalised_weights[i] = npu.toscalar(self._weighting_func(observation, self._prior_particles[i,:], self))
                weight_sum += self._unnormalised_weights[i]
            self._current_particle_idx = None
                
        if weight_sum < ParticleFilter.MIN_WEIGHT_SUM:
            warnings.warn('The sum of weights is less than MIN_WEIGHT_SUM')
            #self._unnormalised_weights[:] = 1. / self._particle_count
            #weight_sum = 1.
        
        self._weights = self._unnormalised_weights / weight_sum
        
        self.effective_sample_size = 1. / np.sum(np.square(self._weights))

        self.log_likelihood += np.log(np.sum(self._unnormalised_weights) / self._particle_count)
        
        self._last_observation = observation
        
        self._cached_posterior_mean = None
        self._cached_posterior_var = None
        
    def _resample(self):
        raise NotImplementedError('Pure virtual method')
        
    def observe(self, observation):
        if self._outlier_threshold is not None:
            if outliers.isoutlier(self.predicted_observation_particles, self.predicted_observation_kde.bw, observation, self._outlier_threshold, 100000, self._random_state):
                print('OUTLIER!!!')
                self._resampled_particles = np.copy(self._prior_particles)
                return False
            else:
                # print('NOT AN OUTLIER!!!')
                pass
        self._weight(observation)
        self._resample()
        return True
        
    @property
    def prior_particles(self):
        return npu.immutablecopyof(self._prior_particles)
    
    @property
    def resampled_particles(self):
        return npu.immutablecopyof(self._resampled_particles)

    @property
    def unnormalised_weights(self):
        return npu.immutablecopyof(self._unnormalised_weights)

    @property
    def weights(self):
        return npu.immutablecopyof(self._weights)

    @property
    def prior_mean(self):
        if self._cached_prior_mean is None:
            self._cached_prior_mean = np.average(self._prior_particles, axis=0)
        return self._cached_prior_mean
    
    @property
    def prior_var(self):
        if self._cached_prior_var is None:
            self._cached_prior_var = np.average((self._prior_particles - self.prior_mean)**2, axis=0)
        return self._cached_prior_var
    
    @property
    def posterior_mean(self):
        if self._cached_posterior_mean is None:
            self._cached_posterior_mean = np.average(self._prior_particles, weights=self._weights, axis=0)
        return self._cached_posterior_mean

    @property
    def posterior_var(self):
        if self._cached_posterior_var is None:
            self._cached_posterior_var = np.average((self._prior_particles - self.posterior_mean)**2, weights=self._weights, axis=0) 
        return self._cached_posterior_var

    @property
    def resampled_mean(self):
        if self._cached_resampled_mean is None:
            self._cached_resampled_mean = np.average(self._resampled_particles, axis=0)
        return self._cached_resampled_mean
    
    @property
    def resampled_var(self):
        if self._cached_resampled_var is None:
            self._cached_resampled_var = np.average((self._resampled_particles - self.resampled_mean)**2, axis=0)
        return self._cached_resampled_var
    
    @property
    def mean(self): return self.resampled_mean
    
    @property
    def var(self): return self.resampled_var
    
    @property
    def last_observation(self): return self._last_observation

    @property
    def particle_count(self): return self._particle_count
    
    @property
    def current_particle_idx(self): return self._current_particle_idx
    
    @property
    def context(self): return self._context
    
class MultinomialResamplingParticleFilter(ParticleFilter):
    def _resample(self):
        counts = self._random_state.multinomial(self._particle_count, self._weights)
        particle_idx = 0
        for i in range(self._particle_count):
            for j in range(counts[i]):  # @UnusedVariable
                self._resampled_particles[particle_idx,:] = self._prior_particles[i,:]
                particle_idx += 1
        
        self._resampled_particles_uptodate = True
        self._cached_resampled_mean = None
        self._cached_resampled_var = None

class RegularisedResamplingParticleFilter(ParticleFilter):
    def _resample(self):
        # TODO This only works when self._state_dim == 1
        # TODO Vectorise
        kde = sm.nonparametric.KDEUnivariate(self._prior_particles)
        kde.fit(fft=False, weights=self._weights)
        counts = self._random_state.multinomial(self._particle_count, self._weights)
        particle_idx = 0
        bw_factor = .5
        for i in range(self._particle_count):
            for j in range(counts[i]):  # @UnusedVariable
                self._resampled_particles[particle_idx,:] = self._prior_particles[i,:]
                particle_idx += 1
        self._resampled_particles[:] += bw_factor * kde.bw * self._random_state.normal(size=(self._particle_count, 1))
        
        self._resampled_particles_uptodate = True
        self._cached_resampled_mean = None
        self._cached_resampled_var = None
            
class SmoothResamplingParticleFilter(ParticleFilter):
    def _resample(self):
        new_weights = np.empty((self._particle_count+1,))
        new_weights[0] = .5*self._weights[0]
        new_weights[self._particle_count] = .5*self._weights[self._particle_count-1]
        for i in range(1, self._particle_count):
            new_weights[i] = .5*(self._weights[i] + self._weights[i-1])

        uniforms = self._random_state.uniform(size=self._particle_count)
        uniforms.sort()
        new_uniforms = np.empty(shape=(self._particle_count,))
        regions = np.empty(shape=(self._particle_count,), dtype=np.int)
        s = 0
        j = 0
        for i in range(self._particle_count + 1):
            s = s + new_weights[i]
            while j < self._particle_count and uniforms[j] <= s:
                regions[j] = i
                new_uniforms[j] = (uniforms[j] - (s - new_weights[i])) / new_weights[i]
                j += 1
                
        for i in range(self._particle_count):
            if regions[i] == 0:
                self._resampled_particles[i,:] = self._prior_particles[0,:]
            if regions[i] == self._particle_count:
                self._resampled_particles[i,:] = self._prior_particles[self._particle_count-1,:]
            else:
                self._resampled_particles[i,:] = (self._prior_particles[regions[i],:] - self._prior_particles[regions[i]-1,:]) * new_uniforms[i] + self._prior_particles[regions[i]-1,:]   
            
        self._resampled_particles_uptodate = True
        self._cached_resampled_mean = None
        self._cached_resampled_var = None
