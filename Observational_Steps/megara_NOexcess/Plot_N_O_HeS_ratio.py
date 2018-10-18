from dazer_methods  import Dazer
from uncertainties  import unumpy
import pandas as pd

dic_cords = {}

# dic_cords['FTDTR-1'] = [0.100132, 0.01859]
# dic_cords['IZw18'] = [0.0722, 0.044]
# dic_cords['MRK36-A1'] = [0.075, 0]
# dic_cords['MRK36-A2'] = [0.08, 0]
# dic_cords['MRK475'] = [0.105, 0]
# dic_cords['IZw70'] = [0.096333, 0.0388715]
# dic_cords['MRK689'] = [0.07, 0]
# dic_cords['MRK67'] = [0.097, 0]
# dic_cords['FTDTR-3'] = [0.0855, 0.053]
# dic_cords['SHOC022'] = [0.079, 0.0466]
# dic_cords['FTDTR-4'] = [0.0904, 0]
dic_cords['SHOC220'] = [0.10, 0.042]
# dic_cords['FTDTR-6'] = [0.085, 0]
# dic_cords['FTDTR-7'] = [0.092, 0.05]
# dic_cords['MRK627'] = [0.082, 0.06]
dic_cords['SHOC592'] = [0.0980326, 0.0813889]
dic_cords['SHOC588'] = [0.091, 0.08664]
dic_cords['SHOC036'] = [0.104812, 0.0567286]
dic_cords['SHOC575'] = [0.101, 0.1323]
dic_cords['SHOC579'] = [0.101, 0.152]
# dic_cords['FTDTR-8'] = [0.07, 0.0265]
# dic_cords['SHOC263'] = [0.087, 0.04323567]
# dic_cords['FTDTR-9'] = [0.091, 0.034]
# dic_cords['FTDTR-10'] = [0.075, 0.06]

dic_cords['SHOC579'] = [0.38,       0.1323]
dic_cords['SHOC575'] = [0.40,       0.1323]
dic_cords['SHOC592'] = [0.77,       0.08664]
dic_cords['SHOC588'] = [0.40,      0.08664]
dic_cords['SHOC036'] = [0.19,       0.08664]
dic_cords['SHOC220'] = [0.10,       0.042]

dic_cords['SHOC579'] = [0.38,       0.147]
dic_cords['SHOC575'] = [0.40,       0.120]
dic_cords['SHOC592'] = [0.555,       0.063]
dic_cords['SHOC588'] = [0.405,      0.072]
dic_cords['SHOC036'] = [0.199,       0.063]
dic_cords['SHOC220'] = [-0.025,       0.055]


factor = 10000

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

x_coords  = HeI_HI/S_values
y_coords  = N_O_ratio

for j in range(objects.size):
    print objects[j], x_coords[j], y_coords[j]

dz.data_plot(unumpy.nominal_values(x_coords), unumpy.nominal_values(y_coords), label = '', markerstyle='o', x_error=unumpy.std_devs(x_coords), y_error=unumpy.std_devs(y_coords))
#dz.plot_text(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), text=objects, x_pad=1.005, y_pad=1.01, fontsize=20)
dz.Axis.set_xlim(-0.04, 0.9)

for i in range(len(objects)):
    if objects[i] in dic_cords:
        label_x, label_y =  dic_cords[objects[i]]
        dz.Axis.annotate(objects[i], xy=(x_coords[i].nominal_value, y_coords[i].nominal_value), xycoords='data', xytext=(label_x,label_y), textcoords='data', fontsize=19)
        #dz.plot_text(label_x, label_y, text=objects[i], x_pad=1.005, y_pad=1.01, fontsize=20)

dz.FigWording(r'$He/S$', r'$N/O$', '')
#dz.display_fig()
dz.savefig('/home/vital/Dropbox/Astrophysics/Telescope Time/MEGARA_NOexcess_Gradients/NOvsHeS.png')

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
