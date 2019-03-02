from dazer_methods import Dazer
from lib.inferenceModel import SpectraSynthesizer
from lib.Astro_Libraries.spectrum_fitting.import_functions import make_folder

# Import functions
dz = Dazer()

# Declare data location
# root_folder = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\bayesianModel\\'
# whtSpreadSheet = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\WHT_Galaxies_properties.xlsx'
root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'
whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'


# Import data
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtSpreadSheet)
dz.quick_indexing(catalogue_df)

default_lines = ['H1_4341A', 'H1_6563A', 'He1_4471A', 'He1_5876A', 'He1_6678A',
       'He2_4686A', 'O2_7319A', 'O2_7330A', 'O3_4363A', 'O3_4959A',
       'O3_5007A', 'N2_6548A', 'N2_6584A', 'S2_6716A', 'S2_6731A',
       'S3_6312A', 'S3_9069A', 'S3_9531A', 'Ar3_7136A', 'Ar4_4740A']

# Loop through the objects
for objName in catalogue_df.index:

    print('Treating object: {}'.format(objName))

    if objName == '8':

            # Generate spectra synthesizer object
            specS = SpectraSynthesizer()

            # Declare object folder
            objectFolder = '{}{}/'.format(root_folder, objName)#'{}{}\\'.format(root_folder, objName)

            # Declare configuration file
            dataFileAddress = '{}{}_objParams.txt'.format(objectFolder, objName)
            obsData = specS.load_obsData(dataFileAddress, objName)

            # Declaring configuration design
            simuName = '{}_emissionHMC'.format(objName)
            reddening_check, Thigh_check = True, True
            fit_conf = dict(obs_data=obsData,
                            ssp_data=None,
                            output_folder=objectFolder,
                            spectra_components=['emission'],
                            input_lines=obsData['input_lines'],
                            prefit_ssp=False,
                            normalized_by_Hbeta=False)

            # Prepare fit data
            specS.prepareSimulation(**fit_conf)

            # Run the simulation
            specS.fitSpectra(model_name= objName + '_HMC_fit_v1', iterations=6000, tuning=3000, include_reddening=reddening_check, include_Thigh_prior=Thigh_check)
