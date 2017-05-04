#!/usr/bin/env python

from dazer_methods import Dazer
from os.path import basename

def ImportDispersionVelocity(lineslog_frame):
    
    O3_5007_sigma       = lineslog_frame['sigma']['O3_5007A'] if 'O3_5007A' in lineslog_frame.index else None
    Hbeta_sigma         = lineslog_frame['sigma']['H1_4861A'] if 'H1_4861A' in lineslog_frame.index else None 
    Sigma               = None
    c_SI                = 300000.0
        
    if O3_5007_sigma >= 0:
        Sigma = O3_5007_sigma / 5007.0 * c_SI
    
    elif Hbeta_sigma >= 0:
        Sigma = Hbeta_sigma / 4861.0 * c_SI
        
    else:
        Sigma = 100
          
    return Sigma


#Declare data to treat
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'

#Define plot frame and colors
dz.FigConf()

#Default configuration file
dz.RootFolder       = '/home/vital/'
GridFileAddress     = dz.RootFolder + 'Starlight/Sl_Config_v1.txt'

#Reddening properties
R_v = 3.4
red_curve = 'G03'
cHbeta_type = 'cHbeta_reduc'

for i in range(len(catalogue_df.index)):
    
    print '-- Treating {} @ {}'.format(catalogue_df.iloc[i].name, AbundancesFileExtension)
    
    try:

        #Locate the objects
        objName             = catalogue_df.iloc[i].name
        
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        fits_file           = catalogue_df.iloc[i].reduction_fits
        lineslog_address    = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=AbundancesFileExtension)
        fits_name           = basename(fits_file)
            
        #Load object data
        lineslog_frame = dz.load_lineslog_frame(lineslog_address)
        wave, flux, header_0 = dz.get_spectra_data(fits_file)
    
        #Declare starlight files
        Grid_FileName                   = fits_name.replace('.fits', '.slGrid')
        Sl_OutputFolder                 = dz.RootFolder + 'Starlight/Output/'
        Sl_OutputFile                   = fits_name.replace('.fits', '.slOutput')
    
        cHbeta      = catalogue_df.loc[objName, cHbeta_type]
        flux_dered = dz.derreddening_spectrum(wave, flux, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
    
    
    
        #Define the maximum sigma for the fitting from the Hbeta line
        Sigma                           = ImportDispersionVelocity(lineslog_frame)
        UpperDispersionVelocity_Limit   =  str(round(Sigma, 1)) + '      [vd_upp (km/s)]     = upper allowed vd\n'
        dz.replace_line(GridFileAddress, 21, UpperDispersionVelocity_Limit)
    
        #Launch starlight
        print '--Initiating starlight for ', fits_name, Sigma
        dz.Starlight_Launcher(Grid_FileName, dz.RootFolder)
        print '--Starlight finished succesfully ended:', Sl_OutputFile 
        
        #Get stellar spectrum from starlight file
        Input_Wavelength, Input_Flux, Output_Flux, MaskPixels, ClippedPixels, FlagPixels, Parameters = dz.File_to_data(Sl_OutputFolder, Sl_OutputFile)
    
        #Export data to fits file
        stellar_cont_fits   = objName + '_StellarContinuum.fits'
        dz.Data_2_Fits(ouput_folder, stellar_cont_fits, header_0, Input_Wavelength, Output_Flux, NewKeyWord = ['STALIGHT', 'Basic Treatment'])
    
        #Plot the data
        dz.data_plot(wave, flux_dered, "obs de-red")
        dz.data_plot(Input_Wavelength, Input_Flux, "Input Spectra")
        dz.data_plot(Input_Wavelength, Output_Flux, "Stellar absorption")
        
        #Set titles and legend  
        PlotTitle = 'Object ' + objName + ' emission and stellar and spectra'
        dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)   
    
        mean_flux = Input_Flux.mean()
        dz.Axis.set_ylim(-0.05*mean_flux, 15*mean_flux)
        dz.Axis.set_xlim(3500, 5250)
            
        #Save plot      
        output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='StellarContinuum')
        dz.save_manager(output_pickle, save_pickle = True)
    
    except:
        dz.log_error(objName) 
                
print 'All data treated', dz.display_errors()
