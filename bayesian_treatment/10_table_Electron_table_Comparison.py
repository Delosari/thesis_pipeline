from dazer_methods import Dazer
from lib.CodeTools.sigfig import round_sig
from uncertainties import unumpy
from collections import OrderedDict
from pylatex import Package, NoEscape
from numpy import isnan
from pandas import isnull
import pandas as pd
import numpy as np
import uncertainties as un
from uncertainties.umath import pow as umath_pow, log10 as umath_log10, exp as umath_exp, isnan as un_isnan

def colorChooser(ObsRatio, TheRatio):
    if (TheRatio * 0.95 < ObsRatio < TheRatio * 1.05):
        color = 'ForestGreen'  # 'green'#

    elif (TheRatio * 0.90 < ObsRatio < TheRatio * 1.10):
        color = 'YellowOrange'  # 'yellow'#

    else:
        color = 'BrickRed'

    return color


#Load observational data
bayes_catalogue_df_address = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_BayesianResults.txt'
bayes_catalogue_df = pd.read_csv(bayes_catalogue_df_address, delim_whitespace=True, header=0, index_col=0)

#Define data to load

# Import library object
dz = Dazer()
dz.load_elements()

# Load observational data
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_emission_2nd.txt'
dz.quick_indexing(catalogue_df)

# Reddening properties
R_v = 3.4
red_curve = 'G03_average'
cHbeta_type = 'cHbeta_emis'

# Define data to load
ext_data = '_emis2nd'
ext_data_bayes = ''
pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/tables/objProperties_Preamble'

# Headers
properties_list = ['neSII', 'TeSIII', 'TeOIII']
properties_list = map((lambda x: x + ext_data), properties_list)
properties_list_bayes = ['neSII', 'TeSIII']

headers_format = ['HII Galaxy', r'$\frac{[OIII]\lambda5007\AA}{[OIII]\lambda4959\AA}$', r'$\frac{[SIII]\lambda9531\AA}{[SIII]\lambda9069\AA}$']
headers_format += [r'$n_{e}[SII](cm^{-3})$', r'$T_{e}[SIII](K)$', r'$T_{e}[OIII](K)$']
headers_format += ['$n_{e}(cm^{-3})$', r'$T_{low}(K)$', r'$T_{high}(K)$']

# Set the pdf format
dz.create_pdfDoc(pdf_address, pdf_type='table')
dz.pdf_insert_table(headers_format)

for objName in catalogue_df.loc[dz.idx_include].index:

    ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
    lineslog_address = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder=ouput_folder, codeName=objName, lineslog_extension=AbundancesFileExtension)

    # Load lines frame
    lineslog_frame = dz.load_lineslog_frame(lineslog_address)

    # Perform the reddening correction
    cHbeta = catalogue_df.loc[objName, cHbeta_type]
    dz.deredden_lines(lineslog_frame, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)

    # Sulfur ratios
    if set(lineslog_frame.index) >= set(['S3_9069A', 'S3_9531A']):
        s3_ratio = lineslog_frame.loc['S3_9531A'].line_Int / lineslog_frame.loc['S3_9069A'].line_Int
        s3_color = colorChooser(s3_ratio.nominal_value, dz.S3_ratio)
        s3_entry = r'\textcolor{' + s3_color + '}{' + dz.format_for_table(s3_ratio, rounddig=3) + '}'
    else:
        s3_entry = '-'

    # Oxygen ratios
    if set(lineslog_frame.index) >= set(['O3_4959A', 'O3_5007A']):
        O3_ratio = lineslog_frame.loc['O3_5007A'].line_Int / lineslog_frame.loc['O3_4959A'].line_Int
        O3_color = colorChooser(O3_ratio.nominal_value, dz.O3_5000_ratio)
        O3_entry = r'\textcolor{' + O3_color + '}{' + dz.format_for_table(O3_ratio, rounddig=3) + '}'
    else:
        O3_entry = '-'

        # Fill the table
    if (catalogue_df.loc[objName].T_low == 'TeSIII') and (catalogue_df.loc[objName].T_high == 'TeOIII'):
        exponent = ''
    elif (catalogue_df.loc[objName].T_low != 'TeSIII'):
        exponent = 'O'
    else:
        exponent = 'S'

    # Add the Bayesian data
    bayesCodeName   = '{}'.format(bayes_catalogue_df.loc[objName].quick_index)
    bayes_values = []
    print '------', bayesCodeName, objName

    if bayesCodeName not in ['SHOC588', 'SHOC592', 'SHOC036', 'SHOC575', 'SHOC579', 'SHOC220']:

        objData = bayes_catalogue_df.loc[objName]

        for param in properties_list_bayes:
            param_value = objData[param]
            param_err   = objData[param + '_err']
            param_un    = un.ufloat(param_value, param_err)

            if np.isnan(param_un.nominal_value):
                param_un = np.nan

            bayes_values.append(param_un)

        param_un = (1.0807 * param_un / 10000.0 - 0.0846) * 10000.0

        bayes_values.append(param_un)

    else:

        bayes_values = ['-', '-', '-']

    entry_name = '{codename}$^{{{elements}}}$'.format(codename=catalogue_df.loc[objName].quick_index, elements=exponent)
    T_low_entry = r'$T_{e}[SIII]$' if catalogue_df.loc[objName].T_low == 'TeSIII' else r'$T_{e}[SIII] eq.16$'
    T_high_entry = r'$T_{e}[OIII]$' if catalogue_df.loc[objName].T_high == 'TeOIII' else r'$T_{e}[OIII] eq.16$'
    row = [entry_name] + [O3_entry] + [s3_entry] + list(catalogue_df.loc[objName, properties_list].values) + bayes_values
    dz.addTableRow(row, last_row=False if catalogue_df.index[-1] != objName else True, rounddig=3)

