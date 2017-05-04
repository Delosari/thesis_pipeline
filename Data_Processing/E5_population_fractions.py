#!/usr/bin/env python

from dazer_methods import Dazer
from uncertainties import ufloat
from numpy import log10
import matplotlib.ticker as mtick
import matplotlib.colors as colors

def Calculate_Total_Mass(CodeName, FileFolder, FileAddress, redshift):
        
    with open(FileAddress) as f:
        line                = f.readlines()[55].split()
        Mass_uncalibrated   = float(line[0])
    
    Huble_Constant  = ufloat(74.3,6.0)
    c               = 299792 #km/s 
    mpc_2_cm        = 3.086e15 

    distance        = redshift * c / Huble_Constant * mpc_2_cm

    Mass = Mass_uncalibrated * 1e17 * 4 * 3.1415 * distance * distance * (1 / 3.826e33)

    LogMass = log10(Mass.nominal_value)

    return LogMass

def light_fraction_plot(Light_fraction, CodeName, output_folder, script_code):
    
    #Generating light fraction plot
    for Histogram in Light_fraction:
        dz.Histogram_One(*Histogram)
 
    # Change the axis format to replicate the style of Dani Miralles
    dz.Axis.set_yscale('log')
    dz.Axis.set_ylim([0,100])
    dz.Axis.set_xlim([5.5,10.5])
    dz.Axis.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
 
    # Set titles and legend
    plot_Title  = 'Galaxy ' + CodeName + ' SSP synthesis ' + r'$log(M_{T})$ = ' + r'$'+str(round(LogMass,2))+'$'
    plot_xlabel = r'$log(Age)$'
    plot_ylabel = r'Light fraction % $(x_j)$'
     
    dz.FigWording(plot_xlabel, plot_ylabel, plot_Title, loc = 'lower right')
        
    #Save the data to the Catalogue folder
    output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=script_code, objCode=CodeName, ext='LightFraction')
    dz.save_manager(output_pickle, save_pickle = True)

    return

def mass_fraction_plot(mass_fraction, CodeName, output_folder, script_code):
    
    #Generating light fraction plot
    for Histogram in mass_fraction:
        dz.Histogram_One(*Histogram)
 
    # Change the axis format to replicate the style of Dani Miralles
    dz.Axis.set_yscale('log')
    dz.Axis.set_ylim([0,100])
    dz.Axis.set_xlim([5.5,10.5])
    dz.Axis.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
 
    # Set titles and legend
    plot_Title  = 'Galaxy ' + CodeName + ' SSP synthesis ' + r'$log(M_{T})$ = ' + r'$'+str(round(LogMass,2))+'$'
    plot_xlabel = r'$log(Age)$'
    plot_ylabel = r'Mass fraction % $(Mcor)$'
     
    dz.FigWording(plot_xlabel, plot_ylabel, plot_Title, loc = 'lower right')
        
    #Save the data to the Catalogue folder
    output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=script_code, objCode=CodeName, ext='MassFraction')
    dz.save_manager(output_pickle, save_pickle = True)
      
    return

#Declare objects

dz = Dazer()
script_code = dz.get_script_code()

#Define data type and location
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
Stellar_ext     = '_StellarContinuum.fits'
Sl_OutputFolder = '/home/vital/Starlight/Output/'

#Define plot frame and colors
dz.FigConf()
colorVector = {
            'dark blue':'#0072B2',
            'green':'#009E73', 
            'orangish':'#D55E00',
            'pink':'#CC79A7',
            'yellow':'#F0E442',
            'cyan':'#56B4E9',
            'olive':'#bcbd22',
            'grey':'#7f7f7f',
            'skin':'#FFB5B8',
            'iron':'#4c4c4c',
            'silver':'#cccccc',  
            }

list_colors = []
for color in colorVector:
    list_colors.append(colors.hex2color(colorVector[color])) 

#Loop through files
for i in range(len(catalogue_df.index)):
    
    print '-- Treating {}'.format(catalogue_df.iloc[i].name)
            
    #Locate the objects
    objName             = catalogue_df.iloc[i].name
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    fits_file           = catalogue_df.iloc[i].reduction_fits
     
    #Declare the ouput file from starlight
    Sl_OutputFile = objName + '_' + catalogue_dict['Datatype'] + ".slOutput"   
    
    LogMass = Calculate_Total_Mass(objName, ouput_folder, Sl_OutputFolder + Sl_OutputFile, catalogue_df.iloc[i].z_Blue)
        
    #Converting starlight population output into a series of histograms
    Light_fraction  = dz.CumulativeHistogram_One(Sl_OutputFolder, Sl_OutputFile, PlotType = 'Light_fraction', Color_Vector = list_colors)
    Mass_fraction   = dz.CumulativeHistogram_One(Sl_OutputFolder, Sl_OutputFile, PlotType = 'Mass_fraction', Color_Vector = list_colors)

    #Generating light fraction histogram
    light_fraction_plot(Light_fraction, objName, ouput_folder, script_code)

    #Generating light fraction histogram
    mass_fraction_plot(Mass_fraction, objName, ouput_folder, dz.ScriptCode[0] + str(int(dz.ScriptCode[1]) + 1))
        
#-----------------------------------------------------------------------------------------------------
print 'All data treated', dz.display_errors()




