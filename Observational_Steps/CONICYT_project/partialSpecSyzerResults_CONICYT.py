import numpy as np
from dazer_methods import Dazer
from lib.inferenceModel import SpectraSynthesizer

# Import library object
dz = Dazer()
specS = SpectraSynthesizer()

# Data root folder
specS.normContants = {'He1r': 0.1, 'He2r': 0.001}
root_folder = '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/'

# HII galaxy
model_name = 'testSimu'
outputFolder = root_folder + 'testing_output/'
specS.objName = 'ObsHIIgalaxySynth_objParams'
specS.configFile = '{}/{}_objParams.txt'.format(outputFolder, specS.objName)

# # Load the results
db_address = outputFolder + model_name + '.db'  #
inferenceTrace, db_dict = specS.load_pymc_database_manual(db_address, sampler='pymc3')
params_list = np.array(db_dict.keys())
params_list = np.array(['T_low', 'n_e' , 'He1r', 'He2r', 'S2', 'S3', 'O2', 'O3', 'Ar3', 'N2', 'tau'])

# Corner plot
print '--Scatter plot matrix'
trueValues = {'T_low':12500.0, 'n_e':125.0 , 'He1r':0.869, 'He2r':0.00088, 'S2':5.48, 'S3':6.36, 'O2':7.80, 'O3':8.05, 'Ar3':5.72, 'N2':5.84, 'tau': 0.875}

specS.corner_plot(params_list, db_dict, true_values=[12500.0, 125.0, 0.0869, 0.00088, 5.48, 6.36, 7.80, 8.05, 5.72, 5.84, 0.875])
folderResults = '/home/vital/Dropbox/Astrophysics/Burocracia/Propuestas_trabajo/Chile_CONICT/Images/'
specS.savefig(folderResults + 'Synth_Partial_CornerPlot', resolution=100)

# # Object database
# dataFolder = '/home/vital/SpecSynthesizer_data/'
# whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'
# catalogue_dict = dz.import_catalogue()
# catalogue_df = dz.load_excel_DF(whtSpreadSheet)
# dz.quick_indexing(catalogue_df)
#
# # Data root folder
# specS.normContants = {'He1r': 0.1, 'He2r': 0.001}
# root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'
#
# # HII galaxy
# objName = 'MAR1318'
# model_name = objName + '_MetalsOnly'
# objectFolder = '{}{}/'.format(root_folder, objName)
# outputFolder = objectFolder + 'output_data/'
# specS.objName = objName
# specS.configFile = '{}{}/{}_objParams.txt'.format(root_folder, objName, objName)
#
# # # Load the results
# db_address = outputFolder + model_name + '.db'  #
# inferenceTrace, db_dict = specS.load_pymc_database_manual(db_address, sampler='pymc3')
# params_list = np.array(db_dict.keys())
# params_list = np.array(['T_low', 'n_e' , 'He1r', 'He2r', 'S2', 'S3', 'O2', 'O3', 'Ar3', 'N2', 'tau'])
#
# # Corner plot
# print '--Scatter plot matrix'
# specS.corner_plot(params_list, db_dict)
# folderResults = '/home/vital/Dropbox/Astrophysics/Burocracia/Propuestas_trabajo/Chile_CONICT/Images/'
# specS.savefig(folderResults + 'Real_Partial_CornerPlot', resolution=100)