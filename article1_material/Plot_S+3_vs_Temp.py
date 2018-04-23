from dazer_methods  import Dazer
from numpy          import nanmean, nanstd, mean, nan as np_nan, zeros
from uncertainties  import ufloat, unumpy
import pandas as pd
 
#Generate dazer object
dz = Dazer()
 
#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
ICF_IR_df       = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/data/SIV_ICF_literature.xlsx')

dz.quick_indexing(catalogue_df)

idcs            = (pd.notnull(catalogue_df.TeSIII_emis2nd)) & (pd.notnull(catalogue_df.ICF_SIV_emis2nd)) & (catalogue_df.quick_index.notnull())
idcs_oxygen     = (pd.notnull(catalogue_df.OI_HI_emis2nd)) & (pd.notnull(catalogue_df.OII_HII_emis2nd)) & (catalogue_df.quick_index.notnull())

for index in catalogue_df.index:
    print 'Troleo', index, catalogue_df.loc[index,'ICF_SIV_emis2nd']

#Define plot frame and colors
size_dict = {'axes.labelsize':35, 'legend.fontsize':22, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':30, 'ytick.labelsize':30}
dz.FigConf(plotSize = size_dict)

x_values        = catalogue_df.loc[idcs].TeSIII_emis2nd.values
y_values        = catalogue_df.loc[idcs].ICF_SIV_emis2nd.values
objects         = catalogue_df.loc[idcs].index.values
quick_reference = catalogue_df.loc[idcs].quick_index.values

x_IR_values     = ICF_IR_df.TeSIII.values
y_IR_values     = ICF_IR_df.ICF_SIV_IR.values
objectsIR       = ICF_IR_df.index.values

T_low_array     = zeros(len(objects))
T_low_err_array = zeros(len(objects))

for i in range(len(objects)):
    obj = objects[i]
    temp_label = catalogue_df.loc[obj, 'T_low']
    T_low_array[i], T_low_err_array[i] = catalogue_df.loc[obj, temp_label].nominal_value, catalogue_df.loc[obj, temp_label].std_dev
    print objects[i], x_values[i], y_values[i]
      
dz.data_plot(T_low_array, unumpy.nominal_values(y_values), label = r'Argon $ICF(S^{3+})$', markerstyle='o', x_error=T_low_err_array, y_error=unumpy.std_devs(y_values))
dz.plot_text(unumpy.nominal_values(T_low_array), unumpy.nominal_values(y_values), text=quick_reference,x_pad=1.005,y_pad=1.005, fontsize=18)

dz.data_plot(unumpy.nominal_values(x_IR_values), unumpy.nominal_values(y_IR_values), color=dz.colorVector['orangish'], label = r'$ICF(S^{3+})$ from IR (Dors 2016)', markerstyle='x', x_error=unumpy.std_devs(x_IR_values), y_error=unumpy.std_devs(y_IR_values))
dz.plot_text(unumpy.nominal_values(x_IR_values), unumpy.nominal_values(y_IR_values), text=objectsIR, fontsize=18)

dz.FigWording(r'$T_{low} (K)$', r'$ICF(S^{+3})$', '', loc=4)

# dz.display_fig()
dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/ICF_S+3')

# from dazer_methods import Dazer
# from numpy import nanmean, nanstd, mean, nan as np_nan, zeros
# from uncertainties import ufloat, unumpy
# import pandas as pd
#
# # Generate dazer object
# dz = Dazer()
#
# # Load catalogue dataframe
# catalogue_dict = dz.import_catalogue()
# catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
# ICF_IR_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/data/SIV_ICF_literature.xlsx')
#
# dz.quick_indexing(catalogue_df)
#
# idcs = (pd.notnull(catalogue_df.TeSIII_emis2nd)) & (pd.notnull(catalogue_df.ICF_SIV_emis2nd)) & (
# catalogue_df.quick_index.notnull())
# idcs_oxygen = (pd.notnull(catalogue_df.OI_HI_emis2nd)) & (pd.notnull(catalogue_df.OII_HII_emis2nd)) & (
# catalogue_df.quick_index.notnull())
#
# # Define plot frame and colors
# size_dict = {'axes.labelsize': 35, 'legend.fontsize': 26, 'font.family': 'Times New Roman',
#              'mathtext.default': 'regular', 'xtick.labelsize': 30, 'ytick.labelsize': 30}
# dz.FigConf(plotSize=size_dict)
#
# x_values = catalogue_df.loc[idcs].TeSIII_emis.values
# y_values = catalogue_df.loc[idcs].ICF_SIV_emis.values
# objects = catalogue_df.loc[idcs].index.values
# quick_reference = catalogue_df.loc[idcs].quick_index.values
#
# x_IR_values = ICF_IR_df.TeSIII.values
# y_IR_values = ICF_IR_df.ICF_SIV_IR.values
# objectsIR = ICF_IR_df.index.values
#
# T_low_array = zeros(len(objects))
# T_low_err_array = zeros(len(objects))
#
# OI_abund = catalogue_df.loc[idcs_oxygen].OI_HI_emis2nd
# OII_abunda = catalogue_df.loc[idcs_oxygen].OII_HII_emis2nd
# x_ratio = OII_abunda / OI_abund
# ICFs_thuan = 1.0 / (0.013 + x_ratio * (5.10 + x_ratio * (-12.78 + x_ratio * (14.77 - 6.11 * x_ratio))))
# t_lows_thua = zeros(len(ICFs_thuan))
# t_lows_thua_err = zeros(len(ICFs_thuan))
#
# for i in range(len(objects)):
#     obj = objects[i]
#     temp_label = catalogue_df.loc[obj, 'T_low']
#     T_low_array[i] = catalogue_df.loc[obj, temp_label].nominal_value
#     T_low_err_array[i] = catalogue_df.loc[obj, temp_label].std_dev
#     t_lows_thua[i] = catalogue_df.loc[obj, temp_label].nominal_value
#     t_lows_thua_err[i] = catalogue_df.loc[obj, temp_label].std_dev
#
# dz.data_plot(T_low_array, unumpy.nominal_values(y_values), label=r'Argon $ICF(S^{3+})$', markerstyle='o',
#              x_error=T_low_err_array, y_error=unumpy.std_devs(y_values))
# dz.plot_text(unumpy.nominal_values(T_low_array), unumpy.nominal_values(y_values), text=quick_reference, x_pad=1.005,
#              y_pad=1.005, fontsize=18)
#
# # dz.data_plot(t_lows_thua, unumpy.nominal_values(ICFs_thuan), label = r'Oxygen $ICF(S^{3+})$ prediction (Thuan et al 1995)', color = '#009E73', markerstyle='^', x_error=t_lows_thua_err, y_error=unumpy.std_devs(ICFs_thuan))
#
# dz.data_plot(unumpy.nominal_values(x_IR_values), unumpy.nominal_values(y_IR_values), color=dz.colorVector['orangish'],
#              label=r'$ICF(S^{3+})$ from IR (Dors 2016)', markerstyle='x', x_error=unumpy.std_devs(x_IR_values),
#              y_error=unumpy.std_devs(y_IR_values))
# dz.plot_text(unumpy.nominal_values(x_IR_values), unumpy.nominal_values(y_IR_values), text=objectsIR, fontsize=18)
#
# # dz.data_plot(unumpy.nominal_values(x_values), unumpy.nominal_values(y_values), label= '', x_error=unumpy.std_devs(x_values), y_error=unumpy.std_devs(y_values))
#
# dz.FigWording(r'$T_{low} (K)$', r'$ICF(S^{+3})$', '', loc='best')
#
# # dz.display_fig()
# dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/ICF_S+3')