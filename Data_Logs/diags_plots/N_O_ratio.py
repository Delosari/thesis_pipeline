from dazer_methods  import Dazer
from numpy          import nanmean, nanstd, mean, nan as np_nan
from uncertainties  import ufloat, unumpy
import pandas as pd
 
#Generate dazer object
dz = Dazer()

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Plot configuration
dz.FigConf()

idcs = (pd.notnull(catalogue_df.OI_HI_emis2nd)) & (pd.notnull(catalogue_df.NI_HI_emis2nd)) & (~catalogue_df.index.isin(['0564', '3', '70', '51991-224']))

#Prepare data
O_values  = catalogue_df.loc[idcs].OI_HI_emis2nd.values 
N_values  = catalogue_df.loc[idcs].NI_HI_emis2nd.values
objects   = catalogue_df.loc[idcs].index.values

print objects

N_O_ratio = N_values/O_values

for i in range(len(N_O_ratio)):
    print objects[i], O_values[i], N_values[i], N_O_ratio[i]

dz.data_plot(unumpy.nominal_values(O_values)*1e5, unumpy.nominal_values(N_O_ratio), label = 'Abundances from our sample', markerstyle='o', x_error=unumpy.std_devs(O_values)*1e5, y_error=unumpy.std_devs(N_O_ratio))
dz.plot_text(unumpy.nominal_values(O_values)*1e5, unumpy.nominal_values(N_O_ratio), text=objects)

dz.FigWording(r'$O/H$ $(10^5)$', r'$N/O$', r'N/O relation for HII galaxy sample')

dz.display_fig()