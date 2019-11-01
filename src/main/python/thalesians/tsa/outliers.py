import numpy as np
import statsmodels.api as sm

def problessthan(sample, bw, value, count, random_state):
    sample = sample.flatten()
    idxs = random_state.randint(0, len(sample), size=count)
    epsilons = random_state.normal(size=count)
    lessthanflags = sample[idxs] + bw * epsilons < value
    return float(np.sum(lessthanflags))/float(count)

def isoutlier(sample, bw, value, threshold, count, random_state):
    plt = problessthan(sample, bw, value, count, random_state)
    pgt = 1. - plt
    return plt <= threshold or pgt <= threshold

if __name__ == '__main__':
    random_state = np.random.RandomState(seed=42)
    nobs = 300
    sample = random_state.normal(size=nobs)
    kde = sm.nonparametric.KDEUnivariate(np.random.normal(size=nobs))
    kde.fit()
    value=1.
    print(isoutlier(sample, kde.bw, value, threshold=.1, count=10000, random_state=random_state))
