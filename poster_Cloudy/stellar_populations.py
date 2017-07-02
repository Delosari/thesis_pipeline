from dazer_methods import Dazer
import os
import numpy as np


dz = Dazer()
dz.FigConf()

data_folder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/popstar_kroupa_004/'

for file_name in sorted(os.listdir(data_folder)):
    
    print file_name
    
    file_address = os.path.abspath(os.path.join(data_folder, file_name))
    
    wave, flux = np.loadtxt(file_address, usecols = (0, 3), unpack = True)
    
    age_float = 10**float(file_name[file_name.find('_t')+2:])
    print age_float / 1000000
    
    age = 'age = {} Myr'.format(round(age_float/ 1000000,2))
    
    dz.data_plot(wave, flux, label = age)

dz.Axis.set_xlim(0,10000)
dz.Axis.set_ylim(1e-9,1)
dz.Axis.set_yscale('log')    

dz.FigWording(r'Wavelength $(\AA)$', r'Normalized flux', 'Popstar grid for Kroupa IMF, $Z_{gas}=0.004$\n (including nebular continua)')

dz.display_fig()