import numpy as np
from scipy.linalg import block_diag

import thalesians.tsa.checks as checks
from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.filtering as filtering
import thalesians.tsa.filtering.kalman as kalman
import thalesians.tsa.numpyutils as npu
    
class LinearGaussianObsModel(kalman.KalmanFilterObsModel):
    def __init__(self, obs_matrix):
        super().__init__()
        if not checks.is_numpy_array(obs_matrix) and not checks.is_iterable(obs_matrix):
            obs_matrix = (obs_matrix,)
        self._obs_matrix = npu.make_immutable(
                block_diag(
                        *[npu.to_ndim_2(om, ndim_1_to_col=False, copy=False) for om in obs_matrix]))
        self._to_string_helper_LinearGaussianObsModel = None
        self._str_LinearGaussianObsModel = None
        
    @staticmethod
    def create(*args):
        return LinearGaussianObsModel(args)
    
    @property
    def obs_matrix(self):
        return self._obs_matrix
    
    def predict_obs(self, time, state_distr, observable=None):
        obs_mean = np.dot(self._obs_matrix, state_distr.mean)
        cross_cov = np.dot(self._obs_matrix, state_distr.cov)
        obs_cov = np.dot(cross_cov, self._obs_matrix.T)
        return filtering.PredictedObs(observable, time, N(mean=obs_mean, cov=obs_cov), cross_cov)
    
    def to_string_helper(self):
        if self._to_string_helper_LinearGaussianObsModel is None:
            self._to_string_helper_LinearGaussianObsModel = super().to_string_helper() \
                    .set_type(self) \
                    .add('obs_matrix', self._obs_matrix)
        return self._to_string_helper_LinearGaussianObsModel
    
    def __str__(self):
        if self._str_LinearGaussianObsModel is None: self._str_LinearGaussianObsModel = self.to_string_helper().to_string()
        return self._str_LinearGaussianObsModel
