import  pandas as pd
from    dazer_methods import Dazer
from    numpy import isnan, nan, sort, unique, zeros, core, full
from    numpy.core.defchararray import add as add_str_array
from astropy import units as u
from astropy.coordinates import SkyCoord

dz = Dazer()

#Define data location
table_address_new = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Master_table.xlsx'

#Load the tables
new_df = dz.load_excel_DF(table_address_new)

for i in range(len(new_df)):
    
    if pd.notnull(new_df.iloc[i].Ra):
        
        coordinate = r'{} {}'.format(new_df.iloc[i].Ra, new_df.iloc[i].Dec)
        
        c = SkyCoord(coordinate, unit=(u.hourangle, u.deg)).to_string('decimal').split()
        
        pn_code = new_df.iloc[i].name
                
        new_df.loc[pn_code, 'Ra_deg'] = c[0]
        new_df.loc[pn_code, 'Dec_deg'] = c[1]
        
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(table_address_new, engine='xlsxwriter')
      
# Convert the dataframe to an XlsxWriter Excel object.
new_df.to_excel(writer, sheet_name='Sheet1')
        
# Close the Pandas Excel writer and output the Excel file.
writer.save()

