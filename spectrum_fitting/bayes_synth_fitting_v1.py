import numpy as np
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.multi_comp_v1 import SpecSynthesizer

a = {'a':1, 'b':2}
b = a
b['c'] = 3

# Simulation configuration
sim_conf = {'temp_grid'                 :[5000, 25000, 10],
            'den_grid'                  :[0, 1000, 5],
            'high_temp_ions'            :['He1','He2','O3','Ar4'],
            'R_v'                       :3.4,
            'reddenig_curve'            :'G03_average',
            'lowlimit_sspContribution'  :0.01}

# Simulation object data
synth_data = {'spectra_components'  :['emission', 'nebular', 'stellar'],
            'wavelengh_limits'      :[4200,6900],
            'resample_inc'          :1,
            'norm_interval'         :[5100,5150],
            'input_ions'            :['H1','He1','He2','O2','O3','Ar3','Ar4','S2','S3','N2'],
            'output_folder'         :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
            'obj_mask_file'         :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_linesMask.txt',
            'obj_lines_file'        :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objlines.txt',
            'obj_properties_file'   :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objProperties.txt',
            'ssp_lib_type'          :'starlight',  # TODO In here we will add "test" for the pip
            'data_folder'           :'/home/vital/Starlight/Bases/',
            'data_file'             :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
            'obj_ssp_coeffs_file'   :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_stellarPop.txt',
            'error_stellarContinuum':0.01,
            'error_recomb_lines'    :0.02,
            'error_collexc_lines'   :0.02}

# wave_resam
# flux_resam
# flux_norm
# normFlux_coeff

# Stellar library data
starlight_ssp = {'ssp_lib_type'     :'starlight',  # TODO In here we will add "test" for the pip
                'data_folder'       :'/home/vital/Starlight/Bases/',
                'data_file'         :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
                'wavelengh_limits'  :[3600, 6900],
                'resample_inc'      :1,
                'norm_interval'     :[5100, 5150]
                 }

# Real object data
obj_data = {'Normalize by Hbeta'    :True,
            'address_fits'          :None,
            'address_spectrum'      :None,
            'obs_mask_address'      :None,
            'obs_wavelength'        :None,
            'obs_flux'              :None,
            'recomb_fluxes'         :None,
            'metal_fluxes'          :None,
            'wavelengh_limits'      :[4000,6900],
            'resample_inc'          :1,
            'norm_interval'         :[5100, 5150],
            'input_ions'            :['H1','He1','He2','O2','O3','Ar3','Ar4','S2','S3','N2'],
            'T_low'                 :'',
            'T_high'                :'',
            'cHbeta'                :'',
            'obj_lines_file'        :'',
            'obj_mask_file'         :'',
            'flux_hbeta'            :'',
            'eqw_hbeta'             :'',
            'sigma_gas'             :'',
            'z_star'                :0.0}


# Generate dazer object
dz      = Dazer()
specS   = SpecSynthesizer(**sim_conf)

# Generate the synthetic data
synth_observation = specS.gen_synth_obs(**synth_data)

# Import stellar library
ssp_starlight = specS.load_ssp_library(**starlight_ssp)

#Run the fit
fit_conf    =   {'model_name'           :'Remaking_v1' + '_neb_stars_Abunds',
                'iterations'            :15000,
                'burn'                  :7000,
                'thin'                  :1,
                'wavelengh_limits'      :[4200,6900],
                'resample_inc'          :1,
                'norm_interval'         :[5100, 5150],
                'input_ions'            :['H1','He1','He2','O2','O3','Ar3','Ar4','S2','S3','N2'],
                'fitting_components'    :['emission', 'nebular', 'stellar'],
                'params_list'           :['He1_abund', 'T_He', 'T_low', 'ne','tau','cHbeta','S2_abund','S3_abund','O2_abund',\
                                        'O3_abund', 'N2_abund', 'Ar3_abund', 'Ar4_abund', 'sigma_star', 'Av_star']}

specS.fit_observation(obs_data = synth_observation, ssp_data = ssp_starlight, **fit_conf)



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