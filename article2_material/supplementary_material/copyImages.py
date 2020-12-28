from dazer_methods import Dazer
from lib.inferenceModel import SpectraSynthesizer
from lib.Astro_Libraries.spectrum_fitting.import_functions import make_folder
import shutil

# Import functions
dz = Dazer()
specS = SpectraSynthesizer()

# Declare data location
root_folder = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\bayesianModel\\' # root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'
whtSpreadSheet = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\WHT_Galaxies_properties.xlsx' # whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'
article_supplementary_folder = 'E:\\Dropbox\\Astrophysics\\Papers\\Yp_BayesianMethodology\\supplementary material online\\'
fluxes_folder = article_supplementary_folder + 'emission_line_fluxes\\'
results_folder = article_supplementary_folder + 'model_parameters\\'

# Make new folder
make_folder(fluxes_folder)
make_folder(results_folder)

# Import data
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtSpreadSheet)

default_lines = ['H1_4341A', 'H1_6563A', 'He1_4471A', 'He1_5876A', 'He1_6678A',
       'He2_4686A', 'O2_7319A', 'O2_7319A_b', 'O2_7330A', 'O3_4363A', 'O3_4959A',
       'O3_5007A', 'N2_6548A', 'N2_6584A', 'S2_6716A', 'S2_6731A',
       'S3_6312A', 'S3_9069A', 'S3_9531A', 'Ar3_7136A', 'Ar4_4740A']

# Quick indexing
dz.quick_indexing(catalogue_df)

# Sample objects
excludeObjects = ['SHOC579', 'SHOC575_n2', '11', 'SHOC588', 'SDSS3', 'SDSS1', 'SHOC36']  # SHOC579, SHOC575, SHOC220, SHOC588, SHOC592, SHOC036
sampleObjects = catalogue_df.loc[dz.idx_include & ~catalogue_df.index.isin(excludeObjects)].index.values

# File conversions
conversionFileReferences = {'_meanOutput.pdf':              '_fitting_results.pdf',
                            '_ParamsTracesPosterios.png':   '_fitting_posteriors.png',
                            '_LineFluxes.pdf':              '_simulation_emission_fluxes.pdf',
                            '_LineFluxesPosteriors.png':    '_emission_flux_distributions.png',
                            '_CornerPlot.png':              '_corner_plot.png'}

fileFolders = {'_meanOutput.pdf':              results_folder,
               '_ParamsTracesPosterios.png':   results_folder,
               '_LineFluxes.pdf':              fluxes_folder,
               '_LineFluxesPosteriors.png':    fluxes_folder,
               '_CornerPlot.png':              results_folder}

# Loop through the objects
for i in range(sampleObjects.size):

    # Object references
    objName = sampleObjects[i]
    local_refenrence = objName.replace('_', '-')
    quick_reference = catalogue_df.loc[objName].quick_index

    # Declare object folder
    objectFolder = '{}{}\\'.format(root_folder, objName)

    # Declare configuration file
    dataFileAddress = '{}{}_objParams.txt'.format(objectFolder, objName)
    #obsData = specS.load_obsData(dataFileAddress, objName)

    # Folder where the fitting results are stored
    inputFileReference = objectFolder + 'output_data\\' + objName + '_HMC_fit_v2'

    for itemExtension in conversionFileReferences:
        originalFile = '{}{}'.format(inputFileReference, itemExtension)
        targetFile = '{}{}{}'.format(fileFolders[itemExtension], quick_reference, conversionFileReferences[itemExtension])
        shutil.copyfile(originalFile, targetFile)







    # print '- Treating object {}: {} {}'.format(i, objName, quick_reference)
    #
    #     # Generate spectra synthesizer object
    #     specS = SpectraSynthesizer()
    #
    #     # Declare object folder
    #     objectFolder = '{}{}/'.format(root_folder, objName)#'{}{}\\'.format(root_folder, objName)
    #
    #     # Declare configuration file
    #     dataFileAddress = '{}{}_objParams.txt'.format(objectFolder, objName)
    #     obsData = specS.load_obsData(dataFileAddress, objName)
    #
    #     # Declaring configuration design
    #     simuName = '{}_emissionHMC'.format(objName)
    #     fit_conf = dict(obs_data=obsData,
    #                     ssp_data=None,
    #                     output_folder=objectFolder,
    #                     spectra_components=['emission'],
    #                     input_lines=obsData['input_lines'],
    #                     prefit_ssp=False,
    #                     normalized_by_Hbeta=False)
    #
    #     # Prepare fit data
    #     specS.prepareSimulation(**fit_conf)
    #
    #     # Run the simulation
    #     specS.fitSpectra(model_name=objName + '_HMC_fit_v2', iterations=6000, tuning=3000,
    #                      include_reddening=obsData['redening_check'], include_Thigh_prior=obsData['Thigh_check'])
    #
    #     print '- Finished object {}: {} {}'.format(i, objName, quick_reference)
