import numpy as np

FileAddress             = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue_SulfurRegression/Objects/08/08_WHT_EmissionFlux_LinesLog_v3.txt'
data_type               = float
LinesLog_HeaderLength   = 2
headers = 
idx_of_a_in_b           = [ 2,  3,  4,  7,  9, 10]
columns                 = np.transpose(np.loadtxt(FileAddress, dtype=data_type, skiprows = LinesLog_HeaderLength, usecols = idx_of_a_in_b))
a,b,c,d,e,f             = np.loadtxt(FileAddress, dtype=data_type, skiprows = LinesLog_HeaderLength, usecols = idx_of_a_in_b, unpack = True)

# print 'Antes', columns
# size = columns.size
print 'Despues', columns[0]



# print a
# print b
# print c

# from uncertainties.umath import *
# from uncertainties import ufloat
# import uncertainties.unumpy as unumpy  
# import numpy  
# import numpy as np
# 
# mags    = np.ones(10)
# errors  = np.zeros(10) + 0.1
# 
# print mags
# print errors
# 
# combined = unumpy.uarray(mags, errors)
# print 'una', combined[0]
# print 'dos', combined[0].std_dev

# x = ufloat(0.20, 0.01)
# print sin(x**2)
# 
# def random_normal(mean,std,n):  
# #       """  
# #  Returns an array of n elements of random variables, following a normal   
# #  distribution with the supplied mean and standard deviation.  
# #       """  
#     import scipy  
#     return std*scipy.random.standard_normal(n)+mean  
#  
#  
# Flux_gamma  = ufloat(454, 11)
# Flux_beta   = ufloat(1000, 10)
# chbeta      = ufloat(0.12, 0.02)
# f_gamma     = 0.157
#  
# print 'flux', Flux_gamma
# flux_derred = Flux_gamma * unumpy.pow(10, (f_gamma * chbeta))
# print 'flux derred', flux_derred
#  
# # pow_Coef =              unumpy.uarray(0.12,0.02) * (f_gamma)
# #  
# # print 'my power coeff', pow_Coef
# #  
# # print 'power 1',        Flux* 10**(pow_Coef)
# # derr_flux   =           Flux * unumpy.pow(10, (pow_Coef))
# # print 'derflux' 
# # print 'power 2',        unumpy.nominal_values(derr_flux), unumpy.std_devs(derr_flux)
# #  
# # print 'basic relation', unumpy.log10(unumpy.uarray(474,28)/unumpy.uarray(454, 11))
# # print 'by /flambda',    unumpy.log10(unumpy.uarray(474,28)/unumpy.uarray(454, 11)) / 0.157
#  
# f_gamma             = ufloat(0.157, 0.0)
# f_beta              = ufloat(0.0,0.0)
# chbeta              = ufloat(0.12,0.02)
#  
# # normalizing_flux    = unumpy.uarray(2.70e-15, 0.010 * 2.70e-15)
# # test = 1000 * normalizing_flux / 2.70e-15
# # print 'esto esta bien?', unumpy.nominal_values(test), unumpy.std_devs(test)
# # 
# # normalizing_flux    = unumpy.uarray(0.454*2.70e-15, 0.011*2.70e-15)
# # test = 1000 * normalizing_flux / 2.70e-15
# # print 'esto esta bien2?', unumpy.nominal_values(test), unumpy.std_devs(test)
# print
# print
# print 'normalizing flux',
# normalizing_flux = ufloat(2.70e-15, 0.010 * 2.70e-15)
#  
# Flux_Hbeta          = ufloat(2.70e-15, 0.010 * 2.70e-15)
# Flux_Hgamma         = ufloat(0.454*2.70e-15, 0.011*2.70e-15)
#  
# Flux_Hbeta_derred   =    Flux_Hbeta     * unumpy.pow(10, f_beta * chbeta)
# Flux_Hgamma_derred  =    Flux_Hgamma    * unumpy.pow(10, f_gamma * chbeta)
#  
# print 'F beta',     Flux_Hbeta  
# print 'F gamma',    Flux_Hgamma / normalizing_flux
#  
# print 'I beta',     Flux_Hbeta_derred / normalizing_flux
# print 'I gamma',    Flux_Hgamma_derred / normalizing_flux
# print 'I ratio',    Flux_Hgamma_derred / Flux_Hbeta_derred
#  
# # Defines x and y  
# x=numpy.linspace(0,10,50)  
# y=numpy.linspace(15,20,50)  
#    
# # Defines the error arrays, values follow a normal distribution  
# # (method random_normal defined in http://astropython.blogspot.com/2012/04/how-to-generate-array-of-random-numbers.html)  
# errx=random_normal(0.1,0.2,50);     errx=numpy.abs(errx)  
# erry=random_normal(0.3,0.2,50);     erry=numpy.abs(erry)  
#    
# # Defines special arrays holding the values *and* errors  
# x=unumpy.ufloat([ x],[ errx ])  
# y=unumpy.uarray([ y],[ erry ])  
#    
# # """  
# # Now any operation that you carry on xerr and yerr will   
# # automatically propagate the associated errors, as long  
# # as you use the methods provided with uncertainties.unumpy  
# # instead of using the numpy methods.  
# #   
# # Let's for instance define z as   
# # z = log10(x+y**2)  
# # and estimate errz.  
# # """  
# z=unumpy.log10(x+y**2)  
#    
# # Print the propagated error errz  
# errz=unumpy.std_devs(z)  
# # print errz  