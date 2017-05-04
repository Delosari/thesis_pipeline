import math, ephem, pandas as pd
import astropy.units        as u
from numpy import empty, min, max, zeros, array
from astroquery.sdss                        import SDSS
from astroquery.alfalfa                     import Alfalfa
from collections                            import OrderedDict
from ManageFlow                             import DataToTreat
from CodeTools.PlottingManager              import myPickle
from uncertainties                          import ufloat
from Plotting_Libraries.dazer_plotter       import Plot_Conf
from astropy.coordinates                    import EarthLocation
from pytz                                   import timezone
from astroplan                              import Observer
from astropy.coordinates                    import SkyCoord
from astroplan                              import FixedTarget
from astropy.time                           import Time
from astroplan.plots                        import plot_airmass
import matplotlib.pyplot                    as plt
from astropy                                import coordinates as coords


favoured_objects = ['72', '44', 'IZw18_b', '20', '43', '67', '59', '65', '48', '51', '62', '39', '66', '54', 'Mrk475']

#Generate dazer object
pv = myPickle()
dz = Plot_Conf()

#Define figure format
dz.FigConf(n_colors = 2)
cmap = dz.cmap_pallete()

#Define operation
Catalogue_Dic   = DataToTreat('WHT_CandiatesObjects_2016A')
Pattern         = '_log'

FilesList = pv.Folder_Explorer(Pattern,  Catalogue_Dic['Obj_Folder'], CheckComputer=False)
Hbeta_values, Flux_values, names, sn_values, z_values = [], [], [], [], []
g_mags, r_mags = [], []
Declination_values  = []

for i in range(len(FilesList)):

    #Get the frame row
    CodeName, FileName, FileFolder = pv.Analyze_Address(FilesList[i])
    
    
    #Load the observational data
    Hbeta_Flux  = pv.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_Flux_Hbeta', Assumption = 'float')
    Hbeta_Ew    = pv.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_Eqw_Hbeta', Assumption = 'float')
    SN_median   = pv.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_SNmedian', Assumption = 'float')
    z_SDSS      = pv.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_z', Assumption = 'float')
    g_mag       = pv.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_g_magModel', Assumption = 'float')
    r_mag       = pv.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_r_magModel', Assumption = 'float')
    Declination = pv.GetParameter_ObjLog(CodeName, FileFolder, 'SDSS_DEC_deg', Assumption = 'float')
    
    if (Hbeta_Flux and Hbeta_Ew) != None:
        print 'Going for', FileName, Hbeta_Ew
        Hbeta_values.append(Hbeta_Ew.nominal_value)
        Flux_values.append(Hbeta_Flux.nominal_value)
        names.append(CodeName.replace('_',''))
        sn_values.append(SN_median)
        Declination_values.append(Declination)
        
        if z_SDSS != None:
            z_values.append(float(z_SDSS))
            g_mags.append(g_mag)
            r_mags.append(r_mag)
        else:
            z_values.append(0)
            g_mags.append(12)
            r_mags.append(12)
            



#------Plot magnitudes

x_values    = array(r_mags)
y_values    = array(g_mags)

dz.Axis.set_xlim(12 , 22)
dz.Axis.set_ylim(12 , 22)

dz.data_plot(x_values, y_values, color = dz.ColorVector[2][0], label='Candidate objects', markerstyle='o')
dz.text_plot(names, x_values, y_values, color = dz.ColorVector[1], fontsize = 11)
dz.Axis.axhline(y = 20, color=dz.ColorVector[2][1])
dz.Axis.axvline(x = 19, color=dz.ColorVector[2][1])

Title   = r'Sample SDSS model magnitudes' 
Title_X = r'r $(model)$'
Title_Y = r'g $(model)$'
dz.FigWording(Title_X, Title_Y, Title, legend_loc='best')
dz.savefig(output_address = Catalogue_Dic['Data_Folder'] + 'g_r_magnitudes', reset_fig = True)


#------Plot magnitudes

x_values    = array(Hbeta_values)
y_values    = array(Declination_values)


