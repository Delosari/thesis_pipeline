import numpy as np
import pandas as pd
import uncertainties as unc
from collections import OrderedDict
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.import_functions import make_folder, parseObjData
from lib.Astro_Libraries.spectrum_fitting.plot_tools import Basic_plots
from uncertainties.unumpy import nominal_values, std_devs
from uncertainties import umath

def convertTo12logScale(df, objRef, variable, ext):

        value_natural = df.loc[objRef, variable + ext]

        if not umath.isnan(value_natural):
                if ('HeII' not in variable) and ('Ymass' not in variable) and ('ICF' not in variable):
                        value_log12 = 12.0 + umath.log10(value_natural)
                        newFormat = [value_log12.nominal_value, value_log12.std_dev]
                else:
                        newFormat = [value_natural.nominal_value, value_natural.std_dev]
        else:
                newFormat = [None, None]

        return newFormat

# Import library object
dz = Dazer()
bp = Basic_plots()

# Files location
rootOutput = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'
spectraFolder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/'
whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'
# rootOutput = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\bayesianModel\\'
# spectraFolder = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\objects\\'
# whtSpreadSheet = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\WHT_Galaxies_properties.xlsx'

# Files extensions
lineslog_ext = '_WHT_linesLog_emission_2nd.txt'
masklog_ext = '_Mask.lineslog'

# Load observational data
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtSpreadSheet)
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + lineslog_ext
dz.quick_indexing(catalogue_df)

# Reformatting params
columnsMaskLog = ['w3', 'w4', 'pixel_tag', 'comment']
lineslogDfNewHeaders = {'lambda_obs': 'obs_wavelength', 'Ion': 'Ion_label', 'Wave1': 'w1', 'Wave2': 'w2', 'Wave3': 'w3',
                        'Wave4': 'w4', 'Wave5': 'w5', 'Wave6': 'w6', 'group_label': 'region_label'}
lineslogDfNewIndeces = {'H1_4340A': 'H1_4341A', 'He1_4472A': 'He1_4471A'}

# Line labels for the objects
hydrogenLines   = ['H1_4341A', 'H1_6563A']
helium1Lines    = ['He1_4471A', 'He1_5876A', 'He1_6678A']
helium2Lines    = ['He2_4686A']
oxygen2Lines    = ['O2_7319A_b'] # ['O2_7319A', 'O2_7330A']
oxygen3Lines    = ['O3_4363A', 'O3_4959A', 'O3_5007A']
nitrogenLines   = ['N2_6548A', 'N2_6584A']
sulfurLines     = ['S2_6716A', 'S2_6731A'] + ['S3_6312A', 'S3_9069A', 'S3_9531A']
argon3Lines     = ['Ar3_7136A']
argon4Lines     = ['Ar4_4740A']
defaultLines = np.array(hydrogenLines + helium1Lines + helium2Lines + oxygen2Lines + oxygen3Lines + nitrogenLines + sulfurLines + argon3Lines + argon4Lines)

obj_AssignLines = {}
obj_AssignLines['MRK689'] = helium1Lines + sulfurLines + oxygen3Lines + nitrogenLines + oxygen2Lines + argon3Lines
obj_AssignLines['FTDTR-3'] = helium1Lines + sulfurLines + oxygen3Lines + nitrogenLines + oxygen2Lines + argon3Lines + argon4Lines
obj_AssignLines['FTDTR-5'] = helium1Lines + sulfurLines + oxygen3Lines + argon3Lines + argon4Lines
obj_AssignLines['MRK627'] = helium1Lines + sulfurLines + oxygen3Lines + nitrogenLines + oxygen2Lines + argon3Lines
obj_AssignLines['SHOC592'] = helium1Lines + sulfurLines + oxygen3Lines + nitrogenLines + oxygen2Lines + argon3Lines + argon4Lines
obj_AssignLines['SHOC575'] = helium1Lines + sulfurLines + oxygen3Lines + nitrogenLines + oxygen2Lines + argon3Lines
obj_AssignLines['FTDTR-8'] = helium1Lines + sulfurLines + oxygen3Lines + nitrogenLines + oxygen2Lines + argon3Lines + argon4Lines
obj_AssignLines['SHOC263'] = helium1Lines + sulfurLines + oxygen3Lines + nitrogenLines + oxygen2Lines + argon3Lines
obj_AssignLines['PHL293B'] = helium1Lines + helium2Lines + sulfurLines + oxygen3Lines + oxygen2Lines + argon3Lines + argon4Lines
obj_AssignLines['FTDTR-2'] = helium1Lines + helium2Lines + sulfurLines + oxygen3Lines + nitrogenLines + argon3Lines + argon4Lines
obj_AssignLines['IZw70'] = helium1Lines + helium2Lines + sulfurLines + oxygen3Lines + oxygen2Lines + nitrogenLines + argon3Lines
obj_AssignLines['FTDTR-9'] = helium1Lines + helium2Lines + sulfurLines + oxygen3Lines + oxygen2Lines + nitrogenLines + argon3Lines
obj_AssignLines['FTDTR-10'] = helium1Lines + helium2Lines + sulfurLines + oxygen3Lines + oxygen2Lines + nitrogenLines + argon3Lines
obj_AssignLines['SHOC036'] = hydrogenLines + helium1Lines + helium2Lines + oxygen3Lines + nitrogenLines + sulfurLines + argon3Lines + argon4Lines

