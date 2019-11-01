import datetime as dt

import numpy as np
import scipy.linalg as la

import thalesians.tsa.checks as checks
import thalesians.tsa.distrs as distrs
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.numpychecks as npc
import thalesians.tsa.randomness as rnd
import thalesians.tsa.stats as stats
from thalesians.tsa.strings import ToStringHelper

class Process(object):
    def __init__(self, **kwargs):
        self._to_string_helper_Process = None
        self._str_Process = None
        
        try:
            super(Process, self).__init__(**kwargs)
        except TypeError:
            super(Process, self).__init__()
            
    def to_string_helper(self):
        if self._to_string_helper_Process is None:
            self._to_string_helper_Process = ToStringHelper(self)
        return self._to_string_helper_Process
    
    def __str__(self):
        if self._str_Process is None: self._str_Process = self.to_string_helper().to_string()
        return self._str_Process
    
    def __repr__(self):
        return str(self)

class ItoProcess(Process):
    def __init__(self, process_dim=1, noise_dim=None, drift=None, diffusion=None, **kwargs):
        self._process_dim = process_dim
        self._noise_dim = process_dim if noise_dim is None else noise_dim
        # Note: the brackets around the lambdas below are essential, otherwise the result of the parsing will not be what we need:
        self._drift = (lambda t, x: npu.row_of(self._process_dim, 0.)) if drift is None else drift
        self._diffusion = (lambda t, x: npu.matrix_of(self._process_dim, self._noise_dim, 0.)) if diffusion is None else diffusion
        #if not checks.is_callable(self._drift): self._drift = lambda t, x: self._drift
        #if not checks.is_callable(self._diffusion): self._diffusion = lambda t, x: self._diffusion
        self._to_string_helper_ItoProcess = None
        self._str_ItoProcess = None
        
        super(ItoProcess, self).__init__(process_dim=self._process_dim, noise_dim=self._noise_dim,
                drift=self._drift, diffusion=self._diffusion, **kwargs)
        
    @property
    def process_dim(self):
        return self._process_dim
    
    @property
    def noise_dim(self):
        return self._noise_dim
    
    @property
    def drift(self):
        return self._drift
    
    @property
    def diffusion(self):
        return self._diffusion
    
    def to_string_helper(self):
        if self._to_string_helper_ItoProcess is None:
            self._to_string_helper_ItoProcess = super().to_string_helper() \
                    .set_type(self) \
                    .add('process_dim', self._process_dim) \
                    .add('noise_dim', self._noise_dim)
        return self._to_string_helper_ItoProcess
    
    def __str__(self):
        if self._str_ItoProcess is None: self._str_ItoProcess = self.to_string_helper().to_string()
        return self._str_ItoProcess
    
class SolvedItoProcess(ItoProcess):
    def __init__(self, process_dim=1, noise_dim=None, drift=None, diffusion=None, **kwargs):
        self._to_string_helper_SolvedItoProcess = None
        self._str_SolvedItoProcess = None

        super(SolvedItoProcess, self).__init__(process_dim=process_dim, noise_dim=noise_dim,
                drift=drift, diffusion=diffusion, **kwargs)
        
    def propagate(self, time0, value0, time, variate=None, state0=None, random_state=None):
        raise NotImplementedError()
    
    def to_string_helper(self):
        if self._to_string_helper_SolvedItoProcess is None:
            self._to_string_helper_SolvedItoProcess = super().to_string_helper().set_type(self)
        return self._to_string_helper_SolvedItoProcess
    
    def __str__(self):
        if self._str_SolvedItoProcess is None: self._str_SolvedItoProcess = self.to_string_helper().to_string()
        return self._str_SolvedItoProcess

