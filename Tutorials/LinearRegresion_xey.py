'''
Created on Mar 26, 2014

@author: vital
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import *

import random

# Initiate some data, giving some randomness using random.random().

x = np.array([0.0, 0.9, 1.8, 2.6, 3.3, 4.4, 5.2, 6.1, 6.5, 7.4])
y = np.array([5.9, 5.4, 4.4, 4.6, 3.5, 3.7, 2.8, 2.8, 2.4, 1.5])
wx = np.array([1000.0,1000,500,800,200,80,60,20,1.8,1.0])
wy = np.array([1,1.8,4,8,20,20,70,70,100,500])
x_err = 1/np.sqrt(wx)  # We need the errors in the residuals functions
y_err = 1/np.sqrt(wy)


# Define a function (quadratic in our case) to fit the data with.
def Linear_Func(p, x):
    m, c = p
    return m*x + c

# Create a model for fitting.
linear_model = Model(Linear_Func)

# Create a RealData object using our initiated data from above.
data = RealData(x, y, sx=x_err, sy=y_err)

# Set up ODR with the model and data.
odr = ODR(data, linear_model, beta0=[0., 1.])

# Run the regression.
out = odr.run()

# Use the in-built pprint method to give us results.
out.pprint()

print "Gradient m", out.beta[0], "+/-", out.sd_beta[0]
print "Y_p", out.beta[1], "+/-", out.sd_beta[1]

x_fit = np.linspace(x[0], x[-1], 1000)
y_fit = Linear_Func(out.beta, x_fit)

plt.errorbar(x, y, xerr=x_err, yerr=y_err, linestyle='None', marker='x')
plt.plot(x_fit, y_fit)

plt.show()


# Help on Output in module scipy.odr.odrpack object:
# 
# class Output(__builtin__.object)
#  |  The Output class stores the output of an ODR run.
#  |  
#  |  Attributes
#  |  ----------
#  |  beta : ndarray
#  |      Estimated parameter values, of shape (q,).
#  |  sd_beta : ndarray
#  |      Standard errors of the estimated parameters, of shape (p,).
#  |  cov_beta : ndarray
#  |      Covariance matrix of the estimated parameters, of shape (p,p).
#  |  delta : ndarray, optional
#  |      Array of estimated errors in input variables, of same shape as `x`.
#  |  eps : ndarray, optional
#  |      Array of estimated errors in response variables, of same shape as `y`.
#  |   : ndarray, optional
#  |      Array of ``x + delta``.
#  |  y : ndarray, optional
#  |      Array ``y = fcn(x + delta)``.
#  |  res_var : float, optional
#  |      Residual variance.
#  |  sum_sqare : float, optional
#  |      Sum of squares error.
#  |  sum_square_delta : float, optional
#  |      Sum of squares of delta error.
#  |  sum_square_eps : float, optional
#  |      Sum of squares of eps error.
#  |  inv_condnum : float, optional
#  |      Inverse condition number (cf. ODRPACK UG p. 77).
#  |  rel_error : float, optional
#  |      Relative error in function values computed within fcn.
#  |  work : ndarray, optional
#  |      Final work array.
#  |  work_ind : dict, optional
#  |      Indices into work for drawing out values (cf. ODRPACK UG p. 83).
#  |  info : int, optional
#  |      Reason for returning, as output by ODRPACK (cf. ODRPACK UG p. 38).
#  |  stopreason : list of str, optional
#  |      `info` interpreted into English.
#  |  
#  |  Notes
#  |  -----
#  |  Takes one argument for initialization, the return value from the
#  |  function `odr`. The attributes listed as "optional" above are only
#  |  present if `odr` was run with ``full_output=1``.
