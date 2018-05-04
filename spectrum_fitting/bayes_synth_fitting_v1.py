import json
import ConfigParser
from collections import OrderedDict

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
              'wavelengh_limits'        :[4000,6900],
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

# Declare synthesizer object
specS = SpecSynthesizer(**sim_conf)

# Generate the synthetic data
specS.gen_synth_obs(**synth_data)

# Import data
obsData = specS.load_obsData('/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_obj.txt', 'synth_obj')

#TODO integrate these better
obsData['TSIII'],obsData['TSIII_error'] = 15000, 700
obsData['nSII'], obsData['nSII_error'] = 100, 50
obsData['cHbeta'], obsData['cHbeta_error'] = 0.75, 0.20

# Import stellar library
ssp_starlight = specS.load_ssp_library(**starlight_ssp)

# Object fit configuration
fit_conf = {'model_name'                :'Helium_test_2',
            'obs_data'                  :obsData,
            'ssp_data'                  :ssp_starlight,
            'iterations'                :30000,
            'burn'                      :10000,
            'thin'                      :1,
            'output_folder'             :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
            'wavelengh_limits'          :[4200,6900],
            'resample_inc'              :1,
            'norm_interval'             :[5100, 5150],
            'input_ions'                :['H1','He1','He2','O2','O3','Ar3','Ar4','S2','S3','N2'],
            'fitting_components'        :['emission'],
            'prefit_SSP'                :False,
            'prefit_model'              :True,
            'params_list'               :['He1_abund', 'T_low', 'n_e','tau','cHbeta', ]}

# Run fit
specS.fit_observation(**fit_conf)

# Helium_Metals_v1: 4743.5 sec, 10000 iter -> Una hora y media, 0.47 por ciclo
# -He1_abund 0.0857058597896
# -T_low 15874.8959008
# -n_e 130.000888354
# -tau 0.753184296125
# -cHbeta 0.107783255006
# -S2_abund 1.43107990555e-05
# -S3_abund 5.21963011135e-05
# -O2_abund 0.00022779450224
# -O3_abund 0.000697289547509
# -N2_abund 0.000334280935697
# -Ar3_abund 0.000621647699413
# -Ar4_abund 0.000113279366549

# Helium_v2: 4743.5 sec, 10000 iter -> 0.001 secs por ciclo
# -He1_abund 0.0856320421642
# -T_low 15666.13966
# -n_e 125.772863909
# -tau 0.754111410318
# -cHbeta 0.107173854206

# Metals_v2 3382.7 sec, 8000 iter ->  0.42 secs por ciclo
# -T_low 15599.9622395
# -n_e 130.000098141
# -cHbeta 0.149922379801
# -S2_abund 1.42478526503e-05
# -S3_abund 5.13974116139e-05
# -O2_abund 0.000234569905116
# -O3_abund 0.000739881695492
# -N2_abund 0.000334158053399
# -Ar3_abund 0.000612783364282
# -Ar4_abund 0.000118858021959