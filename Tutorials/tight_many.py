'''
Created on Sep 29, 2016

@author: vital
'''

from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import download_file
from matplotlib import pyplot as plt

fits_file   = 'http://data.astropy.org/tutorials/FITS-images/HorseHead.fits'
image_file  = download_file(fits_file, cache=True)
hdu         = fits.open(image_file)[0]
wcs         = WCS(hdu.header)

Fig, GridAxis = plt.subplots(1, 2, figsize=(15, 20))  
GridAxis_list = GridAxis.ravel()

for i in range(2):
    GridAxis_list[i].imshow(hdu.data, origin='lower', cmap='cubehelix', interpolation='nearest')
    GridAxis_list[i].set_ylabel('RA')
    GridAxis_list[i].set_xlabel('Dec')
    GridAxis_list[i].scatter(450, 450) #If data is not plotted over the image the tight layout seems to work as espected #GridAxis_list[i].set_adjustable('box-forced')
    GridAxis_list[i].set_ylim(0, hdu.data.shape[0])
    GridAxis_list[i].set_xlim(0, hdu.data.shape[1])
    
    
#plt.axis('tight')

#plt.tight_layout()

plt.show()
