# QUESTION Ask how to hide some warnings the files
import json
import ConfigParser
from collections import OrderedDict

from lib.Astro_Libraries.spectrum_fitting.multi_comp_v2 import SpecSynthesizer

#TODO add these as attributes of your library
He_lines = ['He1_4026A', 'He1_4471A', 'He1_5876A', 'He1_6678A']
H_lines  = ['H1_4102A', 'H1_4341A', 'H1_6563A']
O_lines  = ['O3_4363A', 'O3_4959A', 'O3_5007A', 'O2_7319A', 'O2_7330A']
S_lines  = ['S3_6312A', 'S2_6716A', 'S2_6731A', 'S3_9069A', 'S3_9531A']
N_lines  = ['N2_6548A', 'N2_6584A']
Ar_lines = ['Ar4_4740A', 'Ar3_7136A', 'Ar3_7751A']


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
obsData['cHbeta_prior'], obsData['cHbeta_error_prior'] = 0.075, 0.05

# Import stellar library
ssp_starlight = specS.load_ssp_library(**starlight_ssp)

# Simulation configuration
fit_conf = {'model_name'                :'Metals_adaptive',
            'obs_data'                  :obsData,
            'ssp_data'                  :ssp_starlight,
            'iterations'                :10000,
            'burn'                      :2000,
            'thin'                      :1,
            'output_folder'             :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
            'wavelengh_limits'          :[4200,6900],
            'resample_inc'              :1,
            'norm_interval'             :[5100, 5150],
            'input_lines'               :O_lines + S_lines,
            'fitting_components'        :['emission'],
            'prefit_SSP'                :False,
            'prefit_model'              :True,
            'params_list'               :['T_low', 'n_e','cHbeta'],
            'model_type'                :'pymc3'}

# Run fit
specS.fit_observation(**fit_conf)