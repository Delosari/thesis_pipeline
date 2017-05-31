from DZ_observation_reduction   import spectra_reduction
from astropy.io                 import fits

dz = spectra_reduction()

gain_key        = 'GAIN'
readnoise_key   = 'READNOIS'
header_ext      = 0
data_ext        = 1

fits_address    = '/home/vital/Astrodata/WHT_2011_11/Night1/raw_fits/r01725572.fits'
#output_address  = '/home/vital/Astrodata/WHT_2011_11/Night1/raw_fits/r01725572_error.fits'
output_address  = '/home/vital/Astrodata/WHT_2011_11/Night1/raw_fits/r01725572_data_error.fits'

#Open the image
with fits.open(fits_address) as hdu_list:
    image_data    = hdu_list[data_ext].data
    header        = hdu_list[data_ext].header    
    gain          = header[gain_key]
    readout_noise = header[readnoise_key]
    header_0      = hdu_list[0].header
    header_1      = hdu_list[1].header
    
for key in header_0:
    print key, header_0[key]
print
print '-------------Length array 0', len(header_0)
print
for key in header_1:
    print key, header_1[key]
print
print '-------------Length array 1', len(header_1)
print

variance_data     = (1.0 / gain) * image_data + readout_noise**2

#Store the frames        
hdu1_header = fits.PrimaryHDU(header = header_0)
hdu1_data   = fits.ImageHDU(data=image_data, header = header_1)
hdu2_error  = fits.ImageHDU(data=variance_data)
new_hdul    = fits.HDUList([hdu1_header, hdu1_data, hdu2_error])
new_hdul.writeto(output_address, overwrite=True)
                