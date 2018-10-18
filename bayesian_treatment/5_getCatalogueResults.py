import numpy as np
import pandas as pd
import uncertainties as un
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.inferenceModel import SpectraSynthesizer
import matplotlib.pyplot as plt
from uncertainties.umath import pow as umath_pow, log10 as umath_log10, exp as umath_exp, isnan as un_isnan
from uncertainties.unumpy import uarray, nominal_values, std_devs, log10 as unum_log10, pow as unnumpy_pow
from collections import OrderedDict

def load_unVariables(df, obj_idx, variable_keys):

    if not isinstance(variable_keys, (np.ndarray, list)):
        variable_keys = [variable_keys]

    output_params = [None] * len(variable_keys)

    for i in range(len(variable_keys)):
        key = variable_keys[i]
        param, paramErr = catalogueDf.loc[objName, key], catalogueDf.loc[objName, key+'_err']
        paramUn = un.ufloat(param, paramErr)
        output_params[i] = paramUn

    return output_params

def save_unVariables(df, obj_idx, variable_keys, variable_values, variable_errs):

    if not isinstance(variable_keys, (np.ndarray, list)):
        variable_keys, variable_values, variable_errs = [variable_keys], [variable_values], [variable_errs]

    for i in range(len(variable_keys)):
        df.loc[obj_idx, variable_keys[i]] = variable_values[i]
        df.loc[obj_idx, variable_keys[i] + '_err'] = variable_errs[i]

    return

# Ar vs S ionisation fractions relation
m_SIV_correction = un.ufloat(1.1628, 0.00559)
n_SIV_correction = un.ufloat(0.0470, 0.0097)

# Ohrs 2016 relation for the OI_SI gradient
logSI_OI_Gradient = un.ufloat(-1.53, 0.05)
OI_SI_un = umath_pow(10, -logSI_OI_Gradient)

# Constants
normContants = {'He1r': 0.1, 'He2r': 0.001}

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

rawData = OrderedDict([
                ('neSII','n_e'),
                ('TeSIII','T_low'),
                ('cHbeta','cHbeta'),
                ('tau' , 'tau'),
                ('SII_HII' , 'S2'),
                ('SIII_HII','S3'),
                ('OII_HII', 'O2'),
                ('OIII_HII','O3'),
                ('NII_HII','N2'),
                ('ArIII_HII','Ar3'),
                ('ArIV_HII','Ar4'),
                ('HeII_HII','He1r'),
                ('HeIII_HII', 'He2r'),
                # ('HeII_HII_from_S','He1r'),
                # ('HeIII_HII_from_S','He2r'),
                ('Av_star','Av_prefit'),
                ('sigma_star','sigma_star_prefit')])

log_variables = ['SII_HII', 'SIII_HII', 'OII_HII', 'OIII_HII', 'NII_HII', 'ArIII_HII', 'ArIV_HII']

calcParams = OrderedDict([
                ('SIV_HII', np.nan),
                ('ICF_SIV', np.nan),
                ('NI_OI',   np.nan),
                ('OI_HI',   np.nan),
                ('NI_HI',   np.nan),
                ('SI_HI',   np.nan),
                ('HeI_HI',  np.nan),
                ('Ymass_O', np.nan),
                ('Ymass_S', np.nan)])

catalogueDf = pd.DataFrame()

