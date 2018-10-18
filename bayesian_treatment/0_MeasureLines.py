import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.inferenceModel import SpectraSynthesizer
from lib.Astro_Libraries.spectrum_fitting.import_functions import ImportModelData
from scipy import stats
from numpy.random import normal
from scipy.optimize import curve_fit

# Let's create a function to model and create data
def gaussFunc(ind_params, a, mu, sigma):
    x, z = ind_params
    return a*np.exp(-((x-mu)*(x-mu))/(2*(sigma*sigma))) + z

def generate_object_mask(linesDf, wavelength, linelabels):
    # TODO This will not work for a redshifted lines log
    idcs_lineMasks = linesDf.index.isin(linelabels)
    idcs_spectrumMasks = ~linesDf.index.isin(linelabels)

    # Matrix mask for integring the emission lines
    n_lineMasks = idcs_lineMasks.sum()
    boolean_matrix = np.zeros((n_lineMasks, wavelength.size), dtype=bool)

    # Total mask for valid regions in the spectrum
    n_objMasks = idcs_spectrumMasks.sum()
    int_mask = np.ones(wavelength.size, dtype=bool)
    object_mask = np.ones(wavelength.size, dtype=bool)

    # Loop through the emission lines
    wmin, wmax = linesDf['w3'].loc[idcs_lineMasks].values, linesDf['w4'].loc[idcs_lineMasks].values
    idxMin, idxMax = np.searchsorted(wavelength, [wmin, wmax])
    for i in range(n_lineMasks):
        idx_currentMask = (wavelength >= wavelength[idxMin[i]]) & (wavelength <= wavelength[idxMax[i]])
        boolean_matrix[i, :] = idx_currentMask
        int_mask = int_mask & ~idx_currentMask

    # Loop through the object masks
    wmin, wmax = linesDf['w3'].loc[idcs_spectrumMasks].values, linesDf['w4'].loc[idcs_spectrumMasks].values
    idxMin, idxMax = np.searchsorted(wavelength, [wmin, wmax])
    for i in range(n_objMasks):
        idx_currentMask = (wavelength >= wavelength[idxMin[i]]) & (wavelength <= wavelength[idxMax[i]])
        int_mask = int_mask & ~idx_currentMask
        object_mask = object_mask & ~idx_currentMask

    return boolean_matrix

# Declare synthesizer object
specS = ImportModelData()

#Import library object
dz = Dazer()

# Object database
dataFolder = '/home/vital/SpecSynthesizer_data/'
whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtSpreadSheet)
dz.quick_indexing(catalogue_df)

# Data root folder
root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'

objName = '8'

objectFolder = '{}{}/'.format(root_folder, objName)
dataLocation = '{}{}/{}_objParams.txt'.format(root_folder, objName, objName)
obsData = specS.load_obsData(dataLocation, objName)
objLinesLogDf = pd.read_csv(obsData['obj_lines_file'], delim_whitespace=True, header=0, index_col=0)

wave = obsData['obs_wavelength']
flux = obsData['obs_flux']
linesDf = objLinesLogDf.loc[:'H1_9546A']

lineLabels = linesDf.index.values   # TODO in here we use the lines proposed by the user
normFluxCoeff = np.median(flux)     # TODO in here we use the norm flux from the continuum
fluxNorm = flux/normFluxCoeff

lines_mask = generate_object_mask(linesDf, wave, lineLabels)

areaWaveN_matrix = linesDf.loc[:,'w1':'w6'].values # TODO in here we use the lines proposed by the user

#Get line and adjacent continua region
ares_indcs = np.searchsorted(wave, areaWaveN_matrix)
idcsLines = (wave[ares_indcs[:,2]] <= wave[:,None]) & (wave[:,None] <= wave[ares_indcs[:,3]])
idcsContinua = ((wave[ares_indcs[:,0]] <= wave[:,None]) & (wave[:,None] <= wave[ares_indcs[:,1]])) | ((wave[ares_indcs[:,4]] <= wave[:,None]) & (wave[:,None] <= wave[ares_indcs[:,5]]))