dz.generate_pdf(clean_tex=False)
# dz.generate_pdf(output_address=pdf_address)

print 'Table generated'
















# from dazer_methods import Dazer
# from uncertainties import unumpy
# from collections import OrderedDict
# from pylatex import Package, NoEscape
# from numpy import isnan
# from pandas import isnull
# import pandas as pd
# import numpy as np
# import uncertainties as un
# from uncertainties.umath import pow as umath_pow, log10 as umath_log10, exp as umath_exp, isnan as un_isnan
#
# dz = Dazer()
#
# #Load observational data
# bayes_catalogue_df_address = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_BayesianResults.txt'
# bayes_catalogue_df = pd.read_csv(bayes_catalogue_df_address, delim_whitespace=True, header=0, index_col=0)
#
# #Define data to load
# ext_data = ''
# pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/tables/bayes_AbundancesTable'
#
# #Headers
# headers_dic = OrderedDict()
# headers_dic['HeI_HI']   = r'$\nicefrac{He}{H}$'
# headers_dic['Ymass_O']  = r'$Y_{\left(\nicefrac{O}{H}\right)}$'
# headers_dic['Ymass_S']  = r'$Y_{\left(\nicefrac{S}{H}\right)}$'
# headers_dic['OI_HI']    = r'$12 + log\left(\nicefrac{O}{H}\right)$'
# headers_dic['NI_HI']    = r'$12 + log\left(\nicefrac{N}{H}\right)$'
# headers_dic['SI_HI']    = r'$12 + log\left(\nicefrac{S}{H}\right)$'
#
# properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
# headers_format = ['HII Galaxy'] + headers_dic.values()
#
# # Create a new list for the different entries
# metals_list = properties_list[:]
#
# del metals_list[metals_list.index('HeI_HI' + ext_data)]
# del metals_list[metals_list.index('Ymass_O' + ext_data)]
# del metals_list[metals_list.index('Ymass_S' + ext_data)]
#
# #Set the pdf format
# dz.pdf_insert_table(headers_format)
#
# print properties_list
#
# for objName in bayes_catalogue_df.index:
#
#     entry_name   = '{}'.format(bayes_catalogue_df.loc[objName].quick_index)
#
#     if entry_name not in ['SHOC588', 'SHOC592', 'SHOC036', 'SHOC575', 'SHOC579', 'SHOC220']:
#
#         objData = bayes_catalogue_df.loc[objName]
#         row = [entry_name]
#
#         for param in properties_list:
#             param_value = objData[param]
#             param_err   = objData[param + '_err']
#             param_un    = un.ufloat(param_value, param_err)
#
#             if param not in ['HeI_HI', 'Ymass_O', 'Ymass_S']:
#                 param_un = 12 + umath_log10(param_un)
#
#             if np.isnan(param_un.nominal_value):
#                 param_un = np.nan
#
#             row.append(param_un)
#
#     dz.addTableRow(row, last_row = False if bayes_catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)
#
# dz.generate_pdf()
# #dz.generate_pdf(output_address=pdf_address)
