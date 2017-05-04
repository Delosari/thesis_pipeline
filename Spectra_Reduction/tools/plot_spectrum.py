'''
Created on Oct 21, 2016

@author: vital
'''
import  matplotlib.pyplot as plt
from DZ_observation_reduction import spectra_reduction
import matplotlib.style
matplotlib.style.use('dark_background')

#Load iraf pypeline object

dz = spectra_reduction()

fig, axis = plt.subplots(1, 1, figsize=(10, 7))

files_list = [
'/home/vital/Astrodata/WHT_2011_11/Night1/objects/F34_Blue_Wide_f_t_w_e_flocal.fits',
'/home/vital/Astrodata/WHT_2011_11/Night1/objects/F34_Blue_Wide_f_t_w_e_fglobal.fits',
'/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/fcF34fl.fits'
]
# files_list = [
# '/home/vital/Astrodata/WHT_2011_11/Night1/objects/F34_Blue_Wide_f_t_w_e.fits',
# '/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/wcblueF34fl.fits'
# ]

for file_fits in files_list:
    
    wavelength, Flux_array, header = dz.get_spectra_data(file_fits, ext=0)
    
    axis.plot(wavelength, Flux_array[0][0], label = file_fits[file_fits.rfind('/'):-1])
   
axis.legend()
axis.set_yscale('log')
plt.show()

# /home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/fcPHL-f34.fits