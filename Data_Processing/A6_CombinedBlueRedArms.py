#!/usr/bin/python
from numpy import searchsorted, median, concatenate
from dazer_methods import Dazer

#Create class object
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Set figure format
size_dict = {'figure.figsize' : (21, 8), 'axes.labelsize':32, 'legend.fontsize':24, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':28, 'ytick.labelsize':28}
dz.FigConf(plotSize = size_dict)

#Loop through the objects
for i in range(len(catalogue_df.index)):
     
    #Object
    objName = catalogue_df.iloc[i].name

    if objName == 'SHOC579':

        #Joining pointing
        joining_wavelength = catalogue_df.iloc[i].join_wavelength

        #Treat each arm file
        blue_fits_file = catalogue_df.iloc[i]['zBlue_file']
        red_fits_file = catalogue_df.iloc[i]['zRed_file']

        CodeName_Blue, FileName_Blue, FileFolder_Blue = dz.Analyze_Address(blue_fits_file)
        CodeName_Red, FileName_Red, FileFolder_Red = dz.Analyze_Address(red_fits_file)

        wave_Blue, flux_Blue, ExtraData_Blue = dz.get_spectra_data(blue_fits_file)
        wave_Red, flux_Red, ExtraData_Red = dz.get_spectra_data(red_fits_file)

        idx_blue = searchsorted(wave_Blue, joining_wavelength)
        idx_red  = searchsorted(wave_Red, joining_wavelength)

        wave_comb = concatenate([wave_Blue[0:idx_blue], wave_Red[idx_red:-1]])
        flux_comb = concatenate([flux_Blue[0:idx_blue], flux_Red[idx_red:-1]])

        dz.data_plot(wave_Blue, flux_Blue, label = 'Blue arm')
        dz.data_plot(wave_Red, flux_Red, label = 'Red arm')

        dz.FigWording(r'Wavelength $(\AA)$', 'Flux ' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', '', ncols_leg = 2)
        dz.savefig('/home/vital/Dropbox/Astrophysics/Thesis/images/SHOC579_z.png')

        # dz.display_fig()

        # #Store the figure
        # output_pickle = FileFolder_Blue + script_code + '_' + CodeName_Blue + '_combined_emission'
        # dz.save_manager(output_pickle, save_pickle = True)
        # dz.Data_2_Fits(FileFolder_Blue, CodeName_Blue + '_WHT.fits', ExtraData_Blue, wave_comb, flux_comb, NewKeyWord = ['WHTJOINW', str(joining_wavelength)])
        #
        # #Store file address in dataframe
        # combined_fits_name = FileFolder_Blue + CodeName_Blue + '_WHT.fits'
        # catalogue_df.loc[objName, 'reduction_fits'] = combined_fits_name

print "\nAll data treated generated"
 



# # !/usr/bin/python
# from numpy import searchsorted, median, concatenate
# from dazer_methods import Dazer
#
# # Create class object
# dz = Dazer()
# script_code = dz.get_script_code()
#
# # Load catalogue dataframe
# catalogue_dict = dz.import_catalogue()
# catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
#
# # Set figure format
# dz.FigConf()
#
# # Loop through the objects
# for i in range(len(catalogue_df.index)):
#     # Object
#     objName = catalogue_df.iloc[i].name
#
#     # Joining pointing
#     joining_wavelength = catalogue_df.iloc[i].join_wavelength
#
#     # Treat each arm file
#     blue_fits_file = catalogue_df.iloc[i]['zBlue_file']
#     red_fits_file = catalogue_df.iloc[i]['zRed_file']
#
#     CodeName_Blue, FileName_Blue, FileFolder_Blue = dz.Analyze_Address(blue_fits_file)
#     CodeName_Red, FileName_Red, FileFolder_Red = dz.Analyze_Address(red_fits_file)
#
#     wave_Blue, flux_Blue, ExtraData_Blue = dz.get_spectra_data(blue_fits_file)
#     wave_Red, flux_Red, ExtraData_Red = dz.get_spectra_data(red_fits_file)
#
#     idx_blue = searchsorted(wave_Blue, joining_wavelength)
#     idx_red = searchsorted(wave_Red, joining_wavelength)
#
#     wave_comb = concatenate([wave_Blue[0:idx_blue], wave_Red[idx_red:-1]])
#     flux_comb = concatenate([flux_Blue[0:idx_blue], flux_Red[idx_red:-1]])
#
#     dz.data_plot(wave_comb, flux_comb, label='{} combined arms emission'.format(objName))
#
#     dz.FigWording(r'Wavelength $(\AA)$', 'Flux ' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', 'Redshift correction')
#
#     # Store the figure
#     output_pickle = FileFolder_Blue + script_code + '_' + CodeName_Blue + '_combined_emission'
#     dz.save_manager(output_pickle, save_pickle=True)
#     dz.Data_2_Fits(FileFolder_Blue, CodeName_Blue + '_WHT.fits', ExtraData_Blue, wave_comb, flux_comb,
#                    NewKeyWord=['WHTJOINW', str(joining_wavelength)])
#
#     # Store file address in dataframe
#     combined_fits_name = FileFolder_Blue + CodeName_Blue + '_WHT.fits'
#     catalogue_df.loc[objName, 'reduction_fits'] = combined_fits_name
#
# print "\nAll data treated generated"
#
# # Store the dataframe
# dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx',
#                  df_sheet_format='catalogue_data')
#