dz.data_plot(x_values, y_values, color = dz.ColorVector[2][0], label='Candidate objects', markerstyle='o')
dz.text_plot(names, x_values, y_values, color = dz.ColorVector[1], fontsize = 11)

Title   = r'Sample declination versus equivalent width' 
Title_X = r'$Eqw$ $(H\beta)$'
Title_Y = r'dec $(deg)$'
dz.FigWording(Title_X, Title_Y, Title, legend_loc='best')
dz.savefig(output_address = Catalogue_Dic['Data_Folder'] + 'dec_eqw', reset_fig = True)

#------Plot Flux vs Eqw
            
x_values    = array(Hbeta_values)
y_values    = array(Flux_values)
sn_values   = array(sn_values)
z_values    = array(z_values)

dz.data_plot(x_values, y_values, color = sn_values, label='Candidate objects', markerstyle='o', cmap=cmap, markersize=100)
dz.text_plot(names, x_values, y_values, color = dz.ColorVector[1])

#if CodeName in favoured_objects:
# dz.data_plot(Hbeta_Ew.nominal_value, Hbeta_Flux.nominal_value, color = 'grey', label='Candidate objects', markerstyle='o', markersize=400)

dz.Axis.set_ylim(min(y_values)*0.9 , max(y_values)*1.1)

Title   = r'$H(\beta)$ flux versus its equivalent width' 
Title_X = r'EqW $(\AA)$'
Title_Y = r'$F(H\beta)$'
dz.FigWording(Title_X, Title_Y, Title, legend_loc='best', cb_title = 'S/N (Median value)')
dz.savefig(output_address = Catalogue_Dic['Data_Folder'] + 'FHbeta_EwHbeta', reset_fig = True)

#------Table with the redshifts----------------

pv.RedShifted_linesog_header()

lines_wavelength = OrderedDict()

lines_wavelength['OIII4363']    = 4363.0
lines_wavelength['OIII5007']    = 5007.0
lines_wavelength['Halpha']      = 6563.0
lines_wavelength['HeI6678']     = 6678.0
lines_wavelength['SIIII9531']   = 9531.0   

#Generate object row of data 
data_keys   = pv.header_dict.keys()
Object_row  = ['None'] * len(pv.header_dict)

#Establish table format
pv.latex_header(table_address = Catalogue_Dic['Data_Folder'] + 'Refence_shifted_lines')

Hbeta_array = array(Hbeta_values)

Sorted_indeces_Ew = Hbeta_array.argsort()[::-1]

for i in Sorted_indeces_Ew:

    Object_row[0] = names[i]
    Object_row[1] = pv.format_for_table(z_values[i], rounddig = 5)
    Object_row[2] = pv.format_for_table(Hbeta_array[i], rounddig = 3)
        
    print 'Before', Object_row
    for j in range(len(lines_wavelength.keys())):
        key = lines_wavelength.keys()[j]
        value = lines_wavelength[key] * (1.0 + z_values[i])
        
        if key == 'OIII4363':
            color = pv.color_evaluator_uplimits(value, 4250, evaluation_pattern = [200.0, 100.0])
            Object_row[j + 3] = r'\textcolor{{{color}}}{{{value}}}'.format(color = color, value = pv.format_for_table(value, 3))
            

        elif key == 'HeI6678':
            color = pv.color_evaluator_lowlimits(value, 7250, evaluation_pattern = [200.0, 100.0])
            Object_row[j + 3] = r'\textcolor{{{color}}}{{{value}}}'.format(color = color, value = pv.format_for_table(value, 3))
            
        elif key == 'SIIII9531':
            color = pv.color_evaluator_lowlimits(value, 9800, evaluation_pattern = [200.0, 100.0])
            Object_row[j + 3] = r'\textcolor{{{color}}}{{{value}}}'.format(color = color, value = pv.format_for_table(value, 3))
            
        else:
            Object_row[j + 3] = pv.format_for_table(value, rounddig = 3)
    
    print 'After', Object_row
           
    #Insert the row
    pv.table.add_row(Object_row, escape=False)
 
    Object_row  = ['None'] * len(pv.header_dict)
 
#Adding a double line for different section
pv.table.add_hline()

#Closing the table
pv.table_footer()


print 'Data treated'




















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


