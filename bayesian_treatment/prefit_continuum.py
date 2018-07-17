import numpy as np
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.inferenceModel import SpectraSynthesizer

# Declare synthesizer object
specS = SpectraSynthesizer()

#Import library object
dz = Dazer()

# Object database
whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtSpreadSheet)
dz.quick_indexing(catalogue_df)

# Data root folder
root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'

# Import stellar library data
starlight_ssp = {'ssp_lib_type'         :'starlight',  # TODO In here we will add "test" for the pip
                'data_folder'           :'/home/vital/Starlight/Bases/',
                'data_file'             :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
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
            'wavelengh_limits'          :[4350,6900], #TODO remake this to the actual limit
            'resample_inc'              :1,
            'norm_interval'             :[5100,5150]}
# test_lines = np.array(['H1_4341A', 'O3_4363A', 'Ar4_4740A', 'H1_4861A', 'O3_4959A', 'O3_5007A', 'S3_6312A', 'H1_6563A', 'S2_6716A', 'S2_6731A', 'S3_9069A', 'S3_9531A' ]

ssp_starlight = specS.load_ssp_library(**starlight_ssp)

#Loop throught the objects
for objName in catalogue_df.loc[dz.idx_include].index:

    if objName == '8':

        print('Treating {}'.format(objName))
        dataFolder = '{}{}/'.format(root_folder, objName)
        dataLocation = '{}{}/{}_objParams.txt'.format(root_folder, objName, objName)
        obsData = specS.load_obsData(dataLocation, objName)

        # Declaring configuration format
        fit_conf['obs_data'] = obsData
        fit_conf['ssp_data'] = ssp_starlight
        fit_conf['output_folder'] = dataFolder
        fit_conf['spectra_components'] = ['stellar']

        # Prepare fit data
        specS.prepareSimulation(**fit_conf)

# test_lines = np.array(['H1_3835A', 'O2_3726A', 'O2_3729A', 'H1_3889A', 'He1_3889A', 'H1_3970A', 'He1_4026A', 'H1_4102A', 'H1_4341A', 'O3_4363A', 'He1_4471A', 'Ar4_4740A', 'He2_4686A', 'H1_4861A', 'O3_4959A', 'O3_5007A', 'N2_5755A', 'He1_5876A', 'S3_6312A', 'N2_6548A', 'H1_6563A', 'N2_6584A', 'He1_6678A', 'S2_6716A', 'S2_6731A', 'He1_7065A']