class MarkovProcess(Process):
    def __init__(self, process_dim, time_unit=dt.timedelta(days=1), **kwargs):
        self._process_dim = checks.check_int(process_dim)
        self._time_unit = time_unit
        
        self._cached_time = None
        self._cached_time0 = None
        self._cached_distr0 = None
        self._cached_distr = None
        
        self._to_string_helper_MarkovProcess = None
        self._str_MarkovProcess = None
        
        super(MarkovProcess, self).__init__(process_dim=process_dim, **kwargs)
        
    def propagate_distr(self, time0, distr0, time, assume_distr=False):
        if time == time0: return distr0
        if self._cached_time is None or self._cached_time != time or self._cached_time0 != time0 or self._cached_distr0 != distr0:
            time_delta = time - time0
            if isinstance(time_delta, np.timedelta64):
                time_delta = time_delta.item()
            if isinstance(time_delta, dt.timedelta):
                time_delta = time_delta.total_seconds() / self._time_unit.total_seconds()
            self._cached_distr = self._propagate_distr_impl(distr0, time_delta, assume_distr)
            self._cached_time = time
            self._cached_time0 = time0
            self._cached_distr0 = distr0
        return self._cached_distr
    
    def _propagate_distr_impl(self, distr0, time_delta, assume_distr=False):
        raise NotImplementedError()
    
    def to_string_helper(self):
        if self._to_string_helper_MarkovProcess:
            self._to_string_helper_MarkovProcess = super().to_string_helper() \
                    .set_type(self) \
                    .add('process_dim', self._process_dim)
        return self._to_string_helper_MarkovProcess
    
    def __str__(self):
        if self._str_MarkovProcess is None: self._str_MarkovProcess = self.to_string_helper().to_string()
        return self._str_MarkovProcess
    
class SolvedItoMarkovProcess(MarkovProcess, SolvedItoProcess):
    def __init__(self, process_dim=1, noise_dim=None, drift=None, diffusion=None, time_unit=dt.timedelta(days=1), **kwargs):
        self._to_string_helper_SolvedItoMarkovProcess = None
        self._str_SolvedItoMarkovProcess = None
        
        super(SolvedItoMarkovProcess, self).__init__(process_dim=process_dim, noise_dim=noise_dim,
                drift=drift, diffusion=diffusion, time_unit=time_unit, **kwargs)
    
    def propagate(self, time0, value0, time, variate=None, state0=None, random_state=None):
        if self.noise_dim != self.process_dim:
            raise NotImplementedError('Cannot utilise the propagate_distr of the Markov process in propagate if noise_dim != process_dim; provide a custom implementation')
        if time == time0: return npu.to_ndim_2(value0, ndim_1_to_col=True, copy=True)
        value0 = npu.to_ndim_2(value0, ndim_1_to_col=True, copy=False)
        if variate is None:
            if random_state is None: random_state = rnd.random_state()
            variate = random_state.normal(size=self.noise_dim)
        variate = npu.to_ndim_2(variate, ndim_1_to_col=True, copy=False)
        distr = self.propagate_distr(time, time0, distrs.DiracDeltaDistr.create(value0), assume_distr=True)
        return distr.mean + np.dot(np.linalg.cholesky(distr.cov), variate)
    
    def to_string_helper(self):
        if self._to_string_helper_SolvedItoMarkovProcess is None:
            self._to_string_helper_SolvedItoMarkovProcess = ToStringHelper(self) \
                    .add('process_dim', self.process_dim) \
                    .add('noise_dim', self.noise_dim)
        return self._to_string_helper_SolvedItoMarkovProcess

    def __str__(self):
        if self.str_SolvedItoMarkovProcess is None:
            self.str_SolvedItoMarkovProcess = self.to_string_helper().to_string()
        return self.str_SolvedItoMarkovProcess
    
    def __repr__(self):
        return str(self)

# TODO To be implemented
class KalmanProcess(MarkovProcess):
    def __init__(self):
        pass
    
