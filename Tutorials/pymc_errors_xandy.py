import pymc                         as pm
import numpy                        as np
import matplotlib.pyplot            as plt
from numpy                          import random
from scipy.odr                      import RealData, ODR, Model

#True values for linear equation
x_true = np.arange(0,50,3)
m_true    = 1
n_true    = 5
y_true    = m_true * x_true + n_true

# add noise_y to the data points
noise_y     = np.random.normal(loc = 0, scale=3, size = len(x_true)) 
y_error     = np.random.normal(loc = 0, scale=3, size = len(x_true))  
y_obs           = y_true + noise_y 

noise_x     = np.random.normal(loc = 0, scale=4, size = len(x_true)) 
x_error     = np.random.normal(loc = 0, scale=4, size = len(x_true)) 
x_obs       = x_true + noise_x

def quad_func(p, x):
    m, c = p
    return m*x + c

# Create a model for fitting.
quad_model = Model(quad_func)

# Create a RealData object using our initiated data from above.
data = RealData(x_obs, y_obs, sx=x_error, sy=y_error)

# Set up ODR with the model and data.
odr = ODR(data, quad_model, beta0=[0.15, 1.0])

# Run the regression.
out = odr.run()

# define the model/function to be fitted.
def model(x_obs, y_obs): 
    m       = pm.Uniform('m', 0, 10, value= 0.15)
    n       = pm.Uniform('n', -10, 10, value= 1.0)
    x_pred  = pm.Normal('x_true', mu=x_obs, tau=(x_error)**-2)           # this allows error in x_obs
  
    #Theoretical values
    @pm.deterministic(plot=False)
    def linearD(x_true=x_pred, m=m, n=n):
        return m * x_true + n
    
    @pm.deterministic
    def random_operation_on_observable(y_obs=y_obs):
        return y_obs + 0
      
    #likelihood
    y = pm.Normal('y', mu=linearD, tau=1.0/y_error**2, value=random_operation_on_observable.value, observed=True)
      
    return locals()

def bayesian_model(xdata, ydata):
     
    alpha = pm.Uniform('alpha', -100, 100)
    x_rand  = pm.Normal('x_obs', mu=xdata, tau=(x_error)**-2)           # this allows error in x_obs
 
    @pm.stochastic(observed=False)
    def beta(value=10):
        return -1.5 * np.log(1 + value ** 2)
     
    @pm.stochastic(observed=False)
    def sigma(value=1):
        return -np.log(abs(value))
     
    # Define the form of the model and likelihood
    @pm.deterministic
    def y_model(x=x_rand, alpha=alpha, beta=beta):
        return alpha + beta * x
     
    y = pm.Normal('y2', mu=y_model, tau=1. / sigma ** 2, observed=True, value=ydata)
     
    return locals()

# def bayesian_model(xdata, ydata):
#      
#     alpha = pm.Uniform('alpha', -100, 100)
#     x_rand  = pm.Normal('x_obs', mu=xdata, tau=(x_error)**-2)           # this allows error in x_obs
#  
#     @pm.stochastic(observed=False)
#     def beta(value=10):
#         return -1.5 * np.log(1 + value ** 2)
#      
#     @pm.observed
#     def sigma(value=y_error):
#         return sum(-np.log(abs(value)))
#      
#     # Define the form of the model and likelihood
#     @pm.deterministic
#     def y_model(x=x_rand, alpha=alpha, beta=beta):
#         return alpha + beta * x
#      
#     y = pm.Normal('y2', mu=y_model, tau=1. / sigma ** 2, observed=True, value=ydata)
#      
#     return locals()


MAP_Model               = pm.MAP(model(x_obs, y_obs))
MAP_Model.fit(method    = 'fmin_powell') 
MAP_Model.revert_to_max()
 
MDL = pm.MCMC(MAP_Model.variables, db = 'pickle', dbname =  '/home/vital/workspace/X_Data/' + 'linear_regression_InferenceModel')
MDL.use_step_method(pm.AdaptiveMetropolis, [MAP_Model.x_pred]) # use AdaptiveMetropolis to "learn" how to step
MDL.sample(200000, 100000, 10)  

MAP_Model2               = pm.MAP(bayesian_model(x_obs, y_obs))
MAP_Model2.fit() 
MAP_Model2.revert_to_max()

# package the full model in a dictionary
S = pm.MCMC(MAP_Model2.variables)
# S = pymc.MCMC(bayesian_model(xdata, ydata))
S.sample(200000, 100000, 10)  

 

print 'MAP predictions'
print 'm',  MAP_Model.m.value
print 'n',  MAP_Model.n.value

print 'Inference predictions'
print 'm', MDL.stats()['m']['mean']
print 'n', MDL.stats()['n']['mean']

print 'ODR predictions'
print 'm', out.beta[0]
print 'n', out.beta[1]

print 'MAP predictions 2'
print 'm',  MAP_Model2.beta.value
print 'n',  MAP_Model2.alpha.value

print 'Inference predictions 2'
print 'm', S.stats()['beta']['mean']
print 'n', S.stats()['alpha']['mean']

# extract and plot results
y_inf =  MDL.stats()['m']['mean'] * x_obs + MDL.stats()['n']['mean']
y_odr = quad_func(out.beta, x_obs)
y_inf2 = S.stats()['beta']['mean'] * x_obs + S.stats()['alpha']['mean']

