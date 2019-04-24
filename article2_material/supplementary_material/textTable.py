import numpy as np
from collections import OrderedDict
from dazer_methods import Dazer
from lib.inferenceModel import SpectraSynthesizer
from lib.Astro_Libraries.spectrum_fitting.import_functions import make_folder

# Import functions
dz = Dazer()
specS = SpectraSynthesizer()

# Declare data location
root_folder = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\bayesianModel\\'
whtSpreadSheet = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\WHT_Galaxies_properties.xlsx'

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
excludeObjects = ['SHOC579', 'SHOC575_n2', '11', 'SHOC588', 'SDSS3', 'SDSS1', 'SHOC36']
sampleObjects = catalogue_df.loc[dz.idx_include & ~catalogue_df.index.isin(excludeObjects)].index.values

# Generate spectra synthesizer object
specS = SpectraSynthesizer()

# Loop through the objects
for i in range(sampleObjects.size):

    # Object references
    objName = sampleObjects[i]
    local_refenrence = objName.replace('_', '-')
    quick_reference = catalogue_df.loc[objName].quick_index

    print '- Treating object {}: {} {}'.format(i, objName, quick_reference)

    if objName == '4_n1':

        # Declare object folder
        objectFolder = '{}{}/'.format(root_folder, objName)#'{}{}\\'.format(root_folder, objName)

        # Declare configuration file
        dataFileAddress = '{}{}_objParams.txt'.format(objectFolder, objName)
        obsData = specS.load_obsData(dataFileAddress, objName)

        # Run the sampler
        # TODO need to decide where to place this
        model_name=objName + '_HMC_fit_v2',
        db_address = objectFolder + model_name + '.db'

        # Load the results
        interenceParamsDict = specS.load_pymc_database_manual(db_address, sampler='pymc3')

        # Compute elemental abundances from the traces
        obsAtoms = self.obsAtoms
        specS.elementalChemicalModel(interenceParamsDict, obsAtoms, (6000 + 3000) * 2)

        # Save parameters into the object log #TODO make a new mechanism to delete the results region
        store_params = OrderedDict()
        for parameter in interenceParamsDict.keys():
            if ('_log__' not in parameter) and ('interval' not in parameter) and ('_op' not in parameter):
                trace = interenceParamsDict[parameter]
                store_params[parameter] = np.array([trace.mean(), trace.std()])

        # Plot output data
        specS.plotOuputData(objectFolder + model_name, interenceParamsDict, specS.modelParams)
