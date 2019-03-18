import numpy as np
from uncertainties import unumpy
import uncertainties as unc
from dazer_methods import Dazer
from collections import OrderedDict
from numpy import concatenate, unique, round, nan, isnan
from pandas import read_csv, isnull, notnull, DataFrame
from lib.CodeTools.sigfig import round_sig
import matplotlib.pyplot as plt
import seaborn as sns
from dazer_methods  import Dazer

#Generate dazer object
dz = Dazer()

#Define plot frame and colors
size_dict = {'figure.figsize':(20, 4), 'axes.labelsize':20, 'legend.fontsize':22, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':15, 'ytick.labelsize':15}
dz.FigConf(plotSize = size_dict)

# lines_log_format_address = '/home/vital/PycharmProjects/dazer/format/emlines_pyneb_optical_infrared.dz'
# whtDataFile = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'

lines_log_format_address = 'C:\\Users\\Vital\\PycharmProjects\\dazer\\format\\emlines_pyneb_optical_infrared.dz'
whtDataFile = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\WHT_Galaxies_properties.xlsx'
output_folder = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\objects\\'
saving_folder = 'E:\\Dropbox\\Astrophysics\\Papers\\Yp_BayesianMethodology\\source files\\images\\'

lines_log_format_headers = ['line_label', 'ion', 'lambda_theo', 'latex_format']
lines_df = read_csv(lines_log_format_address, index_col=0, names=lines_log_format_headers, delim_whitespace=True)
# linformat_df = read_csv(lines_log_format_address, names=['line_label', 'ion', 'lambda_theo', 'latex_format'], delim_whitespace=True)



# Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtDataFile)
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
    # ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)

    linelog_reducAddress = '{rootFolder}{objfolder}\\{codeName}_WHT_linesLog_reduc.txt'.format(rootFolder=output_folder, objfolder=objName, codeName=objName)
    reduc_linedf = dz.load_lineslog_frame(linelog_reducAddress)

    linelog_emisAddress = '{rootFolder}{objfolder}\\{codeName}_WHT_linesLog_emission_2nd.txt'.format(rootFolder=output_folder, objfolder=objName, codeName=objName)
    emission_linedf = dz.load_lineslog_frame(linelog_emisAddress)

    # Normalizing fluxes
    Hbeta_F = reduc_linedf.loc['H1_4861A'].line_Flux
    Hbeta_emisF = emission_linedf.loc['H1_4861A'].line_Flux

    # Short array and remove repeated entries
    lambdas_array = emission_linedf['lambda_theo'].values
    lambdas_array = unique(lambdas_array)

    # Loop through the observed lines an ad them to the Df
    for i in range(len(reduc_linedf.index)):

        lineIon = reduc_linedf.iloc[i].Ion
        lineLabel = reduc_linedf.iloc[i].name
        wave = reduc_linedf.iloc[i].lambda_theo
        recombLine = True if (('H1' in lineLabel) or ('He1' in lineLabel) or ('He2' in lineLabel))and wave > 3800  and wave < 6900 else False

        if recombLine and (lineLabel not in ['H1_6563A_w']):

            line_F = reduc_linedf.iloc[i].line_Flux
            line_emisF = emission_linedf.iloc[i].line_Flux
            diff = (1.0 - line_F / line_emisF) * 100

            linesDf_reduc.loc[lineLabel, 'wavelength'], linesDf_emis.loc[lineLabel, 'wavelength'] = wave, wave
            linesDf_reduc.loc[lineLabel, 'Ion'], linesDf_emis.loc[lineLabel, 'Ion'] = lineIon, lineIon
            linesDf_reduc.loc[lineLabel, objName], linesDf_emis.loc[lineLabel, objName] = line_F, line_emisF

#Sort by increasing wavelength just in case
linesDf_reduc.sort_values('wavelength', axis=0, ascending=True, inplace=True)
linesDf_emis.sort_values('wavelength', axis=0, ascending=True, inplace=True)

data, lineTags = [], []
lineLabelList = linesDf_reduc.index.values #['H1_6563A', 'He1_5876A']

for lineLabel in lineLabelList:
    if lineLabel not in ['H1_3889A', 'He1_4388A', 'He1_4388A', 'He1_4438A']:
        line_F, line_emisF = linesDf_reduc.loc[lineLabel].iloc[2::].values, linesDf_emis.loc[lineLabel].iloc[2::].values

        ionTag = linformat_df.loc[lineLabel, 'latex_format']
        labelTag = linformat_df.loc[lineLabel, 'latex_format']
        wave = 4861.0 if lineLabel == 'H1_4861A' else linformat_df.loc[lineLabel, 'lambda_theo']
        n_items = np.count_nonzero(~np.isnan(unumpy.nominal_values(line_F)))
        line_label = r'{} ${}$'.format(int(round(wave, 0)), ionTag) + "\n" + "{} HIIGs".format(n_items)

        diff = (1.0 - line_F / line_emisF) * 100
        diff_nv = unumpy.nominal_values(diff)
        diff_nv_noNAN = diff_nv[~np.isnan(diff_nv)]
        data.append(diff_nv_noNAN)
        lineTags.append(line_label)

dz.Axis.boxplot(data, showfliers=False)
dz.Axis.set_xticklabels(lineTags)

dz.Axis.set_xlabel(r'Recombination lines')
dz.Axis.set_ylabel(r'Intensity increment percentage')

dz.savefig(saving_folder + 'recombinationAbsorption')

# dz.display_fig()
