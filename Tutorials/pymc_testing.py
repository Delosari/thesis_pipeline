import matplotlib.pyplot as plt
import numpy as np
import pymc

def compute_sigma_level(trace1, trace2, nbins=20):
    """From a set of traces, bin by number of standard deviations"""
    L, xbins, ybins = np.histogram2d(trace1, trace2, nbins)
    L[L == 0] = 1E-16
    logL = np.log(L)

    shape = L.shape
    L = L.ravel()

    # obtain the indices to sort and unsort the flattened array
    i_sort = np.argsort(L)[::-1]
    i_unsort = np.argsort(i_sort)

    L_cumsum = L[i_sort].cumsum()
    L_cumsum /= L_cumsum[-1]
    
    xbins = 0.5 * (xbins[1:] + xbins[:-1])
    ybins = 0.5 * (ybins[1:] + ybins[:-1])

    return xbins, ybins, L_cumsum[i_unsort].reshape(shape)

def plot_MCMC_trace(ax, xdata, ydata, trace, scatter=False, **kwargs):
    """Plot traces and contours"""
    xbins, ybins, sigma = compute_sigma_level(trace[0], trace[1])
    ax.contour(xbins, ybins, sigma.T, levels=[0.683, 0.955], **kwargs)
    if scatter:
        ax.plot(trace[0], trace[1], ',k', alpha=0.1)
    ax.set_xlabel(r'$\alpha$')
    ax.set_ylabel(r'$\beta$')

def plot_MCMC_model(ax, xdata, ydata, trace):
    """Plot the linear model and 2sigma contours"""
    ax.plot(xdata, ydata, 'ok')

    alpha, beta = trace[:2]
    xfit = np.linspace(-20, 120, 10)
    yfit = alpha[:, None] + beta[:, None] * xfit
    mu = yfit.mean(0)
    sig = 2 * yfit.std(0)

    ax.plot(xfit, mu, '-k')
    ax.fill_between(xfit, mu - sig, mu + sig, color='lightgray')

    ax.set_xlabel('x')
    ax.set_ylabel('y')

def plot_MCMC_results(xdata, ydata, trace, colors='k'):
    """Plot both the trace and the model together"""
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    plot_MCMC_trace(ax[0], xdata, ydata, trace, True, colors=colors)
    plot_MCMC_model(ax[1], xdata, ydata, trace)

def bayesian_model(xdata, ydata):
    
    alpha = pymc.Uniform('alpha', -100, 100)

    @pymc.stochastic(observed=False)
    def beta(value=10):
        return -1.5 * np.log(1 + value ** 2)
    
    @pymc.stochastic(observed=False)
    def sigma(value=1):
        return -np.log(abs(value))
    
    # Define the form of the model and likelihood
    @pymc.deterministic
    def y_model(x=xdata, alpha=alpha, beta=beta):
        return alpha + beta * x
    
    y = pymc.Normal('y', mu=y_model, tau=1. / sigma ** 2, observed=True, value=ydata)
    
    return locals()


# np.random.seed(42)
theta_true = (25, 0.5)
xdata = 100 * np.random.random(20)
ydata = theta_true[0] + theta_true[1] * xdata

# add scatter to points
xdata = np.random.normal(xdata, 10)
ydata = np.random.normal(ydata, 10)

MAP_Model               = pymc.MAP(bayesian_model(xdata, ydata))
MAP_Model.fit() 
MAP_Model.revert_to_max()

# package the full model in a dictionary
S = pymc.MCMC(MAP_Model.variables, db='sqlite', dbname ='D:/Inference_data/testing_saving')#, dbmode='w', dbcomplevel=5, dbcomplib='zlib')
# S = pymc.MCMC(bayesian_model(xdata, ydata))
S.sample(iter=100000, burn=50000)

pymc_trace = [S.trace('alpha')[:],
              S.trace('beta')[:],
              S.trace('sigma')[:]]


S.db.close()
plot_MCMC_results(xdata, ydata, pymc_trace)

print 'Inference predictions'
print 'm', S.stats()['beta']['mean']
print 'n', S.stats()['alpha']['mean']

print 'MAP predictions'
print 'm', MAP_Model.beta.value
print 'n', MAP_Model.alpha.value

plt.show()