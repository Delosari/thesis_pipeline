from pandas import read_csv
from dazer_methods import Dazer
from uncertainties import ufloat
from DZ_observation_reduction import spectra_reduction

#Define main class
dz              = Dazer()
dz_sr           = spectra_reduction()
 
#Making the plot:
dz.FigConf()

#Set object and line to measure
objName         = 'IZW18_A1'
extension       = 1
S3_lines        = ['S3_9069A', 'S3_9531A']

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

lickIndcs_ext   = '_lick_indeces.txt'
ouput_folder    = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
lick_idcs_df    = read_csv(ouput_folder + objName + lickIndcs_ext, delim_whitespace = True, header = 0, index_col = 0, comment='L') #Dirty trick to avoid the Line_label row

#Define fits file:
ratios_dict = {}
for extension in [0, 1]: 
    fits_file                           = '/home/vital/Astrodata/WHT_2016_04/Night1/objects/IZW18_Red_cr_f_t_w_e_{testing_extension}_fglobal.fits'.format(testing_extension=dz_sr.testing_extension)
    #fits_file                           = '/home/vital/Astrodata/WHT_2016_04/Night1/objects/IZW18_Red_cr_f_t_w_bg_e_fglobal.fits'
    redshift_factor                     = 1 + catalogue_df.loc[objName].z_Red
    wave_obs, flux_obs, header_0_obs    = dz.get_spectra_data(fits_file)
    wave                                = wave_obs / redshift_factor
    flux                                = flux_obs[extension]
    
    for line in S3_lines:
        dz.Current_Label    = lick_idcs_df.loc[line].name
        dz.Current_Ion      = lick_idcs_df.loc[line].Ion
        dz.Current_TheoLoc  = lick_idcs_df.loc[line].lambda_theo
        selections          = lick_idcs_df.loc[line][3:9].values
    
        #Proceed to measure
        line_data = dz.measure_line(wave, flux, selections, None, Measuring_Method = 'MC_lmfit', store_data = False)
        
        entry_key               = '{}_ext{}'.format(line, extension)
        ratios_dict[entry_key]  = ufloat(line_data.flux_intg, line_data.flux_intg_er)
    
    print 'Extension {} ratio: {}'.format(extension + 1, ratios_dict['S3_9531A_ext{}'.format(extension)]/ratios_dict['S3_9069A_ext{}'.format(extension)])
    

# #Plot features
# dz.Axis.plot(line_data.x_resample, line_data.y_resample, linestyle='--')
# dz.Axis.step(wave[dz.fit_dict.idx0-5:dz.fit_dict.idx5+5], flux[dz.fit_dict.idx0-5:dz.fit_dict.idx5+5], label='Line: {}'.format(line), where='mid')
# dz.Axis.fill_between(wave[dz.fit_dict.idx0:dz.fit_dict.idx1], dz.fit_dict.zerolev_mean, flux[dz.fit_dict.idx0:dz.fit_dict.idx1], facecolor =dz.colorVector['green'],  step='mid', alpha=0.5)
# dz.Axis.fill_between(wave[dz.fit_dict.idx2:dz.fit_dict.idx3], dz.fit_dict.zerolev_mean, flux[dz.fit_dict.idx2:dz.fit_dict.idx3], facecolor =dz.colorVector['dark blue'],  step='mid', alpha=0.5)
# dz.Axis.fill_between(wave[dz.fit_dict.idx4:dz.fit_dict.idx5], dz.fit_dict.zerolev_mean, flux[dz.fit_dict.idx4:dz.fit_dict.idx5], facecolor =dz.colorVector['green'],  step='mid', alpha=0.5)
# dz.Axis.plot(dz.fit_dict.x_resample, dz.fit_dict.y_resample, linestyle='--')
# dz.Axis.plot(dz.fit_dict.x_resample, dz.fit_dict.zerolev_resample, linestyle='--')
# dz.Axis.scatter(dz.Current_TheoLoc, dz.fit_dict.zerolev_mean)
# 
# dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', r'Object {} emission line: {}'.format(objName, line), loc='upper right') 
#  
# dz.display_fig()


 