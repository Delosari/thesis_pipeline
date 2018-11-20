from dazer_methods import Dazer
from collections import OrderedDict
from numpy import concatenate, unique, round, nan, isnan
import numpy as np
from pandas import read_csv, isnull, notnull, DataFrame
from lib.CodeTools.sigfig import round_sig

lines_log_format_headers = ['Ions', 'lambda_theo', 'notation']
lines_log_format_address = '/home/vital/PycharmProjects/dazer/format/emlines_pyneb_optical_infrared.dz'
lines_df = read_csv(lines_log_format_address, index_col=0, names=lines_log_format_headers, delim_whitespace=True)

# Generate dazer object
dz = Dazer()

# Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
norm_factor = 100

# Treatment add quick index
dz.quick_indexing(catalogue_df)

# Declare data for the analisis
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'

# Reddening properties
R_v = 3.4
red_curve = 'G03_average'
cHbeta_type = 'cHbeta_emis'

# Define table properties
obj_per_page = 1
column_code = ['line_Eqw', 'line_Flux', 'line_Int']
linformat_df = read_csv(lines_log_format_address, names=['ion', 'lambda_theo', 'latex_format'], header=0, delim_whitespace=True)
linformat_df.lambda_theo = round(linformat_df.lambda_theo.values, 2)

# Create new dictionaries to store the recombination line fluxes
linesDf_reduc = DataFrame(columns=['wavelength', 'Ion'])
linesDf_emis = DataFrame(columns=['wavelength', 'Ion'])

# Loop for objects
for objName in catalogue_df.loc[dz.idx_include].index:

    # Get object reference
    local_reference = objName.replace('_', '-')
    quick_reference = catalogue_df.loc[objName].quick_index

    # Get dataframes
    ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)

    linelog_reducAddress    = '{objfolder}{codeName}_WHT_linesLog_reduc.txt'.format(objfolder=ouput_folder, codeName=objName)
    reduc_linedf            = dz.load_lineslog_frame(linelog_reducAddress)

    linelog_emisAddress     = '{objfolder}{codeName}_WHT_linesLog_emission_2nd.txt'.format(objfolder=ouput_folder, codeName=objName)
    emission_linedf         = dz.load_lineslog_frame(linelog_emisAddress)

    # Normalizing fluxes
    Hbeta_F     = reduc_linedf.loc['H1_4861A'].line_Flux
    Hbeta_emisF = emission_linedf.loc['H1_4861A'].line_Flux

    # Short array and remove repeated entries
    lambdas_array = emission_linedf['lambda_theo'].values
    lambdas_array = unique(lambdas_array)

    # Loop through the observed lines an ad them to the Df
    for i in range(len(reduc_linedf.index)):

        lineLabel   = reduc_linedf.iloc[i].name
        wave        = reduc_linedf.iloc[i].lambda_theo
        recombLine  = True if (('H1' in lineLabel) or ('He1' in lineLabel) or ('He2' in lineLabel)) and wave < 6900 else False

        if recombLine and (lineLabel not in ['H1_6563A_w']):

            line_F      = reduc_linedf.iloc[i].line_Flux
            line_emisF  = emission_linedf.iloc[i].line_Flux
            diff        = (1.0 - line_F / line_emisF) * 100

            linesDf_reduc.loc[lineLabel, 'wavelength'] = reduc_linedf.iloc[i].lambda_theo
            linesDf_reduc.loc[lineLabel, 'Ion'] = reduc_linedf.iloc[i].Ion
            linesDf_reduc.loc[lineLabel, objName] = diff

            # linesDf_emis.loc[lineLabel, 'wavelength'] = emission_linedf.iloc[i].lambda_theo
            # linesDf_emis.loc[lineLabel, 'Ion'] = emission_linedf.iloc[i].Ion
            # linesDf_emis.loc[lineLabel, objName] = emission_linedf.iloc[i].line_Flux


        # linesDf_emis
        # if lineLabel in
        # print 'wave', wave, recombLine
        #
        # if recombLine:
        #
        #     if lineLabel != 'H1_6563A_w':
        #         #idx_label = (linformat_df['lambda_theo'] == wave)
        #         ion = linformat_df.loc[lineLabel, 'latex_format']
        #         wave = 4861.0 if lineLabel == 'H1_4861A' else wave
        #         wave_lam_ref = int(round(wave, 0))
        #         lineFlabel = r'{} ${}$'.format(wave_lam_ref, ion)
        #         row = [lineFlabel]
        #         row_i = [row] * 3
        #
        #         line_F = reduc_linedf.iloc[i].line_Flux
        #         line_emisF = emission_linedf.iloc[i].line_Flux
        #
        #         row_i[0] = line_F/Hbeta_F * norm_factor
        #         row_i[1] = line_emisF/Hbeta_F * norm_factor
        #         diff = (1.0 - line_F/line_emisF) * 100
        #         row_i[2] = round(diff.nominal_value,1)#/Hbeta_emisF * norm_factor
        #
        #         row = row + row_i
        #
        #         dz.addTableRow(row, last_row=False)



#Sort by increasing wavelength just in case
linesDf_reduc.sort_values('wavelength', axis=0, ascending=True, inplace=True)

#Loop through the lines wavelength
for i in range(len(linesDf_reduc.index)):

    lineLabel = linesDf_reduc.iloc[i].name
    lineWave = linesDf_reduc.iloc[i].wavelength
    diffPercentage = linesDf_reduc.iloc[i,2:].values

    # Remove nan entries
    diffPercentage = diffPercentage[~isnull(diffPercentage)]

    print lineLabel, lineWave, diffPercentage

