import numpy as np
from dazer_methods import Dazer

#Create class object
dz = Dazer()

# #Load columns data
format_file = '/home/vital/git/Dazer/Dazer/dazer/bin/catalogue_dataframe_format.dz'
column_codes, explanations, transciptions = np.loadtxt(format_file, dtype=str, delimiter=';', usecols = (0,1,2), unpack = True)

#Load catalogue
catalogue_dict = dz.import_catalogue()
catalogue_df   = dz.load_dataframe(catalogue_dict['dataframe'])

# for column_name in column_codes:
#     
#     if column_name not in catalogue_df.columns:
# 
#         catalogue_df[column_name] = None #Not sure if this should be NaN or float
# 
# catalogue_df = catalogue_df.ix[:,column_codes] #Organize columns by initial format


#Load data from the anexing file
sciData_table = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.txt'

objects, parameter_value = dz.get_TableColumn(['Objects','telluric_star'], TableAddress = sciData_table, datatype = str)

for i in range(len(objects)):
         
    if objects[i] in catalogue_df.index:
        
            catalogue_df.loc[objects[i], 'telluric_star'] = parameter_value[i]

#Sort by orders
catalogue_df = catalogue_df[column_codes]

dz.save_dataframe(catalogue_df, catalogue_dict['dataframe'])

print 'Process finished'



