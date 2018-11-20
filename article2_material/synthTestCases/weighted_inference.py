##----------------------------ERROR X and Y--------------------------------------------------------------
##----------------------------------------------------------------------------------------------------------------------
#
#
# from os import environ
# environ["MKL_THREADING_LAYER"] = "GNU"
# import numpy as np
# import pymc3 as pm
# import matplotlib.pyplot as plt
#
# # set random seed for reproducibility
# np.random.seed(12345)
#
# x = np.arange(5,400,10)*1e3
#
# # Parameters for gaussian
# amp_true    = 0.2
# size_true   = 1.8
# ps_true     = 0.1
#
# #Gaussian function
# gauss = lambda x,amp,size,ps: amp*np.exp(-1*(np.pi**2/(3600.*180.)*size*x)**2/(4.*np.log(2.)))+ps
# f_true = gauss(x=x,amp=amp_true, size=size_true, ps=ps_true )
#
# # add noise to the data points
# noise = np.random.normal(size=len(x)) * .02
# f = f_true + noise
# #f_error = np.ones_like(f_true) * 0.05 * f.max()
# f_error = np.random.normal(loc=0.015,scale=0.005,size=x.size)
# w = 1.0 / f_error**2
# y_sd = np.ones_like(f_true)
#
# # with pm.Model() as model2:
# #     amp2 = pm.Uniform('amp2', 0.05, 0.4, testval= 0.15)
# #     size2 = pm.Uniform('size2', 0.5, 2.5, testval= 1.0)
# #     ps2 = pm.Normal('ps2', 0.13, 40, testval=0.15)
# #
# #     gauss2 = pm.Deterministic('gauss2',amp2*np.exp(-1*(np.pi**2*size2*x/(3600.*180.))**2/(4.*np.log(2.)))+ps2)
# #
# #     y2 = pm.Potential('Y2', w * pm.Normal.dist(mu=gauss2, sd=y_sd, shape=(40)).logp(f))
# #
# #     trace2 = pm.sample(2000, tune=2000)
# #
# # with pm.Model() as model3:
# #     amp3 = pm.Uniform('amp3', 0.05, 0.4, testval= 0.15)
# #     size3 = pm.Uniform('size3', 0.5, 2.5, testval= 1.0)
# #     ps3 = pm.Normal('ps3', 0.13, 40, testval=0.15)
# #
# #     gauss3 = pm.Deterministic('gauss3',amp3*np.exp(-1*(np.pi**2*size3*x/(3600.*180.))**2/(4.*np.log(2.)))+ps3)
# #
# #     y3 = pm.Normal('Y3', mu=gauss3, sd=f_error, observed=f)
# #
# #     trace3 = pm.sample(2000, tune=2000)
#
#
# # define the model/function to be fitted in PyMC3:
# with pm.Model() as model_xy:
#
#     x_obsx = pm.Normal('x_obsx',mu=x, tau=(1e4)**-2,shape=40).random()
#
#     ampx = pm.Uniform('ampx', 0.05, 0.4, testval= 0.15)
#     sizex = pm.Uniform('sizex', 0.5, 2.5, testval= 1.0)
#     psx = pm.Normal('psx', 0.13, 40, testval=0.15)
#
#     x_pred = pm.Normal('x_pred', mu=x_obsx, tau=(1e4)**-2*np.ones_like(x_obsx),testval=5*np.ones_like(x_obsx),shape=40) # this allows error in x_obs
#
#     gaussX = pm.Deterministic('gaussX',ampx*np.exp(-1*(np.pi**2*sizex*x_pred/(3600.*180.))**2/(4.*np.log(2.)))+psx)
#
#     y = pm.Normal('yX', mu=gaussX, tau=1.0/f_error**2, observed=f)
#
#     tracex=pm.sample(15000, tune = 5000)
#
# # # extract and plot results
# # y_min2 = np.percentile(trace2.gauss2,2.5,axis=0)
# # y_max2 = np.percentile(trace2.gauss2,97.5,axis=0)
# # y_fit2 = np.percentile(trace2.gauss2,50,axis=0)
# # y_min3 = np.percentile(trace3.gauss3,2.5,axis=0)
# # y_max3 = np.percentile(trace3.gauss3,97.5,axis=0)
# # y_fit3 = np.percentile(trace3.gauss3,50,axis=0)
# #
# # plt.plot(x, y_fit2,'k', marker='*', ls='None', ms=5, mew=1, label='Fit with weigths')
# # plt.fill_between(x, y_min2, y_max2, color='green', alpha=0.5)
# #
# # plt.plot(x, y_fit3,'k', marker='+', ls='None', ms=5, mew=1, label='Fit')
# # plt.fill_between(x, y_min3, y_max3, color='purple', alpha=0.5)
#
# y_minYX = np.percentile(tracex.gaussX,2.5,axis=0)
# y_maxYX = np.percentile(tracex.gaussX,97.5,axis=0)
# y_fitYX = np.percentile(tracex.gaussX,50,axis=0)
#
# plt.plot(x, f_true, 'b', marker='None', ls='-', lw=1, label='True')
# plt.errorbar(x, f, yerr=f_error, color='r', marker='.', ls='None', label='Observed')
#
# plt.legend()
# plt.show()


#----------------------------ERROR COMPARISON TWO METHODS--------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------


