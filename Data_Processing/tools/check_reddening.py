colsPerDict_dict = {}
colsPerDict_dict['Physical_Data_emis']       = ['neSII','neOII','TeOII','TeSII','TeNII','TeOIII','TeSIII','TeOII_from_TeOIII','TeNII_from_TeOIII','TeSIII_from_TeOIII','TeOIII_from_TeSIII']
colsPerDict_dict['Chemical_Abundances_emis'] = ['SII_HII','SIII_HII','SIV_HII','OII_HII','OII_HII_3279A','OII_HII_7319A','OIII_HII','NII_HII','ArIII_HII','ArIV_HII','HeII_HII_from_O','HeIII_HII_from_O','HeII_HII_from_S','HeIII_HII_from_S','SI_HI','OI_HI','NI_OI','NI_HI','HeI_HI_from_O','HeI_HI_from_S','Ymass_O','Ymass_S']

for sheet in colsPerDict_dict:
    variables = colsPerDict_dict[sheet]
    for i in range(len(variables)):
        colsPerDict_dict[sheet][i] = colsPerDict_dict[sheet][i] + '_emis'

for sheet in colsPerDict_dict:
    print colsPerDict_dict[sheet]



# '''
# Created on Feb 3, 2017
# 
# @author: vital
# '''
# 
# import numpy as np
# from dazer_methods import Dazer
# from scipy.interpolate import interp1d
# 
# #Declare code classes
# dz = Dazer()
# script_code     = dz.get_script_code()
# 
# dz.FigConf()
# 
# #Reddening properties
# R_v = 3.4
# red_curve = 'G03'
# cHbeta_type = 'cHbeta_reduc'
# 
# catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
# 
# objName         = '8'
# ouput_folder    = '{}{}/'.format(catalogue_df, objName) 
# fits_file       = catalogue_df.loc[objName].reduction_fits
# 
# Wave_T, Int_T, ExtraData_T = dz.get_spectra_data(fits_file)
# 
# cHbeta      = catalogue_df.loc[objName, cHbeta_type]
# Int_T_dered = dz.derreddening_spectrum(Wave_T, Int_T, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
# Int_T_redd  = dz.reddening_spectrum(Wave_T, Int_T_dered, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
# 
# print cHbeta
# 
# dz.data_plot(Wave_T, Int_T, 'Reduced spectra')
# dz.data_plot(Wave_T, Int_T_dered, 'Derred')
# dz.data_plot(Wave_T, Int_T_redd, 'Red again')
# 
# PlotTitle = r'Object {} Stellar continuum substraction'.format(objName)
# dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)   
# 
# dz.display_fig()


