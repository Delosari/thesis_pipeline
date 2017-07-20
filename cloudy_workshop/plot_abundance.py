from collections import OrderedDict
from dazer_methods import Dazer
import numpy as np
 
dz = Dazer()
dz.FigConf()
 
Grid_Values = OrderedDict()
 
Grid_Values = OrderedDict()
Grid_Values['age']          = ['5.0', '5.48', '6.0', '6.48', '6.72']               
Grid_Values['clus_mass']    = ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
Grid_Values['zGas']         = ['0.0004', '0.004', '0.008', '0.02'] 
Grid_Values['zStars']       = ['-2.1'] 

colors_list = ['#0072B2', '#009E73', '#D55E00', '#CC79A7', '#7f7f7f', '#FFB5B8', '#F0E442']

data_folder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/Grid_data_vital/'

for age in Grid_Values['age']:
    for mass in Grid_Values['clus_mass']:
        for zGas in Grid_Values['zGas']:                                        
            for zStar in Grid_Values['zStars']:
                
                idx_color = Grid_Values['age'].index(age)
                
                name_root = 'TGrid' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
                file_address = data_folder + name_root + '.lin'
                
                He2_4685, He1_5875  = np.loadtxt(file_address, usecols = (4, 9), unpack = True)    
                
                dz.data_plot(He1_5875, He2_4685, markerstyle='o', color=colors_list[idx_color], label = r'log(age) = {}'.format(age))
  
dz.data_plot(9.82/100, 15.23/100, markerstyle='o', color='#bcbd22', label = 'Observational point')
               
dz.FigWording(r'$F(HeI5876\AA/H\beta$)', r'$F(HeII4685\AA/H\beta$)', r'Relation He lines', loc='best')
 
dz.Axis.set_yscale('log')    
dz.Axis.set_xscale('log')    
 
# dz.display_fig()              
 
dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/fluxes_grid_obs_age_effect', extension='.jpg')


# from collections import OrderedDict
# from dazer_methods import Dazer
# import numpy as np
#  
# dz = Dazer()
# dz.FigConf()
#  
# Grid_Values = OrderedDict()
#  
# Grid_Values = OrderedDict()
# Grid_Values['age']          = ['5.0', '5.48', '6.0', '6.48', '6.72']               
# Grid_Values['clus_mass']    = ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
# Grid_Values['zGas']         = ['0.0004', '0.004', '0.008', '0.02'] 
# Grid_Values['zStars']       = ['-2.1'] 
# 
# colors_list = ['#0072B2', '#009E73', '#D55E00', '#CC79A7', '#7f7f7f', '#FFB5B8', '#F0E442']
# 
# data_folder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/Grid_data_vital/'
# 
# for age in Grid_Values['age']:
#     for mass in Grid_Values['clus_mass']:
#         for zGas in Grid_Values['zGas']:                                        
#             for zStar in Grid_Values['zStars']:
#                 
#                 idx_color = Grid_Values['clus_mass'].index(mass)
#                 
#                 name_root = 'TGrid' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
#                 file_address = data_folder + name_root + '.lin'
#                 
#                 He2_4685, He1_5875  = np.loadtxt(file_address, usecols = (4, 9), unpack = True)    
#                 
#                 dz.data_plot(He1_5875, He2_4685, markerstyle='o', color=colors_list[idx_color], label = r'Cluster mass = {} $M\odot$'.format(mass))
#   
# dz.data_plot(9.82/100, 15.23/100, markerstyle='o', color='#bcbd22', label = 'Observational point')
#                
# dz.FigWording(r'$F(HeI5876\AA/H\beta$)', r'$F(HeII4685\AA/H\beta$)', r'Relation He lines', loc='best')
#  
# dz.Axis.set_yscale('log')    
# dz.Axis.set_xscale('log')    
#  
# # dz.display_fig()              
#  
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/fluxes_grid_obs_mass_effect', extension='.jpg')