from os import environ
environ["MKL_THREADING_LAYER"] = "GNU"
import numpy as np
import pymc3 as pm
import matplotlib.pyplot as plt

# set random seed for reproducibility
np.random.seed(12345)

x = np.arange(5,400,10)*1e3

# Parameters for gaussian
amp_true    = 0.2
size_true   = 1.8
ps_true     = 0.1

#Gaussian function
gauss = lambda x,amp,size,ps: amp*np.exp(-1*(np.pi**2/(3600.*180.)*size*x)**2/(4.*np.log(2.)))+ps
f_true = gauss(x=x,amp=amp_true, size=size_true, ps=ps_true )

# add noise to the data points
noise = np.random.normal(size=len(x)) * .02
f = f_true + noise
#f_error = np.ones_like(f_true) * 0.05 * f.max()
f_error = np.random.normal(loc=0.015,scale=0.005,size=x.size)
w = 1.0 / f_error**2
y_sd = np.ones_like(f_true)

with pm.Model() as model2:
    amp2 = pm.Uniform('amp2', 0.05, 0.4, testval= 0.15)
    size2 = pm.Uniform('size2', 0.5, 2.5, testval= 1.0)
    ps2 = pm.Normal('ps2', 0.13, 40, testval=0.15)

    gauss2 = pm.Deterministic('gauss2',amp2*np.exp(-1*(np.pi**2*size2*x/(3600.*180.))**2/(4.*np.log(2.)))+ps2)

    y2 = pm.Potential('Y2', w * pm.Normal.dist(mu=gauss2, sd=y_sd, shape=(40)).logp(f))

    trace2 = pm.sample(2000, tune=2000)

with pm.Model() as model3:
    amp3 = pm.Uniform('amp3', 0.05, 0.4, testval= 0.15)
    size3 = pm.Uniform('size3', 0.5, 2.5, testval= 1.0)
    ps3 = pm.Normal('ps3', 0.13, 40, testval=0.15)

    gauss3 = pm.Deterministic('gauss3',amp3*np.exp(-1*(np.pi**2*size3*x/(3600.*180.))**2/(4.*np.log(2.)))+ps3)

    y3 = pm.Normal('Y3', mu=gauss3, sd=f_error, observed=f)

    trace3 = pm.sample(2000, tune=2000)

# extract and plot results
y_min2 = np.percentile(trace2.gauss2,2.5,axis=0)
y_max2 = np.percentile(trace2.gauss2,97.5,axis=0)
y_fit2 = np.percentile(trace2.gauss2,50,axis=0)
y_min3 = np.percentile(trace3.gauss3,2.5,axis=0)
y_max3 = np.percentile(trace3.gauss3,97.5,axis=0)
y_fit3 = np.percentile(trace3.gauss3,50,axis=0)

plt.plot(x, y_fit2,'k', marker='*', ls='None', ms=5, mew=1, label='Fit with weigths')
plt.fill_between(x, y_min2, y_max2, color='green', alpha=0.5)

plt.plot(x, y_fit3,'k', marker='+', ls='None', ms=5, mew=1, label='Fit')
plt.fill_between(x, y_min3, y_max3, color='purple', alpha=0.5)

plt.plot(x, f_true, 'b', marker='None', ls='-', lw=1, label='True')
plt.errorbar(x, f, yerr=f_error, color='r', marker='.', ls='None', label='Observed')

plt.legend()
plt.show()

from os import environ
environ["MKL_THREADING_LAYER"] = "GNU"
import numpy as np
import pymc3 as pm
import matplotlib.pyplot as plt

# set random seed for reproducibility
np.random.seed(12345)

x = np.arange(5,400,10)*1e3

# Parameters for gaussian
amp_true    = 0.2
size_true   = 1.8
ps_true     = 0.1

#Gaussian function
gauss = lambda x,amp,size,ps: amp*np.exp(-1*(np.pi**2/(3600.*180.)*size*x)**2/(4.*np.log(2.)))+ps
f_true = gauss(x=x,amp=amp_true, size=size_true, ps=ps_true )

# add noise to the data points
noise = np.random.normal(size=len(x)) * .02
f = f_true + noise
f_error = np.ones_like(f_true) * 0.05 * f.max()

with pm.Model() as model3:
    amp = pm.Uniform('amp', 0.05, 0.4, testval= 0.15)
    size = pm.Uniform('size', 0.5, 2.5, testval= 1.0)
    ps = pm.Normal('ps', 0.13, 40, testval=0.15)

    gauss = pm.Deterministic('gauss',amp*np.exp(-1*(np.pi**2*size*x/(3600.*180.))**2/(4.*np.log(2.)))+ps)

    y = pm.Normal('y', mu=gauss, sd=f_error, observed=f)

    trace=pm.sample(2000)

# extract and plot results
y_min = np.percentile(trace.gauss,2.5,axis=0)
y_max = np.percentile(trace.gauss,97.5,axis=0)
y_fit = np.percentile(trace.gauss,50,axis=0)
plt.plot(x,f_true,'b', marker='None', ls='-', lw=1, label='True')
plt.errorbar(x,f,yerr=f_error, color='r', marker='.', ls='None', label='Observed')
plt.plot(x,y_fit,'k', marker='+', ls='None', ms=5, mew=1, label='Fit')
plt.fill_between(x, y_min, y_max, color='0.5', alpha=0.5)
plt.legend()
plt.show()