from numpy import sqrt,exp,log,pi
import numpy as np
import pymc

#Example script showing how to fit 


#Generate some fake data to fit.
#Use fixed mean and variance
true_mu = 2.4
true_sigma = 0.7
N = 100
observations = np.random.randn(N)*true_sigma + true_mu

mu      = pymc.Uniform('mu',lower=-5,upper=5)
sigma   = pymc.Uniform('sigma',lower=0.01,upper=2.0)
P       = pymc.Normal('Observed Samples', mu=mu, tau=sigma**-2, value=observations, observed=True)

M = pymc.MCMC([mu,sigma,P])
M.sample(iter=100)

print "Maximum posterior mu = ", mu.value
print "Maximum posterior sigma = ", sigma.value
print M.mu.value