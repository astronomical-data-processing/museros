import numpy.random as npr
import numpy as np
import random as pr
import numpy.linalg as la
import scipy.cluster.vq as vq


class GMM(object):

    def __init__(self, dim = None, ncomps = None, data = None,  method = None, filename = None, params = None):

        if not filename is None:  # load from file
            self.load_model(filename)

        elif not params is None: # initialize with parameters directly
            self.comps = params['comps']
            self.ncomps = params['ncomps']
            self.dim = params['dim']
            self.priors = params['priors']

        elif not data is None: # initialize from data

            assert dim and ncomps, "Need to define dim and ncomps."

            self.dim = dim
            self.ncomps = ncomps
            self.comps = []

            if method is "uniform":
                # uniformly assign data points to components then estimate the parameters
                npr.shuffle(data)
                n = len(data)
                s = n / ncomps
                for i in range(ncomps):
                    self.comps.append(Normal(dim, data = data[i * s: (i+1) * s]))

                self.priors = np.ones(ncomps, dtype = "double") / ncomps

            elif method is "random":
                # choose ncomp points from data randomly then estimate the parameters
                mus = pr.sample(data,ncomps)
                clusters = [[] for i in range(ncomps)]
                for d in data:
                    i = np.argmin([la.norm(d - m) for m in mus])
                    clusters[i].append(d)

                for i in range(ncomps):
                    print mus[i], clusters[i]
                    self.comps.append(Normal(dim, mu = mus[i], sigma = np.cov(clusters[i], rowvar=0)))

                self.priors = np.ones(ncomps, dtype="double") / np.array([len(c) for c in clusters])

            elif method is "kmeans":
                # use kmeans to initialize the parameters
                (centroids, labels) = vq.kmeans2(data, ncomps, minit="points", iter=100)
                clusters = [[] for i in range(ncomps)]
                for (l,d) in zip(labels,data):
                    clusters[l].append(d)

                # will end up recomputing the cluster centers
                for cluster in clusters:
                    self.comps.append(Normal(dim, data = cluster))

                self.priors = np.ones(ncomps, dtype="double") / np.array([len(c) for c in clusters])

            else:
                raise ValueError, "Unknown method type!"

        else:

            # these need to be defined
            assert dim and ncomps, "Need to define dim and ncomps."

            self.dim = dim
            self.ncomps = ncomps

            self.comps = []

            for i in range(ncomps):
                self.comps.append(Normal(dim))

            self.priors = np.ones(ncomps,dtype='double') / ncomps

    def __str__(self):
        res = "%d" % self.dim
        res += "\n%s" % str(self.priors)
        for comp in self.comps:
            res += "\n%s" % str(comp)
        return res

    def save_model(self):
        pass

    def load_model(self):
        pass

    def mean(self):
        return np.sum([self.priors[i] * self.comps[i].mean() for i in range(self.ncomps)], axis=0)

    def covariance(self): # computed using Dan's method
        m = self.mean()
        s = -np.outer(m,m)

        for i in range(self.ncomps):
            cm = self.comps[i].mean()
            cvar = self.comps[i].covariance()
            s += self.priors[i] * (np.outer(cm,cm) + cvar)

        return s

    def pdf(self, x):
        responses = [comp.pdf(x) for comp in self.comps]
        return np.dot(self.priors, responses)

    def condition(self, indices, x):
        """
        Create a new GMM conditioned on data x at indices.
        """
        condition_comps = []
        marginal_comps = []

        for comp in self.comps:
            condition_comps.append(comp.condition(indices, x))
            marginal_comps.append(comp.marginalize(indices))

        new_priors = []
        for (i,prior) in enumerate(self.priors):
            new_priors.append(prior * marginal_comps[i].pdf(x))
        new_priors = npa(new_priors) / np.sum(new_priors)

        params = {'ncomps' : self.ncomps, 'comps' : condition_comps,
                  'priors' : new_priors, 'dim' : marginal_comps[0].dim}

        return GMM(params = params)

    def em(self, data, nsteps = 100):

        k = self.ncomps
        d = self.dim
        n = len(data)

        for l in range(nsteps):

            # E step

            responses = np.zeros((k,n))

            for j in range(n):
                for i in range(k):
                    responses[i,j] = self.priors[i] * self.comps[i].pdf(data[j])

            responses = responses / np.sum(responses,axis=0) # normalize the weights

            # M step

            N = np.sum(responses,axis=1)

            for i in range(k):
                mu = np.dot(responses[i,:],data) / N[i]
                sigma = np.zeros((d,d))

                for j in range(n):
                   sigma += responses[i,j] * np.outer(data[j,:] - mu, data[j,:] - mu)

                sigma = sigma / N[i]

                self.comps[i].update(mu,sigma) # update the normal with new parameters
                self.priors[i] = N[i] / np.sum(N) # normalize the new priors


npa = np.array
ix  = np.ix_ # urgh - sometimes numpy is ugly!

