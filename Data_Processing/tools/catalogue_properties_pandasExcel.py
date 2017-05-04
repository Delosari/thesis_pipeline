from numpy import object_
import pyneb as pn
import pandas as pd
from string import ascii_uppercase
from dazer_methods import Dazer
from collections import OrderedDict
from uncertainties import UFloat, unumpy 

#Generate dazer object
dz = Dazer()

sciData_address = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations_BackUp/WHT_Galaxies_properties.xlsx'
sciData_saving_test = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations_BackUp/WHT_Galaxies_properties_saveTest.xlsx'

catalogue_sheetDF = dz.load_excel_DF(sciData_address)

# for coso in dz.ipExcel_sheetColumns:
#     print coso, dz.ipExcel_sheetColumns[coso]
# 
# print catalogue_sheetDF.columns.values

# print catalogue_sheetDF['Code1']

# catalogue_sheetDF['Code3'] = unumpy.uarray(catalogue_sheetDF.Code1.values, catalogue_sheetDF.Code2.values)
# catalogue_sheetDF['Code4'] = unumpy.uarray(catalogue_sheetDF.Code1.values, catalogue_sheetDF.Code2.values)
#   
# dz.ipExcel_sheetColumns['Data_Properties'].append('Code3')
# dz.ipExcel_sheetColumns['Data_Properties'].append('Code4')

dz.save_excel_DF(catalogue_sheetDF, sciData_saving_test, df_sheet_format = 'catalogue_data')



# df_sheet_format = OrderedDict()
# 
# ipExcel_sheetColumns = OrderedDict() 
# with pd.ExcelFile(sciData_address) as xlsx_file:
# 
#     #Load all sheets
#     list_Df_sheet_i, sheets_names = [], xlsx_file.sheet_names
#     for sheet in sheets_names:
#         df_i = xlsx_file.parse(sheet, index_col=0)
#         list_Df_sheet_i.append(df_i)
#         ipExcel_sheetColumns[sheet] = df_i.columns.values
# 
# df = pd.concat(list_Df_sheet_i, axis=1)
#  
# with pd.ExcelWriter(sciData_saving_test, engine='xlsxwriter') as writer:
#      
#     #Saving the sheets
#     for sheet in ipExcel_sheetColumns:
#         sheet_columns = ipExcel_sheetColumns[sheet]
#         df[sheet_columns].to_excel(writer, sheet_name=sheet)
#         worksheet = writer.sheets[sheet]
#          
#         #Saving the columns
#         for idx in range(len(sheet_columns) + 1):
#             if sheet_columns[idx-1] not in df_sheet_format:
# 
#                 #Choose column width
#                 header_maxlengh = len(sheet_columns[idx-1]) + 2
#                 data_maxlength  = df[sheet_columns[idx-1]].astype(str).map(len).max() + 2
#                 letter          = '{columm_letter}:{columm_letter}'.format(columm_letter = ascii_uppercase[idx])
#                 
#                 #Set the format
#                 worksheet.set_column(letter, header_maxlengh if header_maxlengh > data_maxlength else data_maxlength, None) 
#          
#     writer.save()
