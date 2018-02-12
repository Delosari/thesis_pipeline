from dazer_methods  import Dazer
from numpy          import nanmean, nanstd, mean, nan as np_nan
from uncertainties  import ufloat, unumpy, umath
import pandas as pd
 
#Generate dazer object
dz = Dazer()

#Declare figure format
size_dict = {'figure.figsize':(14,6), 'axes.labelsize':20, 'legend.fontsize':20, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':20, 'ytick.labelsize':20}
dz.FigConf(plotSize = size_dict)

#Declare data location
folder_data       = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/Grid_data_vital/'
file_name_list_S  = ['TGrid_Mass100000.0_age5.48_zStar-2.1_zGas0.008.ele_S','TGrid_Mass200000.0_age5.48_zStar-2.1_zGas0.008.ele_S']
file_name_list_O  = ['TGrid_Mass100000.0_age5.48_zStar-2.1_zGas0.008.ele_O', 'TGrid_Mass200000.0_age5.48_zStar-2.1_zGas0.008.ele_O']
z_list            = ['100000', '200000']
ions_list_S       = ['S+', 'S+2', 'S+3']
ions_labels_S     = [r'$S^{+}$', r'$S^{2+}$', r'$S^{3+}$']
ions_list_O       = ['O+', 'O+2']
ions_labels_O     = [r'$O^{+}$', r'$O^{2+}$']
labels_coords_S   = [[(1.60e18,0.98), (2.35e18,0.98)],
                   [(1.0e18,0.72), (1.77e18,0.72)],
                   [(0.75e18,0.000005), (2.0e18,0.015)]]
labels_coords_O   = [[(1.55e18,0.5), (2.3e18,0.5)],
                   [(1.03e18,0.6),(1.8e18,0.6)]]
ions_colors_S   = ['tab:orange', 'tab:red', 'tab:brown']
ions_colors_O   = ['tab:blue', 'tab:green']

line_type       = ['--', '-']


for i in range(len(file_name_list_S)):
    
    file_name = file_name_list_S[i]
    
    elemIon_df = pd.read_csv(folder_data + file_name, sep = '\t')
    
    for j in range(len(ions_list_S)):
        
        ion         = ions_list_S[j]
        radious     = elemIon_df['#depth'].values
        ion_frac    = elemIon_df[ion].values
        label       = r'{0:1.1e} $M_\odot$'.format(float(z_list[i]))
        dz.data_plot(radious/1e19, ion_frac, color=ions_colors_S[j], linestyle=line_type[i], label = r'Cluster mass {}'.format(label), linewidth = 2)
        dz.plot_text(labels_coords_S[j][i][0]/1e19, labels_coords_S[j][i][1], text = ions_labels_S[j], color = ions_colors_S[j], fontsize = 20, axis_plot=None)

    file_name = file_name_list_O[i]
    
    elemIon_df = pd.read_csv(folder_data + file_name, sep = '\t')

    for j in range(len(ions_list_O)):
        
        ion         = ions_list_O[j]
        radious     = elemIon_df['#depth'].values
        ion_frac    = elemIon_df[ion].values
        label       = r'{0:1.1e} $M_\odot$'.format(float(z_list[i]))
        dz.data_plot(radious/1e19, ion_frac, color=ions_colors_O[j], linestyle=line_type[i], label = r'Cluster mass {}'.format(label))
        dz.plot_text(labels_coords_O[j][i][0]/1e19, labels_coords_O[j][i][1], text = ions_labels_O[j], color = ions_colors_O[j], fontsize = 20, axis_plot=None)
        
dz.FigWording(r'$R_{19}$ $(10^{19}cm)$', r'$X(A^{+i})$', '', ncols_leg=1)

leg = dz.Axis.get_legend()
leg.legendHandles[0].set_color('black')
leg.legendHandles[1].set_color('black')

#dz.display_fig()
dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/SulfurIonization_fraction_vs_cloudThickness')
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Stasinska conference/SulfurIonization_fraction_vs_cloudThickness')

# #Load catalogue dataframe
# catalogue_dict  = dz.import_catalogue()
# catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
# 
# #Define plot frame and colors
# size_dict = {'axes.labelsize':24, 'legend.fontsize':24, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':22, 'ytick.labelsize':22}
# dz.FigConf(plotSize = size_dict)
# 
# dz.quick_indexing(catalogue_df)
# idcs = (pd.notnull(catalogue_df.OI_HI_emis2nd)) & (pd.notnull(catalogue_df.NI_HI_emis2nd)) & (pd.notnull(catalogue_df.HeII_HII_from_O_emis2nd)) & (catalogue_df.quick_index.notnull()) & (~catalogue_df.index.isin(['SHOC593']))
# 
# #Prepare data
# O_values  = catalogue_df.loc[idcs].OI_HI_emis2nd.values 
# N_values  = catalogue_df.loc[idcs].NI_HI_emis2nd.values
# HeII_HI   = catalogue_df.loc[idcs].HeII_HII_from_O_emis2nd.values 
# objects   = catalogue_df.loc[idcs].quick_index.values
# 
# N_O_ratio = N_values/O_values
# 
# dz.data_plot(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), label = '', markerstyle='o', x_error=unumpy.std_devs(HeII_HI), y_error=unumpy.std_devs(N_O_ratio))
# dz.plot_text(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), text=objects, x_pad=1.005, y_pad=1.01)
# 
# dz.FigWording(r'y', r'$N/O$', '')
# # dz.display_fig()
# dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/NO_to_y')






# from dazer_methods import Dazer
# from numpy import nanmean, nanstd, mean, nan as np_nan
# from uncertainties import ufloat, unumpy, umath
# import pandas as pd
#
# # Generate dazer object
# dz = Dazer()
#
# # Declare figure format
# size_dict = {'figure.figsize': (10, 10), 'axes.labelsize': 24, 'legend.fontsize': 14, 'font.family': 'Times New Roman',
#              'mathtext.default': 'regular', 'xtick.labelsize': 22, 'ytick.labelsize': 22}
# dz.FigConf(plotSize=size_dict)
#
# # Declare data location
# folder_data = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/Grid_data_vital/'
# file_name_list_S = [
#     'TGrid_Mass100000.0_age5.48_zStar-2.1_zGas0.008.ele_S']  # , 'TGrid_Mass100000.0_age5.48_zStar-2.1_zGas0.008.ele_S']
# file_name_list_O = [
#     'TGrid_Mass100000.0_age5.48_zStar-2.1_zGas0.008.ele_O']  # , 'TGrid_Mass100000.0_age5.48_zStar-2.1_zGas0.008.ele_O']
# z_list = ['200000', '100000']
# ions_list_S = ['S+', 'S+2', 'S+3']
# ions_labels_S = [r'$S^{+}$', r'$S^{2+}$', r'$S^{3+}$']
# ions_list_O = ['O+', 'O+2']
# ions_labels_O = [r'$O^{+}$', r'$O^{2+}$']
# labels_coords_S = [[(1.65e18, 1.0),
#                     (2.4e18, 1.0)],
#                    [(1.0e18, 0.75),
#                     (1.77e18, 0.75)],
#                    [(1.2e18, 0.015),
#                     (2.0e18, 0.015)]]
# labels_coords_O = [[(1.55e18, 0.5),
#                     (2.3e18, 0.5)],
#                    [(1.03e18, 0.6),
#                     (1.8e18, 0.6)]]
# ions_colors_S = ['tab:orange', 'tab:red', 'tab:brown']
# ions_colors_O = ['tab:blue', 'tab:green']
#
# line_type = ['-', '--']
#
# for i in range(len(file_name_list_S)):
#
#     file_name = file_name_list_S[i]
#
#     elemIon_df = pd.read_csv(folder_data + file_name, sep='\t')
#
#     for j in range(len(ions_list_S)):
#         ion = ions_list_S[j]
#         radious = elemIon_df['#depth'].values
#         ion_frac = elemIon_df[ion].values
#         label = r'{0:1.1e} $M_\odot$'.format(float(z_list[i]))
#         dz.data_plot(radious / 1e19, ion_frac, color=ions_colors_S[j], linestyle=line_type[i],
#                      label=r'Cluster mass {}'.format(label), linewidth=3)
#         dz.plot_text(labels_coords_S[j][i][0] / 1e19, labels_coords_S[j][i][1], text=ions_labels_S[j],
#                      color=ions_colors_S[j], fontsize=17, axis_plot=None)
#
#     file_name = file_name_list_O[i]
#
#     elemIon_df = pd.read_csv(folder_data + file_name, sep='\t')
#
#     for j in range(len(ions_list_O)):
#         ion = ions_list_O[j]
#         radious = elemIon_df['#depth'].values
#         ion_frac = elemIon_df[ion].values
#         label = r'{0:1.1e} $M_\odot$'.format(float(z_list[i]))
#         dz.data_plot(radious / 1e19, ion_frac, color=ions_colors_O[j], linestyle=line_type[i],
#                      label=r'Cluster mass {}'.format(label))
#         dz.plot_text(labels_coords_O[j][i][0] / 1e19, labels_coords_O[j][i][1], text=ions_labels_O[j],
#                      color=ions_colors_O[j], fontsize=17, axis_plot=None)
#
# dz.FigWording(r'$R_{19}$ $(10^{19}cm)$', r'$X(A^{+i})$', '', ncols_leg=1)
#
# leg = dz.Axis.get_legend()
# leg.legendHandles[0].set_color('black')
# # leg.legendHandles[1].set_color('black')
#
# # dz.display_fig()
# # dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/SulfurIonization_fraction_vs_cloudThickness')
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Stasinska conference/SulfurIonization_fraction_vs_cloudThickness')
#
# # #Load catalogue dataframe
# # catalogue_dict  = dz.import_catalogue()
# # catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
# #
# # #Define plot frame and colors
# # size_dict = {'axes.labelsize':24, 'legend.fontsize':24, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':22, 'ytick.labelsize':22}
# # dz.FigConf(plotSize = size_dict)
# #
# # dz.quick_indexing(catalogue_df)
# # idcs = (pd.notnull(catalogue_df.OI_HI_emis2nd)) & (pd.notnull(catalogue_df.NI_HI_emis2nd)) & (pd.notnull(catalogue_df.HeII_HII_from_O_emis2nd)) & (catalogue_df.quick_index.notnull()) & (~catalogue_df.index.isin(['SHOC593']))
# #
# # #Prepare data
# # O_values  = catalogue_df.loc[idcs].OI_HI_emis2nd.values
# # N_values  = catalogue_df.loc[idcs].NI_HI_emis2nd.values
# # HeII_HI   = catalogue_df.loc[idcs].HeII_HII_from_O_emis2nd.values
# # objects   = catalogue_df.loc[idcs].quick_index.values
# #
# # N_O_ratio = N_values/O_values
# #
# # dz.data_plot(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), label = '', markerstyle='o', x_error=unumpy.std_devs(HeII_HI), y_error=unumpy.std_devs(N_O_ratio))
# # dz.plot_text(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), text=objects, x_pad=1.005, y_pad=1.01)
# #
# # dz.FigWording(r'y', r'$N/O$', '')
# # # dz.display_fig()
# # dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/NO_to_y')