class Normal(object):
    """
    A class for storing the parameters of a multivariate normal
    distribution. Supports evaluation, sampling, conditioning and
    marginalization.
    """

    def __init__(self, dim, mu = None, sigma = None, data = None,
                 parent = None, cond = None, margin = None):
        """
        Initialize a normal distribution.

        Parameters
        ----------
        dim : int
            Number of dimensions (e.g. number of components in the mu parameter).
        mu : array, optional
            The mean of the normal distribution.
        sigma : array, optional
            The covariance matrix of the normal distribution.
        data : array, optional
            If provided, the parameters of the distribution will be estimated from the data. Rows are observations, columns are components.
        parent : Normal, optional
            A reference to a parent distribution that was marginalized or conditioned.
        cond : dict, optional
            A dict of parameters describing how the parent distribution was conditioned.
        margin : dict, optional
            A dict of parameters describing how the parent distribution was marginalized.

        Examples
        --------
        >>> x = Normal(2,mu = np.array([0.1,0.7]), sigma = np.array([[ 0.6,  0.4], [ 0.4,  0.6]]))
        >>> print x
        [ 0.1  0.7]
        [[ 0.6  0.4]
        [ 0.4  0.6]]

        To condition on a value (and index):

        >>> condx = x.condition([0],0.1)
        >>> print condx
        [ 0.7]
        [[ 0.33333333]]

        """

        self.dim = dim # full data dimension

        if not mu is None  and not sigma is None:
            pass
        elif not data is None:
            # estimate the parameters from data - rows are samples, cols are variables
            mu, sigma = self.estimate(data)
        else:
            # generate random means
            mu = npr.randn(dim)
            sigma = np.eye(dim)

        self.cond = cond
        self.margin = margin
        self.parent = parent

        self.update(npa(mu),npa(sigma))


    def update(self, mu, sigma):
        """
        Update the distribution with new parameters.

        Parameters
        ----------
        mu : array
            The new mean parameters.
        sigma : array
            The new covariance matrix.

        Example
        -------

        >>> x = Normal(2,mu = np.array([0.1,0.7]), sigma = np.array([[ 0.6,  0.4], [ 0.4,  0.6]]))
        >>> print x
        [ 0.1  0.7]
        [[ 0.6  0.4]
        [ 0.4  0.6]]

        >>> x.update(np.array([0.0,0.0]), x.E)
        >>> print x
        [ 0.0  0.0]
        [[ 0.6  0.4]
        [ 0.4  0.6]]
        """

        self.mu = mu
        self.E = sigma

        det = None
        if self.dim == 1:
            self.A = 1.0 / self.E
            det = np.fabs(self.E[0])
        else:
            self.A = la.inv(self.E) # precision matrix
            det = np.fabs(la.det(self.E))

        self.factor = (2.0 * np.pi)**(self.dim / 2.0) * (det)**(0.5)

    def __str__(self):
        return "%s\n%s" % (str(self.mu), str(self.E))

    def mean(self):
        return self.mu

    def covariance(self):
        return self.E

    def pdf(self, x):
        dx = x - self.mu
        A = self.A
        fE = self.factor

        return np.exp(-0.5 * np.dot(np.dot(dx,A),dx)) / fE

    def pdf_mesh(self, x, y):
        # for 2d meshgrids
        # use matplotlib.mlab.bivariate_normal -- faster (vectorized)

        z = np.zeros((len(y),len(x)))

        for (i,v) in enumerate(x):
            for (j,w) in enumerate(y):
                z[j,i] = self.pdf([v,w])

        return z

    def simulate(self, ndata = 100):
        """
        Draw pts from the distribution.
        """
        return npr.multivariate_normal(self.mu, self.E, ndata)

    def estimate(self, data):
        mu = np.mean(data, axis=0)
        sigma = np.cov(data, rowvar=0)
        return mu, sigma

    def marginalize(self, indices):
        """
        Creates a new marginal normal distribution for ''indices''.
        """
        indices = npa(indices)
        return Normal(len(indices), mu = self.mu[indices], sigma = self.E[ix(indices,indices)], margin = {'indices' : indices}, parent = self)

    def condition(self, indices, x):
        """
        Creates a new normal distribution conditioned on the data x at indices.
        """

        idim = indices
        odim = npa([i for i in range(self.dim) if not i in indices])

        Aaa = self.A[ix(odim,odim)]
        Aab = self.A[ix(odim,idim)]
        iAaa = None
        det = None

        if len(odim) == 1: # linalg does not handle d1 arrays
            iAaa = 1.0 / Aaa
            det = np.fabs(iAaa[0])
        else:
            iAaa = la.inv(Aaa)
            det = np.fabs(la.det(iAaa))

        # compute the new mu
        premu = np.dot(iAaa, Aab)

        mub = self.mu[idim]
        mua = self.mu[odim]
        new_mu = mua - np.dot(premu, (x - mub))

        new_E = iAaa
        return Normal(len(odim), mu = new_mu, sigma = new_E,
                      cond = {'data' : x, 'indices' : indices},
                      parent = self)