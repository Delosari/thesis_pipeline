import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from line_measuring import LineMesurer
from astropy.io import fits

# Declare line mesurer object
lm = LineMesurer()

# Data location object
dataFolder = 'C:\\Users\\Vital\\PycharmProjects\\thesis_pipeline\\article3_material\\'
linesLogFile = 'obj_lineRegions'
spectrumAddress = 'E:\\Dropbox\\Astrophysics\\Papers\\Determination 2photon continua\\spec_in_cos_app.fits'
outputFile = 'E:\\Research\\NebularContinuum_fitting\\' + 'lineFluxes.txt'

z_obj = 0.0135

# Extract data
header_0, header_1 = fits.getheader(spectrumAddress, ext=0), fits.getheader(spectrumAddress, ext=1)
data_0, data_1 = fits.getdata(spectrumAddress, ext=0), fits.getdata(spectrumAddress, ext=1)
objLinesDF = pd.read_csv(dataFolder + linesLogFile, delim_whitespace=True, header=0, index_col=0)
objLinesDF.drop('N2_5755A', inplace=True)

# Declare object spectrum
wavel = data_0['wavel']
spec, specw = data_1['spec'], data_1['specw']
sigma_spectrum = np.sqrt(data_1['spec_var'])
wave, flux = wavel/(1+z_obj), spec/np.median(spec)

# Perform line fit
linesLog = lm.batch_line_fit(wave, flux, objLinesDF)

# Convert to string format and save to text file
string_frame = linesLog.to_string()
with open(outputFile, 'wb') as outputScript:
    outputScript.write(string_frame.encode('UTF-8'))

# Plot the spectrum
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.plot(wave, flux, color='tab:cyan', label='Object spectrum')
ax.update({'xlabel': r'Wavelength $(\AA)$', 'ylabel': 'Flux (normalised)'})
ax.legend()
plt.show()

