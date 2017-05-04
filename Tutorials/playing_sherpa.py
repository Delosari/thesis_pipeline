'''
Created on Oct 13, 2016

@author: vital
'''
import numpy as np
import matplotlib.pyplot as plt
from sherpa.data import Data1D
from sherpa.models import PowLaw1D, Gauss1D
from sherpa.stats import Chi2DataVar
from sherpa.optmethods import LevMar
from sherpa.fit import Fit
from astropy.io import fits

def plot_data(x, y, err=None, fmt='.', clear=True):
    if clear:
        plt.clf()
    plt.plot(x, y, fmt)
    if err is not None:
        plt.errorbar(x, y, err, fmt=None, ecolor='b')

url = 'http://python4astronomers.github.com/_downloads/3c273.fits'
# open('3c273.fits', 'wb').write(request.urlopen(url).read())

dat     = fits.open('3c273.fits')[1].data
wlen    = dat.field('WAVELENGTH')
flux    = dat.field('FLUX')

wave = dat.field('WAVELENGTH')
flux = dat.field('FLUX') * 1e14
err  = dat.field('FLUX') * 0.02e14

data = Data1D('3C 273', wave, flux, err)
plot_data(data.x, data.y, data.staterror)
pl = PowLaw1D('pl')
g1 = Gauss1D('g1')
g2 = Gauss1D('g2')
g3 = Gauss1D('g3')
g4 = Gauss1D('g4')

g1.pos = 3250
g2.pos = 5000
g3.pos = 5260
g4.pos = 5600

# for p in [g1, g2, g3, g4]:
#     p.fwhm = 50

parameters = pl + g1 + g2 + g3 + g4

pl.ref = 4000.

print g1
print type(g1)

g1broad = Gauss1D('g1broad')
g1broad.pos = g1.pos
g1broad.fwhm = g1.fwhm * 4

parameters = parameters + g1broad

f = Fit(data, parameters, Chi2DataVar(), LevMar())
result = f.fit()

plot_data(data.x, parameters(data.x), fmt="-", clear=False)
plt.show()
print 'hola'


