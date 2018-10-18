from dazer_methods import Dazer
from uncertainties import unumpy
from collections import OrderedDict
from pylatex import Package
import pandas as pd
import numpy as np
import uncertainties as un
from uncertainties.umath import pow as umath_pow, log10 as umath_log10, exp as umath_exp, isnan as un_isnan

#Import library object
dz = Dazer()

#Load observational data
# catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
# dz.quick_indexing(catalogue_df)
bayes_catalogue_df_address = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_BayesianResults.txt'
bayes_catalogue_df = pd.read_csv(bayes_catalogue_df_address, delim_whitespace=True, header=0, index_col=0)

#Define data to load
ext_data        = ''
pdf_address     = '/home/vital/Dropbox/Astrophysics/Thesis/tables/bayes_ionicAbundancesTable_SAr'

#Headers
headers_dic  = OrderedDict()
headers_dic['SII_HII']          = r'$12 + log\left(\nicefrac{S^{+}}{H^{+}}\right)$'
headers_dic['SIII_HII']         = r'$12 + log\left(\nicefrac{S^{2+}}{H^{+}}\right)$'
headers_dic['ICF_SIV']          = r'$ICF\left(S^{3+}\right)$'
headers_dic['ArIII_HII']        = r'$12 + log\left(\nicefrac{Ar^{2+}}{H^{+}}\right)$'
headers_dic['ArIV_HII']         = r'$12 + log\left(\nicefrac{Ar^{3+}}{H^{+}}\right)$'

properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
headers_format  = ['HII Galaxy'] + headers_dic.values()

#Create a new list for the different entries
metals_list   = properties_list[:]
del metals_list[metals_list.index('ICF_SIV' + ext_data)]
print bayes_catalogue_df.index.values

#Set the pdf format
dz.pdf_insert_table(headers_format)

for objName in bayes_catalogue_df.index:

    entry_name   = '{}'.format(bayes_catalogue_df.loc[objName].quick_index)

    if entry_name not in ['SHOC588', 'SHOC592', 'SHOC036', 'SHOC575', 'SHOC579', 'SHOC220']:

        objData = bayes_catalogue_df.loc[objName]
        row = [entry_name]

        for param in properties_list:
            param_value = objData[param]
            param_err   = objData[param + '_err']
            param_un    = un.ufloat(param_value, param_err)

            if param not in ['HeII_HII', 'HeIII_HII', 'ICF_SIV']:
                param_un = 12 + umath_log10(param_un)

            if np.isnan(param_un.nominal_value):
                param_un = np.nan

            row.append(param_un)

        dz.addTableRow(row, last_row = False if bayes_catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)


    # objData     = bayes_catalogue_df.loc[objName]
    # abundValues = objData[metals_list].values
    # objData[metals_list] = 12.0 + unumpy.log10(abundValues)
    #
    # row         = [entry_name]
    # row         += list(objData[['SII_HII' + ext_data, 'SIII_HII' + ext_data, 'ICF_SIV' + ext_data, 'ArIII_HII' + ext_data, 'ArIV_HII' + ext_data]].values)
    #
    # dz.addTableRow(row, last_row = False if bayes_catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=2)
    
dz.generate_pdf(output_address=pdf_address)



