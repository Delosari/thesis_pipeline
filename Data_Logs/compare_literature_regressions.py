from numpy import loadtxt
from dazer_methods  import Dazer

table_address = '/home/vital/Dropbox/Astrophysics/Data/Literature linear regression/Peimbert2016'

types_list = [('f8',str),('f1',float),('f2',float),('f3',float),('f4',float),('f5',float)]
objects, Y_mean, Y_sys, Y_random, O_mean, O_err = loadtxt(table_address, dtype=types_list, unpack=True)
objects = loadtxt(table_address, dtype=str, usecols=(0),unpack=True)

O_mean  = O_mean * 1e-4
O_err   = O_err * 1e-4

print objects
print Y_mean
print Y_sys
print Y_random
print O_mean
print O_err

dz = Dazer()

dz.FigConf()

dz.data_plot(O_mean, Y_mean, label='Peimbert et al (2016)', markerstyle='o', x_error=O_err, y_error=Y_sys)
dz.plot_text(O_mean, Y_mean, text=objects)

dz.FigWording(xlabel='Oxygen abundance', ylabel = 'Helium mass fraction', title = r'$Y_{P}$ oxygen regression, Peimbert et al (2016)')

dz.display_fig()