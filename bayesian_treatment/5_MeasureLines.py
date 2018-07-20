import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.inferenceModel import SpectraSynthesizer
from lib.Astro_Libraries.spectrum_fitting.import_functions import ImportModelData

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
    for i in range(n_lineMasks):
        idx_currentMask = (wavelength > wmin[i]) & (wavelength < wmax[i])
        boolean_matrix[i, :] = idx_currentMask
        int_mask = int_mask & ~idx_currentMask

    # Loop through the object masks
    wmin, wmax = linesDf['w3'].loc[idcs_spectrumMasks].values, linesDf['w4'].loc[idcs_spectrumMasks].values
    for i in range(n_objMasks):
        idx_currentMask = (wavelength > wmin[i]) & (wavelength < wmax[i])
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
lineLabels = objLinesLogDf.loc[:'H1_10049A','w1':'w6'].index.values
lines_mask = generate_object_mask(objLinesLogDf, wave, lineLabels)
normFluxCoeff = np.median(flux)
fluxNorm = flux/normFluxCoeff
linesDb = pd.read_excel('/home/vital/PycharmProjects/dazer/bin/lib/Astro_Libraries/spectrum_fitting/lines_data.xlsx', sheetname=0, header=0, index_col=0)

areas_matrix = objLinesLogDf.loc[:'H1_10049A','w1':'w6'].values # In here replace : by the lines actually observed
ares_indcs = np.searchsorted(wave, areas_matrix)

blueRegionFluxes = fluxNorm[ares_indcs[0,0]:ares_indcs[0,1]].mean() #Use the approach of idcsContinua to generate the whole arrays of true and false
lineRegionFluxes = fluxNorm[ares_indcs[0,2]:ares_indcs[0,3]].sum()
redRegionFluxes = fluxNorm[ares_indcs[0,4]:ares_indcs[0,5]].mean()

blueRegionWaves = (wave[ares_indcs[0,0]] + wave[ares_indcs[0,1]]) / 2
lineRegionWaves = (wave[ares_indcs[0,2]] + wave[ares_indcs[0,3]]) / 2
redRegionWaves = (wave[ares_indcs[0,4]] + wave[ares_indcs[0,5]]) / 2

lineContPointFluxes = blueRegionFluxes + ((redRegionFluxes-blueRegionFluxes)/(redRegionWaves-blueRegionWaves)) * (lineRegionWaves - blueRegionWaves)
lineContFluxes = lineContPointFluxes * (wave[ares_indcs[0,3]] - wave[ares_indcs[0,2]])

idcsContinua = ((wave[ares_indcs[:,0]] <= wave[:,None]) & (wave[:,None] <= wave[ares_indcs[:,1]])) | ((wave[ares_indcs[:,4]] <= wave[:,None]) & (wave[:,None] <= wave[ares_indcs[:,5]]))
# waveContinua = wave[idcsContinua[:,0]]
# fluxContinua = fluxNorm[idcsContinua,None]

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.plot(wave[wave<4386], fluxNorm[wave<4386], label='spectrum')
ax.plot(wave[idcsContinua[:,0]], fluxNorm[idcsContinua[:,0]], label='spectrum')
ax.update({'xlabel': 'Wavelength (nm)', 'ylabel': 'Flux (normalised)'})
ax.legend()
plt.show()

# blueRegionFluxes  fluxNorm[ares_indcs[:,0]:ares_indcs[:,1]].mean(axis=1)
# lineRegionFluxes = fluxNorm[ares_indcs[:,0]:ares_indcs[:,1]].sum(axis=1)
# redRegionFluxes = fluxNorm[ares_indcs[:,0]:ares_indcs[:,1]].mean(axis=1)
#
# blueRegionWaves = (wave[ares_indcs[:,0]] + wave[ares_indcs[:,1]]) / 2
# lineRegionWaves = (wave[ares_indcs[:,2]] + wave[ares_indcs[:,3]]) / 2
# redRegionWaves = (wave[ares_indcs[:,4]] + wave[ares_indcs[:,5]]) / 2
#
# lineContPointFluxes = redRegionFluxes + (redRegionFluxes-blueRegionFluxes)/(redRegionWaves-blueRegionWaves) * (lineRegionWaves - blueRegionWaves)
# lineContFluxes = lineContPointFluxes * (wave[ares_indcs[:,3]] - wave[ares_indcs[:,2]])

# idcsContinua = ((wave[ares_indcs[:,0]] <= wave[:,None]) & (wave[:,None] <= wave[ares_indcs[:,1]])) | ((wave[ares_indcs[:,4]] <= wave[:,None]) & (wave[:,None] <= wave[ares_indcs[:,5]]))


# lineFluxes = np.empty(lineLabels.size)
# linesWithAbsorption = objLinesLogDf.index.str.contains('H1_') | objLinesLogDf.index.str.contains('He1_') | objLinesLogDf.index.str.contains('He2_')
# np.random.normal()
# #Loop measure fluxes
# for i in np.arange(lineLabels.size):
#
#     lineLabel = lineLabels[i]
#
#     if lineLabel not in ['H1_6563A_w', 'Upper_Edge', 'WHT_Spectra_Joining']:
#
#         fluxB =
#         fluxR =





# fig, ax = plt.subplots(1, 1, figsize=(10, 6))
# ax.plot(wave, flux,label='spectrum')
# for i in range(lines_mask.shape[0]):
#     ax.plot(wave[lines_mask[i,:]], flux[lines_mask[i,:]],label=lineLabels[i])
#     ax.scatter(wavesB[i], normFluxCoeff,label='Blue region',color='blue')
#     ax.scatter(WavesL[i], normFluxCoeff,label='line region',color='green')
#     ax.scatter(WavesR[i], normFluxCoeff,label='Red region',color='red')
#
# ax.update({'xlabel': 'Wavelength (nm)', 'ylabel': 'Flux (normalised)'})
# ax.legend()
# plt.show()

# import numpy as np
#
# myArray = np.arange(10)
#
# lowLimit = 2
# highLimit = 5
#
# print myArray[lowLimit:highLimit]
#
# lowLimit = np.ones(10) * 2
# highLimit = np.ones(10) * 5
#
# print myArray[lowLimit:highLimit:None]
#
# print


