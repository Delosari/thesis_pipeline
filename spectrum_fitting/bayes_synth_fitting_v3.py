from lib.Astro_Libraries.spectrum_fitting.multi_comp_v3 import SpecSynthesizer

# Simulation configuration
sim_conf = {'temp_grid'                 :[5000, 25000, 20],
            'den_grid'                  :[0, 500, 20],
            'high_temp_ions'            :['He1r','He2r','O3','Ar4'],
            'R_v'                       :3.4,
            'reddenig_curve'            :'G03 LMC',
            'lowlimit_sspContribution'  :0.001}

# Object data
synth_data = {'spectra_components'      :['emission', 'nebular', 'stellar'],
              'wavelengh_limits'        :[4000,6900],
              'resample_inc'            :1,
              'norm_interval'           :[5100,5150],
              'input_ions'              :['H1r','He1r','He2r','O2','O3','Ar3','Ar4','S2','S3','N2'],
              'output_folder'           :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
              'obs_name'                :'ObsHIIgalaxySynth',
              'obj_mask_file'           :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_linesMask.txt',
              'obj_lines_file'          :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objlines.txt',
              'obj_properties_file'     :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objProperties.txt',
              'ssp_lib_type'            :'starlight',  # TODO In here we will add "test" for the pip
              'data_folder'             :'/home/vital/Starlight/Bases/',
              'data_file'               :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
              'obj_ssp_coeffs_file'     :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_stellarPop.txt',
              'error_stellarContinuum'  :0.01,
              'error_lines'             :0.02}

# Stellar library data
starlight_ssp = {'ssp_lib_type'         :'starlight',  # TODO In here we will add "test" for the pip
                'data_folder'           :'/home/vital/Starlight/Bases/',
                'data_file'             :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
                'wavelengh_limits'      :[3600, 6900],
                'resample_inc'          :1,
                'norm_interval'         :[5100, 5150]}

# Declare synthesizer object
specS = SpecSynthesizer(**sim_conf)

# # Generate the synthetic data
# specS.gen_synth_obs(**synth_data)

# Import data
data_address = '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/' + 'ObsHIIgalaxySynth' + '_objParams.txt'
obsData = specS.load_obsData(data_address, 'ObsHIIgalaxySynth')

# Import stellar library
ssp_starlight = specS.load_ssp_library(**starlight_ssp)

# Simulation configuration
fit_conf = {'model_name'                :'TestingPymc3',
            'obs_data'                  :obsData,
            'ssp_data'                  :ssp_starlight,
            'iterations'                :10000,
            'burn'                      :2000,
            'thin'                      :1,
            'output_folder'             :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
            'wavelengh_limits'          :[4200,6900],
            'resample_inc'              :1,
            'norm_interval'             :[5100, 5150],
            'input_lines'               :'all',
            'fitting_components'        :['emission', 'nebular', 'stellar'],
            'prefit_SSP'                :True,
            'prefit_model'              :True,
            'params_list'               :['T_low', 'n_e','cHbeta'],
            'model_type'                :'pymc3'}

# Run fit
specS.fit_observation(**fit_conf)