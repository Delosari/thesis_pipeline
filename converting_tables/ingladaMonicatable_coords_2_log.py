import  pandas as pd
from    dazer_methods import Dazer
from    numpy import isnan, nan, sort, unique, zeros, core, full
from    numpy.core.defchararray import add as add_str_array

dz = Dazer()

#Define data location
table_address_old = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Database/7_Delgado/Objects_ID.xlsx'
table_address_new = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Master_table.xlsx'

#Load the tables
old_df = dz.load_excel_DF(table_address_old)
new_df = dz.load_excel_DF(table_address_new)

print old_df.columns

for region in old_df.index.values:
     
    if region.replace('PN ', '') in new_df.index:        
        new_df.loc[region.replace('PN ', ''), 'Ra']             = old_df.loc[region, 'RA']
        new_df.loc[region.replace('PN ', ''), 'Dec']            = old_df.loc[region, 'DEC']
        new_df.loc[region.replace('PN ', ''), 'Simbad_name']    = region
        
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(table_address_new, engine='xlsxwriter')
    
# Convert the dataframe to an XlsxWriter Excel object.
new_df.to_excel(writer, sheet_name='Sheet1')
      
# Close the Pandas Excel writer and output the Excel file.
writer.save()

