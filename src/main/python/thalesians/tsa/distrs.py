import numpy as np

import thalesians.tsa.checks as checks
import thalesians.tsa.numpychecks as npc
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.randomness as rnd
import thalesians.tsa.stats as stats
from thalesians.tsa.strings import ToStringHelper

class Distr(object):
    def __init__(self):
        self._to_string_helper_Distr = None
        self._str_Distr = None

    @property
    def dim(self):
        raise NotImplementedError()
    
    @property
    def mean(self):
        raise NotImplementedError()
    
    @property
    def cov(self):
        raise NotImplementedError()
    
    def sample(self, size=1, random_state=None):
        raise NotImplementedError()

    def to_string_helper(self):
        if self._to_string_helper_Distr is None:
            self._to_string_helper_Distr = ToStringHelper(self)
        return self._to_string_helper_Distr
    
    def __str__(self):
        if self._str_Distr is None: self._str_Distr = self.to_string_helper().to_string()
        return self._str_Distr

    def __repr__(self):
        return str(self)
    
class WideSenseDistr(Distr):
    def __init__(self, mean=None, cov=None, vol=None, dim=None, copy=True, do_not_init=False):
        if not do_not_init:
            if mean is not None and dim is not None and np.size(mean) == 1:
                mean = npu.col_of(dim, npu.to_scalar(mean))
            
            if mean is None and vol is None and cov is None:
                self._dim = 1 if dim is None else dim
                mean = npu.col_of(self._dim, 0.)
                cov = np.eye(self._dim)
                vol = np.eye(self._dim)
                
            self._dim, self._mean, self._vol, self._cov = None, None, None, None
            
            # TODO We don't currently check whether cov and vol are consistent, i.e. that cov = np.dot(vol, vol.T) -- should we?
            
            if mean is not None:
                self._mean = npu.to_ndim_2(mean, ndim_1_to_col=True, copy=copy)
                self._dim = npu.nrow(self._mean)
            if cov is not None:
                self._cov = npu.to_ndim_2(cov, ndim_1_to_col=True, copy=copy)
                self._dim = npu.nrow(self._cov)
            if vol is not None:
                self._vol = npu.to_ndim_2(vol, ndim_1_to_col=True, copy=copy)
                self._dim = npu.nrow(self._vol)
            
            if self._mean is None: self._mean = npu.col_of(self._dim, 0.)
            if self._cov is None and self._vol is None:
                self._cov = np.eye(self._dim)
                self._vol = np.eye(self._dim)
            npc.check_col(self._mean)
            npc.check_nrow(self._mean, self._dim)
            if self._cov is not None:
                npc.check_nrow(self._cov, self._dim)
                npc.check_square(self._cov)
            if self._vol is not None:
                npc.check_nrow(self._vol, self._dim)
            
            npu.make_immutable(self._mean)
            if self._cov is not None: npu.make_immutable(self._cov)
            if self._vol is not None: npu.make_immutable(self._vol)
        
        self._to_string_helper_WideSenseDistr = None
        self._str_WideSenseDistr = None
        
        super().__init__()
        
    @property
    def dim(self):
        return self._dim
    
    @property
    def mean(self):
        return self._mean
    
    @property
    def cov(self):
        if self._cov is None:
            self._cov = stats.vol_to_cov(self._vol)
        return self._cov
    
    @property
    def vol(self):
        if self._vol is None:
            self._vol = stats.cov_to_vol(self._cov)
        return self._vol
    
    def __eq__(self, other):
        if isinstance(other, WideSenseDistr):
            if self.dim != other.dim: return False
            if not np.array_equal(self.mean, other.mean): return False
            return np.array_equal(self.cov, other.cov)
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def to_string_helper(self):
        if self._to_string_helper_WideSenseDistr is None:
            self._to_string_helper_WideSenseDistr = super().to_string_helper() \
                    .set_type(self) \
                    .add('mean', self.mean) \
                    .add('cov', self.cov)
        return self._to_string_helper_WideSenseDistr
    
    def __str__(self):
        if self._str_WideSenseDistr is None: self._str_WideSenseDistr = self.to_string_helper().to_string()
        return self._str_WideSenseDistr

