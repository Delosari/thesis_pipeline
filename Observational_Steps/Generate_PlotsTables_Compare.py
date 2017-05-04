# import math, ephem, pandas as pd
# import astropy.units        as u
# from numpy import empty, min, max, zeros, array
# from astroquery.sdss                        import SDSS
# from astroquery.alfalfa                     import Alfalfa
# from collections                            import OrderedDict
# from ManageFlow                             import DataToTreat
# from CodeTools.PlottingManager              import myPickle
# from uncertainties                          import ufloat
# from Plotting_Libraries.dazer_plotter       import Plot_Conf
# from astropy.coordinates                    import EarthLocation
# from pytz                                   import timezone
# from astroplan                              import Observer
# from astropy.coordinates                    import SkyCoord
# from astroplan                              import FixedTarget
# from astropy.time                           import Time
# from astroplan.plots                        import plot_airmass
# import matplotlib.pyplot                    as plt
# from astropy                                import coordinates as coords

from dazer_methods import Dazer
from numpy import empty, min, max, zeros, array
# from collections                            import OrderedDict
# from ManageFlow                             import DataToTreat
# from CodeTools.PlottingManager              import myPickle
# from Plotting_Libraries.dazer_plotter       import Plot_Conf
# from astropy.coordinates                    import EarthLocation
# from astropy.coordinates                    import SkyCoord
# from astropy.time                           import Time

# favoured_objects = ['72', '60', '61', '12', '29', '36', 'Mar1987', 'Mar2232', 'Mar2474', 'Mar88', 'Mar1315', 'Mar1390', 'Mar652', 'Mar2018', 'Mar1715', 'Mar2260', 'Mar1342', 'Mar87']

favoured_objects = ['02', '03', '05', '09', 'Mar2232']

#Generate dazer object
dz = Dazer()

#Define figure format
dz.FigConf(n_colors = 2)
cmap = dz.cmap_pallete()

#Define operation
Catalogue_Dic   = dz.import_catalogue()
Pattern         = '_log'

FilesList = dz.Folder_Explorer(Pattern,  Catalogue_Dic['Obj_Folder'], CheckComputer=False)
Hbeta_values, Flux_values, names, sn_values, z_values = [], [], [], [], []
g_mags, r_mags = [], []
Declination_values  = []

for i in range(len(FilesList)):

    #Get the frame row
    CodeName, FileName, FileFolder = dz.Analyze_Address(FilesList[i], verbose=False)
    
    #Load the observational data
    Hbeta_Flux  = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_Flux_Hbeta', Assumption = 'float')
    Hbeta_Ew    = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_Eqw_Hbeta', Assumption = 'float')
    SN_median   = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_SNmedian', Assumption = 'float')
    z_SDSS      = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_z', Assumption = 'float')
    g_mag       = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_g_magModel', Assumption = 'float')
    r_mag       = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_r_magModel', Assumption = 'float')
    Ra          = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_RA_deg', Assumption = 'float')
    Declination = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_DEC_deg', Assumption = 'float')
    mjd         = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_MJD', Assumption = 'float')
    fiberid     = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_Fiber', Assumption = 'float')
    plate       = dz.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_Plate', Assumption = 'float')
        
    if (Hbeta_Flux and Hbeta_Ew) != None:

        if CodeName in favoured_objects:
  
            website = "http://dr12.sdss3.org/spectrumDetail?mjd={mjd}&fiber={fiber}&plateid={plateid}".format(mjd = int(mjd), fiber = int(fiberid), plateid = int(plate))
        
#             if CodeName in favoured_objects:
#                 print '\n--', 'Object', CodeName
#                 print website
            print '['+CodeName+']', Ra, Declination, website
  
            
            Hbeta_values.append(Hbeta_Ew.nominal_value)
            Flux_values.append(Hbeta_Flux.nominal_value)
            names.append(CodeName.replace('_',''))
            sn_values.append(SN_median)
            Declination_values.append(Declination)
            
