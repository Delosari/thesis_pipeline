from pandas import read_csv
from dazer_methods import Dazer
from timeit import default_timer as timer
from DZ_LineMesurer import LineMesurer_v2

#Define main class
dz = Dazer()
lm = LineMesurer_v2('/home/vital/workspace/dazer/format/', 'DZT_LineLog_Headers.dz')

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
line                    = 'S3_9069A'

#Establish current line
lm.Current_Label        = lick_idcs_df.loc[line].name
lm.Current_Ion          = lick_idcs_df.loc[line].Ion
lm.Current_TheoLoc      = lick_idcs_df.loc[line].lambda_theo
selections              = lick_idcs_df.loc[line][3:9].values

#Proceed to measure
start = timer()
line_data = lm.measure_line(wave, flux, selections, None, Measuring_Method = 'lmfit', store_data = False) 
end = timer()
print 'measure_line', (end - start)


#Plot features
dz.Axis.plot(line_data.x_resample, line_data.y_resample, linestyle='--')
dz.Axis.step(wave[lm.fit_dict.idx0-5:lm.fit_dict.idx5+5], flux[lm.fit_dict.idx0-5:lm.fit_dict.idx5+5], label='Line: {}'.format(line), where='mid')
dz.Axis.fill_between(wave[lm.fit_dict.idx0:lm.fit_dict.idx1], lm.fit_dict.zerolev_mean, flux[lm.fit_dict.idx0:lm.fit_dict.idx1], facecolor =dz.colorVector['green'],  step='mid', alpha=0.5)
dz.Axis.fill_between(wave[lm.fit_dict.idx2:lm.fit_dict.idx3], lm.fit_dict.zerolev_mean, flux[lm.fit_dict.idx2:lm.fit_dict.idx3], facecolor =dz.colorVector['dark blue'],  step='mid', alpha=0.5)
dz.Axis.fill_between(wave[lm.fit_dict.idx4:lm.fit_dict.idx5], lm.fit_dict.zerolev_mean, flux[lm.fit_dict.idx4:lm.fit_dict.idx5], facecolor =dz.colorVector['green'],  step='mid', alpha=0.5)
dz.Axis.plot(lm.fit_dict.x_resample, lm.fit_dict.y_resample, linestyle='--')
dz.Axis.plot(lm.fit_dict.x_resample, lm.fit_dict.zerolev_resample, linestyle='--')
dz.Axis.scatter(lm.Current_TheoLoc, lm.fit_dict.zerolev_mean)

dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', r'Object {} emission line: {}'.format(objName, line), loc='upper right') 
 
dz.display_fig()
print 'DOne'