class NormalDistr(WideSenseDistr):
    def __init__(self, mean=None, cov=None, vol=None, dim=None, copy=True):
        super().__init__(mean, cov, vol, dim, copy)

    @staticmethod
    def approximate(distr, copy=True):
        if isinstance(distr, NormalDistr) and not copy: return distr
        return NormalDistr(distr.mean, distr.cov, None, distr.dim, copy)

    def sample(self, size=1, random_state=None):
        return rnd.multivariate_normal(self.mean, self.cov, size=size, random_state=random_state)

    def __eq__(self, other):
        if isinstance(other, NormalDistr):
            if self.dim != other.dim: return False
            if not np.array_equal(self.mean, other.mean): return False
            return np.array_equal(self.cov, other.cov)
        return False

class DiracDeltaDistr(NormalDistr):
    def __init__(self, mean=None, dim=None, copy=True):
        if mean is not None and dim is not None and np.size(mean) == 1:
            mean = npu.col_of(dim, npu.to_scalar(mean))
        
        if mean is None:
            dim = 1 if dim is None else dim
            mean = npu.col_of(dim, 0.)
            

        self._mean = npu.to_ndim_2(mean, ndim_1_to_col=True, copy=copy)
        if dim is None: dim = npu.nrow(self._mean)
        self._dim = dim

        npc.check_col(self._mean)
        npc.check_nrow(self._mean, self._dim)
            
        npu.make_immutable(self._mean)
        
        self._zero_cov = None
        
        self._to_string_helper_DiracDeltaDistr = None
        self._str_DiracDeltaDistr = None
        
    @staticmethod
    def create(value=None, dim=None):
        return DiracDeltaDistr(value, dim)

    @property
    def cov(self):
        if self._zero_cov is None:
            self._zero_cov = np.zeros((self._dim, self._dim))
        return self._zero_cov
    
    @property
    def vol(self):
        return self.cov

    def to_string_helper(self):
        if self._to_string_helper_DiracDeltaDistr is None:
            self._to_string_helper_DiracDeltaDistr = ToStringHelper(self).add('mean', self._mean)
        return self._to_string_helper_DiracDeltaDistr 
    
    def __str__(self):
        if self._str_DiracDeltaDistr is None: self._str_DiracDeltaDistr = self.to_string_helper().to_string()
        return self._str_DiracDeltaDistr

class LogNormalDistr(WideSenseDistr):
    def __init__(self, mean_of_log=None, cov_of_log=None, vol_of_log=None, dim=None, copy=True):
        if mean_of_log is not None and dim is not None and np.size(mean_of_log) == 1:
            mean_of_log = npu.col_of(dim, npu.to_scalar(mean_of_log))
        
        if mean_of_log is None and vol_of_log is None and cov_of_log is None:
            self._dim = 1 if dim is None else dim
            mean_of_log = npu.col_of(self._dim, 0.)
            cov_of_log = np.eye(self._dim)
            vol_of_log = np.eye(self._dim)
            
        self._dim, self._mean_of_log, self._vol_of_log, self._cov_of_log = None, None, None, None
        
        # TODO We don't currently check whether cov_of_log and vol_of_log are consistent, i.e. that cov_of_log = np.dot(vol_of_log, vol_of_log.T) -- should we?
        
        if mean_of_log is not None:
            self._mean_of_log = npu.to_ndim_2(mean_of_log, ndim_1_to_col=True, copy=copy)
            self._dim = npu.nrow(self._mean_of_log)
        if cov_of_log is not None:
            self._cov_of_log = npu.to_ndim_2(cov_of_log, ndim_1_to_col=True, copy=copy)
            self._dim = npu.nrow(self._cov_of_log)
        if vol_of_log is not None:
            self._vol_of_log = npu.to_ndim_2(vol_of_log, ndim_1_to_col=True, copy=copy)
            self._dim = npu.nrow(self._vol_of_log)
        
        if self._mean_of_log is None: self._mean_of_log = npu.col_of(self._dim, 0.)
        if self._cov_of_log is None and self._vol_of_log is None:
            self._cov_of_log = np.eye(self._dim)
            self._vol_of_log = np.eye(self._dim)
        npc.check_col(self._mean_of_log)
        npc.check_nrow(self._mean_of_log, self._dim)
        if self._cov_of_log is not None:
            npc.check_nrow(self._cov_of_log, self._dim)
            npc.check_square(self._cov_of_log)
        if self._vol_of_log is not None:
            npc.check_nrow(self._vol_of_log, self._dim)

        if self._cov_of_log is None: self._cov_of_log = stats.vol_to_cov(self._vol_of_log)
        if self._vol_of_log is None: self._vol_of_log = stats.cov_to_vol(self._cov_of_log)
            
        npu.make_immutable(self._mean_of_log)
        npu.make_immutable(self._cov_of_log)
        npu.make_immutable(self._vol_of_log)

        mean = np.exp(self._mean_of_log + .5 * npu.col(*[self._cov_of_log[i,i] for i in range(self._dim)]))
        cov = np.array([[np.exp(self._mean_of_log[i,0] + self._mean_of_log[j,0] + .5 * (self._cov_of_log[i,i] + self._cov_of_log[j,j])) * (np.exp(self._cov_of_log[i,j]) - 1.) for j in range(self._dim)] for i in range(self._dim)])
        vol = stats.cov_to_vol(cov)
        
        self._to_string_helper_LogNormalDistr = None
        self._str_LogNormalDistr = None
        
        super().__init__(mean, cov, vol, self._dim, copy)

    @property
    def mean_of_log(self):
        return self._mean_of_log
    
    @property
    def vol_of_log(self):
        return self._vol_of_log

    @property
    def cov_of_log(self):
        return self._cov_of_log

    def sample(self, size=1, random_state=None):
        return rnd.multivariate_lognormal(self.mean_of_log, self.cov_of_log, size=size, random_state=random_state)
    
    def __eq__(self, other):
        if isinstance(other, LogNormalDistr):
            if self.dim != other.dim: return False
            if not np.array_equal(self.mean_of_log, other.mean_of_log): return False
            return np.array_equal(self.cov_of_log, other.cov_of_log)
        return False
    
    def to_string_helper(self):
        if self._to_string_helper_LogNormalDistr is None:
            self._to_string_helper_LogNormalDistr = super().to_string_helper() \
                    .set_type(self) \
                    .add('mean_of_log', self._mean_of_log) \
                    .add('cov_of_log', self._cov_of_log)
        return self._to_string_helper_LogNormalDistr
    
    def __str__(self):
        if self._str_LogNormalDistr is None: self._str_LogNormalDistr = self.to_string_helper().to_string()
        return self._str_LogNormalDistr

