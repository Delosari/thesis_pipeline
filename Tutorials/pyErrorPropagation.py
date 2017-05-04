import Scientific_Lib.AstroMethods as astro
import numpy as np

from uncertainties import ufloat


x = np.array([4.52])
y = np.array([2.0])
z = np.array([3.0])
 
pi = 3.14159265359

sigma_x = np.array([0.02])
sigma_y = np.array([0.2])
sigma_z = np.array([0.2])

x_y_err = ufloat( x, sigma_x )
y_y_err = ufloat( y, sigma_y )
z_y_err = ufloat( z, sigma_z )

result =  2*pi*z_y_err

error_unc = result.std_dev

print "Resultado", result
print "Error unc", error_unc
print "Valor", result.nominal_value

#print "Error mio", astro.EP_Sum([0.02,0.2,0.6])

#print astro.EP_Constant([1.0,-2.0], [0.2,0.6])
# 
# z = np.array([0.67])
# x = np.array([2.0,3.0])
# Sigma = np.array([0.2,0.6])
# 
# print "resultado"
# print astro.EP_MulDiv(z,  x, Sigma)

#result =  x_y_err * z_y_err**2 / unumpy.sqrt(y_y_err)       #How to execute powers and square roots
