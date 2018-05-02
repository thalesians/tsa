import numpy as np
import statsmodels.api as sm

def problessthan(sample, bw, value, count, randomstate):
    sample = sample.flatten()
    idxs = randomstate.randint(0, len(sample), size=count)
    epsilons = randomstate.normal(size=count)
    lessthanflags = sample[idxs] + bw * epsilons < value
    return float(np.sum(lessthanflags))/float(count)

def isoutlier(sample, bw, value, threshold, count, randomstate):
    plt = problessthan(sample, bw, value, count, randomstate)
    pgt = 1. - plt
    return plt <= threshold or pgt <= threshold

if __name__ == '__main__':
    randomstate = np.random.RandomState(seed=42)
    nobs = 300
    sample = randomstate.normal(size=nobs)
    kde = sm.nonparametric.KDEUnivariate(np.random.normal(size=nobs))
    kde.fit()
    value=1.
    print(isoutlier(sample, kde.bw, value, threshold=.1, count=10000, randomstate=randomstate))
