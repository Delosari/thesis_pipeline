from dazer_methods  import Dazer
from uncertainties  import unumpy
import pandas as pd

dic_cords = {}

dic_cords['SHOC579'] = [0.105,       0.147]
dic_cords['SHOC575'] = [0.1,       0.120]
dic_cords['SHOC592'] = [0.1047,      0.0686]
dic_cords['SHOC588'] = [0.1012,      0.048]
dic_cords['SHOC036'] = [0.0894,      0.078]
dic_cords['SHOC220'] = [0.0904,     0.0575]

#Generate dazer object
dz = Dazer()

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Define plot frame and colors
size_dict = {'figure.figsize':(14, 6), 'axes.labelsize':35, 'legend.fontsize':26, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':32, 'ytick.labelsize':32}
dz.FigConf(plotSize = size_dict)

dz.quick_indexing(catalogue_df)
idcs = (pd.notnull(catalogue_df.SI_HI_emis2nd)) & (pd.notnull(catalogue_df.OI_HI_emis2nd)) & (pd.notnull(catalogue_df.NI_HI_emis2nd)) & (pd.notnull(catalogue_df.HeII_HII_from_O_emis2nd)) & (catalogue_df.quick_index.notnull()) & (~catalogue_df.index.isin(['SHOC593']))

#Prepare data
O_values  = catalogue_df.loc[idcs].OI_HI_emis2nd.values 
N_values  = catalogue_df.loc[idcs].NI_HI_emis2nd.values
S_values  = catalogue_df.loc[idcs].SI_HI_emis2nd.values
HeI_HI   = catalogue_df.loc[idcs].HeI_HI_from_O_emis2nd.values
objects   = catalogue_df.loc[idcs].quick_index.values

N_O_ratio = N_values/O_values

x_coords  = HeI_HI
y_coords  = N_O_ratio

for j in range(objects.size):
    print objects[j], x_coords[j], y_coords[j]

dz.data_plot(unumpy.nominal_values(x_coords), unumpy.nominal_values(y_coords), label = '', markerstyle='o', x_error=unumpy.std_devs(x_coords), y_error=unumpy.std_devs(y_coords))
#dz.plot_text(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), text=objects, x_pad=1.005, y_pad=1.01, fontsize=20)

for i in range(len(objects)):
    if objects[i] in dic_cords:
        label_x, label_y =  dic_cords[objects[i]]
        dz.Axis.annotate(objects[i], xy=(x_coords[i].nominal_value, y_coords[i].nominal_value), xycoords='data', xytext=(label_x,label_y), textcoords='data', fontsize=19)
        #dz.plot_text(label_x, label_y, text=objects[i], x_pad=1.005, y_pad=1.01, fontsize=20)

dz.Axis.set_xlabel(r'$He/H$')
dz.Axis.set_ylabel(r'$N/O$')

#dz.display_fig()
dz.savefig('/home/vital/Dropbox/Astrophysics/Telescope Time/MEGARA_NOexcess_Gradients/NOvsHe.png')

# from dazer_methods import Dazer
# from uncertainties import unumpy
# import pandas as pd
#
# # Generate dazer object
# dz = Dazer()
#
# # Load catalogue dataframe
# catalogue_dict = dz.import_catalogue()
# catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
#
# # Define plot frame and colors
# size_dict = {'figure.figsize': (18, 8), 'axes.labelsize': 35, 'legend.fontsize': 26, 'font.family': 'Times New Roman',
#              'mathtext.default': 'regular', 'xtick.labelsize': 32, 'ytick.labelsize': 32}
# dz.FigConf(plotSize=size_dict)
#
# dz.quick_indexing(catalogue_df)
# idcs = (pd.notnull(catalogue_df.OI_HI_emis2nd)) & (pd.notnull(catalogue_df.NI_HI_emis2nd)) & (
# pd.notnull(catalogue_df.HeII_HII_from_O_emis2nd)) & (catalogue_df.quick_index.notnull()) & (
#        ~catalogue_df.index.isin(['SHOC593']))
#
# # Prepare data
# O_values = catalogue_df.loc[idcs].OI_HI_emis2nd.values
# N_values = catalogue_df.loc[idcs].NI_HI_emis2nd.values
# HeII_HI = catalogue_df.loc[idcs].HeII_HII_from_O_emis2nd.values
# objects = catalogue_df.loc[idcs].quick_index.values
#
# N_O_ratio = N_values / O_values
#
# dz.data_plot(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), label='', markerstyle='o',
#              x_error=unumpy.std_devs(HeII_HI), y_error=unumpy.std_devs(N_O_ratio))
# dz.plot_text(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), text=objects, x_pad=1.005, y_pad=1.01,
#              fontsize=20)
# # dz.Axis.set_yscale('log')
#
#
# dz.FigWording(r'y', r'$N/O$', '')
# # dz.display_fig()
# dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/NO_to_y')