MDL.db.close() 

plt.plot(x_true,y_true,'b', marker='.', ls='-',color='blue', lw=1, label='True')
plt.errorbar(x_obs, y_obs, yerr=y_error, xerr = x_error, color='black', marker='.', ls='None', label='Observed')
plt.plot(x_obs,y_inf,'k', marker='+', ls='-', color='red', ms=5, mew=1, label='Inference fit')
plt.plot(x_obs,y_odr,'k', marker='+', ls='-', color='green', ms=5, mew=1, label='odr fit')
plt.plot(x_obs,y_inf2,'k', marker='+', ls='-', color='brown', ms=5, mew=1, label='New inference fit')

plt.legend()
plt.show()


# import pymc                         as pm
# import numpy                        as np
# import matplotlib.pyplot            as plt
# from numpy                          import random
# from scipy.odr                      import *
# from Math_Libraries.bces_script     import bces
# 
# # set random seed for reproducibility
# 
# #True values for linear equation
# x_true = np.arange(0,50,3)
# m_true    = 1
# n_true    = 5
# y_true    = m_true * x_true + n_true
# 
# 
# # add noise_y to the data points
# noise_y     = np.random.normal(loc = 0, scale=3, size = len(x_true)) 
# y_error     = np.random.normal(loc = 0, scale=3, size = len(x_true))  
# y_obs           = y_true + noise_y 
# 
# noise_x     = np.random.normal(loc = 0, scale=4, size = len(x_true)) 
# x_error     = np.random.normal(loc = 0, scale=4, size = len(x_true)) 
# x_obs       = x_true + noise_x
# 
# def quad_func(p, x):
#     m, c = p
#     return m*x + c
# 
# # Create a model for fitting.
# quad_model = Model(quad_func)
# 
# # Create a RealData object using our initiated data from above.
# data = RealData(x_obs, y_obs, sx=x_error, sy=y_error)
# 
# # Set up ODR with the model and data.
# odr = ODR(data, quad_model, beta0=[0.15, 1.0])
# 
# # Run the regression.
# out = odr.run()
# 
# # Use the in-built pprint method to give us results.
# out.pprint()
# 
# Method_index  = 0
# m_bcesO ,n_bcesO, m_errO, n_errO, covabO = bces(x_obs, x_error, y_obs, y_error, np.zeros(len(x_error)))
# 
# 
# # define the model/function to be fitted.
# def model(x_obs, y_obs): 
#     m       = pm.Uniform('m', 0, 10, value= 0.15)
#     n       = pm.Uniform('n', -10, 10, value= 1.0)
#     x_pred  = pm.Normal('x_true', mu=x_obs, tau=(x_error)**-2)           # this allows error in x_obs
#   
#     #Theoretical values
#     @pm.deterministic(plot=False)
#     def linearD(x_true=x_pred, m=m, n=n):
#         return m * x_true + n
#     
#     @pm.deterministic
#     def random_operation_on_observable(y_obs=y_obs):
#         return y_obs + 0
#       
#     #likelihood
#     y = pm.Normal('y', mu=linearD, tau=1.0/y_error**2, value=random_operation_on_observable.value, observed=True)
#       
#     return locals()
# 
# 
# MAP_Model               = pm.MAP(model(x_obs, y_obs))
# MAP_Model.fit(method    = 'fmin_powell') 
# MAP_Model.revert_to_max()
# 
# 
# MDL = pm.MCMC(MAP_Model.variables, db = 'pickle', dbname =  '/home/vital/workspace/X_Data/' + 'linear_regression_inference2')
# MDL.use_step_method(pm.AdaptiveMetropolis, [MAP_Model.x_pred])          # use AdaptiveMetropolis to "learn" how to step
# MDL.sample(400000, 100000, 10)   
# 
# print 'Inference predictions'
# print 'm', MDL.stats()['m']['mean']
# print 'n', MDL.stats()['n']['mean']
# 
# print 'bces predictions'
# print 'm', m_bcesO[Method_index]
# print 'n', n_bcesO[Method_index]
# 
# print 'ODR predictions'
# print 'm', out.beta[0]
# print 'n', out.beta[1]
# 
# print 'MAP predictions'
# print 'm',  MAP_Model.m.value
# print 'n',  MAP_Model.n.value
# 
# 
# # extract and plot results
# y_inf =  MDL.stats()['m']['mean'] * x_obs + MDL.stats()['n']['mean']
# y_odr = quad_func(out.beta, x_obs)
# y_bces = m_bcesO[Method_index] * x_obs + n_bcesO[Method_index]
# 
# 
# MDL.db.close() 
# 
# plt.plot(x_true,y_true,'b', marker='.', ls='-',color='blue', lw=1, label='True')
# plt.errorbar(x_obs, y_obs, yerr=y_error, xerr = x_error, color='black', marker='.', ls='None', label='Observed')
# plt.plot(x_obs,y_inf,'k', marker='+', ls='-', color='red', ms=5, mew=1, label='Inference fit')
# plt.plot(x_obs,y_odr,'k', marker='+', ls='-', color='green', ms=5, mew=1, label='odr fit')
# plt.plot(x_obs,y_bces,'k', marker='+', ls='-', color='orange', ms=5, mew=1, label='bces fit')
# 
# plt.legend()
# plt.show()