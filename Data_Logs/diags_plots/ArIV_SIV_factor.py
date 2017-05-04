from dazer_methods  import Dazer
from numpy          import nanmean, nanstd, mean, nan as np_nan
from uncertainties  import ufloat
import pandas as pd
 
#Generate dazer object
dz = Dazer()
 
#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
 
for objName in catalogue_df.index:
     
    objData     = catalogue_df.loc[objName] 
     
    #Reducted data
    check_ions  = pd.notnull(objData[['SII_HII_emis2nd', 'SIII_HII_emis2nd', 'SIV_HII_emis2nd']]).all()
     
    if check_ions:
           
        #ICF_Sulfur = (objData.SII_HII_emis + objData.SIII_HII_emis + objData.SIV_HII_emis) / (objData.SII_HII_emis + objData.SIII_HII_emis)
        ICF_Sulfur = (objData.SIV_HII) / (objData.SIII_HII)
         
        catalogue_df.loc[objName, 'ICF_SIV'] = ICF_Sulfur    
     
    #Emission
    check_ions  = pd.notnull(objData[['SII_HII_emis2nd', 'SIII_HII_emis2nd', 'SIV_HII_emis2nd']]).all() 
          
    if check_ions:
           
        #ICF_Sulfur = (objData.SII_HII_emis + objData.SIII_HII_emis + objData.SIV_HII_emis) / (objData.SII_HII_emis + objData.SIII_HII_emis)
        ICF_Sulfur = (objData.SIV_HII_emis2nd) / (objData.SIII_HII_emis2nd)
         
        catalogue_df.loc[objName, 'ICF_SIV_emis2nd'] = ICF_Sulfur
 
dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx', df_sheet_format = 'catalogue_data')

# import pyneb as pn
# import numpy as np
# from dazer_methods import Dazer
#   
# #Create class object
# dz = Dazer()
#   
# #Set figure format
# dz.FigConf()
#    
# Temp_range  = np.linspace(5000, 20000, 100)
# den_range   = np.ones(100) * 100
#  
# #pn.atomicData.getAllAvailableFiles('He2')
# #pn.atomicData.setDataFile('he_ii_trc_SH95-caseA.dat')
# #he_ii_trc_SH95-caseA.dat
# #he_ii_trc_SH95-caseB.dat
#  
# H1  = pn.RecAtom('H', 1)
# He1 = pn.RecAtom('He', 1)
# He2 = pn.RecAtom('He', 2)
# S3  = pn.Atom('S', 3)
# O3  = pn.Atom('O', 3)
#  
# H1.printSources()
# He1.printSources()
# He2.printSources()
#  
# # pn.atomicData.setDataFile('3he_ii_coll_cloudy.dat')
# # He2_cloudy  = pn.RecAtom('He', 2)
# # AtomicData2 = He2_cloudy.printSources()
# #   
# # print type(AtomicData1)
# # print type(AtomicData2)
#  
# He1_Emissivity = He1.getEmissivity(tem = Temp_range, den = den_range, wave=5876, product=False)
# He2_Emissivity = He2.getEmissivity(tem = Temp_range, den = den_range, wave=4686)
# O3_Emissivity = O3.getEmissivity(tem = Temp_range, den = den_range, wave=4363)
# S3_Emissivity = S3.getEmissivity(tem = Temp_range, den = den_range, wave=9069)
#   
# dz.data_plot(Temp_range, He2_Emissivity)
#     
# dz.FigWording(r'$T_{e} (K)$', r'$E(\lambda)$', r'$He^{+2}$ $\lambda4686\AA$ line emissivity versus temperature')
#     
# dz.display_fig()

# import pyneb as pn
# import numpy as np
# from dazer_methods import Dazer
#   
# #Create class object
# dz = Dazer()
#   
# #Set figure format
# dz.FigConf(plotStyle='ggplot')
# 
# H1  = pn.RecAtom('H', 1)
# He2 = pn.RecAtom('He', 2)
#  
# He2_4686_emis       = He2.getEmissivity(tem = 18000, den = 100, wave=4686, product=False)
# HBeta_emissivity    = H1.getEmissivity(tem = 18000, den = 100, wave=4861, product=False)
#  
# temperature_range   = np.array([10000.0, 11000.0, 12000.0, 13000.0, 14000.0, 15000.0, 16000.0, 17000.0, 18000.0, 19000.0, 20000.0, 21000.0, 22000.0])
# density_range       = np.ones(len(temperature_range)) * 100
# 
# He2_4686_flux       = 0.001 * He2_4686_emis * np.ones(len(temperature_range))
# 
# ionic_abund         = He2.getIonAbundance(int_ratio = He2_4686_flux, tem=temperature_range, den=density_range, to_eval = 'L(4685)', Hbeta = HBeta_emissivity)
# print ionic_abund
# 
# ionic_variation     = ((ionic_abund / (np.ones(len(temperature_range)) * 0.001))-1) * 100 
# print ionic_variation
#   
# dz.data_plot(temperature_range, ionic_variation, label= r'$He2$ measured from $\lambda4686\AA$ line')
# dz.data_plot(18000.0, 0.0, label= r'True abundance at $T_e = 18000K$', markerstyle='o', color = 'green')
# 
# 
# dz.FigWording(r'$T_{e} (K)$', r'Percentage difference', r'$He^{+2}$ $\lambda4686\AA$ abundance calculation as a function of the input temperature')
#     
# dz.display_fig()


