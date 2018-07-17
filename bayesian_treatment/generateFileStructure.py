import numpy as np
import pandas as pd
from collections import OrderedDict
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.import_functions import make_folder, parseObjData

#Import library object
dz = Dazer()

# Files naming
whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'
spectrum_ext = '_ext'
lineslog_ext = '_WHT_linesLog_reduc.txt'
masklog_ext = '_Mask.lineslog'

#Load observational data
catalogue_dict  = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtSpreadSheet)
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + lineslog_ext
dz.quick_indexing(catalogue_df)

#New format
root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'

#Reformating params
columnsMaskLog = ['w3', 'w4', 'pixel_tag', 'comment']
lineslogDfNewHeaders = {'lambda_obs':'obs_wavelength', 'Ion':'Ion_label', 'flux_intg':'obs_flux', 'flux_intg_er':'obs_fluxErr',
                        'Wave1':'w1','Wave2':'w2','Wave3':'w3','Wave4':'w4','Wave5':'w5','Wave6':'w6'}

#Loop throught the objects
for objName in catalogue_df.loc[dz.idx_include].index:

    print('Treating {}'.format(objName))

    # Article refernce
    quick_reference = catalogue_df.loc[objName].quick_index

    # Object folder
    oldFolder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
    objectNewFolder = root_folder + objName
    make_folder(objectNewFolder)

    # Get fits data
    fits_file = catalogue_df.loc[objName].reduction_fits
    wave, flux, etraData = dz.get_spectra_data(fits_file)

    # Convert spectrum fits to text file
    newsSpectrumAddress = '{}/{}_WHT.txt'.format(objectNewFolder, objName)
    np.savetxt(newsSpectrumAddress, np.transpose(np.array([wave, flux])), fmt="%7.1f %10.4e")

    # Get lines log data
    lineslog_address = '{}{}{}'.format(oldFolder,objName,lineslog_ext)
    linesLogDf = dz.load_lineslog_frame(lineslog_address)
    linesLogDf.rename(columns=lineslogDfNewHeaders, inplace=True)

    # Add continuum masks
    masksLogAddress = '{}{}{}'.format(oldFolder,objName,masklog_ext)
    masksDf = pd.read_csv(masksLogAddress, names=columnsMaskLog, delim_whitespace=True, header=1)
    masksDf.set_index('comment', inplace=True)

    for row in masksDf.index:
        if row not in linesLogDf.index:
            linesLogDf.loc[row] = np.nan
            linesLogDf.loc[row, 'w3':'w4'] = masksDf.loc[row, 'w3':'w4']

    # Save txt lines log
    newsLinesLogAddress = '{}/{}_linesLog.txt'.format(objectNewFolder, objName)
    with open(newsLinesLogAddress, 'w') as f:
        f.write(linesLogDf.ix[:, :'group_label'].to_string(index=True, index_names=False))

    # Create object log file
    objDict = OrderedDict()

    # Temperature favored for the calculations
    temp_low_key = catalogue_df.loc[objName].T_low
    temp_high_key = catalogue_df.loc[objName].T_high

    objDict['address_lines_log']   = newsLinesLogAddress
    objDict['address_spectrum']    = newsSpectrumAddress
    objDict['flux_hbeta']          = linesLogDf.loc['H1_4861A'].obs_flux
    objDict['flux_halpha']         = linesLogDf.loc['H1_6563A'].obs_flux
    objDict['Normalized_by_Hbeta'] = False
    objDict['eqw_hbeta']           = linesLogDf.loc['H1_4861A'].eqw
    objDict['sigma_gas']           = linesLogDf.loc['O3_5007A'].sigma
    objDict['n_e']                 = catalogue_df.loc[objName].neSII_emis2nd.nominal_value
    objDict['T_low']               = catalogue_df.loc[objName, temp_low_key + '_emis2nd'].nominal_value
    objDict['T_high']              = catalogue_df.loc[objName, temp_high_key + '_emis2nd'].nominal_value
    objDict['cHbeta']              = catalogue_df.loc[objName].cHbeta_emis.nominal_value
    objDict['z_obj']               = 0
    objDict['Av_star']             = None
    objDict['sigma_star']          = None
    objDict['continuum_sigma']     = 0.05
    objDict['resample_inc']        = 1
    objDict['wavelengh_limits']    = [4300,6900]
    objDict['norm_interval']       = [4500,4550]
    objDict['Te_prior']            = [catalogue_df.loc[objName, temp_low_key + '_emis2nd'].nominal_value, catalogue_df.loc[objName, temp_low_key + '_emis2nd'].std_dev]
    objDict['ne_prior']            = [catalogue_df.loc[objName].neSII_emis2nd.nominal_value, catalogue_df.loc[objName].neSII_emis2nd.std_dev]

    # Save the data into an "ini" configuration file
    objLogAddress = '{}/{}_objParams.txt'.format(objectNewFolder,objName,lineslog_ext)
    parseObjData(objLogAddress, objName, objDict)