# Formulae for means and covariances of weighted samples can be found in
#
# George R. Price. Extension of covariance selection mathematics. Ann. Hum. Genet., Lond. (1972), 35, 485 - 490.
#
# See the reference on https://stats.stackexchange.com/questions/61225/correct-equation-for-weighted-unbiased-sample-covariance
class EmpiricalDistr(WideSenseDistr):
    def __init__(self, particles=None, weights=None, dim=None, use_n_minus_1_stats=False, sampler=None, copy=True):
        self._particles, self._weights, self._dim = None, None, None

        if particles is not None:
            self._particles = npu.to_ndim_2(particles, ndim_1_to_col=True, copy=copy)
            self._dim = npu.ncol(self._particles)
            if weights is None:
                weights = np.ones((npu.nrow(self._particles), 1))
                weights /= float(npu.nrow(self._particles))

        if weights is not None:
            checks.check_not_none(particles)
            self._weights = npu.to_ndim_2(weights, ndim_1_to_col=True, copy=copy)
            self._dim = npu.ncol(self._particles)

        if dim is not None:
            self._dim = dim

        if self._particles is not None:
            npc.check_ncol(self._particles, self._dim)
        if self._weights is not None:
            npc.check_nrow(self._weights, npu.nrow(self._particles))

        npu.make_immutable(self._particles, allow_none=True)
        npu.make_immutable(self._weights, allow_none=True)

        self._use_n_minus_1_stats = use_n_minus_1_stats

        # "n minus 1" (unbiased) stats only make sense when using "repeat"-type weights, meaning that each weight
        # represents the number of occurrences of one observation.
        #
        # See https://stats.stackexchange.com/questions/61225/correct-equation-for-weighted-unbiased-sample-covariance

        self._effective_particle_count = None
        self._weight_sum = None
        self._mean = None
        self._var_n = None
        self._var_n_minus_1 = None
        self._cov_n = None
        self._cov_n_minus_1 = None
        self._vol_n = None
        self._vol_n_minus_1 = None

        self._to_string_helper_EmpiricalDistr = None
        self._str_EmpiricalDistr = None
        
        super().__init__(do_not_init=True)

    @property
    def dim(self):
        return self._dim

    @property
    def particle_count(self):
        return npu.nrow(self._particles) if self._particles is not None else 0
    
    @property
    def effective_particle_count(self):
        # Using Kish's approximate formula for computing the effective sample size: 
        # http://surveyanalysis.org/wiki/Design_Effects_and_Effective_Sample_Size#Kish.27s_approximate_formula_for_computing_effective_sample_size
        if self._effective_particle_count is None:
            self._effective_particle_count = 1.0 / np.sum(self.normalised_weights ** 2)
        return self._effective_particle_count

    @property
    def particles(self):
        return self._particles

    def particle(self, idx):
        if self.particle_count == 0: raise IndexError('The empirical distribution has no particles')
        return npu.to_ndim_2(self._particles[idx,:], ndim_1_to_col=True, copy=False)

    @property
    def weights(self):
        return self._weights

    def weight(self, idx):
        if self.particle_count == 0: raise IndexError('The empirical distribution has no particles')
        return self._weights[idx,0]

    @property
    def weight_sum(self):
        if self._weight_sum is None:
            self._weight_sum = np.sum(self._weights)
        return self._weight_sum

    @property
    def normalised_weights(self):
        return self.weights / self.weight_sum
    
    def normalised_weight(self, idx):
        return self.weight(idx) / self.weight_sum

    @property
    def mean(self):
        if self._mean is None:
            self._mean = np.average(self._particles, weights=self._weights.flat, axis=0)
            self._mean = npu.to_ndim_2(self._mean, ndim_1_to_col=True, copy=False)
            npu.make_immutable(self._mean)
        return self._mean

    @property
    def var_n(self):
        if self._var_n is None:
            self._var_n = np.average((self._particles - self.mean.T)**2, weights=self._weights.flat, axis=0)
            self._var_n = npu.to_ndim_2(self._var_n, ndim_1_to_col=True, copy=False)
            npu.make_immutable(self._var_n)
        return self._var_n

    @property
    def var_n_minus_1(self):
        if self._var_n_minus_1 is None:
            self._var_n_minus_1 = self.var_n * self.weight_sum / (self.weight_sum - 1.)
            npu.make_immutable(self._var_n_minus_1)
        return self._var_n_minus_1

    @property
    def var(self):
        return self.var_n_minus_1 if self._use_n_minus_1_stats else self.var_n

    @property
    def cov_n(self):
        if self._cov_n is None:
            self._cov_n = np.sum([self.weight(i) * np.dot(self.particle(i) - self.mean, (self.particle(i) - self.mean).T) for i in range(self.particle_count)], axis=0)
            # The following is more efficient:
            # self._cov_n = np.dot(self._particles.T - self.mean, self.particles - self.mean.T)
            self._cov_n /= self.weight_sum
            npu.make_immutable(self._cov_n)
        return self._cov_n

    @property
    def cov_n_minus_1(self):
        if self._cov_n_minus_1 is None:
            self._cov_n_minus_1 = np.sum([self.weight(i) * np.dot(self.particle(i) - self.mean, (self.particle(i) - self.mean).T) for i in range(self.particle_count)], axis=0)
            # The following is more efficient:
            # self._cov_n_minus_1 = np.dot(self._particles.T - self.mean, self.particles - self.mean.T)
            self._cov_n_minus_1 /= self.weight_sum - 1.
            npu.make_immutable(self._cov_n_minus_1)
        return self._cov_n_minus_1

    @property
    def cov(self):
        return self.cov_n_minus_1 if self._use_n_minus_1_stats else self.cov_n

    @property
    def vol_n(self):
        if self._vol_n is None:
            self._vol_n = stats.cov_to_vol(self.cov_n)
            npu.make_immutable(self._vol_n)
        return self._vol_n

    @property
    def vol_n_minus_1(self):
        if self._vol_n_minus_1 is None:
            self._vol_n_minus_1 = stats.cov_to_vol(self.cov_n_minus_1)
            npu.make_immutable(self._vol_n_minus_1)
        return self._vol_n_minus_1

    @property
    def vol(self):
        return self.vol_n_minus_1 if self._use_n_minus_1_stats else self.vol_n

    def sample(self, size=1, random_state=None):
        return multinomial_resample(self, target_particle_count=size, random_state=random_state).particles
    
    def __eq__(self, other):
        if isinstance(other, EmpiricalDistr):
            if self._dim != other._dim: return False
            if checks.is_exactly_one_not_none(self._particles, other._particles): return False
            if checks.is_exactly_one_not_none(self._weights, other._weights): return False
            if self._particles is not None:
                if not np.array_equal(self._particles, other._particles): return False
            if self._weights is not None:
                if not np.array_equal(self._weights, other._weights): return False
            return True
        return False
    
    def to_string_helper(self):
        if self._to_string_helper_EmpiricalDistr is None:
            self._to_string_helper_EmpiricalDistr = super().to_string_helper() \
                    .set_type(self) \
                    .add('particle_count', self.particle_count) \
                    .add('dim', self.dim)
        return self._to_string_helper_EmpiricalDistr
    
    def __str__(self):
        if self._str_EmpiricalDistr is None: self._str_EmpiricalDistr = self.to_string_helper().to_string()
        return self._str_EmpiricalDistr
    