n_randomPoints = 1000
rangeFittings = np.arange(n_randomPoints)
n_lines = ares_indcs.shape[0]
recombLinesIdx = linesDf.index.str.contains('He1') + linesDf.index.str.contains('He2') + linesDf.index.str.contains('H1')
removeContinuumCheck = True

p1_matrix = np.empty((n_randomPoints, 3))
sqrt2pi = np.sqrt(2*np.pi)

# fig, ax = plt.subplots(1, 1, figsize=(10, 6))
for i in np.arange(n_lines):

    # Get line_i wave and continua
    lineWave, lineFlux = wave[idcsLines[:,i]], fluxNorm[idcsLines[:,i]]
    continuaWave, continuaFlux = wave[idcsContinua[:,i]], fluxNorm[idcsContinua[:,i]]

    # Compute linear line continuum and get the standard deviation on the continuum
    slope, intercept, r_value, p_value, std_err = stats.linregress(continuaWave, continuaFlux)
    continuaFit     = continuaWave * slope + intercept
    std_continuum   = np.std(continuaFlux - continuaFit)
    lineContinuumFit = lineWave * slope + intercept
    continuumInt    = lineContinuumFit.sum()
    centerWave      = lineWave[np.argmax(lineFlux)]
    centerContInt   = centerWave * slope + intercept

    # Compute matrix with random noise from the continua standard deviation
    normalNoise = normal(0.0, std_continuum, (n_randomPoints, lineWave.size))
    line_iFluxMatrix = lineFlux + normalNoise

    # Compute integrated flux
    areasArray = line_iFluxMatrix.sum(axis=1)
    integInt, integStd = areasArray.mean(), areasArray.std()

    # # Initial values for fit
    # p0 = (lineFlux.max(),lineWave.mean(),1.0)
    #
    # # Perform fit in loop
    # for j in rangeFittings: #This one is not powerfull enought... add more points
    #     p1_matrix[j], pcov = curve_fit(gaussFunc, (lineWave, lineContinuumFit), lineFlux + normalNoise[j], p0=p0)
    #
    # # Compute mean values and std from gaussian fit
    # gIntArray = p1_matrix[:, 0] * p1_matrix[:, 2] * sqrt2pi
    # p1Mean, gInt = p1_matrix.mean(axis=0), gIntArray.mean()
    # p1Std, gIntStd = p1_matrix.std(axis=0), gIntArray.std()

    # # Remove continuum from metallic lines
    # if removeContinuumCheck and not recombLinesIdx[i]:
    #     integInt = integInt - continuumInt
    #     gInt = gInt - continuumInt
    #
    # resampleGaus = np.linspace(lineWave[0]-10, lineWave[-1]+10, 100)
    # resampleContinuum = resampleGaus * slope + intercept
    # gaussianFlux = gaussFunc((resampleGaus, resampleContinuum), *p1Mean)
    # gaussianFlux2 = gaussFunc((resampleGaus, np.zeros(resampleGaus.size)), *p1Mean)
    #
    # ax.plot(lineWave, lineFlux, color='tab:red', label='lines')
    # ax.plot(continuaWave, continuaFlux, color='tab:blue', label='continuum')
    # ax.plot(continuaWave, continuaFit, color='tab:green', label='fit continuum')
    # ax.plot(resampleGaus, gaussianFlux, color='tab:purple', label='gaussian fit')
    # ax.plot(resampleGaus, gaussianFlux2, color='tab:cyan', label='gaussian fit2')
    #
    # ax.update({'xlabel': r'Wavelength $(\AA)$', 'ylabel': 'Flux (normalised)'})
    # ax.legend()
    # plt.show()

    #print lineLabels[i], lineFlux.sum(), (fluxNorm * lines_mask[i]).sum(), integInt, gInt + continuumInt # TODO gInt is not giving the same as the ohers
