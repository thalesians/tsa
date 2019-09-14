# The following code has been adapted from Till A. Hoffmann.
# See https://nbviewer.jupyter.org/gist/tillahoffmann/f844bce2ec264c1c8cb5
# and https://stackoverflow.com/questions/27623919/weighted-gaussian-kernel-density-estimation-in-python

import numpy as np
from scipy.spatial.distance import cdist

import thalesians.tsa.checks as checks
import thalesians.tsa.distrs as distrs
import thalesians.tsa.numpyutils as npu

class GaussianKDEDistr(distrs.Distr):
    """
    Representation of a kernel-density estimate using Gaussian kernels.

    Kernel density estimation is a way to estimate the probability density function (PDF) of a random variable in a non-parametric way. `GaussianKDEDistr` works for both univariate
    and multivariate data. It includes automatic bandwidth determination. The estimation works best for a unimodal distribution; bimodal or multimodal distributions tend to be
    oversmoothed.

    Parameters
    ----------
    dataset : array_like
        Datapoints to estimate from. In case of univariate data this is a 1-D array, otherwise a 2-D array with shape (# of data points / particles, # of dimensions in each
        particle).
    weights : array_like, shape (n, ), optional, default: None
        An array of weights, of the same shape as `x`.  Each value in `x` only contributes its associated weight towards the bin count (instead of 1).
    bw_method : str, scalar or callable, optional
        The method used to calculate the estimator bandwidth.  This can be 'scott', 'silverman', a scalar constant or a callable.  If a scalar, this will be used directly as
        `kde.factor`. If a callable, it should take a `GaussianKDEDistr` instance as the only parameter and return a scalar. If None (default), 'scott' is used. See Notes for more
        details.

    Attributes
    ----------
    dataset : ndarray
        The dataset with which `GaussianKDEDistr` was initialized.
    d : int
        Number of dimensions.
    n : int
        Number of datapoints.
    factor : float
        The bandwidth factor, obtained from `kde.covariance_factor`, with which the covariance matrix is multiplied.
    covariance : ndarray
        The covariance matrix of `dataset`, scaled by the calculated bandwidth (`kde.factor`).
    inv_cov : ndarray
        The inverse of `covariance`.

    Methods
    -------
    kde.evaluate(points) : ndarray
        Evaluate the estimated pdf on a provided set of points.
    kde(points) : ndarray
        Same as kde.evaluate(points)
    kde.pdf(points) : ndarray
        Alias for ``kde.evaluate(points)``.
    kde.set_bandwidth(bw_method='scott') : None
        Computes the bandwidth, i.e. the coefficient that multiplies the data covariance matrix to obtain the kernel covariance matrix.
    kde.covariance_factor : float
        Computes the coefficient (`kde.factor`) that multiplies the data covariance matrix to obtain the kernel covariance matrix. The default is `scotts_factor`. A subclass can
        overwrite this method to provide a different method, or set it through a call to `kde.set_bandwidth`.

    Notes
    -----
    Bandwidth selection strongly influences the estimate obtained from the KDE (much more so than the actual shape of the kernel). Bandwidth selection can be done by a "rule of
    thumb", by cross-validation, by "plug-in methods" or by other means; see [3]_, [4]_ for reviews. `GaussianKDEDistr` uses a rule of thumb, the default is Scott's Rule.

    Scott's Rule [1]_, implemented as `scotts_factor`, is::

        n**(-1./(d+4)),

    with ``n`` the number of data points and ``d`` the number of dimensions.
    
    Silverman's Rule [2]_, implemented as `silverman_factor`, is::

        (n * (d + 2) / 4.)**(-1. / (d + 4)).

    Good general descriptions of kernel density estimation can be found in [1]_ and [2]_, the mathematics for this multi-dimensional implementation can be found in [1]_.

    References
    ----------
    .. [1] D.W. Scott, "Multivariate Density Estimation: Theory, Practice, and Visualization", John Wiley & Sons, New York, Chichester, 1992.
    .. [2] B.W. Silverman, "Density Estimation for Statistics and Data Analysis", Vol. 26, Monographs on Statistics and Applied Probability, Chapman and Hall, London, 1986.
    .. [3] B.A. Turlach, "Bandwidth Selection in Kernel Density Estimation: A Review", CORE and Institut de Statistique, Vol. 19, pp. 1-33, 1993.
    .. [4] D.M. Bashtannyk and R.J. Hyndman, "Bandwidth selection for kernel conditional density estimation", Computational Statistics & Data Analysis, Vol. 36, pp. 279-298, 2001.

    Examples
    --------
    Generate some random two-dimensional data:

    >>> from scipy import stats
    >>> def measure(n):
    >>>     "Measurement model, return two coupled measurements."
    >>>     m1 = np.random.normal(size=n)
    >>>     m2 = np.random.normal(scale=0.5, size=n)
    >>>     return m1+m2, m1-m2

    >>> m1, m2 = measure(2000)
    >>> xmin = m1.min()
    >>> xmax = m1.max()
    >>> ymin = m2.min()
    >>> ymax = m2.max()

    Perform a kernel density estimate on the data:

    >>> X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    >>> positions = np.vstack([X.ravel(), Y.ravel()])
    >>> values = np.vstack([m1, m2])
    >>> kernel = stats.gaussian_kde(values)
    >>> Z = np.reshape(kernel(positions).T, X.shape)

    Plot the results:

    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[xmin, xmax, ymin, ymax])
    >>> ax.plot(m1, m2, 'k.', markersize=2)
    >>> ax.set_xlim([xmin, xmax])
    >>> ax.set_ylim([ymin, ymax])
    >>> plt.show()
    """
    def __init__(self, empirical_distr, bw_method=None):
        """
        Compute the estimator bandwidth with given method.
    
        The new bandwidth calculated after a call to `set_bandwidth` is used for subsequent evaluations of the estimated density.
    
        Parameters
        ----------
        bw_method : str, scalar or callable, optional
            The method used to calculate the estimator bandwidth.  This can be 'scott', 'silverman', a scalar constant or a callable. If a scalar, this will be used directly as
            `kde.factor`.  If a callable, it should take a `GaussianKDEDistr` instance as only parameter and return a scalar.  If None (default), nothing happens; the current
            `kde.covariance_factor` method is kept.
    
        Examples
        --------
        >>> x1 = np.array([-7, -5, 1, 4, 5.])
        >>> kde = stats.gaussian_kde(x1)
        >>> xs = np.linspace(-10, 10, num=50)
        >>> y1 = kde(xs)
        >>> kde.set_bandwidth(bw_method='silverman')
        >>> y2 = kde(xs)
        >>> kde.set_bandwidth(bw_method=kde.factor / 3.)
        >>> y3 = kde(xs)
    
        >>> fig = plt.figure()
        >>> ax = fig.add_subplot(111)
        >>> ax.plot(x1, np.ones(x1.shape) / (4. * x1.size), 'bo', label='Data points (rescaled)')
        >>> ax.plot(xs, y1, label='Scott (default)')
        >>> ax.plot(xs, y2, label='Silverman')
        >>> ax.plot(xs, y3, label='Const (1/3 * Silverman)')
        >>> ax.legend()
        >>> plt.show()
        """
        self._empirical_distr = empirical_distr

        if bw_method is None:
            pass
        elif bw_method == 'scott':
            self.covariance_factor = self.scotts_factor
        elif bw_method == 'silverman':
            self.covariance_factor = self.silverman_factor
        elif np.isscalar(bw_method) and not checks.is_string(bw_method):
            self._bw_method = 'use constant'
            self.covariance_factor = lambda: bw_method
        elif callable(bw_method):
            self._bw_method = bw_method
            self.covariance_factor = lambda: self._bw_method(self)
        else:
            raise ValueError("`bw_method` should be 'scott', 'silverman', a scalar or a callable.")
        
        self._cov = None
        self._inv_cov = None
        self._pdf_norm_factor = None

    def _compute_covariance(self):
        """
        Computes the covariance matrix for each Gaussian kernel using covariance_factor().
        """
        self._cov = self.empirical_distr.cov * self.covariance_factor()**2
        self._inv_cov = np.linalg.inv(self.empirical_distr.cov) / self.covariance_factor()**2
        self._pdf_norm_factor = np.sqrt(np.linalg.det(2 * np.pi * self._cov)) #* self.n

    def scotts_factor(self):
        return np.power(self.empirical_distr.effective_particle_count, -1. / (self.dim + 4))

    def silverman_factor(self):
        return np.power(self.empirical_distr.effective_particle_count * (self.dim + 2.0) / 4.0, -1. / (self.dim + 4))

    # Default method to calculate bandwidth, can be overwritten by subclass:
    covariance_factor = scotts_factor

    @property
    def empirical_distr(self):
        return self._empirical_distr

    @property
    def dim(self):
        return self._empirical_distr.dim

    @property
    def particle_count(self):
        return self._empirical_distr.particle_count

    @property
    def mean(self):
        return self._empirical_distr.mean
    
    @property
    def cov(self):
        if self._cov is None:
            self._compute_covariance()
        return self._cov

    @property    
    def inv_cov(self):
        if self._inv_cov is None:
            self._compute_covariance()
        return self._inv_cov
    
    @property
    def pdf_norm_factor(self):
        if self._pdf_norm_factor is None:
            self._compute_covariance()
        return self._pdf_norm_factor
    
    def sample(self, size=1, random_state=None):
        raise NotImplementedError()

    def pdf(self, points):
        """
        Evaluate the estimated pdf on a set of points.

        Parameters
        ----------
        points : (# of dimensions, # of points)-array
            Alternatively, a (# of dimensions,) vector can be passed in and treated as a single point.

        Returns
        -------
        values : (# of points,)-array
            The values at each point.

        Raises
        ------
        ValueError : if the dimensionality of the input points is different than the dimensionality of the KDE.
        """
        points = npu.to_ndim_2(points, ndim_1_to_col=True)

        m, d = np.shape(points)
        if d != self.dim:
            if d == 1 and m == self.dim:
                # points was passed in as a column vector
                points = np.reshape(points, (1, self.dim))
                m = 1
            else:
                msg = "points have dimension %s, particles has dimension %s" % (d, self.dim)
                raise ValueError(msg)
        
        # compute the normalised residuals
        chi2 = cdist(points, self.empirical_distr.particles, 'mahalanobis', VI=self.inv_cov) ** 2
        # compute the pdf
        result = np.sum(np.exp(-.5 * chi2) * self.empirical_distr.normalised_weights.T, axis=1) / self.pdf_norm_factor        

        return result
