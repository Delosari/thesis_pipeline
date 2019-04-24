from lib.inferenceModel import SpectraSynthesizer
from lib.Astro_Libraries.spectrum_fitting.import_functions import make_folder

# Import functions
specS = SpectraSynthesizer()

# Data location
objName = 'obj'
objectFolder = 'E:\\Research\\NebularContinuum_fitting\\'

# Declare configuration file
dataFileAddress = '{}{}Params.txt'.format(objectFolder, objName)
obsData = specS.load_obsData(dataFileAddress, objName)

# Declaring configuration design
simuName = '{}_emissionHMC'.format(objName)
fit_conf = dict(obs_data=obsData,
                ssp_data=None,
                output_folder=objectFolder,
                spectra_components=['emission'],
                input_lines=obsData['input_lines'],
                prefit_ssp=False,
                normalized_by_Hbeta=False)

# Prepare fit data
specS.prepareSimulation(**fit_conf)

# Run the simulation
specS.fitSpectra(model_name=objName + '_HMC_fit_v0', iterations=6000, tuning=3000,
                 include_reddening=obsData['redening_check'], include_Thigh_prior=obsData['Thigh_check'])

