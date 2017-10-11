from pandas import read_csv
from dazer_methods import Dazer
from timeit import default_timer as timer

#Define main class
dz = Dazer()
 
#Making the plot:
dz.FigConf()
 
#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
lickIndcs_extension     = '_lick_indeces.txt'

#Declare object to treat
objName                 = 'SHOC575_n2'

#Load line regions
ouput_folder            = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
lick_idcs_df            = read_csv(ouput_folder + objName + lickIndcs_extension, delim_whitespace = True, header = 0, index_col = 0, comment='L') #Dirty trick to avoid the Line_label row

#Load spectrum data
fits_file               = catalogue_df.loc[objName].emission_fits
wave, flux, header_0    = dz.get_spectra_data(fits_file)

#Declare line to measure
line                    = 'N2_6548A'

#Establish current line
dz.Current_Label        = lick_idcs_df.loc[line].name
dz.Current_Ion          = lick_idcs_df.loc[line].Ion
dz.Current_TheoLoc      = lick_idcs_df.loc[line].lambda_theo
selections              = lick_idcs_df.loc[line][3:9].values

#Proceed to measure

# print '--Single fit'
# start = timer()
line_data = dz.measure_line(wave, flux, selections, None, Measuring_Method = 'lmfit', store_data = False)
# end = timer()
# print 'lmfit', (end - start) 


#Plot features
dz.Axis.plot(line_data.x_resample, line_data.y_resample, linestyle='--')
dz.Axis.step(wave[dz.fit_dict.idx0-5:dz.fit_dict.idx5+5], flux[dz.fit_dict.idx0-5:dz.fit_dict.idx5+5], label='Line: {}'.format(line), where='mid')
dz.Axis.fill_between(wave[dz.fit_dict.idx0:dz.fit_dict.idx1], dz.fit_dict.zerolev_mean, flux[dz.fit_dict.idx0:dz.fit_dict.idx1], facecolor =dz.colorVector['green'],  step='mid', alpha=0.5)
dz.Axis.fill_between(wave[dz.fit_dict.idx2:dz.fit_dict.idx3], dz.fit_dict.zerolev_mean, flux[dz.fit_dict.idx2:dz.fit_dict.idx3], facecolor =dz.colorVector['dark blue'],  step='mid', alpha=0.5)
dz.Axis.fill_between(wave[dz.fit_dict.idx4:dz.fit_dict.idx5], dz.fit_dict.zerolev_mean, flux[dz.fit_dict.idx4:dz.fit_dict.idx5], facecolor =dz.colorVector['green'],  step='mid', alpha=0.5)
dz.Axis.plot(dz.fit_dict.x_resample, dz.fit_dict.y_resample, linestyle='--')
dz.Axis.plot(dz.fit_dict.x_resample, dz.fit_dict.zerolev_resample, linestyle='--')
dz.Axis.scatter(dz.Current_TheoLoc, dz.fit_dict.zerolev_mean)

dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', r'Object {} emission line: {}'.format(objName, line), loc='upper right') 
 
dz.display_fig()




# '''
# Created on Feb 1, 2017
# 
# @author: vital
# '''
# from pandas import read_csv
# from dazer_methods import Dazer
# 
# #Define main class
# dz = Dazer()
# 
# #Set object and line to measure
# line    = 'S3_9069A'
# objName = '71'
# 
# #Making the plot:
# dz.FigConf()
# 
# #Load catalogue dataframe
# catalogue_dict = dz.import_catalogue()
# catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
# lickIndcs_extension = '_lick_indeces.txt'
# ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
# lick_idcs_df = read_csv(ouput_folder + objName + lickIndcs_extension, delim_whitespace = True, header = 0, index_col = 0, comment='L') #Dirty trick to avoid the Line_label row
# 
# #Load object data
# fits_file                           = catalogue_df.loc[objName].Red_file
# redshift_factor                     = 1 + catalogue_df.loc[objName].z_Red
# wave_obs, flux_obs, header_0_obs    = dz.get_spectra_data(fits_file)
# wave = wave_obs / redshift_factor 
#  
# #Load the line region
# dz.Current_Label    = lick_idcs_df.loc[line].name
# dz.Current_Ion      = lick_idcs_df.loc[line].Ion
# dz.Current_TheoLoc  = lick_idcs_df.loc[line].lambda_theo
# selections          = lick_idcs_df.loc[line][3:9].values
# 
# print '-Measuring {} for object {}'.format(line, objName)
# print dz.Current_Label
# print dz.Current_Ion
# print dz.Current_TheoLoc
# print selections
# 
# # print line_fit_orig
# for i in range(50):
#     line_fit_orig = dz.measure_line(wave, flux_obs, selections, None, 'lmfit', store_data = False)
#     print 'i:', i, ' ', line_fit_orig.flux_intg, line_fit_orig.flux_gauss0, line_fit_orig.A0, line_fit_orig.sigma0 
#     dz.Axis.plot(line_fit_orig.x_resample, line_fit_orig.y_resample, linestyle='--')
# 
# #plot features
# dz.Axis.step(wave[dz.fit_dict.idx0-5:dz.fit_dict.idx5+5], flux_obs[dz.fit_dict.idx0-5:dz.fit_dict.idx5+5], label='Line: {}'.format(line), where='mid')
# dz.Axis.fill_between(wave[dz.fit_dict.idx0:dz.fit_dict.idx1], dz.fit_dict.zerolev_mean, flux_obs[dz.fit_dict.idx0:dz.fit_dict.idx1], facecolor =dz.colorVector['green'],  step='mid', alpha=0.5)
# dz.Axis.fill_between(wave[dz.fit_dict.idx2:dz.fit_dict.idx3], dz.fit_dict.zerolev_mean, flux_obs[dz.fit_dict.idx2:dz.fit_dict.idx3], facecolor =dz.colorVector['dark blue'],  step='mid', alpha=0.5)
# dz.Axis.fill_between(wave[dz.fit_dict.idx4:dz.fit_dict.idx5], dz.fit_dict.zerolev_mean, flux_obs[dz.fit_dict.idx4:dz.fit_dict.idx5], facecolor =dz.colorVector['green'],  step='mid', alpha=0.5)
# #dz.Axis.plot(dz.fit_dict.x_resample, dz.fit_dict.y_resample, linestyle='--')
# # dz.Axis.plot(dz.fit_dict.x_resample, dz.fit_dict.zerolev_resample, linestyle='--')
# dz.Axis.scatter(dz.Current_TheoLoc, dz.fit_dict.zerolev_mean)
# 
# dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', r'Object {} emission line: {}'.format(objName, line), loc='upper right') 
# 
# dz.display_fig()


