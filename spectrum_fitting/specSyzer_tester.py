import numpy as np
from lib.Astro_Libraries.spectrum_fitting.inferenceModel import SpectraSynthesizer

# Declare synthesizer object
specS = SpectraSynthesizer()

# Object data to prepare a synthetic observation
synth_data = {'spectra_components'      :['emission', 'nebular', 'stellar'],
              'wavelengh_limits'        :[4000,6900],
              'resample_inc'            :1,
              'norm_interval'           :[5100,5150],
              'output_folder'           :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
              'obs_name'                :'ObsHIIgalaxySynth',
              'obj_lines_file'          :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objlines.txt',
              'obj_properties_file'     :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objProperties.txt',
              'ssp_lib_type'            :'starlight',  # TODO In here we will add "test" for the pip
              'data_folder'             :'/home/vital/Starlight/Bases/',
              'data_file'               :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
              'obj_ssp_coeffs_file'     :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_stellarPop.txt',
              'error_stellarContinuum'  :0.01,
              'error_lines'             :0.02}

# Generate the synthetic data
specS.gen_synth_obs(**synth_data)

# Import observation
data_address = '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/' + 'ObsHIIgalaxySynth' + '_objParams.txt'
obsData = specS.load_obsData(data_address, 'ObsHIIgalaxySynth')

# Import stellar library data
starlight_ssp = {'ssp_lib_type'         :'starlight',  # TODO In here we will add "test" for the pip
                'data_folder'           :'/home/vital/Starlight/Bases/',
                'data_file'             :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
                'wavelengh_limits'      :[3600, 6900],
                'resample_inc'          :1,
                'norm_interval'         :[5100, 5150]}
ssp_starlight = specS.load_ssp_library(**starlight_ssp)

# Declare model
idcsLineTest = specS.linesDb.ion.isin(['S2', 'S3', 'O2', 'O3','N2', 'Ar3', 'Ar4', 'H1r', 'He1r', 'He2r'])
#idcsLineTest = specS.linesDb.ion.isin(['H1r', 'He1r', 'He2r'])
fittingLines = np.squeeze(specS.linesDb.loc[idcsLineTest].index.values,)
outpuFolder = '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/'
specS.NoReddening = False

# Simulation Data
fit_conf = dict(obs_data=obsData,
                ssp_data=ssp_starlight,
                output_folder=outpuFolder,
                spectra_components=['emission'], #['emission', 'nebular', 'stellar'],
                input_lines=fittingLines,
                prefit_ssp=False,
                prefit_data='/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/input_data/',
                wavelengh_limits=[4200, 6900],
                resample_inc=1,
                norm_interval=[5100, 5150])

# Prepare fit data
specS.prepareSimulation(**fit_conf)

# # Run the simulation
simuName = 'testSimu'
specS.fitSpectra(model_name=simuName, iterations=4000, tuning=3000, output_folder=outpuFolder)