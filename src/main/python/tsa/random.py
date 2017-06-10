import datetime as dt

import numpy as np

import tsa.numpyutils as npu
import tsa.numpychecks as npc

__randomstate = None

def randomstate(randomstate=None, force=False):
    global __randomstate
    if __randomstate is None:
        __randomstate = np.random.RandomState(seed=42) if randomstate is None else randomstate
    elif randomstate is not None:
        if force:
            __randomstate = randomstate
        else:
            raise npu.NumericError('Process-wide random state is already set; it may not be set twice')
    return __randomstate

# So we don't have the clash between the "randomstate" function and the "randomstate" argument name occurring later
__rs = randomstate

def beta(a, b, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.beta(a, b, size)

def binomial(n, p, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.binomial(n, p, size)

def bytes(length, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.bytes(length)

def chisquare(df, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.chisquare(df, size)

def choice(a, size=None, replace=True, p=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.choice(a, size)

def dirichlet(alpha, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.dirichlet(alpha, size)

def exponential(scale=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    if isinstance(scale, dt.timedelta):
        scale = scale.total_seconds()
        td = True
    else:
        td = False
    r = randomstate.exponential(scale, size)
    if td: r = np.vectorize(lambda x: dt.timedelta(seconds=x))(r)
    return r

def f(shape, scale=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.f(shape, scale, size)

def gamma(shape, scale=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.gamma(shape, scale, size)

def geometric(p, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.geometric(p, size)

def gumbel(loc=0., scale=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.gumbel(loc, scale, size)

def hypergeometric(ngood, nbad, nsample, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.hypergeometric(ngood, nbad, nsample, size)

def laplace(loc=0., scale=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.laplace(loc, scale, size)

def logistic(loc=0., scale=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.logistic(loc, scale, size)

def lognormal(mean=0., sigma=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.lognormal(mean, sigma, size)

def logseries(p, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.logseries(p, size)

def multinomial(n, pvals, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.multinomial(n, pvals, size)

def multivariate_normal(mean=None, cov=None, size=None, ndim=None, randomstate=None):
    global __rs
    if ndim is None:
        if mean is not None: ndim = np.size(mean)
        elif cov is not None: ndim = npu.nrow(cov)
        else: ndim = 1
    if ndim is not None:
        if mean is None: mean = npu.ndim1of(ndim, 0.)
        if cov is None: cov = np.eye(ndim, ndim)
    mean = npu.tondim1(mean)
    cov = npu.tondim2(cov)
    npc.checksize(mean, ndim)
    npc.checknrow(cov, ndim)
    npc.checksquare(cov)
    if randomstate is None: randomstate = __rs()
    return randomstate.multivariate_normal(mean, cov, size)

def multivatiate_normals(mean=None, cov=None, size=None, count=None, ndim=None, randomstate=None):
    i = 0
    while count is None or i < count:
        yield multivariate_normal(mean, cov, size, ndim, randomstate)
        i += 1

def negative_binomial(n, p, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.negative_binomial(n, p, size)

def noncentral_chisquare(df, nonc, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.noncentral_chisquare(df, nonc, size)

def noncentral_f(dfnum, dfden, nonc, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.noncentral_f(dfnum, dfden, nonc, size)

def normal(loc=0., scale=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.normal(loc, scale, size)

def pareto(a, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.pareto(a, size)

def permutation(x, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.permutation(x)

def poisson(lam=1.0, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.poisson(lam, size)

def power(a, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.power(a, size)

def randint(low, high=None, size=None, dtype='I', randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.randint(low, high, size, dtype)

def random_integers(low, high=None, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.random_integers(low, high, size)

def random_sample(size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.random_sample(size)

def rayleigh(scale=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.rayleigh(scale, size)

def shuffle(x, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.shuffle(x)

def standard_cauchy(size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.standard_cauchy(size)

def standard_exponential(size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.standard_exponential(size)

def standard_gamma(shape, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.standard_gamma(shape, size)

def standard_normal(size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.standard_normal(size)

def standard_t(df, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.standard_t(df, size)

def tomaxint(size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.tomaxint(size)

def triangular(left, mode, right, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.triangular(left, mode, right, size)

def uniform(low=0., high=1., size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.uniform(low, high, size)

def vonmises(mu, kappa, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.vonmises(mu, kappa, size)

def wald(mean, scale, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.wald(mean, scale, size)

def weibull(a, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.weibull(a, size)

def zipf(a, size=None, randomstate=None):
    global __rs
    if randomstate is None: randomstate = __rs()
    return randomstate.zipf(a, size)
