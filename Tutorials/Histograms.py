'''
Created on Aug 26, 2015

@author: vital
'''

import pymc
from numpy                                  import linspace, zeros, exp, array, arange, histogram, random
from CodeTools.PlottingManager              import myPickle
from Astro_Libraries.he_bayesian            import He_methods

def AverData():
    
    tau_mag         = linspace(0.25, 6.25, 13)
    tau_freq_WD     = array([22,8,6,3,3,2,2,1,0,2,0,0,1])
    tau_freq_UWD    = array([11,5,1,2,2,0,1,0,0,1,0,0,0])
    
    xi_frac         = linspace(0.05, 0.95, 10)
    xi_mag          = xi_frac / (1- xi_frac)
    xi_freq_WD      = array([45,5,2,7,1,3,1,2,1,3])
    xi_freq_UWD     = array([19,3,1,0,0,1,0,1,0,0])
    
    tau             = linspace(0.25, 6.25)
    
linspace(0.25, 6.25, 13)
#Generate dazer object
pv = myPickle()

#Define plot frame and colors
pv.FigFormat_One(ColorConf='Night1')


samples         = 10000
PyMC_Normal     = zeros(samples)
PyMC_Poisson    = zeros(samples)
x_EW            = arange(100, 400, 10)
mu_EW           = 1
sigma_EW        = 50

Normal_numpy = zeros(samples)
Poisson_numpy = zeros(samples)


for i in range(samples):
#     PyMC_Normal[i] = pymc.distributions.normal_like(x_EW, mu_EW, sigma_EW**-2)
    PyMC_Normal[i]      = pymc.Normal('sigma', mu_EW, sigma_EW**-2)
    Normal_numpy[i]     = random.normal(mu_EW, sigma_EW, 1)
    PyMC_Poisson[i]     = pymc.TruncatedPoisson('sigmaP', mu=mu_EW, k=0)
    Poisson_numpy[i]    = random.poisson(lam=mu_EW)

# HistData_NormalPymc, bin_edges_NormalPymc = histogram(PyMC_Normal, 20)
# HistData_np_NormalNumpy, bin_edges_np_NormalNumpy = histogram(Normal_numpy, 20)
#  
# pv.Axis1.bar(bin_edges_NormalPymc[:-1], HistData_NormalPymc, color='blue')
# pv.Axis1.bar(bin_edges_np_NormalNumpy[:-1], HistData_np_NormalNumpy, color='red')

HistData_PoissonPymc, bin_edges_PoissonPymc = histogram(PyMC_Poisson, 20)
HistData_np_PoissonNumpy, bin_edges_np_PoissonNumpy = histogram(Poisson_numpy, 20)

pv.Axis1.bar(bin_edges_PoissonPymc[:-1], HistData_PoissonPymc, color='green')
pv.Axis1.bar(bin_edges_np_PoissonNumpy[:-1], HistData_np_PoissonNumpy, color='purple')


pv.DisplayFigure()