class WienerProcess(SolvedItoMarkovProcess):
    def __init__(self, mean=None, vol=None, time_unit=dt.timedelta(days=1)):
        if mean is None and vol is None:
            mean = 0.; vol = 1.
        
        self._mean, self._vol = None, None
        
        if mean is not None:
            self._mean = npu.to_ndim_2(mean, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self._mean)
        if vol is not None:
            self._vol = npu.to_ndim_2(vol, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self._vol)
        
        if self._mean is None: self._mean = npu.col_of(process_dim, 0.)
        if self._vol is None: self._vol = np.eye(process_dim)
        
        npc.check_col(self._mean)
        npc.check_nrow(self._mean, process_dim)
        npc.check_nrow(self._vol, process_dim)
        
        noise_dim = npu.ncol(self._vol)
        self._cov = stats.vol_to_cov(self._vol)
        
        npu.make_immutable(self._mean)
        npu.make_immutable(self._vol)
        npu.make_immutable(self._cov)
        
        self._to_string_helper_WienerProcess = None
        self._str_WienerProcess = None
        
        super(WienerProcess, self).__init__(process_dim=process_dim, noise_dim=noise_dim,
                drift=lambda t, x: self._mean, diffusion=lambda t, x: self._vol,
                time_unit=time_unit)
        
    @staticmethod
    def create_2d(mean1, mean2, sd1, sd2, cor):
        return WienerProcess(npu.col(mean1, mean2), stats.make_vol_2d(sd1, sd2, cor))
    
    @staticmethod
    def create_from_cov(mean, cov):
        vol = None if cov is None else stats.cov_to_vol(cov)
        return WienerProcess(mean, vol)
    
    @property
    def mean(self):
        return self._mean
    
    @property
    def vol(self):
        return self._vol
    
    @property
    def cov(self):
        return self._cov
    
    def propagate(self, time0, value0, time, variate=None, state0=None, random_state=None):
        if time == time0: return npu.to_ndim_2(value0, ndim_1_to_col=True, copy=True)
        value0 = npu.to_ndim_2(value0, ndim_1_to_col=True, copy=False)
        if variate is None:
            if random_state is None: random_state = rnd.random_state()
            variate = random_state.normal(size=self.noise_dim)
        variate = npu.to_ndim_2(variate, ndim_1_to_col=True, copy=False)
        time_delta = time - time0
        if isinstance(time_delta, np.timedelta64):
            time_delta = time_delta.item()
        if isinstance(time_delta, dt.timedelta):
            time_delta = time_delta.total_seconds() / self._time_unit.total_seconds()
        return value0 + self._mean * time_delta + np.dot(self._vol, np.sqrt(time_delta) * variate)
    
    def _propagate_distr_impl(self, distr0, time_delta, assume_distr=False):
        if not isinstance(distr0, distrs.NormalDistr) and not assume_distr:
            raise ValueError('Do not know how to propagate a distribution that is not normal')
        mean = distr0.mean + self._mean * time_delta
        cov = distr0.cov + time_delta * self._cov
        return distrs.NormalDistr(mean=mean, cov=cov)
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._mean == other._mean and self._vol == other._vol
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def to_string_helper(self):
        if self._to_string_helper_WienerProcess is None:
            self._to_string_helper_WienerProcess = super().to_string_helper() \
                    .set_type(self) \
                    .add('mean', self._mean) \
                    .add('vol', self._vol)
        return self._to_string_helper_WienerProcess

    def __str__(self):
        if self._str_WienerProcess is None: self._str_WienerProcess = self.to_string_helper().to_string()
        return self._str_WienerProcess