def multinomial_resample(empirical_distr, target_particle_count=None, random_state=None):
    if target_particle_count is None: target_particle_count = empirical_distr.particle_count
    if random_state is None: random_state = rnd.random_state()
    counts = rnd.multinomial(target_particle_count, npu.to_ndim_1(empirical_distr.normalised_weights))
    assert np.sum(counts) == target_particle_count
    particle_idx = 0
    resampled_particles = np.empty((target_particle_count, np.shape(empirical_distr.particles)[1]))
    for i in range(empirical_distr.particle_count):
        for _ in range(counts[i]):
            resampled_particles[particle_idx,:] = npu.to_ndim_1(empirical_distr.particle(i))
            particle_idx += 1
    return EmpiricalDistr(particles=resampled_particles, weights=np.ones((target_particle_count,)))

'''
class RegularisedResamplingParticleFilter(ParticleFilter):
    def _resample(self):
        # TODO This only works when state_dim == 1
        # TODO Vectorise
        kde = sm.nonparametric.KDEUnivariate(self._prior_particles)
        kde.fit(fft=False, weights=self._weights)
        counts = self._random_state.multinomial(self.particle_count, self._weights)
        particle_idx = 0
        bw_factor = .5
        for i in range(self.particle_count):
            for j in range(counts[i]):  # @UnusedVariable
                self._resampled_particles[particle_idx,:] = self._prior_particles[i,:]
                particle_idx += 1
        self._resampled_particles[:] += bw_factor * kde.bw * self._random_state.normal(size=(self.particle_count, 1))
        
        self._resampled_particles_uptodate = True
        self._cached_resampled_mean = None
        self._cached_resampled_var = None
            
class SmoothResamplingParticleFilter(ParticleFilter):
    def _resample(self):
        new_weights = np.empty((self.particle_count+1,))
        new_weights[0] = .5*self._weights[0]
        new_weights[self.particle_count] = .5*self._weights[self.particle_count-1]
        for i in range(1, self.particle_count):
            new_weights[i] = .5*(self._weights[i] + self._weights[i-1])

        uniforms = self._random_state.uniform(size=self.particle_count)
        uniforms.sort()
        new_uniforms = np.empty(shape=(self.particle_count,))
        regions = np.empty(shape=(self.particle_count,), dtype=np.int)
        s = 0
        j = 0
        for i in range(self.particle_count + 1):
            s = s + new_weights[i]
            while j < self.particle_count and uniforms[j] <= s:
                regions[j] = i
                new_uniforms[j] = (uniforms[j] - (s - new_weights[i])) / new_weights[i]
                j += 1
                
        for i in range(self.particle_count):
            if regions[i] == 0:
                self._resampled_particles[i,:] = self._prior_particles[0,:]
            if regions[i] == self.particle_count:
                self._resampled_particles[i,:] = self._prior_particles[self.particle_count-1,:]
            else:
                self._resampled_particles[i,:] = (self._prior_particles[regions[i],:] - self._prior_particles[regions[i]-1,:]) * new_uniforms[i] + self._prior_particles[regions[i]-1,:]   
            
        self._resampled_particles_uptodate = True
        self._cached_resampled_mean = None
        self._cached_resampled_var = None

class Sampler(object):
    def __init__(self, particles, weights):
        pass

    def sample(self):
        raise NotImplementedError()

class SimpleSampler(Sampler):
    def __init__(self):
        super(SimpleSampler, self).__init__()

class KDESampler(Sampler):
    def __init__(self):
        super(KDESampler, self).__init__()
'''