# from collections import OrderedDict
# from dazer_methods import Dazer
# import numpy as np
#  
# dz = Dazer()
# dz.FigConf()
#  
# Grid_Values = OrderedDict()
#  
# Grid_Values = OrderedDict()
# Grid_Values['age']          = ['5.0', '5.48', '6.0', '6.48', '6.72']               
# Grid_Values['clus_mass']    = ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
# Grid_Values['zGas']         = ['0.0004', '0.004', '0.008', '0.02'] 
# Grid_Values['zStars']       = ['-2.1'] 
# 
# colors_list = ['#0072B2', '#009E73', '#D55E00', '#CC79A7']
# 
# data_folder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/Grid_data_vital/'
# 
# for age in Grid_Values['age']:
#     for mass in Grid_Values['clus_mass']:
#         for zGas in Grid_Values['zGas']:                                        
#             for zStar in Grid_Values['zStars']:
#                 
#                 idx_color = Grid_Values['zGas'].index(zGas)
#                 
#                 name_root = 'TGrid' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
#                 file_address = data_folder + name_root + '.lin'
#                 
#                 He2_4685, He1_5875  = np.loadtxt(file_address, usecols = (4, 9), unpack = True)    
#                 
#                 dz.data_plot(He1_5875, He2_4685, markerstyle='o', color=colors_list[idx_color], label = 'Zgas = {}'.format(zGas))
#   
# dz.data_plot(9.82/100, 15.23/100, markerstyle='o', color='#bcbd22', label = 'Observational point')
#                
# dz.FigWording(r'$F(HeI5876\AA/H\beta$)', r'$F(HeII4685\AA/H\beta$)', r'Relation He lines', loc='best')
#  
# dz.Axis.set_yscale('log')    
# dz.Axis.set_xscale('log')    
#  
# # dz.display_fig()              
#  
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/fluxes_grid_obs', extension='.jpg')



# from collections import OrderedDict
# from dazer_methods import Dazer
# import numpy as np
#  
# dz = Dazer()
# dz.FigConf()
#  
# Grid_Values = OrderedDict()
#  
# Grid_Values = OrderedDict()
# Grid_Values['age']          = ['5.0', '5.48', '6.0', '6.48', '6.72']               
# Grid_Values['clus_mass']    = ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
# Grid_Values['zGas']         = ['0.0004', '0.004', '0.008', '0.02'] 
# Grid_Values['zStars']       = ['-2.1'] 
# 
# # Grid_Values['age']          = ['5.0']               
# # Grid_Values['clus_mass']    = ['12000.0']
# # Grid_Values['zGas']         = ['0.02'] 
# # Grid_Values['zStars']       = ['-2.1'] 
# 
# data_folder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/Grid_data_vital/'
# 
# for age in Grid_Values['age']:
#     for mass in Grid_Values['clus_mass']:
#         for zGas in Grid_Values['zGas']:                                        
#             for zStar in Grid_Values['zStars']:
#  
#                 name_root = 'TGrid' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
#                 file_address = data_folder + name_root + '.lin'
#                 
#                 He2_4685, He1_5875  = np.loadtxt(file_address, usecols = (4, 9), unpack = True)    
#                 
#                 dz.data_plot(He1_5875, He2_4685, markerstyle='o', color='black', label = 'Grid points')
#   
# dz.data_plot(9.82/100, 15.23/100, markerstyle='o', color='red', label = 'Observational')
#                
# dz.FigWording(r'$F(HeI5876\AA/H\beta$)', r'$F(HeII4685\AA/H\beta$)', r'Relation He lines', loc='best')
#  
# dz.Axis.set_yscale('log')    
# dz.Axis.set_xscale('log')    
#  
# # dz.display_fig()              
#  
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/fluxes_grid_obs', extension='.jpg')


 




# from collections import OrderedDict
# from dazer_methods import Dazer
# import numpy as np
#  
# dz = Dazer()
# dz.FigConf()
#  
# Grid_Values = OrderedDict()
#  
# Grid_Values = OrderedDict()
# Grid_Values['age']          = ['5.48']               
# Grid_Values['clus_mass']    = ['60000.0']#['12000.', '20000.', '60000.', '100000.', '200000.'] 
# Grid_Values['zGas']         = ['0.0004', '0.004', '0.008']                     #['0.0001', '0.0004', '0.004', '0.008', '0.02', '0.05'] 
# Grid_Values['zStars']       = ['-2.1']  
#  
# # ['5.0', '5.48', '6.0']
# # ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
# # ['0.0004', '0.004', '0.008', '0.02']
# # ['-2.1']
#  
# data_folder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/Grid_data_vital/'
# 
# ax2 = dz.Axis.twinx()
# 
# for age in Grid_Values['age']:
#     for mass in Grid_Values['clus_mass']:
#         for zGas in Grid_Values['zGas']:                                        
#             for zStar in Grid_Values['zStars']:
#  
#                 name_root = 'TGrid' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
#                 file_address = data_folder + name_root + '.ovr'
#                  
#                 depth, Te, HeI, HeII = np.loadtxt(file_address, usecols = (0, 1, 8, 9), unpack = True)    
#                           
#                                      
#                 dz.data_plot(depth, Te, label = r'Z= {}'.format(zGas))
#                 
#                 print r'HeII/HeI,  Z = {}'.format(zGas)
#                 
#                 dz.data_plot(depth, HeII / HeI, label = r'HeII/HeI, Z = {}'.format(zGas), graph_axis=ax2, linestyle='--')
#                 
# ax2.axhline(y=0.5,linestyle=':', label = 'observational value = 0.92')
#                 
# ax2.legend()
 
