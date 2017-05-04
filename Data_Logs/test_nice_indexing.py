from numpy          import nan as np_nan
from dazer_methods  import Dazer
from pandas import notnull

#Generate dazer object
dz = Dazer()
   
#Load catalogue dataframe
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

dz.quick_indexing(catalogue_df)

# counter = 1
# for obj in catalogue_df.index:
#     
#     if catalogue_df.loc[obj,'Ignore_article'] != 'yes':
#     
#         if notnull(catalogue_df.loc[obj,'Favoured_ref']):
#             catalogue_df.loc[obj,'quick_index'] = catalogue_df.loc[obj,'Favoured_ref']
#         else:
#             catalogue_df.loc[obj,'quick_index'] = str(counter)
#             counter += 1
    
idx_include = notnull(catalogue_df['quick_index'])

print catalogue_df.loc[idx_include, 'quick_index']

print 'Otra\n'
for obj in catalogue_df.loc[idx_include].index:
    print obj, catalogue_df.loc[obj, 'quick_index']



