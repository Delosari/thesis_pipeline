import numpy as np
from astropy.io import fits
from dazer_methods import Dazer


def show_me_the_bits(variable):

    for coso in variable:
        print coso, variable[coso]

    return

dz = Dazer()

dz.FigConf()

fits_address    = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/spec_in_cos_app.fits'

# wave, flux, ExtraData = dz.get_spectra_data(fits_address)
header_0        = fits.getheader(fits_address, ext=0)
header_1        = fits.getheader(fits_address, ext=1)
data_array_0    = fits.getdata(fits_address, ext=0)
data_array_1    = fits.getdata(fits_address, ext=1)

show_me_the_bits(header_0)
show_me_the_bits(header_1)

# wavel       Angstrom
# spec        Angstrom-1 cm-2 erg s-1
# spec_var    Angstrom-2 cm-4 erg2 s-2
# specw       Angstrom-1 cm-2 erg s-1

wavel           = data_array_0['wavel']
spec            = data_array_1['spec']
sigma_spectrum  = np.sqrt(data_array_1['spec_var'])
specw            = data_array_1['specw']

print wavel
print spec
print sigma_spectrum

dz.data_plot(wavel, spec, label='spec key')
# dz.data_plot(wavel, sigma_spectrum, label='sqrt(var)')


dz.Axis.fill_between(wavel, spec-sigma_spectrum, spec+sigma_spectrum, alpha=0.5)
dz.data_plot(wavel, specw, label='spec', linestyle=':')

dz.Axis.set_yscale('log')

dz.FigWording(r'Wavelength $(\AA)$', 'Flux ' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', 'Muse spectrum')
dz.display_fig()