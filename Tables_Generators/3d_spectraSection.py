# """
# Demonstrates using custom hillshading in a 3D surface plot.
# """
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cbook
# from matplotlib import cm
# from matplotlib.colors import LightSource
# import matplotlib.pyplot as plt
# import numpy as np
# 
# filename = cbook.get_sample_data('jacksboro_fault_dem.npz', asfileobj=False)
# with np.load(filename) as dem:
#     z = dem['elevation']
#     nrows, ncols = z.shape
#     x = np.linspace(dem['xmin'], dem['xmax'], ncols)
#     y = np.linspace(dem['ymin'], dem['ymax'], nrows)
#     x, y = np.meshgrid(x, y)
# 
# 
# 
# region = np.s_[5:50, 5:50]
# # x, y, z = x[region], y[region], z[region]
# 
# print x.shape
# print y.shape
# print z.shape
# 
# fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
# 
# ls = LightSource(270, 45)
# # To use a custom hillshading mode, override the built-in shading and pass
# # in the rgb colors of the shaded surface calculated from "shade".
# rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
# surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb, linewidth=0, antialiased=False, shade=False)
# 
# plt.show()


# from mpl_toolkits.mplot3d import axes3d
# import matplotlib.pyplot as plt
# 
# 
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# 
# # Grab some test data.
# X, Y, Z = axes3d.get_test_data(0.05)
# 
# 
# print X.shape, Y.shape, Z.shape
# 
# # Plot a basic wireframe.
# ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
# 
# plt.show()


'''
Created on Mar 13, 2017
 
@author: vital
'''
# from mpl_toolkits.mplot3d import Axes3D
from astropy.io             import fits
from dazer_methods          import Dazer
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np

#Create class object
dz = Dazer()
 
#Plot configuration
dz.frames_colors  = {'Blue arm':'bone', 'Red arm':'gist_heat'}
 
#Load the data
Spectra_address = '/home/vital/Astrodata/WHT_2011_11/Night1/objects/11_Blue_cr_f_t_w.fits' 
 
#Open the image
with fits.open(Spectra_address) as hdu_list:
    image_data = hdu_list[0].data

xmin, xmax, ymin, ymax = 90, 120, 400, 800

y = np.arange(ymin,ymax)
x = np.arange(xmin,xmax)
y,x = np.meshgrid(y, x)

image_section = np.rot90(image_data[ymin:ymax, xmin:xmax],1)

print y.shape
print x.shape
print image_section.shape

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
ls = LightSource(3, 50)
rgb = ls.shade(image_section, cmap=cm.viridis, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(x, y, image_section, rstride=1, cstride=1, facecolors=rgb, linewidth=0, antialiased=False, shade=False)
#ax.plot_wireframe(x, y, image_section, rstride=10, cstride=5)
ax.set_title(r'HII Galaxy 11: Galaxy spectrum $4659\AA$ to $4740\AA$')

# # image_data[:, x_max-2:x_max+2].mean(axis=1)
# # dz.fits_to_frame(Spectra_address, dz.Axis, color = 'Blue arm')
#                                                               
# #Get zscale limits for plotting the image
# IntensityLimits     = ZScaleInterval()
# int_min, int_max    = IntensityLimits.get_limits(image_data)[0], IntensityLimits.get_limits(image_data)[1]
#  
# #Plot the data
# dz.Axis.imshow(image_section, cmap='bone', origin='lower', vmin = int_min, vmax = int_max, interpolation='nearest', aspect='auto')
# # axis_plot.set_xlim(0, image_data.shape[1])
# # axis_plot.set_ylim(0, image_data.shape[0])
# 
# dz.FigWording(xlabel='', ylabel='', title = r'Object 11 WHT spectrum: $4659\AA$ to $4740\AA$')
#  
# dz.display_fig()

plt.show()


