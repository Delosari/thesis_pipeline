#!/usr/bin/env python
 
from dazer_methods import Dazer
from uncertainties import ufloat
from numpy import log10, trapz
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
 
def light_fraction_plot(Sl_OutputFolder, Sl_OutputFile, objName, parameter, ouput_folder, script_code):
    
#     #Load nebular and stellar spectra
#     Wave_N, Int_N, ExtraData_N = dz.get_spectra_data(ouput_folder + objName + '_NebularContinuum.fits')
#     Wave_S, Int_S, ExtraData_S = dz.get_spectra_data(ouput_folder + objName + '_StellarContinuum.fits')    
#     
#     idx_neb = (Wave_N > 3550) & (Wave_N < 6995)
#     idx_ste = (Wave_S > 3550) & (Wave_S < 6995)
#     
#     area_neb        = trapz(Int_N[idx_neb], Wave_N[idx_neb])
#     area_stellar    = trapz(Int_S[idx_ste], Wave_S[idx_ste])
#     
#     ratio_flux      = area_neb/area_stellar * 100
    
    #Generate the data from the starlight file
    dz.populations_histogram(Sl_OutputFolder, Sl_OutputFile, parameter)
    
#     dz.Axis.axhline(ratio_flux, label = 'Nebular to stellar flux fraction', linestyle='--', color='#D55E00')
    
    # Change the axis format to replicate the style of Dani Miralles
    dz.Axis.set_yscale('log')
    dz.Axis.set_ylim([1,100])
    dz.Axis.set_xlim([5.5,10.5])
    dz.Axis.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
  
    # Set titles and legend
    plot_Title  = 'Galaxy ' + objName + ' SSP synthesis light fraction' 
    plot_xlabel = r'$log(Age)$'
    plot_ylabel = r'Light fraction %'
      
    dz.FigWording(plot_xlabel, plot_ylabel, plot_Title, loc = (0.57,0.50), sort_legend=True)       
    
    #Save the data to the Catalogue folder
    output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=script_code, objCode=objName, ext='LightFraction')
    dz.save_manager(output_pickle, save_pickle = True)
 
    return
 
def mass_fraction_plot(Sl_OutputFolder, Sl_OutputFile, parameter, ouput_folder, redshift, script_code):
     
    #Generate the data from the starlight file
    dz.populations_histogram(Sl_OutputFolder, Sl_OutputFile, parameter)
    
    #Galaxy mass
    LogMass = Calculate_Total_Mass(objName, ouput_folder, Sl_OutputFolder + Sl_OutputFile, redshift)
    
    # Change the axis format to replicate the style of Dani Miralles
    dz.Axis.set_yscale('log')
    dz.Axis.set_ylim([0,100])
    dz.Axis.set_xlim([5.5,10.5])
    dz.Axis.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
  
    # Set titles and legend
    plot_Title  = 'Galaxy ' + objName + ' SSP synthesis ' + r'$log(M_{T})$ = ' + r'$'+str(round(LogMass,2))+'$'
    plot_xlabel = r'$log(Age)$'
    plot_ylabel = r'Mass fraction %$'
      
    dz.FigWording(plot_xlabel, plot_ylabel, plot_Title, loc = 'best', sort_legend=True)
         
    #Save the data to the Catalogue folder
    output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=script_code, objCode=objName, ext='MassFraction')
    dz.save_manager(output_pickle, save_pickle = True)
       
    return
 
#Declare objects
 
dz = Dazer()
script_code = dz.get_script_code()
 
#Define data type and location
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
Sl_OutputFolder = '/home/vital/Starlight/Output/'
 
#Define plot frame and colors
size_dict = {'axes.labelsize':20, 'legend.framealpha':None, 'legend.fontsize':17, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':18, 'ytick.labelsize':18}
dz.FigConf(plotSize = size_dict)

#Loop through files
for i in range(len(catalogue_df.index)):
     
    print '-- Treating {}'.format(catalogue_df.iloc[i].name)
             
    #Locate the objects
    objName             = catalogue_df.iloc[i].name
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    fits_file           = catalogue_df.iloc[i].reduction_fits
    redshift            = catalogue_df.iloc[i].z_Blue
          
    #Declare the ouput file from starlight
    Sl_OutputFile = objName + '_' + catalogue_dict['Datatype'] + ".slOutput" + '_emision'
    
    light_fraction_plot(Sl_OutputFolder, Sl_OutputFile, objName, 'Light_fraction', ouput_folder, script_code)
    
    mass_fraction_plot(Sl_OutputFolder, Sl_OutputFile, 'Mass_fraction', ouput_folder, redshift, dz.ScriptCode[0] + str(int(dz.ScriptCode[1]) + 1))
                       
#-----------------------------------------------------------------------------------------------------
print 'All data treated', dz.display_errors()