class GeometricBrownianMotion(SolvedItoMarkovProcess):
    def __init__(self, pct_drift=None, pct_vol=None, time_unit=dt.timedelta(days=1)):
        if pct_drift is None and pct_vol is None:
            pct_drift = 0.; pct_vol = 1.
        
        self._pct_drift, self._pct_vol = None, None
        
        if pct_drift is not None:
            self._pct_drift = npu.to_ndim_2(pct_drift, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self._pct_drift)
        if pct_vol is not None:
            self._pct_vol = npu.to_ndim_2(pct_vol, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self._pct_vol)
        
        if self._pct_drift is None: self._pct_drift = npu.col_of(process_dim, 0.)
        if self._pct_vol is None: self._pct_vol = np.eye(process_dim)
        
        npc.check_col(self._pct_drift)
        npc.check_nrow(self._pct_drift, process_dim)
        npc.check_nrow(self._pct_vol, process_dim)
        
        noise_dim = npu.ncol(self._pct_vol)
        self._pct_cov = stats.vol_to_cov(self._pct_vol)
        
        npu.make_immutable(self._pct_drift)
        npu.make_immutable(self._pct_vol)
        npu.make_immutable(self._pct_cov)
        
        self._to_string_helper_GeometricBrownianMotion = None
        self._str_GeometricBrownianMotion = None
        
        super(GeometricBrownianMotion, self).__init__(process_dim=process_dim, noise_dim=noise_dim,
                drift=lambda t, x: self._pct_drift * x,
                diffusion=lambda t, x: x * self._pct_vol,
                time_unit=time_unit)
        
    @staticmethod
    def create_2d(pct_drift1, pct_drift2, pct_sd1, pct_sd2, pct_cor):
        return GeometricBrownianMotion(npu.col(pct_drift1, pct_drift2), stats.make_vol_2d(pct_sd1, pct_sd2, pct_cor))
    
    @staticmethod
    def create_from_pct_cov(pct_drift, pct_cov):
        pct_vol = None if pct_cov is None else stats.cov_to_vol(pct_cov)
        return GeometricBrownianMotion(pct_drift, pct_vol)
    
    @property
    def pct_drift(self):
        return self._pct_drift
    
    @property
    def pct_vol(self):
        return self._pct_vol
    
    @property
    def pct_cov(self):
        return self._pct_cov
    
    def propagate(self, time0, value0, time, variate=None, state0=None, random_state=None):
        if time == time0: return npu.to_ndim_2(value0, ndim_1_to_col=True, copy=True)
        value0 = npu.to_ndim_2(value0, ndim_1_to_col=True, copy=False)
        if variate is None:
            if random_state is None: random_state = rnd.random_state()
            variate = random_state.normal(size=self.noise_dim)
        variate = npu.to_ndim_2(variate, ndim_1_to_col=True, copy=False)
        time_delta = time - time0
        if isinstance(time_delta, np.timedelta64):
            time_delta = time_delta.item()
        if isinstance(time_delta, dt.timedelta):
            time_delta = time_delta.total_seconds() / self._time_unit.total_seconds()
        return value0 * np.exp(
                (self._pct_drift - .5 * npu.col(*np.sum(self._pct_vol**2, axis=1))) * time_delta + \
                np.dot(self._pct_vol, np.sqrt(time_delta) * variate))
    
    def _propagate_distr_impl(self, distr0, time_delta, assume_distr=False):
        if not isinstance(distr0, distrs.LogNormalDistr) and not assume_distr:
            raise ValueError('Do not know how to propagate a distribution that is not log-normal')
        # Note: the sum of two independent log-normal distributions is only approximately log-normal
        mean = np.log(distr0.mean) + (self._pct_drift - .5 * npu.col([self._pct_cov[i, i] for i in range(self.process_dim)])) * time_delta
        cov = distr0.cov + time_delta * self._pct_cov
        return distrs.LogNormalDistr(mean_of_log=mean, cov_of_log=cov)
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._pct_drift == other._pct_drift and self._pct_vol == other._pct_vol
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def to_string_helper(self):
        if self._to_string_helper_GeometricBrownianMotion is None:
            self._to_string_helper_GeometricBrownianMotion = super().to_string_helper() \
                    .set_type(self) \
                    .add('pct_drift', self._pct_drift) \
                    .add('pct_vol', self._pct_vol)
        return self._to_string_helper_GeometricBrownianMotion

    def __str__(self):
        if self._str_GeometricBrownianMotion is None: self._str_GeometricBrownianMotion = self.to_string_helper().to_string()
        return self._str_GeometricBrownianMotion

