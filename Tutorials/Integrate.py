'''
Created on Feb 18, 2015

@author: vital
'''
from numpy import abs, exp, linspace
from scipy.integrate import simps, trapz, quad
import matplotlib.pyplot as plt

def SingleGaussian_Cont(Ind_Variables, A, mu, sigma):

#   In order to increase somehow the speed we simplify the code by no asigning many variables
    x           = Ind_Variables[0]
    continuum   = Ind_Variables[1]
    y = A * exp(-(x-mu)*(x-mu)/(2.0*sigma*sigma)) + continuum

    return y

def IntegrateSimps(x,y,zerolev):

    Area_Continuum  = simps(zerolev, x) 
    Area_Total      = simps(y, x)
    
    AreaGauss       = Area_Total - Area_Continuum
    
    print 'Simps Continuum', Area_Continuum
    print 'Simps Total', Area_Total
    print 'Gauss', AreaGauss,'\n'
    
    return

def IntegrateTrapz(x,y,zerolev):

    Area_Continuum  = trapz(zerolev, x) 
    Area_Total      = trapz(y, x)
    
    AreaGauss       = Area_Total - Area_Continuum
    
    print 'trapz Continuum', Area_Continuum
    print 'trapz Total', Area_Total
    print 'Gauss', AreaGauss,'\n'
    
    return


def triangle_line(Ind_Variables, A, mu, sigma):

#   In order to increase somehow the speed we simplify the code by no asigning many variables
    x   = Ind_Variables[0]
    m   = Ind_Variables[1]
    n   = Ind_Variables[2]
    
    y = m * x + n
    
    
    
    idx = (np.abs(array-value)).argmin()
    
    
    mu  = Ind_Variables[1]
    y   = A * exp(-(x-mu)*(x-mu)/(2.0*sigma*sigma)) + continuum

    return y





x           = linspace(-1, 1, 101)
Continuum   = [10] * len(x) 
Continuum_0 = [0] * len(x) 

A           =  1
mu          =  0
sigma       =  1
# y         = SingleGaussian_Cont((x, Continuum), A, mu, sigma)
y_alone     = SingleGaussian_Cont((x, Continuum_0), A, mu, sigma)
IntegrateTrapz(x,y_alone,Continuum_0)
# print 'y_alone', y_alone

print 'New area'

x           = linspace(3, 5, 101)
Continuum   = [10] * len(x) 
Continuum_0 = [0] * len(x) 

A           =  10
mu          =  0
sigma       =  1
print x
y_alone2    = SingleGaussian_Cont((x, Continuum_0), A, mu, sigma)
IntegrateTrapz(x,y_alone,Continuum_0)
# print 'y_alone', y_alone

print 'Rate', y_alone2/y_alone

plt.plot(x,y_alone)
plt.show()