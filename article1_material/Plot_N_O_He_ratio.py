from dazer_methods  import Dazer
from uncertainties  import unumpy
import pandas as pd
 
#Generate dazer object
dz = Dazer()

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Define plot frame and colors
size_dict = {'axes.labelsize':35, 'legend.fontsize':26, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':32, 'ytick.labelsize':32}
dz.FigConf(plotSize = size_dict)

dz.quick_indexing(catalogue_df)
idcs = (pd.notnull(catalogue_df.OI_HI_emis2nd)) & (pd.notnull(catalogue_df.NI_HI_emis2nd)) & (pd.notnull(catalogue_df.HeII_HII_from_O_emis2nd)) & (catalogue_df.quick_index.notnull()) & (~catalogue_df.index.isin(['SHOC593']))

#Prepare data
O_values  = catalogue_df.loc[idcs].OI_HI_emis2nd.values 
N_values  = catalogue_df.loc[idcs].NI_HI_emis2nd.values
HeII_HI   = catalogue_df.loc[idcs].HeII_HII_from_O_emis2nd.values 
objects   = catalogue_df.loc[idcs].quick_index.values

N_O_ratio = N_values/O_values

dz.data_plot(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), label = '', markerstyle='o', x_error=unumpy.std_devs(HeII_HI), y_error=unumpy.std_devs(N_O_ratio))
dz.plot_text(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), text=objects, x_pad=1.005, y_pad=1.01, fontsize=20)
# dz.Axis.set_yscale('log')


dz.FigWording(r'y', r'$N/O$', '')
#dz.display_fig()
dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/NO_to_y')

