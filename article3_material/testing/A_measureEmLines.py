import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, optimize
from dazer_methods import Dazer
from scipy.integrate import simps
from lib.Astro_Libraries.spectrum_fitting.import_functions import ImportModelData
from article3_material.line_measuring import LineMesurer
from article3_material.line_measuring import line_regions_matrix

# Let's create a function to model and create data
def gaussFunc(ind_params, a, mu, sigma):
    x, z = ind_params
    return a * np.exp(-((x - mu) * (x - mu)) / (2 * (sigma * sigma))) + z


def generate_object_mask(lines_DF, wavelength, line_labels):

    # TODO This will not work for a redshifted lines log
    idcs_lineMasks = linesDf.index.isin(line_labels)
    idcs_spectrumMasks = ~linesDf.index.isin(line_labels)

    # Matrix mask for integring the emission lines
    n_lineMasks = idcs_lineMasks.sum()
    boolean_matrix = np.zeros((n_lineMasks, wavelength.size), dtype=bool)

    # Total mask for valid regions in the spectrum
    n_objMasks = idcs_spectrumMasks.sum()
    int_mask = np.ones(wavelength.size, dtype=bool)
    object_mask = np.ones(wavelength.size, dtype=bool)

    # Loop through the emission lines
    wmin, wmax = lines_DF['w3'].loc[idcs_lineMasks].values, lines_DF['w4'].loc[idcs_lineMasks].values
    idxMin, idxMax = np.searchsorted(wavelength, [wmin, wmax])
    for i in range(n_lineMasks):
        idx_currentMask = (wavelength >= wavelength[idxMin[i]]) & (wavelength <= wavelength[idxMax[i]])
        boolean_matrix[i, :] = idx_currentMask
        int_mask = int_mask & ~idx_currentMask

    # Loop through the object masks
    wmin, wmax = lines_DF['w3'].loc[idcs_spectrumMasks].values, lines_DF['w4'].loc[idcs_spectrumMasks].values
    idxMin, idxMax = np.searchsorted(wavelength, [wmin, wmax])
    for i in range(n_objMasks):
        idx_currentMask = (wavelength >= wavelength[idxMin[i]]) & (wavelength <= wavelength[idxMax[i]])
        int_mask = int_mask & ~idx_currentMask
        object_mask = object_mask & ~idx_currentMask

    return boolean_matrix


# Declare synthesizer object
lm = LineMesurer()
specS = ImportModelData('C:\\Users\\Vital\\PycharmProjects\\dazer\\bin\\lib')

# Import library object
dz = Dazer()

# Object database
whtSpreadSheet = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\WHT_Galaxies_properties.xlsx'
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtSpreadSheet)
dz.quick_indexing(catalogue_df)

# Declare data location
objName = '8'
root_folder = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\bayesianModel\\'
objectFolder = '{}{}\\'.format(root_folder, objName)
dataLocation = '{}{}\\{}_objParams.txt'.format(root_folder, objName, objName)

# Load the spectrum
obsData = specS.load_obsData(dataLocation, objName)
wave, flux = obsData['obs_wavelength'], obsData['obs_flux']

# Normalizing the spectrum # TODO in here we use the norm flux from the continuum
normFluxCoeff = np.median(flux)
fluxNorm = flux / normFluxCoeff

# Load lines data # TODO in here we use the lines proposed by the user
objLinesLogDf = pd.read_csv(obsData['obj_lines_file'], delim_whitespace=True, header=0, index_col=0)
idcs_validLines = ~objLinesLogDf.index.isin(['O2_7319A_b', 'H1_6563A_w'])
linesDf = objLinesLogDf.loc[idcs_validLines]
linesDf = linesDf.loc[:'H1_9546A']
lineLabels = linesDf.index.values
areaWaveN_matrix = linesDf.loc[:, 'w1':'w6'].values  # TODO in here we use the lines proposed by the user

# Get line and adjacent continua region
ares_indcs = np.searchsorted(wave, areaWaveN_matrix)
idcsLines = (wave[ares_indcs[:, 2]] <= wave[:, None]) & (wave[:, None] <= wave[ares_indcs[:, 3]])
idcsContinua = ((wave[ares_indcs[:, 0]] <= wave[:, None]) & (wave[:, None] <= wave[ares_indcs[:, 1]])) | (
            (wave[ares_indcs[:, 4]] <= wave[:, None]) & (wave[:, None] <= wave[ares_indcs[:, 5]]))