#Loop throught the objects
for objName in catalogue_df.loc[dz.idx_include].index:


            print('Treating {}'.format(objName))
            objectFolder = '{}{}/'.format(root_folder, objName)
            dataLocation = '{}{}/{}_objParams.txt'.format(root_folder, objName, objName)
            obsData = specS.load_obsData(dataLocation, objName)

            # Save fit parameters to log
            for param in rawData.keys():
                logEntry = rawData[param]

                if logEntry in obsData:
                    param_value, param_err = obsData[logEntry]
                else:
                    param_value, param_err = np.nan,  np.nan

                # Change to linear scale
                if param in log_variables:
                    paramLog_un = un.ufloat(param_value, param_err)
                    param_un = umath_pow(10, paramLog_un-12)
                    param_value, param_err = param_un.nominal_value,  param_un.std_dev

                if rawData[param] in normContants:
                    param_value, param_err = param_value * normContants[rawData[param]], param_err * normContants[rawData[param]]

                # Store the parameters
                save_unVariables(catalogueDf, objName, param, param_value, param_err)

            # Set nan values for calculated parameters
            for param in calcParams:
                save_unVariables(catalogueDf, objName, param, np.nan, np.nan)

            # Compute oxygen abundance
            if np.isnan(catalogueDf.loc[objName, ['OII_HII', 'OIII_HII']].values).any() == False:

                OII_HII_un, OIII_HII_un = load_unVariables(catalogueDf, objName, ['OII_HII', 'OIII_HII'])
                OI_HI_un = OII_HII_un + OIII_HII_un

                save_unVariables(catalogueDf, objName, 'OI_HI', OI_HI_un.nominal_value, OI_HI_un.std_dev)

            # Compute sulfur abundance
            if np.isnan(catalogueDf.loc[objName, ['SII_HII','SIII_HII']].values).any() == False:

                SII_HII_un, SIII_HII_un = load_unVariables(catalogueDf, objName, ['SII_HII', 'SIII_HII'])
                SI_HI_un = SII_HII_un + SIII_HII_un

                save_unVariables(catalogueDf, objName, 'SI_HI', SI_HI_un.nominal_value, SI_HI_un.std_dev)

            # Add S+3 contribution from Argon lines
            if np.isnan(catalogueDf.loc[objName, ['SI_HI','ArIII_HII','ArIV_HII']].values).any() == False:

                SI_HI_un, SII_HII_un, SIII_HII_un = load_unVariables(catalogueDf, objName, ['SI_HI', 'SII_HII', 'SIII_HII'])
                ArIII_HII_un, ArIV_HII_un = load_unVariables(catalogueDf, objName, ['ArIII_HII','ArIV_HII'])

                logAr2Ar3 = umath_log10(ArIII_HII_un) / umath_log10(ArIV_HII_un)
                logSIV = umath_log10(SIII_HII_un) - (logAr2Ar3 - n_SIV_correction) / m_SIV_correction
                SIV_HII_un = umath_pow(10, logSIV)

                SI_HI_un += SIV_HII_un
                ICF_SIV = SI_HI_un / (SII_HII_un + SIII_HII_un)

                save_unVariables(catalogueDf, objName, 'SI_HI', SI_HI_un.nominal_value, SI_HI_un.std_dev)
                save_unVariables(catalogueDf, objName, 'SIV_HII', SIV_HII_un.nominal_value, SIV_HII_un.std_dev)
                save_unVariables(catalogueDf, objName, 'ICF_SIV', ICF_SIV.nominal_value, ICF_SIV.std_dev)

            # Compute nitrogen abundance
            if np.isnan(catalogueDf.loc[objName, ['OI_HI', 'NII_HII']].values).any() == False:

                NII_HII_un, = load_unVariables(catalogueDf, objName, 'NII_HII')
                OI_HI_un, OII_HII_un, = load_unVariables(catalogueDf, objName, ['OI_HI', 'OII_HII'])

                NI_OI_un = NII_HII_un / OII_HII_un
                NI_HI_un = NI_OI_un * OI_HI_un

                save_unVariables(catalogueDf, objName, 'NI_OI', NI_OI_un.nominal_value, NI_OI_un.std_dev)
                save_unVariables(catalogueDf, objName, 'NI_HI', NI_HI_un.nominal_value, NI_HI_un.std_dev)

            # Compute helium abundance
            if np.isnan(catalogueDf.loc[objName, ['HeII_HII']].values).any() == False:

                HeII_HII_un, HeIII_HII_un = load_unVariables(catalogueDf, objName, ['HeII_HII', 'HeIII_HII'])

                if not np.isnan(HeIII_HII_un.nominal_value):
                    HeI_HI_un = HeII_HII_un + HeIII_HII_un
                else:
                    HeI_HI_un = HeII_HII_un

                save_unVariables(catalogueDf, objName, 'HeI_HI', HeI_HI_un.nominal_value, HeI_HI_un.std_dev)

            # Adjusting
            if objName == '51991-224':
                catalogueDf.loc['51991-224', 'HeI_HI'] = 0.094

            # Compute helium mass fraction using oxygen
            if np.isnan(catalogueDf.loc[objName, ['OI_HI', 'HeI_HI']].values).any() == False:

                OI_HI_un, HeI_HI_un = load_unVariables(catalogueDf, objName, ['OI_HI', 'HeI_HI'])

                Ymass_O_un = (4 * HeI_HI_un * (1 - 20 * OI_HI_un)) / (1 + 4 * HeI_HI_un)

                save_unVariables(catalogueDf, objName, 'Ymass_O', Ymass_O_un.nominal_value, Ymass_O_un.std_dev)


            # Compute helium mass fraction using sulfur
            if np.isnan(catalogueDf.loc[objName, ['SI_HI', 'HeI_HI']].values).any() == False:

                SI_HI_un, HeI_HI_un = load_unVariables(catalogueDf, objName, ['SI_HI', 'HeI_HI'])

                Ymass_S_un = (4 * HeI_HI_un * (1 - OI_SI_un * SI_HI_un)) / (1 + 4 * HeI_HI_un)

                save_unVariables(catalogueDf, objName, 'Ymass_S', Ymass_S_un.nominal_value, Ymass_S_un.std_dev)


#Loop throught the objects
for objName in catalogue_df.loc[dz.idx_include].index:
    quickReference = catalogue_df.loc[objName, 'quick_index']
    catalogueDf.loc[objName, 'quick_index'] = quickReference



# Save output data to text file
outputDataFile = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_BayesianResults.txt'
print outputDataFile
# with open(outputDataFile, 'w') as f:
#     f.write(catalogueDf.ix[:, :].to_string(index=True, index_names=False))