# #!/usr/bin/env python
# 
# from dazer_methods import Dazer
# from uncertainties import ufloat
# from numpy import log10
# import matplotlib.ticker as mtick
# import matplotlib.colors as colors
# 
# def Calculate_Total_Mass(CodeName, FileFolder, FileAddress, redshift):
#         
#     with open(FileAddress) as f:
#         line                = f.readlines()[55].split()
#         Mass_uncalibrated   = float(line[0])
#     
#     Huble_Constant  = ufloat(74.3,6.0)
#     c               = 299792 #km/s 
#     mpc_2_cm        = 3.086e15 
# 
#     distance        = redshift * c / Huble_Constant * mpc_2_cm
# 
#     Mass = Mass_uncalibrated * 1e17 * 4 * 3.1415 * distance * distance * (1 / 3.826e33)
# 
#     LogMass = log10(Mass.nominal_value)
# 
#     return LogMass
# 
# def light_fraction_plot(Light_fraction, CodeName, output_folder, script_code):
#     
#     #Generating light fraction plot
#     for Histogram in Light_fraction:
#         dz.Histogram_One(*Histogram)
#  
#     # Change the axis format to replicate the style of Dani Miralles
#     dz.Axis.set_yscale('log')
#     dz.Axis.set_ylim([0,100])
#     dz.Axis.set_xlim([5.5,10.5])
#     dz.Axis.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
#  
#     # Set titles and legend
#     plot_Title  = 'Galaxy ' + CodeName + ' SSP synthesis ' + r'$log(M_{T})$ = ' + r'$'+str(round(LogMass,2))+'$'
#     plot_xlabel = r'$log(Age)$'
#     plot_ylabel = r'Light fraction % $(x_j)$'
#      
#     dz.FigWording(plot_xlabel, plot_ylabel, plot_Title, loc = 'lower right')
#         
#     #Save the data to the Catalogue folder
#     output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=script_code, objCode=CodeName, ext='LightFraction')
#     dz.save_manager(output_pickle, save_pickle = True)
# 
#     return
# 
# def mass_fraction_plot(mass_fraction, CodeName, output_folder, script_code):
#     
#     #Generating light fraction plot
#     for Histogram in mass_fraction:
#         dz.Histogram_One(*Histogram)
#  
#     # Change the axis format to replicate the style of Dani Miralles
#     dz.Axis.set_yscale('log')
#     dz.Axis.set_ylim([0,100])
#     dz.Axis.set_xlim([5.5,10.5])
#     dz.Axis.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
#  
#     # Set titles and legend
#     plot_Title  = 'Galaxy ' + CodeName + ' SSP synthesis ' + r'$log(M_{T})$ = ' + r'$'+str(round(LogMass,2))+'$'
#     plot_xlabel = r'$log(Age)$'
#     plot_ylabel = r'Mass fraction % $(Mcor)$'
#      
#     dz.FigWording(plot_xlabel, plot_ylabel, plot_Title, loc = 'lower right')
#         
#     #Save the data to the Catalogue folder
#     output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=script_code, objCode=CodeName, ext='MassFraction')
#     dz.save_manager(output_pickle, save_pickle = True)
#       
#     return
# 
# #Declare objects
# 
# dz = Dazer()
# script_code = dz.get_script_code()
# 
# #Define data type and location
# Catalogue_Dic   = dz.import_catalogue()
# catalogue_dict  = dz.import_catalogue()
# catalogue_df    = dz.load_dataframe(catalogue_dict['dataframe'])
# Stellar_ext     = '_StellarContinuum.fits'
# Sl_OutputFolder = '/home/vital/Starlight/Output/'
# 
# #Define plot frame and colors
# dz.FigConf()
# colorVector = {
#             'dark blue':'#0072B2',
#             'green':'#009E73', 
#             'orangish':'#D55E00',
#             'pink':'#CC79A7',
#             'yellow':'#F0E442',
#             'cyan':'#56B4E9',
#             'olive':'#bcbd22',
#             'grey':'#7f7f7f',
#             'skin':'#FFB5B8',
#             'iron':'#4c4c4c',
#             'silver':'#cccccc',  
#             }
# 
# list_colors = []
# for color in colorVector:
#     list_colors.append(colors.hex2color(colorVector[color])) 
# 
# #Loop through files
# for i in range(len(catalogue_df.index)):
#     
#     print '-- Treating {}'.format(catalogue_df.iloc[i].name)
#     
#     try:
#         
#         #Locate the objects
#         objName             = catalogue_df.iloc[i].name
#         ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
#         fits_file           = catalogue_df.iloc[i].reduction_fits
#          
#         #Declare the ouput file from starlight
#         Sl_OutputFile = objName + '_' + Catalogue_Dic['Datatype'] + ".slOutput"   
#         
#         LogMass = Calculate_Total_Mass(objName, ouput_folder, Sl_OutputFolder + Sl_OutputFile, catalogue_df.iloc[i].z_Blue)
#             
#         #Converting starlight population output into a series of histograms
#         Light_fraction  = dz.CumulativeHistogram_One(Sl_OutputFolder, Sl_OutputFile, PlotType = 'Light_fraction', Color_Vector = list_colors)
#         Mass_fraction   = dz.CumulativeHistogram_One(Sl_OutputFolder, Sl_OutputFile, PlotType = 'Mass_fraction', Color_Vector = list_colors)
#     
#         #Generating light fraction histogram
#         light_fraction_plot(Light_fraction, objName, ouput_folder, script_code)
#     
#         #Generating light fraction histogram
#         mass_fraction_plot(Mass_fraction, objName, ouput_folder, dz.ScriptCode[0] + str(int(dz.ScriptCode[1]) + 1))
#      
#     except:
#         dz.log_error(objName) 
# 
# #-----------------------------------------------------------------------------------------------------
# print 'All data treated', dz.display_errors()