# Lines mask
lines_mask = generate_object_mask(linesDf, wave, lineLabels)

n_randomPoints = 1000
rangeFittings = np.arange(n_randomPoints)
n_lines = ares_indcs.shape[0]
recombLinesIdx = linesDf.index.str.contains('He1') + linesDf.index.str.contains('He2') + linesDf.index.str.contains('H1')
removeContinuumCheck = True

p1_matrix = np.empty((n_randomPoints, 3))
sqrt2pi = np.sqrt(2 * np.pi)

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
for i in np.arange(n_lines):

    # Get line_i wave and continua
    lineWave, lineFlux = wave[idcsLines[:, i]], fluxNorm[idcsLines[:, i]]
    continuaWave, continuaFlux = wave[idcsContinua[:, i]], fluxNorm[idcsContinua[:, i]]

    #lineFit = lm.lineFit(wave, fluxNorm, idcsLines[:, i], plot_data=True)

    # Compute linear line continuum and get the standard deviation on the continuum
    slope, intercept, r_value, p_value, std_err = stats.linregress(continuaWave, continuaFlux)
    continuaFit = continuaWave * slope + intercept
    std_continuum = np.std(continuaFlux - continuaFit)
    lineContinuumFit = lineWave * slope + intercept
    continuumInt = lineContinuumFit.sum()
    centerWave = lineWave[np.argmax(lineFlux)]
    centerContInt = centerWave * slope + intercept
    lineWidth = (lineWave[-1] - lineWave[0]) / lineWave.size
    lineWidth2 = (lineWave[-1] - lineWave[0]) / (lineWave.size - 1)

    # Compute matrix with random noise from the continua standard deviation
    normalNoise = np.random.normal(0.0, std_continuum, (n_randomPoints, lineWave.size))
    line_iFluxMatrix = lineFlux + normalNoise

    # Compute integrated flux
    areasArray = line_iFluxMatrix.sum(axis=1) - continuumInt
    integInt, integStd = areasArray.mean(), areasArray.std()

    # Initial values for fit
    p0 = (lineFlux.max(), lineWave.mean(), 1.0)

    print lineWave
    print lineFlux
    print continuaWave
    print continuaFlux
    print lineContinuumFit
    print line_iFluxMatrix[0]
    print
    print

    # Perform fit in loop
    for j in rangeFittings: # This one is not powerfull enought... add more points
        p1_matrix[j], pcov = optimize.curve_fit(gaussFunc, (lineWave, lineContinuumFit), line_iFluxMatrix[j], p0=p0)

    # Compute mean values and std from gaussian fit
    A, mu, sigma = p1_matrix[:, 0].mean(), p1_matrix[:, 1].mean(), p1_matrix[:, 2].mean()
    gIntArray = p1_matrix[:, 0] * p1_matrix[:, 2] * sqrt2pi
    p1Mean, gInt = p1_matrix.mean(axis=0), gIntArray.mean()
    p1Std, gIntStd = p1_matrix.std(axis=0), gIntArray.std()

    resampleGaus = np.linspace(lineWave[0]-10, lineWave[-1]+10, 100)
    resampleContinuum = resampleGaus * slope + intercept
    gaussianCurve = gaussFunc((resampleGaus, resampleContinuum), *p1Mean)
    gaussianFlux2 = gaussFunc((resampleGaus, np.zeros(resampleGaus.size)), *p1Mean)
    AreaCurve = simps(lineFlux, lineWave) - simps(lineContinuumFit, lineWave)

    lineFit = lm.lineFit(wave, fluxNorm, idcsLines[:, i], idcsContinua[:, i], plot_data=True)

    print lineLabels[i], lineFlux.sum() - continuumInt, (fluxNorm * lines_mask[i]).sum() - continuumInt, integInt, gInt, AreaCurve

    ax.plot(lineWave, lineFlux, color='black', label='lines')
    ax.plot(continuaWave, continuaFlux, '-', color='tab:blue', label='continuum')
    ax.plot(continuaWave, continuaFit, ':', color='tab:green', label='fit continuum')
    ax.plot(lineWave, lineContinuumFit, ':', color='tab:green', label='fit continuum raro')
    ax.plot(resampleGaus, gaussianCurve, ':', color='tab:purple', label='Fit Gaussian')
    ax.plot(lineFit['resampleRegion'], lineFit['resampleCurve'], ':', color='tab:red', label='New fit Gaussian')

    # ax.plot(resampleGaus, gaussianFlux2, color='tab:cyan', label='gaussian fit2')

    ax.update({'xlabel': r'Wavelength $(\AA)$', 'ylabel': 'Flux (normalised)'})
    ax.legend()
    plt.show()

     # TODO gInt is not giving the same as the ohers
