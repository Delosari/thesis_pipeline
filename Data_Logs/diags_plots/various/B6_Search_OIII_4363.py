from numpy import array, median, searchsorted, mean,  max, where, ones
from dazer_methods import Dazer

def Emission_Threshold(LineLoc, TotalWavelen, TotalInten, BoxSize = 70):
    
    #Use this method to determine the box and location of the emission lines
    Bot                 = LineLoc - BoxSize
    Top                 = LineLoc + BoxSize
    
    indmin, indmax      = searchsorted(TotalWavelen, (Bot, Top))
    if indmax > (len(TotalWavelen)-1):
        indmax = len(TotalWavelen)-1
    
    PartialWavelength   = TotalWavelen[indmin:indmax]
    PartialIntensity    = TotalInten[indmin:indmax]
    
    Bot                 = LineLoc - 2
    Top                 = LineLoc + 2
    
    indmin, indmax      = searchsorted(PartialWavelength, (Bot, Top))
    
    LineHeight          = max(PartialIntensity[indmin:indmax])
    LineExpLoc          = median(PartialWavelength[where(PartialIntensity == LineHeight)])
          
    return PartialWavelength, PartialIntensity, LineHeight, LineExpLoc

#Create class object

dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Set figure format
dz.FigConf()

#Not sure what this is
dz.force_WD = True

#Loop through the objects
for i in range(len(catalogue_df.index)):

    #Object
    objName         = catalogue_df.iloc[i].name
    fits_file       = catalogue_df.iloc[i].reduction_fits
    ouput_folder    = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 

    print '-- Treating {} @ {}'.format(objName, fits_file)
      
    #Spectrum data
    wave, flux, header_0 = dz.get_spectra_data(fits_file)
    subwave, subflux, lineHeight, LineExpLoc = Emission_Threshold(4363.21, wave, flux)
    
    #Establish current line
    dz.Current_Label    = 'O2_7319A'
    dz.Current_Ion      = 'O2'
    dz.Current_TheoLoc  = 4363.21
    selections          = array([4349.10,4356.77,4360.31,4367.7,4394.3,4413.6 ])

    #Proceed to measure
    line_data = dz.measure_line(wave, flux, selections, lines_dataframe=None, store_data = False)
    
    #Plot Global component
    dz.data_plot(subwave, subflux, label='Spectrum', linestyle='step')
    dz.data_plot(line_data['x_resample'], line_data['y_resample'], 'Gaussian mixture', linewidth=2.0, color = dz.colorVector['yellow'])
    
#     #Plot individual components
#     for i in range(line_data['line_number']):
#         dz.data_plot(line_data['x_resample'], line_data['y_comps'][i], 'Components', linestyle = '--', color=dz.colorVector['orangish'], linewidth=1.0)
    
    #Plot peaks
    #dz.data_plot(line_data['peak_waves'], line_data['peak_Maxima'], 'Input values', markerstyle='o', color = dz.colorVector['pink'])

    dz.Axis.set_xlim([subwave[0],subwave[-1]])
    dz.Axis.set_ylim(median(subflux)/10, lineHeight*2)
    dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', r'Object {} [OII] 7300+ $\AA$'.format(objName))   
    
    #Plot output figures
    output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='OIII_region')
    dz.save_manager(output_pickle, save_pickle = True)

print 'Data treated'
