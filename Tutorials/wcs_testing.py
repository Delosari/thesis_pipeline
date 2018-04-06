import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import download_file
from astropy.nddata import Cutout2D
from astropy import coordinates, units as u

#Import Horsehead Nebula example image from the tutorials database
fits_file = 'http://data.astropy.org/tutorials/FITS-images/HorseHead.fits'
image_file = download_file(fits_file, cache=False)

# Load the image and the world coordinates from the header
hdu = fits.open(image_file)[0]
wcs = WCS(hdu.header)

# Get Horsehead Nebula coordinates
horsehead_coord = coordinates.SkyCoord.from_name('Horsehead Nebula')

# Defining new image pixel size
sizeTrim = (400*u.pixel, 400*u.pixel)

# Making the cutout using the wcs
cutout = Cutout2D(hdu.data, position=horsehead_coord, size=sizeTrim, wcs=wcs)

# Update image data
hdu.data = cutout.data

# Update the WCS from the cutout
hdu.header.update(cutout.wcs.to_header())

# Replace original image by the new "trimmed" version
hdu.writeto(image_file, overwrite=True)

# Load the new image
hdu = fits.open(image_file)[0]
wcs = WCS(hdu.header)

# Plot the image
fig = plt.figure()
fig.add_subplot(111, projection=wcs)
plt.imshow(wcs.data, origin='lower', cmap=plt.cm.viridis)
plt.xlabel('RA')
plt.ylabel('Dec')
plt.show()




# import numpy as np
# from matplotlib import pyplot as plt
# from astropy.io import fits
# from astropy.wcs import WCS
# from astropy.utils.data import download_file
# from astropy.nddata import Cutout2D
# from astropy import coordinates
# from astropy import units as u
#
# fits_file = 'http://data.astropy.org/tutorials/FITS-images/HorseHead.fits'
# image_file = download_file(fits_file, cache=False)
# hdu = fits.open(image_file)[0]
# wcs = WCS(hdu.header)
#
# horsehead_coord = coordinates.SkyCoord.from_name('Horsehead Nebula')
# horseHead_pixCoord = wcs.wcs_world2pix([(horsehead_coord.ra.deg, horsehead_coord.dec.deg)],0)
#
# sizeTrim = (400*u.pixel, 400*u.pixel)
#
# cutout = Cutout2D(hdu.data, position=horseHead_pixCoord[0], size=sizeTrim, wcs=wcs)
#
# #Update image data
# hdu.data = cutout.data
#
# #Update the WCS from the cutout
# fits_hdu_list[1].header.update(wcs.to_header())
#
# #Replace original image by the new "trimmed" version
# hdu.writeto(image_file, overwrite=True)
#
# hdu = fits.open(image_file)[0]
# wcs = WCS(hdu.header)
#
# fig = plt.figure()
# fig.add_subplot(111, projection=wcs)
# plt.imshow(hdu.data, origin='lower', cmap=plt.cm.viridis)
# plt.xlabel('RA')
# plt.ylabel('Dec')
# plt.show()










# plt.imshow(hdu.data, origin='lower', cmap=plt.cm.viridis)
# plt.plot(hxpix, hypix, 's')
#
# plt.xlabel('RA')
# plt.ylabel('Dec')
# plt.show()

# # Print out all of the settings that were parsed from the header
# w.wcs.print_contents()
# print '---------------------'
# print type(w)
# print '%%%%%%%%%%%%%%%%%%%%%'
# print w.crpix
#
# # # Create a new WCS object.  The number of axes must be set
# # # from the start
# wi = WCS(naxis=2)
#
# # Set up an "Airy's zenithal" projection
# # Vector properties may be set with Python lists, or Numpy arrays
# wi.wcs.crpix = [-234.75, 8.3393]
# wi.wcs.cdelt = np.array([-0.066667, 0.066667])
# wi.wcs.crval = [0, -90]
# wi.wcs.ctype = ["RA---AIR", "DEC--AIR"]
# wi.wcs.set_pv([(2, 1, 45.0)])
#
#
# # Three pixel coordinates of interest.
# # Note we've silently assumed a NAXIS=2 image here
# pixcrd = np.array([[0, 0], [24, 38], [45, 98]], np.float_)
#
# # Convert pixel coordinates to world coordinates
# # The second argument is "origin" -- in this case we're declaring we
# # have 1-based (Fortran-like) coordinates.
# world = w.wcs_pix2world(pixcrd, 1)
# print type(world)
#
# # WCS object overwrites the old WCS information in the header
# hdulist[1].header.update(wi.to_header())
#
#