# for i in np.arange(n_lines):
#
#     # Get line_i wave and continua
#     lineWave, lineFlux = wave[idcsLines[:, i]], fluxNorm[idcsLines[:, i]]
#     continuaWave, continuaFlux = wave[idcsContinua[:, i]], fluxNorm[idcsContinua[:, i]]
#
#     # Compute linear line continuum and get the standard deviation on the continuum
#     slope, intercept, r_value, p_value, std_err = stats.linregress(continuaWave, continuaFlux)
#     continuaFit = continuaWave * slope + intercept
#     std_continuum = np.std(continuaFlux - continuaFit)
#     lineContinuumFit = lineWave * slope + intercept
#     continuumInt = lineContinuumFit.sum()
#     centerWave = lineWave[np.argmax(lineFlux)]
#     centerContInt = centerWave * slope + intercept
#     lineWidth = (lineWave[-1] - lineWave[0]) / lineWave.size
#     lineWidth2 = (lineWave[-1] - lineWave[0]) / (lineWave.size - 1)
#
#     # Compute matrix with random noise from the continua standard deviation
#     normalNoise = np.random.normal(0.0, std_continuum, (n_randomPoints, lineWave.size))
#     line_iFluxMatrix = lineFlux + normalNoise
#
#     # Compute integrated flux
#     areasArray = line_iFluxMatrix.sum(axis=1) - continuumInt
#     integInt, integStd = areasArray.mean(), areasArray.std()
#
#     # Initial values for fit
#     p0 = (lineFlux.max(), lineWave.mean(), 1.0)
#
#     # Perform fit in loop
#     for j in rangeFittings: # This one is not powerfull enought... add more points
#         p1_matrix[j], pcov = optimize.curve_fit(gaussFunc, (lineWave, lineContinuumFit), line_iFluxMatrix[j], p0=p0)
#
#     # Compute mean values and std from gaussian fit
#     A, mu, sigma = p1_matrix[:, 0].mean(), p1_matrix[:, 1].mean(), p1_matrix[:, 2].mean()
#     gIntArray = p1_matrix[:, 0] * p1_matrix[:, 2] * sqrt2pi
#     p1Mean, gInt = p1_matrix.mean(axis=0), gIntArray.mean()
#     p1Std, gIntStd = p1_matrix.std(axis=0), gIntArray.std()
#
#     resampleGaus = np.linspace(lineWave[0]-10, lineWave[-1]+10, 100)
#     resampleContinuum = resampleGaus * slope + intercept
#     gaussianCurve = gaussFunc((resampleGaus, resampleContinuum), *p1Mean)
#     gaussianFlux2 = gaussFunc((resampleGaus, np.zeros(resampleGaus.size)), *p1Mean)
#     AreaCurve = simps(lineFlux, lineWave) - simps(lineContinuumFit, lineWave)
#
#     print lineLabels[i], lineFlux.sum() - continuumInt, (fluxNorm * lines_mask[i]).sum() - continuumInt, integInt, gInt, AreaCurve
#
#     ax.plot(lineWave, lineFlux, color='black', label='lines')
#     ax.plot(continuaWave, continuaFlux, '-', color='tab:blue', label='continuum')
#     ax.plot(continuaWave, continuaFit, ':', color='tab:green', label='fit continuum')
#     ax.plot(lineWave, lineContinuumFit, ':', color='tab:green', label='fit continuum raro')
#     ax.plot(resampleGaus, gaussianCurve, ':', color='tab:purple', label='Fit Gaussian')
#     ax.plot(resampleGaus, gaussianFlux2, color='tab:cyan', label='gaussian fit2')
#
#     ax.update({'xlabel': r'Wavelength $(\AA)$', 'ylabel': 'Flux (normalised)'})
#     ax.legend()
#     plt.show()