class BrownianBridge(SolvedItoMarkovProcess):
    def __init__(self, initial_value=None, final_value=None, initial_time=0., final_time=1., vol=None, time_unit=dt.timedelta(days=1)):
        process_dim = 1

        self.__initial_value = None
        self.__final_value = None
        if initial_value is not None:
            self.__initial_value = npu.to_ndim_2(initial_value, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self.__initial_value)
        if final_value is not None:
            self.__final_value = npu.to_ndim_2(final_value, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self.__final_value)
        if self.__initial_value is None:
            self.__initial_value = npu.col_of(process_dim, 0.)
        if self.__final_value is None:
            self.__final_value = npu.col_of(process_dim, 0.)

        self.__vol = None
        if vol is not None:
            self.__vol = npu.to_ndim_2(vol, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self.__vol)
        if self.__vol is None: self.__vol = np.eye(process_dim)

        self.__initial_time = initial_time
        self.__final_time = final_time

        npc.check_col(self.__initial_value)
        npc.check_col(self.__final_value)
        npc.check_nrow(self.__initial_value, process_dim)
        npc.check_nrow(self.__final_value, process_dim)
        
        noise_dim = npu.ncol(self.__vol)
        self.__cov = stats.vol_to_cov(self.__vol)
        
        npu.make_immutable(self.__initial_value)
        npu.make_immutable(self.__final_value)
        npu.make_immutable(self.__vol)
        npu.make_immutable(self.__cov)

        self._to_string_helper_BrownianBridge = None
        self._str_BrownianBridge = None

        super(BrownianBridge, self).__init__(process_dim=process_dim, noise_dim=noise_dim,
                drift=lambda t, x: (self.__final_value - x) / (self.__final_time - t),
                diffusion=lambda t, x: self.__vol,
                time_unit=time_unit)

    @staticmethod
    def create_from_cov(initial_value=None, final_value=None, initial_time=0., final_time=1., cov=None):
        vol = None if cov is None else stats.cov_to_vol(cov)
        return BrownianBridge(initial_value=initial_value, final_value=final_value, initial_time=initial_time, final_time=final_time, vol=vol)
    
    def propagate(self, time0, value0, time, variate=None, state0=None, random_state=None):
        if time == time0: return npu.to_ndim_2(value0, ndim_1_to_col=True, copy=True)
        value0 = npu.to_ndim_2(value0, ndim_1_to_col=True, copy=False)
        if variate is None:
            if random_state is None: random_state = rnd.random_state()
            variate = random_state.normal(size=self.noise_dim)
        variate = npu.to_ndim_2(variate, ndim_1_to_col=True, copy=False)
        time_delta = time - time0
        if isinstance(time_delta, np.timedelta64):
            time_delta = time_delta.item()
        if isinstance(time_delta, dt.timedelta):
            time_delta = time_delta.total_seconds() / self._time_unit.total_seconds()
        final_time_minus_time0 = self.__final_time - time0
        if isinstance(final_time_minus_time0, np.timedelta64):
            final_time_minus_time0 = final_time_minus_time0.item()
        if isinstance(final_time_minus_time0, dt.timedelta):
            final_time_minus_time0 = final_time_minus_time0.total_seconds() / self._time_unit.total_seconds()
        final_time_minus_time = self.__final_time - time
        if isinstance(final_time_minus_time, np.timedelta64):
            final_time_minus_time = time_delta.item()
        if isinstance(final_time_minus_time, dt.timedelta):
            final_time_minus_time = final_time_minus_time.total_seconds() / self._time_unit.total_seconds()
        mean = value0 + time_delta / final_time_minus_time0 * (self.__final_value - value0)
        cov_factor = time_delta * final_time_minus_time / final_time_minus_time0
        vol_factor = np.sqrt(cov_factor)
        vol = vol_factor * self.__vol
        return mean + np.dot(vol, variate)

    def _propagate_distr_impl(self, distr0, time_delta, assume_distr=False):
        if not isinstance(distr0, distrs.NormalDistr) and not assume_distr:
            raise ValueError('Do not know how to propagate a distribution that is not normal')
        mean = value0 + time_delta / (self.__final_time - time0) * (self.__final_value - value0)
        cov_factor = (time - time0) * (self.__final_time - time) / (self.__final_time - time0)
        vol_factor = np.sqrt(cov_factor)
        vol = vol_factor * self.__vol
        mean = distr0.mean + self._mean * time_delta
        cov = distr0.cov + time_delta * self._cov
        return distrs.NormalDistr(mean=mean, cov=cov)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__initial_value == other.__initial_value and \
                    self.__final_value == other.__final_value and \
                    self.__initial_time == other.__initial_time and \
                    self.__final_time == other.__final_time

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_string_helper(self):
        if self._to_string_helper_BrownianBridge is None:
            self._to_string_helper_BrownianBridge = super().to_string_helper() \
                    .set_type(self) \
                    .add('mean', self._mean) \
                    .add('vol', self._vol)
        return self._to_string_helper_BrownianBridge

    def __str__(self):
        if self._str_BrownianBridge is None: self._str_BrownianBridge = self.to_string_helper().to_string()
        return self._str_BrownianBridge

