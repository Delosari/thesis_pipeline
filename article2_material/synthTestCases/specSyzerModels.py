import numpy as np
from lib.inferenceModel import SpectraSynthesizer

# Declare synthesizer object
specS = SpectraSynthesizer()

# # Object data to prepare a synthetic observation
# synth_data ={'obs_name'                 :'synthTestHIIgalaxy',
#              'output_folder'            :'/home/vital/article_YpBayesian/',#'E:\\Research\\article_YpBayesian\\',
#              'obj_properties_file'      :'/home/vital/PycharmProjects/thesis_pipeline/article2_material/synth_TestObjProperties.txt',#'C:\\Users\\Vital\\PycharmProjects\\thesis_pipeline\\article2_material\\synth_TestObjProperties.txt',
#              'obj_lines_file'           :'/home/vital/PycharmProjects/thesis_pipeline/article2_material/synth_TestObjLines.txt',#'C:\\Users\\Vital\\PycharmProjects\\thesis_pipeline\\article2_material\\synth_TestObjLines.txt',
#              'wavelengh_limits'         :[4000, 6900],
#              'resample_inc'             :1,
#              'norm_interval'            :[5100, 5150],
#              'ssp_lib_type'             :'starlight',
#              'ssp_folder'               :'/home/vital/Starlight/Bases/', # E:\\Research\\Starlight\\Bases\\',
#              'ssp_file'                 :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt', # E:\\Research\\Starlight\\Bases\\Dani_Bases_Extra_short.txt',
#              'obj_ssp_coeffs_file'      :'/home/vital/PycharmProjects/thesis_pipeline/article2_material/synth_StellarPop.txt', # C:\\Users\\Vital\\PycharmProjects\\thesis_pipeline\\article2_material\\synth_StellarPop.txt',
#              'error_stellarContinuum'   :0.01,
#              'error_lines'              :0.02,
#              'atomic_data'              :None,
#              'ftau_coeffs'              :None}
#
# # Generate the synthetic data
# specS.gen_synth_obs(**synth_data)
#
# # Import stellar library data
# starlight_ssp = {'ssp_lib_type'         :'starlight',  # TODO In here we will add "test" for the pip
#                 'data_folder'           :'/home/vital/Starlight/Bases/',#'E:\\Research\\Starlight\\Bases\\',
#                 'data_file'             :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',#'E:\\Research\\Starlight\\Bases\\Dani_Bases_Extra_short.txt',
#                 'wavelengh_limits'      :[3600, 6900],
#                 'resample_inc'          :1,
#                 'norm_interval'         :[5100, 5150]}
# ssp_starlight = specS.load_ssp_library(**starlight_ssp)

# Import observation
data_address = '/home/vital/article_YpBayesian/' + 'synthTestHIIgalaxy_objParams.txt' #'E:\\Research\\article_YpBayesian\\' + 'synthTestHIIgalaxy_objParams.txt'
obsData = specS.load_obsData(data_address, 'synthTestHIIgalaxy')

# Simulation Data
fit_conf = dict(obs_data=obsData,
                ssp_data=None,
                output_folder='/home/vital/article_YpBayesian/',#'E:\\Research\\article_YpBayesian\\',
                spectra_components=['emission'], # ['emission', 'nebular', 'stellar'],
                prefit_ssp=False,
                wavelengh_limits=[4200, 6900],
                resample_inc=1,
                norm_interval=[5100, 5150])

# # Only sulfur case
# simuName = '1_Sulfur'
# reddening_check, Thigh_check = False, False
# idcsLineTest = specS.linesDb.ion.isin(['S2', 'S3'])
# fittingLines = np.squeeze(specS.linesDb.loc[idcsLineTest].index.values,)

# # Oxygen and sulfur
# simuName = '2_SulfurOxygen'
# reddening_check, Thigh_check = False, False
# idcsLineTest = specS.linesDb.ion.isin(['S2', 'S3', 'O2', 'O3'])
# fittingLines = np.squeeze(specS.linesDb.loc[idcsLineTest].index.values,)

# # Metals and extinction
# simuName = '3_MetalsAndExtinction'
# reddening_check, Thigh_check = True, False
# idcsLineTest = specS.linesDb.ion.isin(['S2', 'S3', 'O2', 'O3', 'N2', 'Ar3', 'Ar4'])
# fittingLines = np.squeeze(specS.linesDb.loc[idcsLineTest].index.values,)
#
# # Metals and extinction
# simuName = '4_MetalsExtinctionTwoTemps'
# reddening_check, Thigh_check = True, True
# idcsLineTest = specS.linesDb.ion.isin(['S2', 'S3', 'O2', 'O3', 'N2', 'Ar3', 'Ar4'])
# fittingLines = np.squeeze(specS.linesDb.loc[idcsLineTest].index.values,)

# Complete model
simuName = '5_CompleteModel'
reddening_check, Thigh_check = True, True
idcsLineTest = specS.linesDb.ion.isin(['S2', 'S3', 'O2', 'O3', 'N2', 'Ar3', 'Ar4', 'H1r', 'He1r', 'He2r']) & ~specS.linesDb.index.isin(['O2_7319A', 'O2_7330A'])
fittingLines = np.squeeze(specS.linesDb.loc[idcsLineTest].index.values,)

# Prepare fit data
specS.prepareSimulation(input_lines=fittingLines, **fit_conf)

# Run the simulation
specS.fitSpectra(model_name=simuName, iterations=6000, tuning=3000, include_reddening=reddening_check, include_Thigh_prior=Thigh_check)