# Loop throught the objects
for objName in catalogue_df.loc[dz.idx_include].index:

        if objName == '8':

                # Article reference
                quick_reference = catalogue_df.loc[objName].quick_index
                objInputLines = defaultLines if quick_reference not in obj_AssignLines else np.array(obj_AssignLines[quick_reference])

                print objName, (quick_reference)

                # Declare folder structure folder
                # oldFolder = '{}{}\\'.format(spectraFolder, objName)
                # objectNewFolder = rootOutput + objName + '\\'
                # plotFolder = '{}input_data\\'.format(objectNewFolder)
                # plotAddress = '{}{}_lineGrid'.format(plotFolder, objName)
                # fitsAddress = '{}{}_WHT.fits'.format(oldFolder, objName)
                # objLogAddress = '{}{}_objParams.txt'.format(objectNewFolder, objName)
                # lineslog_address = '{}{}{}'.format(oldFolder, objName, lineslog_ext)
                # masksLogAddress = '{}{}{}'.format(oldFolder, objName, masklog_ext)
                # newsLinesLogAddress = '{}{}_linesLog.txt'.format(objectNewFolder, objName)
                # newsSpectrumAddress = '{}{}_WHT.txt'.format(objectNewFolder, objName)
                oldFolder = '{}{}/'.format(spectraFolder, objName)
                objectNewFolder = rootOutput + objName + '/'
                plotFolder = '{}input_data/'.format(objectNewFolder)
                plotAddress = '{}{}_lineGrid'.format(plotFolder, objName)
                fitsAddress = '{}{}_WHT.fits'.format(oldFolder, objName)
                objLogAddress = '{}{}_objParams.txt'.format(objectNewFolder, objName)
                lineslog_address = '{}{}{}'.format(oldFolder, objName, lineslog_ext)
                masksLogAddress = '{}{}{}'.format(oldFolder, objName, masklog_ext)
                newsLinesLogAddress = '{}{}_linesLog.txt'.format(objectNewFolder, objName)
                newsSpectrumAddress = '{}{}_WHT.txt'.format(objectNewFolder, objName)

                # Create folders
                make_folder(plotFolder)
                make_folder(objectNewFolder)

                # Get fits data
                wave, flux, etraData = dz.get_spectra_data(fitsAddress)

                # Get lines log data
                linesLogDf = dz.load_lineslog_frame(lineslog_address)
                linesLogDf.rename(columns=lineslogDfNewHeaders, inplace=True)
                linesLogDf.rename(index=lineslogDfNewIndeces, inplace=True)

                # Generate a grid plot and add continuum contribution in recombination lines
                lineFluxes = linesLogDf['line_Flux'].values
                linesLogDf['obs_flux'], linesLogDf['obs_fluxErr'] = nominal_values(lineFluxes), std_devs(lineFluxes)

                #WARNING this is a dangerous funcion
                bp.linesGrid(linesLogDf, wave, flux, plotAddress)
                linesLogDf['line_Flux'] = nominal_values(lineFluxes)

                # Compute O2_7319A_b flux
                if 'O2_7319A_b' in objInputLines:
                        linesLogDf.loc['O2_7319A', 'obs_flux'] + linesLogDf.loc['O2_7330A', 'obs_flux']

                        O2_7319A_flux = unc.ufloat(linesLogDf.loc['O2_7319A', 'obs_flux'], linesLogDf.loc['O2_7319A', 'obs_fluxErr'])
                        O2_7330A_flux = unc.ufloat(linesLogDf.loc['O2_7330A', 'obs_flux'], linesLogDf.loc['O2_7330A', 'obs_fluxErr'])
                        O2_7319A_b_flux = O2_7319A_flux + O2_7330A_flux

                        linesLogDf.loc['O2_7319A_b', 'obs_flux'] = O2_7319A_b_flux.nominal_value
                        linesLogDf.loc['O2_7319A_b', 'obs_fluxErr'] = O2_7319A_b_flux.std_dev
                        linesLogDf.loc['O2_7319A_b', 'Ion_label'] = linesLogDf.loc['O2_7319A', 'Ion_label']
                        linesLogDf.loc['O2_7319A_b', 'obs_wavelength'] = (7319.0 + 7330.0)/ 2.0

                # Sort the dataframe by wavelength in case it isn't
                linesLogDf.sort_values(by=['obs_wavelength'], ascending=True, inplace=True)

                # Add continuum masks
                masksDf = pd.read_csv(masksLogAddress, names=columnsMaskLog, delim_whitespace=True, header=1)
                masksDf.set_index('comment', inplace=True)

                for row in masksDf.index:
                        if row not in linesLogDf.index:
                            linesLogDf.loc[row] = np.nan
                            linesLogDf.loc[row, 'w3':'w4'] = masksDf.loc[row, 'w3':'w4']
                            linesLogDf.loc[row, 'region_label'] = 'continuum_mask'

                # Save txt lines log
                with open(newsLinesLogAddress, 'w') as f:
                        f.write(linesLogDf.ix[:, :].to_string(index=True, index_names=False))

                # Convert spectrum fits to text file
                np.savetxt(newsSpectrumAddress, np.transpose(np.array([wave, flux])), fmt="%7.1f %10.4e")

                # Create object log file
                objDict = OrderedDict()

                # Temperature favored for the calculations
                temp_low_key = catalogue_df.loc[objName].T_low
                temp_high_key = catalogue_df.loc[objName].T_high

                objDict['address_lines_log'] = newsLinesLogAddress
                objDict['address_spectrum'] = newsSpectrumAddress
                objDict['z_obj'] = 0
                objDict['Av_star'] = None
                objDict['sigma_star'] = None
                objDict['continuum_sigma'] = 0.05
                objDict['resample_inc'] = 1
                objDict['wavelengh_limits'] = [4300, 6900]  # TODO change first value by a 0
                objDict['norm_interval'] = [4500, 4550]
                objDict['flux_hbeta'] = linesLogDf.loc['H1_4861A'].line_Flux
                objDict['flux_halpha'] = linesLogDf.loc['H1_6563A'].line_Flux
                objDict['Normalized_by_Hbeta'] = False
                objDict['eqw_hbeta'] = linesLogDf.loc['H1_4861A'].eqw
                objDict['sigma_gas'] = linesLogDf.loc['O3_5007A'].sigma
                objDict['n_e_true'] = [catalogue_df.loc[objName, 'neSII_emis2nd'].nominal_value, catalogue_df.loc[objName, 'neSII_emis2nd'].std_dev]
                objDict['T_low_true'] = [catalogue_df.loc[objName, temp_low_key + '_emis2nd'].nominal_value, catalogue_df.loc[objName, temp_low_key + '_emis2nd'].std_dev]
                objDict['T_high_true'] = [catalogue_df.loc[objName, temp_high_key + '_emis2nd'].nominal_value, catalogue_df.loc[objName, temp_high_key + '_emis2nd'].std_dev]
                objDict['cHbeta_true'] = [catalogue_df.loc[objName, 'cHbeta_emis'].nominal_value, catalogue_df.loc[objName, 'cHbeta_emis'].std_dev]
                objDict['Te_prior'] = [12000.0, 2500.0]
                objDict['ne_prior'] = [200.0, 100.0]
                objDict['O2_true'] = convertTo12logScale(catalogue_df, objName, 'OII_HII', '_emis2nd')
                objDict['O3_true'] = convertTo12logScale(catalogue_df, objName, 'OIII_HII', '_emis2nd')
                objDict['S2_true'] = convertTo12logScale(catalogue_df, objName, 'SII_HII', '_emis2nd')
                objDict['S3_true'] = convertTo12logScale(catalogue_df, objName, 'SIII_HII', '_emis2nd')
                objDict['N2_true'] = convertTo12logScale(catalogue_df, objName, 'NII_HII', '_emis2nd')
                objDict['Ar3_true'] = convertTo12logScale(catalogue_df, objName, 'ArIII_HII', '_emis2nd')
                objDict['Ar4_true'] = convertTo12logScale(catalogue_df, objName, 'ArIV_HII', '_emis2nd')
                objDict['He1r_true'] = convertTo12logScale(catalogue_df, objName, 'HeII_HII_from_S', '_emis2nd')
                objDict['He2r_true'] = convertTo12logScale(catalogue_df, objName, 'HeIII_HII_from_S', '_emis2nd')
                objDict['O_abund_true'] = convertTo12logScale(catalogue_df, objName, 'OI_HI', '_emis2nd')
                objDict['N_abund_true'] = convertTo12logScale(catalogue_df, objName, 'NI_HI', '_emis2nd')
                objDict['S_abund_true'] = convertTo12logScale(catalogue_df, objName, 'SI_HI', '_emis2nd')
                objDict['ICF_SIV_true'] = convertTo12logScale(catalogue_df, objName, 'ICF_SIV', '_emis2nd')
                objDict['Ymass_O_true'] = convertTo12logScale(catalogue_df, objName, 'Ymass_O', '_emis2nd')
                objDict['Ymass_S_true'] = convertTo12logScale(catalogue_df, objName, 'Ymass_S', '_emis2nd')
                objDict['input_lines'] = objInputLines

                # Save the data into an "ini" configuration file
                parseObjData(objLogAddress, objName, objDict)

