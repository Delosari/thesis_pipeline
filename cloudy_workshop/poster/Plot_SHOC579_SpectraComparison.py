#!/usr/bin/env python
from dazer_methods import Dazer
from numpy import linspace, zeros, hstack, array
from scipy.interpolate import interp1d
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes

#Declare code classes
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
cHbeta_type             = 'cHbeta_reduc'
nebular_exten           = '_NebularContinuum.fits'
Stellar_ext             = '_StellarContinuum.fits'
emitting_ext            = '_Emission.fits'

#Define plot frame and colors
size_dict = {'figure.figsize':(26,10), 'axes.labelsize':35, 'legend.fontsize':35, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':35, 'ytick.labelsize':35}
dz.FigConf(plotSize = size_dict)

#Reddening properties
R_v = 3.4
red_curve = 'G03_average'
cHbeta_type = 'cHbeta_reduc'

recombination_regions = array([3889, 4340,  4101, 4471, 4685, 4862, 5875, 6562, 6678])
metals_regions        = array([3726, 3728, 4363, 4740, 4958, 5007, 6716, 6730, 9069, 6548, 6583, 7135, 9531])
                           
#Loop through files
for i in range(len(catalogue_df.index)):
    
    print '-- Treating {}'.format(catalogue_df.iloc[i].name)
 
    #Locate the objects
    objName             = catalogue_df.iloc[i].name
    
    if objName == 'SHOC579':
    
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        fits_file           = catalogue_df.iloc[i].reduction_fits
        
        blue_fits = catalogue_df.iloc[i].Blue_file
        red_fits = catalogue_df.iloc[i].Red_file
        
        #Get reduce spectrum data
        Wave_O, Int_O, ExtraData_T = dz.get_spectra_data(fits_file)
        Wave_N, Int_N, ExtraData_N = dz.get_spectra_data(ouput_folder + objName + nebular_exten)
        Wave_S, Int_S, ExtraData_S = dz.get_spectra_data(ouput_folder + objName + Stellar_ext)    
        Wave_E, Int_E, ExtraData_E = dz.get_spectra_data(ouput_folder + objName + emitting_ext)    
        
        Wave_B, Int_B, ExtraData_B = dz.get_spectra_data(blue_fits)
        Wave_R, Int_R, ExtraData_R = dz.get_spectra_data(red_fits)
        
#         #Increase the range of Wave_S so it is greater than the observational range
#         Wave_StellarExtension = linspace(3000.0,3399.0,200)
#         Int_StellarExtension  = zeros(len(Wave_StellarExtension))
#      
#         #Increase the range of Wave_S so it is greater than the observational range
#         Int_S   = hstack((Int_StellarExtension, Int_S))
#         Wave_S  = hstack((Wave_StellarExtension, Wave_S))
#      
#         #Resampling stellar spectra
#         Interpolation               = interp1d(Wave_S, Int_S, kind = 'slinear')        
#         Int_Stellar_Resampled       = Interpolation(Wave_O)
#     
#         #Perform the reddening correction
#         cHbeta = catalogue_df.iloc[i][cHbeta_type]
#         IntObs_dered = dz.derreddening_spectrum(Wave_O, Int_O, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
#         IntEmi_dered = dz.derreddening_spectrum(Wave_E, Int_E, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
#     
#         Int_Sum = IntEmi_dered + Int_Stellar_Resampled + Int_N
    
        dz.data_plot(Wave_B, Int_B, 'Blue arm')
        dz.data_plot(Wave_R, Int_R, 'Red arm')
#         dz.data_plot(Wave_N, Int_N, 'Nebular continuum',linestyle='-')
#         dz.data_plot(Wave_S, Int_S, 'Stellar continuum',linestyle='-')
#         dz.insert_image('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/SHOC579_invert.png', Image_Coordinates = [0.07,0.875], Zoom=0.25, Image_xyCoords = 'axes fraction')

#         dz.area_fill(metals_regions - 10 , metals_regions + 10, 'Collisional excitation lines', color = dz.colorVector['olive'], alpha = 0.5)
#         dz.area_fill(recombination_regions - 10 , recombination_regions + 10, 'Recombination lines', color = dz.colorVector['pink'], alpha = 0.5)


        #Set titles and legend
        PlotTitle = ''
        dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle, loc='upper right', ncols_leg=2)   
        
#         dz.Axis.set_xlim(3550, 10000)
#         
#         axins2 = zoomed_inset_axes(dz.Axis, zoom=16, loc=7)
#         axins2.step(Wave_O, Int_O, label='Observed spectrum') #, linestyle='--', color=colorVector['dark blue'], where = 'mid')       
#         axins2.step(Wave_N, Int_N, label='Nebular continuum model',linestyle='-') #,color=colorVector['orangish'], where = 'mid', linewidth=0.75)
#         axins2.step(Wave_S, Int_S, label='Stellar continuum model',linestyle='-') #,color=colorVector['orangish'], where = 'mid', linewidth=0.75)
#         
#         mean_flux = Int_O.mean()
# 
#         axins2.set_xlim(3600, 3900)
#         axins2.set_ylim(-0.05*mean_flux, 8*mean_flux)
#         mark_inset(dz.Axis, axins2, loc1=2, loc2=4, fc="none", ec="0.5") 
#                      
#         axins2.get_xaxis().set_visible(False)
#         axins2.get_yaxis().set_visible(False)
        #dz.Axis.set_aspect(2)
        
        #dz.display_fig()
        
        dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Stasinska conference/' + objName + '_TwOarms')
        
#-----------------------------------------------------------------------------------------------------
print 'All data treated', dz.display_errors()
