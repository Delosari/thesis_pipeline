'''
Created on Sep 28, 2016

@author: vital
'''
import matplotlib.pyplot as plt
from astropy.io import fits
from numpy import array, empty, arange
from numpy.polynomial.legendre import Legendre, legval
from astropy.visualization import ZScaleInterval

Pdf_Fig, Axis = plt.subplots(1, 1, figsize=(6, 12))  

trace_address   = '/home/vital/Astrodata/WHT_2009_07/Night2/standard_stars/database/ap_home_vital_Astrodata_WHT_2009_07_Night2_standard_stars_BD+28_Blue_Wide_f_t_w'
fits_address    = '/home/vital/Astrodata/WHT_2009_07/Night2/standard_stars/BD+28_Blue_Wide_f_t_w.fits'

file_trace  = open(trace_address)
file_lines  = file_trace.readlines()

idx_start = file_lines.index('\taxis\t1\n') + 1 #That '\t1' is the orientation of the frame
print file_lines

#Load the image data
with fits.open(fits_address) as hdu_list:
    image_data = hdu_list[0].data

# print file_lines '\tcenter\t102.747 400.\n'

# matching    = [s for s in file_lines if '\tcenter\t' in s]
idx_match   = [i for i in range(len(file_lines)) if '\tcenter\t' in file_lines[i]]

center_line = file_lines[idx_match[0]]
lower_line  = file_lines[idx_match[0]+1]
upper_line  = file_lines[idx_match[0]+2]

aper_center = map(float, center_line.split()[1:])
aper_low    = map(float, lower_line.split()[1:])
aper_high   = map(float, upper_line.split()[1:])

y_values = image_data.mean(axis=1) 
x_values = range(len(y_values))

#Load the fit properties
coef_n      = file_lines[idx_start].split()[1]
fit_type    = float(file_lines[idx_start + 1].split()[0])
order       = int(float(file_lines[idx_start + 2].split()[0]))
xmin        = int(float(file_lines[idx_start + 3].split()[0]))
xmax        = int(float(file_lines[idx_start + 4].split()[0]))
coefs       = empty(order)
for i in range(len(coefs)):
    coefs[i] = float(file_lines[idx_start + 5 + i].split()[0]) 

#Plot the polynomial
y_range     = arange(float(xmin), float(xmax))
n           = (2 * y_range - (xmax + xmin)) / (xmax - xmin)
poly_leg    = legval(n, coefs)
trace_curve = poly_leg + aper_center[0]
low_limit   = trace_curve + aper_low[0]
high_limit  = trace_curve + aper_high[0]


#Plot Background region
idx_background  = [i for i in range(len(file_lines)) if '\t\tsample' in file_lines[i]]
background_line = file_lines[idx_background[0]].split()[1:]
for region in background_line:
    limits_region       = map(float, region.split(':'))
    low_limit_region    = trace_curve + limits_region[0]
    high_limit_region   = trace_curve + limits_region[1]    
    Axis.fill_betweenx(y_range, low_limit_region, high_limit_region, alpha=0.1, facecolor='yellow')

 
IntensityLimits = ZScaleInterval()
int_min, int_max = IntensityLimits.get_limits(image_data)[0], IntensityLimits.get_limits(image_data)[1]
Axis.imshow(image_data, cmap='bone', origin='lower', vmin = int_min, vmax = int_max, interpolation='nearest')
Axis.plot(trace_curve, y_range, color='red')
#Axis.plot(low_limit, y_range, color='red')
#Axis.plot(high_limit, y_range, color='red')
Axis.fill_betweenx(y_range, low_limit, high_limit, alpha=0.3, facecolor='purple')


plt.axis('tight')

plt.show()