import numpy as np
import pandas as pd
import ConfigParser
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.inferenceModel import SpectraSynthesizer
from lib.Astro_Libraries.spectrum_fitting.import_functions import parseObjData

# Declare synthesizer object
specS = SpectraSynthesizer()

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

# Import stellar library data
starlight_ssp = {'ssp_lib_type'         :'starlight',  # TODO In here we will add "test" for the pip
                'data_folder'           :'/home/vital/Starlight/Bases/',
                'data_file'             :'/home/vital/Starlight/Bases/Dani_Bases_Extra.txt',
                'wavelengh_limits'      :[3600, 6900],
                'resample_inc'          :1,
                'norm_interval'         :[5100, 5150]}

# Simulation Data
fit_conf = {'obs_data'                  :None,
            'ssp_data'                  :None,
            'output_folder'             :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
            'spectra_components'        :['emission', 'nebular', 'stellar'],
            'input_lines'               :np.array(['H1_4341A', 'O3_4363A', 'Ar4_4740A', 'H1_4861A', 'O3_4959A', 'O3_5007A', 'S3_6312A', 'H1_6563A', 'S2_6716A', 'S2_6731A', 'S3_9069A', 'S3_9531A' ]),
            'prefit_ssp'                :True,
            'prefit_data'               :None,
            'wavelengh_limits'          :[0,6900],
            'resample_inc'              :1,
            'norm_interval'             :[5100,5150]}

ssp_starlight = specS.load_ssp_library(**starlight_ssp)

#Loop throught the objects
failing_objects = []
for objName in catalogue_df.loc[dz.idx_include].index:

    # try:
    #     if objName == 'SDSS3':
            objectFolder = '{}{}/'.format(root_folder, objName)
            dataLocation = '{}{}/{}_objParams.txt'.format(root_folder, objName, objName)
            obsData = specS.load_obsData(dataLocation, objName)
            obsData['wavelengh_limits'][0] = 0 # TODO this value is inherited from previous object. It must be recheck
            fit_conf['wavelengh_limits'][0] = 0

            # Set object wmin
            if obsData['obs_wavelength'][0] < 4270 and 'SHOC' not in objName:
                if obsData['obs_wavelength'][0] < 3600:
                    fit_conf['wavelengh_limits'][0] = 3600
                    obsData['wavelengh_limits'][0] = 3600
                else:
                    fit_conf['wavelengh_limits'][0] = 0
                    obsData['wavelengh_limits'][0] = 0

                print '\nTreating {}'.format(objName)

                # Assign nebular continuum parameters
                specS.nebDefault['Te_neb']      = obsData['Te_prior'][0]
                specS.nebDefault['cHbeta_neb']  = obsData['cHbeta_prior']
                specS.nebDefault['flux_halpha'] = obsData['flux_halpha']

                # Declaring configuration format
                fit_conf['obs_data'] = obsData
                fit_conf['ssp_data'] = ssp_starlight
                fit_conf['prefit_data'] = dataFolder
                fit_conf['output_folder'] = objectFolder
                fit_conf['spectra_components'] = ['stellar', 'nebular', 'emission']

                # Prepare fit data
                specS.prepareSimulation(**fit_conf)

#     except:
#         failing_objects.append(objName)
#
# if len(failing_objects) > 0:
#     print 'These objects failed their analysis'
#     for j in range(len(failing_objects)):
#         print failing_objects[j]