#             print CodeName, Hbeta_Flux.nominal_value
#             print website
            
#             if CodeName in ['Mar2260', 'Mar1342', 'Mar2191', 'Mar1318', 'Mar2071', 'Mar1987']:
#             
#                 print '['+CodeName+']', '; sloan', '; ' + str(mjd), '; ' + str(plate), '; ' + str(fiberid) , '; none;', '; none'
            
            if z_SDSS != None:
                z_values.append(float(z_SDSS))
                g_mags.append(g_mag)
                r_mags.append(r_mag)
            else:
                z_values.append(0)
                g_mags.append(12)
                r_mags.append(12)
            



#------Plot magnitudes
 
# x_values    = array(r_mags)
# y_values    = array(g_mags)
#  
# dz.Axis.set_xlim(12 , 22)
# dz.Axis.set_ylim(12 , 22)
#  
# dz.data_plot(x_values, y_values, color = dz.ColorVector[2][0], label='Candidate objects', markerstyle='o')
# dz.text_plot(names, x_values, y_values, color = dz.ColorVector[1], fontsize = 11)
# dz.Axis.axhline(y = 20, color=dz.ColorVector[2][1])
# dz.Axis.axvline(x = 19, color=dz.ColorVector[2][1])
#  
# Title   = r'Sample SDSS model magnitudes' 
# Title_X = r'r $(model)$'
# Title_Y = r'g $(model)$'
# dz.FigWording(Title_X, Title_Y, Title, legend_loc='best')
# dz.display_fig()
# dz.savefig(output_address = Catalogue_Dic['Data_Folder'] + 'g_r_magnitudes_M', reset_fig = True)
# 
# 
#------Plot magnitudes
 
x_values    = array(Hbeta_values)
y_values    = array(Declination_values)
 
 
dz.data_plot(x_values, y_values, color = dz.ColorVector[2][0], label='Candidate objects', markerstyle='o')
dz.text_plot( x_values, y_values,  names, color = dz.ColorVector[1], fontsize = 11)
 
Title   = r'Sample declination versus equivalent width' 
Title_X = r'$Eqw$ $(H\beta)$'
Title_Y = r'dec $(deg)$'
dz.FigWording(Title_X, Title_Y, Title, legend_loc='best')
# dz.display_fig()
dz.savefig(output_address = Catalogue_Dic['Folder'] + 'dec_eqw_M', reset_fig = True)

# print 'donde va esto',  Catalogue_Dic['Folder'] + 'dec_eqw_M'

#------Plot Flux vs Eqw
             
x_values    = array(Hbeta_values)
y_values    = array(Flux_values)
sn_values   = array(sn_values)
z_values    = array(z_values)
 
dz.data_plot(x_values, y_values, color = sn_values, label='Candidate objects', markerstyle='o', cmap=cmap, markersize=100)
dz.text_plot(x_values, y_values, names, color = dz.ColorVector[1])
 
#if CodeName in favoured_objects:
# dz.data_plot(Hbeta_Ew.nominal_value, Hbeta_Flux.nominal_value, color = 'grey', label='Candidate objects', markerstyle='o', markersize=400)
 
dz.Axis.set_ylim(min(y_values)*0.9 , max(y_values)*1.1)
 
Title   = r'$H(\beta)$ flux versus its equivalent width' 
Title_X = r'EqW $(\AA)$'
Title_Y = r'$F(H\beta)$'
dz.FigWording(Title_X, Title_Y, Title, legend_loc='best', cb_title = 'S/N (Median value)')
dz.display_fig()
dz.savefig(output_address = Catalogue_Dic['Folder'] + 'FHbeta_EwHbeta_M', reset_fig = True)

