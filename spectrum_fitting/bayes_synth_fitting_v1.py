from lib.Astro_Libraries.spectrum_fitting.multi_comp_v1 import SpecSynthesizer

# Simulation configuration
sim_conf = {'temp_grid'                 :[5000, 25000, 10],
            'den_grid'                  :[0, 1000, 5],
            'high_temp_ions'            :['He1','He2','O3','Ar4'],
            'R_v'                       :3.4,
            'reddenig_curve'            :'G03_average',
            'lowlimit_sspContribution'  :0.001}

# Object data
synth_data = {'spectra_components'      :['emission', 'nebular', 'stellar'],
              'wavelengh_limits'        :[4200,6900],
              'resample_inc'            :1,
              'norm_interval'           :[5100,5150],
              'input_ions'              :['H1','He1','He2','O2','O3','Ar3','Ar4','S2','S3','N2'],
              'output_folder'           :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
              'obj_mask_file'           :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_linesMask.txt',
              'obj_lines_file'          :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objlines.txt',
              'obj_properties_file'     :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objProperties.txt',
              'ssp_lib_type'            :'starlight',  # TODO In here we will add "test" for the pip
              'data_folder'             :'/home/vital/Starlight/Bases/',
              'data_file'               :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
              'obj_ssp_coeffs_file'     :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_stellarPop.txt',
              'error_stellarContinuum'  :0.01,
              'error_recomb_lines'      :0.02,
              'error_collexc_lines'     :0.02}

# Stellar library data
starlight_ssp = {'ssp_lib_type'         :'starlight',  # TODO In here we will add "test" for the pip
                'data_folder'           :'/home/vital/Starlight/Bases/',
                'data_file'             :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
                'wavelengh_limits'      :[3600, 6900],
                'resample_inc'          :1,
                'norm_interval'         :[5100, 5150]}

# Real object data
obj_data = {'Normalize by Hbeta'        :True,
            'address_fits'              :None,
            'address_spectrum'          :None,
            'obs_mask_address'          :None,
            'obs_wavelength'            :None,
            'obs_flux'                  :None,
            'recomb_fluxes'             :None,
            'metal_fluxes'              :None,
            'wavelengh_limits'          :[4000,6900],
            'resample_inc'              :1,
            'norm_interval'             :[5100, 5150],
            'input_ions'                :['H1','He1','He2','O2','O3','Ar3','Ar4','S2','S3','N2'],
            'run_prefit'                :'',
            'T_low'                     :'',
            'T_high'                    :'',
            'cHbeta'                    :'',
            'obj_lines_file'            :'',
            'obj_mask_file'             :'',
            'flux_hbeta'                :'',
            'flux_halpha'               :'',
            'eqw_hbeta'                 :'',
            'sigma_gas'                 :'',
            'z_star'                    :0.0,
            'continuum_sigma'           :0.02}

# Declare initial fit
specS = SpecSynthesizer(**sim_conf)

# Generate the synthetic data
synth_observation = specS.gen_synth_obs(**synth_data)

# Import stellar library
ssp_starlight = specS.load_ssp_library(**starlight_ssp)

# Object fit configuration
fit_conf = {'model_name'                :'Remaking_v1' + '_neb_stars_Abunds',
            'obs_data'                  :synth_observation,
            'ssp_data'                  :ssp_starlight,
            'iterations'                :15000,
            'burn'                      :7000,
            'thin'                      :1,
            'output_folder'             :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
            'wavelengh_limits'          :[4200,6900],
            'resample_inc'              :1,
            'norm_interval'             :[5100, 5150],
            'input_ions'                :['H1','He1','He2','O2','O3','Ar3','Ar4','S2','S3','N2'],
            'fitting_components'        :['emission', 'nebular', 'stellar'],
            'prefit_SSP'                :True,
            'prefit_model'              :False,
            'params_list'               :['He1_abund', 'T_He', 'T_low', 'ne','tau','cHbeta','S2_abund','S3_abund','O2_abund','O3_abund', 'N2_abund', 'Ar3_abund', 'Ar4_abund', 'sigma_star', 'Av_star']}

fit_conf = {'model_name'                :'Remaking_v1' + '_only_helium',
            'obs_data'                  :synth_observation,
            'ssp_data'                  :ssp_starlight,
            'iterations'                :15000,
            'burn'                      :7000,
            'thin'                      :1,
            'output_folder'             :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
            'wavelengh_limits'          :[4200,6900],
            'resample_inc'              :1,
            'norm_interval'             :[5100, 5150],
            'input_ions'                :['H1','He1','He2','O2','O3','Ar3','Ar4','S2','S3','N2'],
            'fitting_components'        :['emission'],
            'prefit_SSP'                :False,
            'prefit_model'              :True,
            'params_list'               :['He1_abund', 'T_low', 'n_e','tau','cHbeta']}

# Run fit
specS.fit_observation(**fit_conf)
