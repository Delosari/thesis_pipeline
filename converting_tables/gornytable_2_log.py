import  pandas as pd
from    dazer_methods import Dazer
from    numpy import isnan, nan, sort, unique, zeros, core, full
from    numpy.core.defchararray import add as add_str_array

dz = Dazer()

#Define data location
table_address_old = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Database/4_Gorny/4Gorny_table_plasma_diagnostics.xlsx'
table_address_new = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Master_table.xlsx'

#Load the tables
old_df = dz.load_excel_DF(table_address_old)
new_df = dz.load_excel_DF(table_address_new)

#Define the conversion dict:
conver_dict = {}
conver_dict['Name']     = 'Simbad_name'
conver_dict['Ne[SII]']  = 'neSII'
conver_dict['Te[OIII]'] = 'TOIII'
conver_dict['Te[NII]']  = 'TNII'

for column in old_df.columns:
     
    if column == 'Name':
        idcs                                    = old_df[column].index
        mag_values                              = old_df.loc[idcs, column].values
        new_df.loc[idcs, conver_dict[column]]   = mag_values
     
    elif column in conver_dict:
        idcs        = (pd.notnull(old_df[column])) & (pd.notnull(old_df['E_' + column])) & (pd.notnull(old_df['e_' + column]))
        objs_match  = old_df.loc[idcs, 'e_' + column].index
        mag_values  = old_df.loc[idcs, column].values
        error_sup   = (old_df.loc[idcs, 'E_' + column].values - mag_values).astype(str)
        error_min   = (mag_values - old_df.loc[idcs, 'e_' + column].values).astype(str)
        lim_sup     = add_str_array(full(len(error_sup), '+', dtype=str), error_sup)
        lim_inf     = add_str_array(full(len(error_sup), '-', dtype=str), error_min)
        
        #Write data in the new df
        new_df.loc[objs_match, conver_dict[column]]             = mag_values
        new_df.loc[objs_match, conver_dict[column] + '_error']  = add_str_array(lim_sup, lim_inf)
        
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(table_address_new, engine='xlsxwriter')
    
# Convert the dataframe to an XlsxWriter Excel object.
new_df.to_excel(writer, sheet_name='Sheet1')
      
# Close the Pandas Excel writer and output the Excel file.
writer.save()

