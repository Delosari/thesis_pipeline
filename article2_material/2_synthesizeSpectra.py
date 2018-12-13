import numpy as np
from dazer_methods import Dazer
from lib.inferenceModel import SpectraSynthesizer
import matplotlib.pyplot as plt

# Declare synthesizer object
specS = SpectraSynthesizer()

#Import library object
dz = Dazer()

# Object database
dataFolder = '/home/vital/SpecSynthesizer_data/'
whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtSpreadSheet)
dz.quick_indexing(catalogue_df)

# Data root folder
root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'

# Import stellar library data
starlight_ssp = {'ssp_lib_type'         :'starlight',
                'data_folder'           :'/home/vital/Starlight/Bases/',
                'data_file'             :'/home/vital/Starlight/Bases/Dani_Bases_Extra.txt',
                'wavelengh_limits'      :[3600, 6900],
                'resample_inc'          :1,
                'norm_interval'         :[5100, 5150]}

# Simulation Data
fit_conf = {'obs_data'                  :None,
            'ssp_data'                  :None,
            'output_folder'             :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
            'spectra_components'        :['emission', 'nebular', 'stellar'],
            'input_lines'               :'all',
            'prefit_ssp'                :False,
            'prefit_data'               :None,
            'wavelengh_limits'          :[0,6900],
            'resample_inc'              :1,
            'norm_interval'             :[5100,5150]}

specS.NoReddening = False

#Loop throught the objects
failing_objects = []
for objName in catalogue_df.index:

    # try:

    if objName == 'SHOC579':

            print('Treating {}'.format(objName))
            objectFolder = '{}{}/'.format(root_folder, objName)
            dataLocation = '{}{}/{}_objParams.txt'.format(root_folder, objName, objName)
            obsData = specS.load_obsData(dataLocation, objName)

            # Set object wmin
            if obsData['obs_wavelength'][0] < 4270 and 'SHOC' not in objName:
                if obsData['obs_wavelength'][0] < 3600:
                    fit_conf['wavelengh_limits'][0] = 3600
                    obsData['wavelengh_limits'][0] = 3600
                else:
                    fit_conf['wavelengh_limits'][0] = 0
                    obsData['wavelengh_limits'][0] = 0

            # Assign nebular continuum parameters
            specS.nebDefault['Te_neb']      = obsData['Te_prior'][0]
            specS.nebDefault['cHbeta_neb']  = obsData['cHbeta_prior']
            specS.nebDefault['flux_halpha'] = obsData['flux_halpha']

            # Treat the stellar database for the object
            sigma_prefit = obsData['sigma_star_prefit'][0]

            # Get resampled obj wave
            adjusting_prefit = {}
            specS.treat_input_spectrum(adjusting_prefit, obsData['obs_wavelength'], obsData['obs_flux'],
                                       fit_conf['wavelengh_limits'], fit_conf['resample_inc'], fit_conf['norm_interval'])

            # Treat the stellar database to match the object wavelength and prior
            starlight_ssp['wavelengh_limits'] = [adjusting_prefit['wave_resam'][0], 6900]
            ssp_starlight = specS.load_ssp_library(**starlight_ssp)
            ssp_fluxNorm_sigmaTreated = specS.physical_SED_model(ssp_starlight['wave_resam'], adjusting_prefit['wave_resam'], ssp_starlight['flux_norm'], 0.0, 0.0, sigma_prefit, Rv_coeff=specS.Rv_model)
            ssp_starlight['flux_norm'] = ssp_fluxNorm_sigmaTreated.T

            # Declaring configuration format
            fit_conf = {'obs_data': obsData,
                        'ssp_data': ssp_starlight,
                        'output_folder': objectFolder,
                        'spectra_components': ['emission'],
                        'input_lines': obsData['input_lines'],
                        'prefit_ssp': False,
                        'prefit_data':dataFolder,
                        'wavelengh_limits': [0, 6900],
                        'resample_inc': 1,
                        'norm_interval': [5100, 5150]}

            # Prepare fit data
            specS.prepareSimulation(**fit_conf)

            #Fit the data
            model_name = objName + '_MetalsOnly'
            output_folder = objectFolder + 'output_data/'
            specS.fitSpectra(model_name=model_name, iterations=5000, tuning=5000, output_folder=output_folder)

#     except:
#         failing_objects.append(objName)
#
# if len(failing_objects) > 0:
#     print 'These objects failed their analysis'
#     for j in range(len(failing_objects)):
#         print failing_objects[j]


        # except:
        #     print 'It failed'

        # Av_starPrefit = specS.stellarAv_prior[0]
        # prefitContinuum = specS.sspPrefitCoeffs.dot(specS.onBasesFluxNorm) * np.power(10, -0.4 * Av_starPrefit * specS.Xx_stellar)
        #
        # print Av_starPrefit, specS.sspPrefitCoeffs
        #
        # fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        # ax.plot(specS.inputWave, specS.inputContinuum, label='Input object')
        # ax.plot(specS.inputWave, prefitContinuum + specS.nebDefault['synth_neb_flux'], label='prefit continuum')
        # ax.update({'xlabel': 'Wavelength (nm)', 'ylabel': 'Flux (normalised)'})
        # ax.legend()
        # plt.show()
        # for i in specS.range_bases:
        #     ax.plot(specS.inputWave, specS.onBasesFluxNorm[i,:] * specS.sspPrefitCoeffs[i], label='base {}'.format(i))