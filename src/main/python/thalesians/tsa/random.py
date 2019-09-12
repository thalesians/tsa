import datetime as dt

import numpy as np

import thalesians.tsa.exceptions as exc
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.numpychecks as npc

_random_state = None

def random_state(random_state=None, force=False):
    global _random_state
    if _random_state is None:
        _random_state = np.random.RandomState(seed=42) if random_state is None else random_state
    elif random_state is not None:
        if force:
            _random_state = random_state
        else:
            raise exc.NumericError('Process-wide random state is already set; it may not be set twice')
    return _random_state

# So we don't have the clash between the "random_state" function and the "random_state" argument name occurring later
_rs = random_state

def beta(a, b, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.beta(a, b, size)

def binomial(n, p, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.binomial(n, p, size)

def bytes(length, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.bytes(length)

def chisquare(df, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.chisquare(df, size)

def choice(a, size=None, replace=True, p=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.choice(a, size)

def dirichlet(alpha, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.dirichlet(alpha, size)

def exponential(scale=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    if isinstance(scale, dt.timedelta):
        scale = scale.total_seconds()
        td = True
    else:
        td = False
    r = random_state.exponential(scale, size)
    if td: r = np.vectorize(lambda x: dt.timedelta(seconds=x))(r)
    return r

def f(shape, scale=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.f(shape, scale, size)

def gamma(shape, scale=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.gamma(shape, scale, size)

def geometric(p, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.geometric(p, size)

def gumbel(loc=0., scale=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.gumbel(loc, scale, size)

def hypergeometric(ngood, nbad, nsample, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.hypergeometric(ngood, nbad, nsample, size)

def laplace(loc=0., scale=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.laplace(loc, scale, size)

def logistic(loc=0., scale=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.logistic(loc, scale, size)

def lognormal(mean=0., sigma=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.lognormal(mean, sigma, size)

# The `lognormal` implemented in `RandomState` behaves rather strangely. This implementation uses `RandomState`'s
# `multivariate_normal` and then takes the elementwise exponential.
def multivariate_lognormal(mean_of_log=0., cov_of_log=1., size=None, ndim=None, random_state=None):
    global _rs
    if ndim is None:
        if mean_of_log is not None: ndim = np.size(mean_of_log)
        elif cov_of_log is not None: ndim = npu.nrow(cov_of_log)
        else: ndim = 1
    if ndim is not None:
        if mean_of_log is None: mean_of_log = npu.ndim_1_of(ndim, 0.)
        if cov_of_log is None: cov_of_log = np.eye(ndim, ndim)
    mean_of_log = npu.to_ndim_1(mean_of_log)
    cov_of_log = npu.to_ndim_2(cov_of_log)
    npc.check_size(mean_of_log, ndim)
    npc.check_nrow(cov_of_log, ndim)
    npc.check_square(cov_of_log)
    if random_state is None: random_state = _rs()
    normal = random_state.multivariate_normal(mean_of_log, cov_of_log, size)
    return np.exp(normal)

def logseries(p, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.logseries(p, size)

def multinomial(n, pvals, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.multinomial(n, pvals, size)

def multivariate_normal(mean=None, cov=None, size=None, ndim=None, random_state=None):
    global _rs
    if ndim is None:
        if mean is not None: ndim = np.size(mean)
        elif cov is not None: ndim = npu.nrow(cov)
        else: ndim = 1
    if ndim is not None:
        if mean is None: mean = npu.ndim_1_of(ndim, 0.)
        if cov is None: cov = np.eye(ndim, ndim)
    mean = npu.to_ndim_1(mean)
    cov = npu.to_ndim_2(cov)
    npc.check_size(mean, ndim)
    npc.check_nrow(cov, ndim)
    npc.check_square(cov)
    if random_state is None: random_state = _rs()
    return random_state.multivariate_normal(mean, cov, size)

def multivariate_normals(mean=None, cov=None, size=None, count=None, ndim=None, random_state=None):
    i = 0
    while count is None or i < count:
        yield multivariate_normal(mean, cov, size, ndim, random_state)
        i += 1

def negative_binomial(n, p, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.negative_binomial(n, p, size)

def noncentral_chisquare(df, nonc, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.noncentral_chisquare(df, nonc, size)

def noncentral_f(dfnum, dfden, nonc, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.noncentral_f(dfnum, dfden, nonc, size)

def normal(loc=0., scale=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.normal(loc, scale, size)

def pareto(a, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.pareto(a, size)

def permutation(x, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.permutation(x)

def poisson(lam=1.0, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.poisson(lam, size)

def power(a, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.power(a, size)

def randint(low, high=None, size=None, dtype='I', random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.randint(low, high, size, dtype)

def random_integers(low, high=None, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.random_integers(low, high, size)

def random_sample(size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.random_sample(size)

def rayleigh(scale=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.rayleigh(scale, size)

def shuffle(x, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.shuffle(x)

def standard_cauchy(size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.standard_cauchy(size)

def standard_exponential(size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.standard_exponential(size)

def standard_gamma(shape, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.standard_gamma(shape, size)

def standard_normal(size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.standard_normal(size)

def standard_t(df, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.standard_t(df, size)

def tomaxint(size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.tomaxint(size)

def triangular(left, mode, right, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.triangular(left, mode, right, size)

def uniform(low=0., high=1., size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.uniform(low, high, size)

def vonmises(mu, kappa, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.vonmises(mu, kappa, size)

def wald(mean, scale, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.wald(mean, scale, size)

def weibull(a, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.weibull(a, size)

def zipf(a, size=None, random_state=None):
    global _rs
    if random_state is None: random_state = _rs()
    return random_state.zipf(a, size)
