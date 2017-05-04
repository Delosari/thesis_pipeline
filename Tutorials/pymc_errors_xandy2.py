import pymc                         as pm
import numpy                        as np
import matplotlib.pyplot            as plt
from numpy                          import random
from Math_Libraries.bces_script     import bces
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
    def random_operation_on_observable(obs_values=y_obs, m=m):
        return obs_values + 0 * m

    @pm.deterministic
    def random_operation_on_observable2(obs_values=random_operation_on_observable, m=m):
        return obs_values + 0 * m

    #likelihood
    y = pm.Normal('y', mu=linearD, tau=1.0/y_error**2, value=random_operation_on_observable2.value, observed=True)

    return locals()

MAP_Model               = pm.MAP(model(x_obs, y_obs))
MAP_Model.fit(method    = 'fmin_powell') 
MAP_Model.revert_to_max()

MDL = pm.MCMC(MAP_Model.variables, db = 'pickle', dbname =  '/home/vital/workspace/X_Data/' + 'linear_regression_InferenceModel')
MDL.use_step_method(pm.AdaptiveMetropolis, [MAP_Model.x_pred]) # use AdaptiveMetropolis to "learn" how to step
MDL.sample(400000, 100000, 10)   

print 'MAP predictions'
print 'm',  MAP_Model.m.value
print 'n',  MAP_Model.n.value

print 'Inference predictions'
print 'm', MDL.stats()['m']['mean']
print 'n', MDL.stats()['n']['mean']

print 'ODR predictions'
print 'm', out.beta[0]
print 'n', out.beta[1]

# extract and plot results
y_inf =  MDL.stats()['m']['mean'] * x_obs + MDL.stats()['n']['mean']
y_odr = quad_func(out.beta, x_obs)

MDL.db.close() 

plt.plot(x_true,y_true,'b', marker='.', ls='-',color='blue', lw=1, label='True')
plt.errorbar(x_obs, y_obs, yerr=y_error, xerr = x_error, color='black', marker='.', ls='None', label='Observed')
plt.plot(x_obs,y_inf,'k', marker='+', ls='-', color='red', ms=5, mew=1, label='Inference fit')
plt.plot(x_obs,y_odr,'k', marker='+', ls='-', color='green', ms=5, mew=1, label='odr fit')

plt.legend()
plt.show()