class OrnsteinUhlenbeckProcess(SolvedItoMarkovProcess):
    def __init__(self, transition=None, mean=None, vol=None, time_unit=dt.timedelta(days=1)):
        if transition is None and mean is None and vol is None:
            transition = 1.; mean = 0.; vol = 1.
            
        self._transition, self._mean, self._vol = None, None, None
            
        if transition is not None:
            self._transition = npu.to_ndim_2(transition, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self._transition)
        if mean is not None:
            self._mean = npu.to_ndim_2(mean, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self._mean)
        if vol is not None:
            self._vol = npu.to_ndim_2(vol, ndim_1_to_col=True, copy=True)
            process_dim = npu.nrow(self._vol)
        
        if self._transition is None: self._transition = np.eye(process_dim)
        if self._mean is None: self._mean = npu.col_of(process_dim, 0.)
        if self._vol is None: self._vol = np.eye(process_dim)
        
        npc.check_square(self._transition)
        npc.check_nrow(self._transition, process_dim)
        npc.check_col(self._mean)
        npc.check_nrow(self._mean, process_dim)
        npc.check_nrow(self._vol, process_dim)
        
        noise_dim = npu.ncol(self._vol)
        
        self._transition_x_2 = npu.kron_sum(self._transition, self._transition)
        self._transition_x_2_inverse = np.linalg.inv(self._transition_x_2)
        self._cov = stats.vol_to_cov(self._vol)
        self._cov_vec = npu.vec(self._cov)
        
        self._cached_mean_reversion_factor = None
        self._cached_mean_reversion_factor_time_delta = None
        self._cached_mean_reversion_factor_squared = None
        self._cached_mean_reversion_factor_squared_time_delta = None
        
        npu.make_immutable(self._transition)
        npu.make_immutable(self._transition_x_2)
        npu.make_immutable(self._transition_x_2_inverse)
        npu.make_immutable(self._mean)
        npu.make_immutable(self._vol)
        npu.make_immutable(self._cov)
        npu.make_immutable(self._cov_vec)
        
        self._to_string_helper_OrnsteinUhlenbeckProcess = None
        self._str_OrnsteinUhlenbeckProcess = None
        
        super(OrnsteinUhlenbeckProcess, self).__init__(process_dim=process_dim, noise_dim=noise_dim,
                drift=lambda t, x: -np.dot(self._transition, x - self._mean),
                diffusion=lambda t, x: self._vol,
                time_unit=time_unit)
        
    @staticmethod
    def create_from_cov(transition=None, mean=None, cov=None):
        vol = None if cov is None else stats.cov_to_vol(cov)
        return OrnsteinUhlenbeckProcess(transition, mean, vol)

    @staticmethod
    def create_multiscale_from_vol(transition_vector, mean, vol):
        transition_vector = npu.to_ndim_2(transition_vector, ndim_1_to_col=True, copy=False)
        npc.check_col(transition_vector)
        process_dim = np.size(transition_vector)
        transition = np.zeros((process_dim, process_dim))
        checks.check_some_number(mean)
        mean_vector = np.zeros((process_dim, 1))
        mean_vector[0, 0] = mean
        mean_vector[1, 0] = mean
        for i in range(process_dim):
            transition[(i, i)] = transition_vector[i]
            if i < process_dim - 1: transition[(i+1, i)] = -transition_vector[i+1]
        return OrnsteinUhlenbeckProcess(transition, mean_vector, vol)

    @staticmethod
    def create_multiscale_from_cov(transition_vector, cov):
        vol = None if cov is None else stats.cov_to_vol(cov)
        return create_multiscale_from_vol(transition, mean, vol)
    
    @property
    def transition(self):
        return self._transition
        
    @property
    def mean(self):
        return self._mean
    
    @property
    def vol(self):
        return self._vol
    
    def mean_reversion_factor(self, time_delta):
        if self._cached_mean_reversion_factor_time_delta is None or self._cached_mean_reversion_factor_time_delta != time_delta:
            self._cached_mean_reversion_factor_time_delta = time_delta
            self._cached_mean_reversion_factor = la.expm(self._transition * (-time_delta))
        return self._cached_mean_reversion_factor
    
    def mean_reversion_factor_squared(self, time_delta):
        if self._cached_mean_reversion_factor_squared_time_delta is None or self._cached_mean_reversion_factor_squared_time_delta != time_delta:
            self._cached_mean_reversion_factor_squared_time_delta = time_delta
            self._cached_mean_reversion_factor_squared = la.expm(self._transition_x_2 * (-time_delta))
        return self._cached_mean_reversion_factor_squared
        
    def noise_covariance(self, time_delta):
        mrf_squared = self.mean_reversion_factor_squared(time_delta)
        eye_minus_mrf_squared = np.eye(self.process_dim * self.process_dim) - mrf_squared
        return npu.unvec(np.dot(np.dot(self._transition_x_2_inverse, eye_minus_mrf_squared), self._cov_vec), self.process_dim)
        
    def propagate(self, time0, value0, time, variate=None, state0=None, random_state=None):
        if time == time0: return npu.to_ndim_2(value0, ndim_1_to_col=True, copy=True)
        value0 = npu.to_ndim_2(value0, ndim_1_to_col=True, copy=False)
        if variate is None:
            if random_state is None: random_state = rnd.random_state()
            variate = random_state.normal(size=self.noise_dim)
        variate = npu.to_ndim_2(variate, ndim_1_to_col=True, copy=False)
        time_delta = time - time0
        if isinstance(time_delta, np.timedelta64):
            time_delta = time_delta.item()
        if isinstance(time_delta, dt.timedelta):
            time_delta = time_delta.total_seconds() / self._time_unit.total_seconds()
        mrf = self.mean_reversion_factor(time_delta)
        eye_minus_mrf = np.eye(self.process_dim) - mrf
        m = np.dot(mrf, value0) + np.dot(eye_minus_mrf, self._mean)
        c = self.noise_covariance(time_delta)
        return m + np.dot(np.linalg.cholesky(c), variate)
        
    def _propagate_distr_impl(self, distr0, time_delta, assume_distr=False):
        if not isinstance(distr0, distrs.NormalDistr) and not assume_distr:
            raise ValueError('Do not know how to propagate a distribution that is not normal')
        value0 = distr0.mean
        mrf = self.mean_reversion_factor(time_delta)
        eye_minus_mrf = np.eye(self.process_dim) - mrf
        m = np.dot(mrf, value0) + np.dot(eye_minus_mrf, self._mean)
        c = np.dot(np.dot(mrf, distr0.cov), mrf.T) + self.noise_covariance(time_delta)
        return distrs.NormalDistr(mean=m, cov=c)
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._mean == other._mean and self._vol == other._vol
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def to_string_helper(self):
        if self._to_string_helper_OrnsteinUhlenbeckProcess is None:
            self._to_string_helper_OrnsteinUhlenbeckProcess = super().to_string_helper() \
                    .set_type(self) \
                    .add('transition', self._transition) \
                    .add('mean', self._mean) \
                    .add('vol', self._vol)
        return self._to_string_helper_OrnsteinUhlenbeckProcess

    def __str__(self):
        if self._str_OrnsteinUhlenbeckProcess is None: self._str_OrnsteinUhlenbeckProcess = self.to_string_helper().to_string()
        return self._str_OrnsteinUhlenbeckProcess
