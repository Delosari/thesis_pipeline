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
pdf_address     = '/home/vital/Dropbox/Astrophysics/Thesis/tables/bayes_ionicAbundancesTable_ONHe'

#Headers
headers_dic  = OrderedDict()
headers_dic['HeII_HII'] = r'$\nicefrac{He^{+}}{H^{+}}$'
headers_dic['HeIII_HII'] = r'$\nicefrac{He^{2+}}{H^{+}}$'
headers_dic['OII_HII'] = r'$12 + log\left(\nicefrac{O^{+}}{H^{+}}\right)$'
headers_dic['OIII_HII'] = r'$12 + log\left(\nicefrac{O^{2+}}{H^{+}}\right)$'
headers_dic['NII_HII'] = r'$12 + log\left(\nicefrac{N^{+}}{H^{+}}\right)$'

properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
headers_format  = ['HII Galaxy'] + headers_dic.values()

#Create a new list for the different entries
metals_list   = properties_list[:]
del metals_list[metals_list.index('HeII_HII' + ext_data)]
del metals_list[metals_list.index('HeIII_HII' + ext_data)]

#Set the pdf format
dz.pdf_insert_table(headers_format)
print bayes_catalogue_df.index.values


for objName in bayes_catalogue_df.index:

    entry_name   = '{}'.format(bayes_catalogue_df.loc[objName].quick_index)

    print entry_name

    if entry_name not in ['SHOC588', 'SHOC592', 'SHOC036', 'SHOC575', 'SHOC579', 'SHOC220']:

        objData = bayes_catalogue_df.loc[objName]
        row = [entry_name]

        for param in properties_list:
            param_value = objData[param]
            param_err   = objData[param + '_err']
            param_un    = un.ufloat(param_value, param_err)

            if param not in ['HeII_HII', 'HeIII_HII']:
                param_un = 12 + umath_log10(param_un)

            if np.isnan(param_un.nominal_value):
                param_un = np.nan

            row.append(param_un)

        dz.addTableRow(row, last_row = False if bayes_catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)


        # abundValues = objData[metals_list].values
        # abundErr    = 3
        # objData[metals_list] = 12.0 + unumpy.log10(abundValues)
        #
        # HeII_HII_from_O_entry = dz.format_for_table(bayes_catalogue_df.loc[objName, 'HeII_HII' + ext_data], rounddig=3, rounddig_er=2)
        # HeIII_HII_from_O_entry = dz.format_for_table(bayes_catalogue_df.loc[objName, 'HeIII_HII' + ext_data], rounddig=2, rounddig_er=1)
        #
        # row         = [entry_name] + [HeII_HII_from_O_entry, HeIII_HII_from_O_entry]
        # row         += list(objData[['OII_HII' + ext_data, 'OIII_HII' + ext_data, 'NII_HII' + ext_data]].values)
        #
        # dz.addTableRow(row, last_row = False if bayes_catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)

dz.generate_pdf(output_address=pdf_address)



