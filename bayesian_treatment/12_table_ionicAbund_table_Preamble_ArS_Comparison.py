from dazer_methods import Dazer
from uncertainties import unumpy
from collections import OrderedDict
from collections import OrderedDict
from pylatex import Package
import pandas as pd
import numpy as np
import uncertainties as un
from uncertainties.umath import pow as umath_pow, log10 as umath_log10, exp as umath_exp, isnan as un_isnan


# Import library object
dz = Dazer()

# Load observational data
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
dz.quick_indexing(catalogue_df)
bayes_catalogue_df_address = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_BayesianResults.txt'
bayes_catalogue_df = pd.read_csv(bayes_catalogue_df_address, delim_whitespace=True, header=0, index_col=0)

# Define data to load
ext_data = '_emis2nd'
ext_data_bayes = ''
pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/tables/ionicAbundancesTable_ArS_Comparison'

# Headers
headers_dic = OrderedDict()
headers_dic['SII_HII']          = r'$12 + log\left(\nicefrac{S^{+}}{H^{+}}\right)$'
headers_dic['SIII_HII']         = r'$12 + log\left(\nicefrac{S^{2+}}{H^{+}}\right)$'
headers_dic['ICF_SIV']          = r'$ICF\left(S^{3+}\right)$'
headers_dic['ArIII_HII']        = r'$12 + log\left(\nicefrac{Ar^{2+}}{H^{+}}\right)$'
headers_dic['ArIV_HII']         = r'$12 + log\left(\nicefrac{Ar^{3+}}{H^{+}}\right)$'

headers_dic_bayes = OrderedDict()
headers_dic_bayes['SII_HII']          = r'$12 + log\left(\nicefrac{S^{+}}{H^{+}}\right)$'
headers_dic_bayes['SIII_HII']         = r'$12 + log\left(\nicefrac{S^{2+}}{H^{+}}\right)$'
headers_dic_bayes['ICF_SIV']          = r'$ICF\left(S^{3+}\right)$'
headers_dic_bayes['ArIII_HII']        = r'$12 + log\left(\nicefrac{Ar^{2+}}{H^{+}}\right)$'
headers_dic_bayes['ArIV_HII']         = r'$12 + log\left(\nicefrac{Ar^{3+}}{H^{+}}\right)$'

properties_list = map((lambda x: x + ext_data), headers_dic.keys())
properties_list_bayes = headers_dic_bayes.keys()
headers_format = ['HII Galaxy'] + headers_dic.values() + headers_dic_bayes.values()

#Create a new list for the different entries
metals_list   = properties_list[:]
del metals_list[metals_list.index('ICF_SIV' + ext_data)]

# Set the pdf format
dz.create_pdfDoc(pdf_address, pdf_type='table')
dz.pdf_insert_table(headers_format)

for objName in catalogue_df.loc[dz.idx_include].index:
    entry_name = catalogue_df.loc[objName].quick_index

    objData = catalogue_df.loc[objName]
    abundValues = objData[metals_list].values
    objData[metals_list] = 12.0 + unumpy.log10(abundValues)

    row = [entry_name]
    row += list(objData[['SII_HII' + ext_data, 'SIII_HII' + ext_data, 'ICF_SIV' + ext_data, 'ArIII_HII' + ext_data, 'ArIV_HII' + ext_data]].values)

    # Bayes data
    bayesCodeName = '{}'.format(bayes_catalogue_df.loc[objName].quick_index)
    bayes_values = []

    if bayesCodeName not in ['SHOC588', 'SHOC592', 'SHOC036', 'SHOC575', 'SHOC579', 'SHOC220']:

        objData_bayes = bayes_catalogue_df.loc[objName]

        for param in properties_list_bayes:
            param_value = objData_bayes[param]
            param_err   = objData_bayes[param + '_err']
            param_un    = un.ufloat(param_value, param_err)

            if param not in ['HeII_HII', 'HeIII_HII', 'ICF_SIV']:
                param_un = 12 + umath_log10(param_un)

            if np.isnan(param_un.nominal_value):
                param_un = np.nan

            bayes_values.append(param_un)




    else:
        bayes_values += ['none'] * len(properties_list_bayes)

    dz.addTableRow(row + bayes_values, last_row=False if catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)

dz.generate_pdf(clean_tex=False)


# from dazer_methods import Dazer
# from uncertainties import unumpy
# from collections import OrderedDict
# from pylatex import Package
# import pandas as pd
# import numpy as np
# import uncertainties as un
# from uncertainties.umath import pow as umath_pow, log10 as umath_log10, exp as umath_exp, isnan as un_isnan
#
# #Import library object
# dz = Dazer()
#
# #Load observational data
# bayes_catalogue_df_address = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_BayesianResults.txt'
# bayes_catalogue_df = pd.read_csv(bayes_catalogue_df_address, delim_whitespace=True, header=0, index_col=0)
#
# #Define data to load
# ext_data_bayes        = ''
# pdf_address     = '/home/vital/Dropbox/Astrophysics/Thesis/tables/bayes_ionicAbundancesTable_ONHe'
#
# #Headers
# headers_dic_bayes  = OrderedDict()
# headers_dic_bayes['HeII_HII'] = r'$\nicefrac{He^{+}}{H^{+}}$'
# headers_dic_bayes['HeIII_HII'] = r'$\nicefrac{He^{2+}}{H^{+}}$'
# headers_dic_bayes['OII_HII'] = r'$12 + log\left(\nicefrac{O^{+}}{H^{+}}\right)$'
# headers_dic_bayes['OIII_HII'] = r'$12 + log\left(\nicefrac{O^{2+}}{H^{+}}\right)$'
# headers_dic_bayes['NII_HII'] = r'$12 + log\left(\nicefrac{N^{+}}{H^{+}}\right)$'
#
# properties_list_bayes = map((lambda x: x + ext_data), headers_dic_bayes.keys())
# headers_format_bayes  = ['HII Galaxy'] + headers_dic_bayes.values()
#
# #Create a new list for the different entries
#
# # Set the pdf format
# dz.create_pdfDoc(pdf_address, pdf_type='table')
# dz.pdf_insert_table(headers_format_bayes)
#
# for objName in bayes_catalogue_df.index:
#
#     entry_name = '{}'.format(bayes_catalogue_df.loc[objName].quick_index)
#
#     if entry_name not in ['SHOC588', 'SHOC592', 'SHOC036', 'SHOC575', 'SHOC579', 'SHOC220']:
#
#         objData = bayes_catalogue_df.loc[objName]
#         row = [entry_name]
#
#         for param in properties_list_bayes:
#             param_value = objData[param]
#             param_err   = objData[param + '_err']
#             param_un    = un.ufloat(param_value, param_err)
#
#             if param not in ['HeII_HII', 'HeIII_HII']:
#                 param_un = 12 + umath_log10(param_un)
#
#             if np.isnan(param_un.nominal_value):
#                 param_un = np.nan
#
#             row.append(param_un)
#
#         dz.addTableRow(row, last_row = False if bayes_catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)
#
# dz.generate_pdf(clean_tex=False)



