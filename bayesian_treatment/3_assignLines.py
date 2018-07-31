import numpy as np
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

defaultLines = np.array(['H1_4341A','O3_4363A','Ar4_4740A','O3_4959A','O3_5007A','S3_6312A','N2_6548A','H1_6563A','N2_6584A','S2_6716A','S2_6731A','Ar3_7136A','O2_7319A','O2_7330A','S3_9069A','S3_9531A'])
specialObjects = {'8': np.array(['H1_4341A','O3_4363A','Ar4_4740A','He1_4471A', 'He2_4686A', 'O3_4959A','O3_5007A','He1_5876A', 'S3_6312A','N2_6548A','H1_6563A','N2_6584A','S2_6716A','S2_6731A', 'He1_6678A','Ar3_7136A','O2_7319A','O2_7330A','S3_9069A','S3_9531A'])}

#Loop throught the objects
for objName in catalogue_df.loc[dz.idx_include].index:

    print('Treating {}'.format(objName))
    objectFolder = '{}{}/'.format(root_folder, objName)
    dataLocation = '{}{}/{}_objParams.txt'.format(root_folder, objName, objName)

    if objName in specialObjects:
        lines = specialObjects[objName]
    else:
        lines = defaultLines

    parseObjData(dataLocation, objName, {'input_lines':lines})

