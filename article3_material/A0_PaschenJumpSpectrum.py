import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from dazer_methods import Dazer

def onclick(event):
    print('Wavelength xdata=%f' % (event.xdata))


fits_address = 'E:\\Dropbox\\Astrophysics\\Papers\\Determination 2photon continua\\spec_in_cos_app.fits'

header_0        = fits.getheader(fits_address, ext=0)
header_1        = fits.getheader(fits_address, ext=1)
data_array_0    = fits.getdata(fits_address, ext=0)
data_array_1    = fits.getdata(fits_address, ext=1)

wavel           = data_array_0['wavel']
spec            = data_array_1['spec']
sigma_spectrum  = np.sqrt(data_array_1['spec_var'])
specw           = data_array_1['specw']

z_obj = 0.0135

newsSpectrumAddress = 'E:\\Research\\NebularContinuum_fitting\\' + 'objSpectrum.txt'
np.savetxt(newsSpectrumAddress, np.transpose(np.array([wavel/(1+z_obj), spec])))#, fmt="%4.1f %10.4e")

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
cid = fig.canvas.mpl_connect('button_press_event', onclick)
# fig.canvas.mpl_disconnect(cid)

ax.plot(wavel/(1+z_obj), spec, label='spec key')
ax.plot(wavel/(1+z_obj), sigma_spectrum, label='specw key')
ax.update({'xlabel': r'Wavelength $(\AA)$', 'ylabel': 'Flux (normalised)'})
ax.set_yscale('log')
ax.legend()
plt.show()