import numpy as np
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.multi_comp_v1 import SpecSynthesizer

iterat, burn, thin  = 15000, 0, 1
sim_model           = 'MenosLineas_v2'
sim_components      = '_neb_stars_Abunds'
obs_metals          = ['H1', 'He1', 'S2', 'S3', 'O2', 'O3', 'N2', 'Ar3', 'Ar4'] #TODO ions should be discovered from the lines labels
sim_name            = sim_model + sim_components
params_list         = ['He1_abund', 'T_He', 'T_low', 'ne','tau','cHbeta','S2_abund','S3_abund','O2_abund','O3_abund', 'N2_abund', 'Ar3_abund', 'Ar4_abund', 'sigma_star', 'Av_star']
burning             = 7000

#TODO Cambiar esto por un archivo de texto

# Simulation configuration
sim_conf = {'ssp_type':             'starlight',
            'ssp_folder':           '/home/vital/Starlight/Bases/',
            'ssp_conf_file':        '/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
            'temp_grid':            [5000, 25000, 10],
            'den_grid':             [0, 1000, 5],
            'high_temp_ions':       ['He', 'He1', 'He2', 'O3', 'Ar4'],
            'R_v':                  3.4,
            'reddenig_curve':       'G03_average'}

# Simulation object data
synth_data = {'wavelengh_limits':   [3600,6900],
            'resample_inc':         1,
            'norm_interval':        [5100,5150],
            'obj_mask_file':        '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_linesMask.txt',
            'obj_ssp_coeffs_file':  '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_stellarPop.txt',
            'obj_lines_file':       '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objlines.txt',
            'obj_properties_file':  '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objProperties.txt',
            'error_recomb_lines':   0.02,
            'error_collexc_lines':  0.02}

# Generate dazer object
dz      = Dazer()
specS   = SpecSynthesizer(**sim_conf)

# Generate the synthetic data
specS.gen_synth_obs(**synth_data)



# specS.calculate_simObservation(sim_components, obs_ions = obs_metals)
#
# #Select right model according to data
# bm.select_inference_model(sim_components)
#
# #Variables to save
# db_address = '{}{}_it{}_burn{}'.format(bm.paths_dict['inference_folder'], sim_name, iterat, burn)
#
# # Run sampler
# bm.run_pymc2(db_address, iterat, variables_list=params_list, prefit=False)
#
# # #Load database
# pymc2_db, stat_db_dict = bm.load_pymc_database_manual(db_address, burning, params_list)
#
# #Traces plot
# print '-Generating traces plot'
# dz.traces_plot(params_list, pymc2_db, stat_db_dict)
# dz.save_manager(db_address + '_tracesPlot_Test', save_pickle = False)
#
# #Posteriors plot
# print '-Generating posteriors plot'
# dz.posteriors_plot(params_list, pymc2_db, stat_db_dict)
# dz.save_manager(db_address + '_posteriorPlot', save_pickle = False)
#
# #Posteriors plot
# print '-Generating acorrelation plot'
# dz.acorr_plot(params_list, pymc2_db, stat_db_dict, n_columns=4, n_rows=4)
# dz.save_manager(db_address + '_acorrPlot', save_pickle = False)
#
# #Corner plot
# print '-Generating corner plot'
# dz.corner_plot(params_list, pymc2_db, stat_db_dict, plot_true_values=True)
# dz.save_manager(db_address + '_cornerPlot', save_pickle = False)
#
# print '\nData treated'
#
# dz.FigConf()
# dz.data_plot(bm.obj_data['obs_wave_resam'], bm.obj_data['obs_flux_norm'], label = 'obs_flux_norm')
# dz.data_plot(bm.obj_data['obs_wave_resam'], bm.obj_data['obs_flux_norm_masked'], label = 'obs_flux_norm_masked')
# dz.FigWording(xlabel = 'Wavelength', ylabel = 'Flux', title = '')
# dz.display_fig()