# #------Table with the redshifts----------------
# 
# pv.RedShifted_linesog_header()
# 
# lines_wavelength = OrderedDict()
# 
# lines_wavelength['OIII4363']    = 4363.0
# lines_wavelength['OIII5007']    = 5007.0
# lines_wavelength['Halpha']      = 6563.0
# lines_wavelength['HeI6678']     = 6678.0
# lines_wavelength['SIIII9531']   = 9531.0   
# 
# #Generate object row of data 
# data_keys   = pv.header_dict.keys()
# Object_row  = ['None'] * len(pv.header_dict)
# 
# #Establish table format
# pv.latex_header(table_address = Catalogue_Dic['Data_Folder'] + 'Refence_shifted_lines')
# 
# Hbeta_array = array(Hbeta_values)
# 
# Sorted_indeces_Ew = Hbeta_array.argsort()[::-1]
# 
# for i in Sorted_indeces_Ew:
# 
#     Object_row[0] = names[i]
#     Object_row[1] = pv.format_for_table(z_values[i], rounddig = 5)
#     Object_row[2] = pv.format_for_table(Hbeta_array[i], rounddig = 3)
#         
#     for j in range(len(lines_wavelength.keys())):
#         key = lines_wavelength.keys()[j]
#         value = lines_wavelength[key] * (1.0 + z_values[i])
#         
#         if key == 'OIII4363':
#             color = pv.color_evaluator_uplimits(value, 4250, evaluation_pattern = [200.0, 100.0])
#             Object_row[j + 3] = r'\textcolor{{{color}}}{{{value}}}'.format(color = color, value = pv.format_for_table(value, 3))
#             
# 
#         elif key == 'HeI6678':
#             color = pv.color_evaluator_lowlimits(value, 7250, evaluation_pattern = [200.0, 100.0])
#             Object_row[j + 3] = r'\textcolor{{{color}}}{{{value}}}'.format(color = color, value = pv.format_for_table(value, 3))
#             
#         elif key == 'SIIII9531':
#             color = pv.color_evaluator_lowlimits(value, 9800, evaluation_pattern = [200.0, 100.0])
#             Object_row[j + 3] = r'\textcolor{{{color}}}{{{value}}}'.format(color = color, value = pv.format_for_table(value, 3))
#             
#         else:
#             Object_row[j + 3] = pv.format_for_table(value, rounddig = 3)
#     
#            
#     #Insert the row
#     pv.table.add_row(Object_row, escape=False)
#  
#     Object_row  = ['None'] * len(pv.header_dict)
#  
# #Adding a double line for different section
# pv.table.add_hline()
# 
# #Closing the table
# pv.table_footer()
# 
# 
# print 'Data treated'




















# chararray(['Ly_alpha', 'N_V 1240', 'C_IV 1549', 'He_II 1640', 'C_III] 1908',
#        'Mg_II 2799', '[O_II] 3725', '[O_II] 3727', '[Ne_III] 3868',
#        'H_epsilon', '[Ne_III] 3970', 'H_delta', 'H_gamma', '[O_III] 4363',
#        'He_II 4685', 'H_beta', '[O_III] 4959', '[O_III] 5007',
#        'He_II 5411', '[O_I] 5577', '[O_I] 6300', '[S_III] 6312',
#        '[O_I] 6363', '[N_II] 6548', 'H_alpha', '[N_II] 6583',
#        '[S_II] 6716', '[S_II] 6730', '[Ar_III] 7135'])


# ['PLATE',
#  'MJD',
#  'FIBERID',
#  'LINENAME',
#  'LINEWAVE',
#  'LINEZ',
#  'LINEZ_ERR',
#  'LINESIGMA',
#  'LINESIGMA_ERR',
#  'LINEAREA',
#  'LINEAREA_ERR',
#  'LINEEW',
#  'LINEEW_ERR',
#  'LINECONTLEVEL',
#  'LINECONTLEVEL_ERR',
#  'LINENPIXLEFT',
#  'LINENPIXRIGHT',
#  'LINEDOF',
#  'LINECHI2']