# dz.Axis.set_xlim(0.01,10000)
# dz.Axis.set_ylim(1e-37,1e-22)
# # 
# # # dz.Axis.set_ylim(1e-9,1)
# dz.Axis.set_yscale('log')    
# dz.Axis.set_xscale('log')    
#  
# dz.FigWording(r'Depth (cm)', r'Temperature (K)', r'Cloud Temperature versus depth, Cluster mass 60000 $M\odot$, log(age) = 5.48', loc=1)
#  
# dz.display_fig()
#  
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/evolution_metallicity', extension='.jpg')


# from collections import OrderedDict
# from dazer_methods import Dazer
# import numpy as np
# 
# dz = Dazer()
# dz.FigConf()
# 
# Grid_Values = OrderedDict()
# 
# Grid_Values = OrderedDict()
# Grid_Values['age']          = ['5.48']               
# Grid_Values['clus_mass']    = ['20000.0', '60000.0', '100000.0']                   #['12000.', '20000.', '60000.', '100000.', '200000.'] 
# Grid_Values['zGas']         = ['0.004']                     #['0.0001', '0.0004', '0.004', '0.008', '0.02', '0.05'] 
# Grid_Values['zStars']       = ['-2.1']  
# 
# # ['5.0', '5.48', '6.0']
# # ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
# # ['0.0004', '0.004', '0.008', '0.02']
# # ['-2.1']
# 
# data_folder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/Grid_data_vital/'
# 
# for age in Grid_Values['age']:
#     for mass in Grid_Values['clus_mass']:
#         for zGas in Grid_Values['zGas']:                                        
#             for zStar in Grid_Values['zStars']:
# 
#                 name_root = 'TGrid' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
#                 file_address = data_folder + name_root + '.ovr'
#                 
#                 depth, Te = np.loadtxt(file_address, usecols = (0, 1), unpack = True)    
#                                 
#                 dz.data_plot(depth, Te, label = r'Cluster mass = {} $M\odot$'.format(mass))
# 
#                 
# 
# 
# # dz.Axis.set_xlim(0.01,10000)
# # dz.Axis.set_ylim(1e-37,1e-22)
# # # 
# # # # dz.Axis.set_ylim(1e-9,1)
# # dz.Axis.set_yscale('log')    
# # dz.Axis.set_xscale('log')    
# 
# dz.FigWording(r'Depth (cm)', r'Temperature (K)', 'Cloud Temperature versus depth, Z = 0.004, log(age) = 5.48', loc=1)
# 
# # dz.display_fig()
# 
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/evolution_mass', extension='.jpg')



# from collections import OrderedDict
# from dazer_methods import Dazer
# import numpy as np
#  
# dz = Dazer()
# dz.FigConf()
#  
# Grid_Values = OrderedDict()
#  
# Grid_Values = OrderedDict()
# Grid_Values['age']          = ['5.0', '5.48', '6.0']               
# Grid_Values['clus_mass']    = ['60000.0']                   #['12000.', '20000.', '60000.', '100000.', '200000.'] 
# Grid_Values['zGas']         = ['0.004']                     #['0.0001', '0.0004', '0.004', '0.008', '0.02', '0.05'] 
# Grid_Values['zStars']       = ['-2.1']  
#  
# # ['5.0', '5.48', '6.0']
# # ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
# # ['0.0004', '0.004', '0.008', '0.02']
# # ['-2.1']
#  
# data_folder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/Grid_data_vital/'
#  
# for age in Grid_Values['age']:
#     for mass in Grid_Values['clus_mass']:
#         for zGas in Grid_Values['zGas']:                                        
#             for zStar in Grid_Values['zStars']:
#  
#                 name_root = 'TGrid' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
#                 file_address = data_folder + name_root + '.ovr'
#                  
#                 depth, Te = np.loadtxt(file_address, usecols = (0, 1), unpack = True)    
#                                  
#                 dz.data_plot(depth, Te, label = 'log(Age) = {}'.format(age))
#  
#                  
#  
#  
# # dz.Axis.set_xlim(0.01,10000)
# # dz.Axis.set_ylim(1e-37,1e-22)
# # # 
# # # # dz.Axis.set_ylim(1e-9,1)
# # dz.Axis.set_yscale('log')    
# # dz.Axis.set_xscale('log')    
#  
# dz.FigWording(r'Depth (cm)', r'Temperature (K)', r'Cloud Temperature versus depth, Cluster mass = 60000.0  $M\odot$, Z = 0.004', loc=1)
#  
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/evolution_age', extension='.jpg')

