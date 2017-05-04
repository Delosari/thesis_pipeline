'''
Created on Jan 30, 2017

@author: vital
'''

from numpy import sqrt, pi, exp, linspace, random, empty, array
from scipy.optimize import curve_fit
from lmfit import Model
from timeit import default_timer as timer

def gaussian(x, amp, cen, wid):
    return amp * exp(-(x-cen)**2 /wid)

init_vals = [1, 0, 1]
x = linspace(-10,10)
n_points = len(x) 
gaussian_true = gaussian(x, 2.33, 0.21, 1.51)
gmod = Model(gaussian)


print '--Single fit'
start = timer()
best_vals, covar = curve_fit(gaussian, x, gaussian_true + random.normal(0, 0.2, n_points), p0=init_vals)
end = timer()
print 'curve fit', best_vals, ' time ', (end - start) 
start = timer()
result = gmod.fit(gaussian_true + random.normal(0, 0.2, n_points), x=x, amp=1, cen=0, wid=1)
end = timer()
print 'lmfit', array(result.params.valuesdict().values()), (end - start) 


print '--Bootstrap'
results_matrix_curvefit = empty([3,1000])
results_matrix_lmfit = empty([3,1000])
start = timer()
for i in range(1000):    
    best_vals, covar = curve_fit(gaussian, x, gaussian_true + random.normal(0, 0.2, n_points), p0=init_vals)
    results_matrix_curvefit[:,i] = best_vals
end = timer()
print 'curve fit', results_matrix_curvefit.mean(1), ' time ', (end - start) 


start = timer()
for i in range(1000):
    result = gmod.fit(gaussian_true + random.normal(0, 0.2, n_points), x=x, amp=1, cen=0, wid=1)
    results_matrix_lmfit[:,i] = array(result.params.valuesdict().values())
end = timer()
print 'lmfit', results_matrix_lmfit.mean(1), (end - start)