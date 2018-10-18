#!/usr/bin/env python
from dazer_methods import Dazer
from numpy import linspace, zeros, hstack
from scipy.interpolate import interp1d

#Declare code classes
dz = Dazer()
script_code = dz.get_script_code()

def colorLineZones(wave, int, zones, color):

    for pairWave in zones:
        print pairWave
        idces = (pairWave[0] <= wave) & (wave <= pairWave[1])
        dz.data_plot(wave[idces], int[idces], '', color=color)

def LineZones(wave, int, zones, color):

    for pairWave in zones:
        idces = (pairWave[0] <= wave) & (wave <= pairWave[1])
        dz.data_plot(wave[idces], int[idces], '', color=color)
        # dz.area_fill(wave[idces], int[idces], zeros(int[idces].size), alpha=0.5)
        dz.Axis.fill_between(wave[idces], int[idces], zeros(int[idces].size), color=color, alpha=0.5)



#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
nebular_exten           = '_NebularContinuum_emis.fits'
Stellar_ext             = '_StellarContinuum_emis.fits'
emitting_ext            = '_Emission_2nd.fits'

#Define plot frame and colors
size_dict = {'figure.figsize' : (18, 18), 'axes.labelsize':35, 'legend.fontsize':35, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':35, 'ytick.labelsize':35}
dz.FigConf(plotSize = size_dict)

#Reddening properties
R_v = 3.4
red_curve = 'G03_average'
cHbeta_type = 'cHbeta_emis'

#Loop through files
for i in range(len(catalogue_df.index)):



        #Locate the objects
        objName             = catalogue_df.iloc[i].name
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
        fits_file           = catalogue_df.iloc[i].reduction_fits

        if objName == '8':
            print '-- Treating {}'.format(catalogue_df.iloc[i].name)

            #Get reduce spectrum data
            Wave_O, Int_O, ExtraData_T = dz.get_spectra_data(fits_file)
            Wave_N, Int_N, ExtraData_N = dz.get_spectra_data(ouput_folder + objName + nebular_exten)
            Wave_S, Int_S, ExtraData_S = dz.get_spectra_data(ouput_folder + objName + Stellar_ext)
            Wave_E, Int_E, ExtraData_E = dz.get_spectra_data(ouput_folder + objName + emitting_ext)

            #Increase the range of Wave_S so it is greater than the observational range
            Wave_StellarExtension = linspace(3000.0,3399.0,200)
            Int_StellarExtension  = zeros(len(Wave_StellarExtension))

            #Increase the range of Wave_S so it is greater than the observational range
            # Int_S   = hstack((Int_StellarExtension, Int_S))
            # Wave_S  = hstack((Wave_StellarExtension, Wave_S))

            #Resampling stellar spectra
            Interpolation               = interp1d(Wave_S, Int_S, kind = 'slinear')
            Int_Stellar_Resampled       = Interpolation(Wave_O)

            #Perform the reddening correction
            cHbeta = catalogue_df.iloc[i][cHbeta_type]
            IntObs_dered = dz.derreddening_spectrum(Wave_O, Int_O, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
            IntEmi_dered = dz.derreddening_spectrum(Wave_E, Int_E, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)

            # Int_Sum = IntEmi_dered + Int_Stellar_Resampled + Int_N

            dz.data_plot(Wave_O, IntObs_dered, '', color='black')
            # dz.data_plot(Wave_N, Int_N, '',  color='tab:orange')
            # dz.data_plot(Wave_S, Int_S, '',   color='tab:green')

            recombZones = [[4330, 4350],
                           [4464, 4479],
                           [4707, 4720],
                           [4850, 4870],
                           [4913, 4931],
                           [5013, 5021]]

            colorLineZones(Wave_O, IntObs_dered, recombZones, 'tab:blue')

            recombZones = [[4356, 4373],
                           [4947, 4969],
                           [4992, 5013]]

            colorLineZones(Wave_O, IntObs_dered, recombZones, 'tab:pink')

            #Set titles and legend
            PlotTitle = r'{} continua comparison'.format(objName)
            dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', '', loc='upper right')

            mean_flux = Int_O.mean()
            #dz.Axis.set_yscale('log')
            dz.Axis.set_ylim(-0.05*mean_flux, 4*mean_flux)
            dz.Axis.set_xlim(4580, 4830)

            # colorLineZones(Wave_O, IntObs_dered, [[4750, 4780]], 'tab:red')
            # colorLineZones(Wave_O, IntObs_dered, [[4615, 4636]], 'tab:red')

            adjacentRegions = [[4750, 4780], [4615, 4636]]
            LineZones(Wave_O, IntObs_dered, adjacentRegions, 'tab:red')
            # colorLineZones(Wave_O, IntObs_dered, recombZones, 'tab:pink')

            LineZones(Wave_O, IntObs_dered, [[4707, 4720]], 'tab:blue')


            #Save data
            #dz.display_fig()
            dz.savefig('/home/vital/Dropbox/Astrophysics/Thesis/images/lineFitting')
        #output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='comparison_spectra')
        #dz.save_manager(output_pickle, save_pickle = True)

#-----------------------------------------------------------------------------------------------------
print 'All data treated', dz.display_errors()


# #!/usr/bin/env python
# from dazer_methods import Dazer
# from numpy import linspace, zeros, hstack
# from scipy.interpolate import interp1d
#
# #Declare code classes
# dz = Dazer()
# script_code = dz.get_script_code()
#
# def colorLineZones(wave, int, zones, color):
#
#     for pairWave in zones:
#         print pairWave
#         idces = (pairWave[0] <= wave) & (wave <= pairWave[1])
#         dz.data_plot(wave[idces], int[idces], '', color=color)
#
#
# #Load catalogue dataframe
# catalogue_dict          = dz.import_catalogue()
# catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
# nebular_exten           = '_NebularContinuum_emis.fits'
# Stellar_ext             = '_StellarContinuum_emis.fits'
# emitting_ext            = '_Emission_2nd.fits'
#
# #Define plot frame and colors
# size_dict = {'figure.figsize' : (18, 18), 'axes.labelsize':35, 'legend.fontsize':35, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':35, 'ytick.labelsize':35}
# dz.FigConf(plotSize = size_dict)
#
# #Reddening properties
# R_v = 3.4
# red_curve = 'G03_average'
# cHbeta_type = 'cHbeta_emis'
#
# #Loop through files
# for i in range(len(catalogue_df.index)):
#
#
#
#         #Locate the objects
#         objName             = catalogue_df.iloc[i].name
#         ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
#         fits_file           = catalogue_df.iloc[i].reduction_fits
#
#         if objName == '8':
#             print '-- Treating {}'.format(catalogue_df.iloc[i].name)
#
#             #Get reduce spectrum data
#             Wave_O, Int_O, ExtraData_T = dz.get_spectra_data(fits_file)
#             Wave_N, Int_N, ExtraData_N = dz.get_spectra_data(ouput_folder + objName + nebular_exten)
#             Wave_S, Int_S, ExtraData_S = dz.get_spectra_data(ouput_folder + objName + Stellar_ext)
#             Wave_E, Int_E, ExtraData_E = dz.get_spectra_data(ouput_folder + objName + emitting_ext)
#
#             #Increase the range of Wave_S so it is greater than the observational range
#             Wave_StellarExtension = linspace(3000.0,3399.0,200)
#             Int_StellarExtension  = zeros(len(Wave_StellarExtension))
#
#             #Increase the range of Wave_S so it is greater than the observational range
#             # Int_S   = hstack((Int_StellarExtension, Int_S))
#             # Wave_S  = hstack((Wave_StellarExtension, Wave_S))
#
#             #Resampling stellar spectra
#             Interpolation               = interp1d(Wave_S, Int_S, kind = 'slinear')
#             Int_Stellar_Resampled       = Interpolation(Wave_O)
#
#             #Perform the reddening correction
#             cHbeta = catalogue_df.iloc[i][cHbeta_type]
#             IntObs_dered = dz.derreddening_spectrum(Wave_O, Int_O, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
#             IntEmi_dered = dz.derreddening_spectrum(Wave_E, Int_E, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
#
#             # Int_Sum = IntEmi_dered + Int_Stellar_Resampled + Int_N
#
#             dz.data_plot(Wave_O, IntObs_dered, '', color='black')
#             dz.data_plot(Wave_N, Int_N, '',  color='tab:orange')
#             dz.data_plot(Wave_S, Int_S, '',   color='tab:green')
#
#             recombZones = [[4330, 4350],
#                            [4464, 4479],
#                            [4707, 4720],
#                            [4850, 4870],
#                            [4913, 4931],
#                            [5013, 5021]]
#
#             colorLineZones(Wave_O, IntObs_dered, recombZones, 'tab:blue')
#
#             recombZones = [[4356, 4373],
#                            [4947, 4969],
#                            [4992, 5013]]
#
#             colorLineZones(Wave_O, IntObs_dered, recombZones, 'tab:pink')
#
#             #Set titles and legend
#             PlotTitle = r'{} continua comparison'.format(objName)
#             dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', '', loc='upper right')
#
#             mean_flux = Int_O.mean()
#             #dz.Axis.set_yscale('log')
#             dz.Axis.set_ylim(-0.05*mean_flux, 8*mean_flux)
#             dz.Axis.set_xlim(4320, 5250)
#
#             #Save data
#             dz.display_fig()
#             #dz.savefig('/home/vital/Dropbox/Astrophysics/Thesis/images/spectraComponents')
#         #output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='comparison_spectra')
#         #dz.save_manager(output_pickle, save_pickle = True)
#
# #-----------------------------------------------------------------------------------------------------
# print 'All data treated', dz.display_errors()