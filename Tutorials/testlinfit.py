'''
Created on Sep 26, 2014

@author: INAOE_Vital
'''

from numpy import array

from numpy import array, sqrt

from Math_Libraries.FittingTools                        import linfit

print 'linfit input'
x_mag = array([ 0.001,         -0.31313057, -0.52515563, -0.54554792,-0.55673928, -0.59301119])
y_mag = array([ 0.001,         -0.00951476,  0.25436478,  0.25596026,  0.26149736,  0.        ])
y_err = array([ 0.001,          0.001        ,  0.11393642,  0.05793664,  0.03031095,  0.02321068])

print x_mag
print y_mag
print y_err

Regression_Fit, Uncertainty_Matrix = linfit(x_mag, y_mag, y_err, cov=True, relsigma=False)
m_n_error                   = [sqrt(Uncertainty_Matrix[t,t]) for t in range(2)]

print m_n_error