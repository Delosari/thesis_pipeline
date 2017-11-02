import pyneb as pn
import numpy as np
from scipy import interpolate
from scipy.ndimage.interpolation import map_coordinates
from bisect import bisect_left
from timeit import default_timer as timer

def bilinear_interpolator_axis(x, y, x_range, y_range, data_grid):
     
    i = bisect_left(x_range, x) - 1
    j = bisect_left(y_range, y) - 1
         
    x1, x2      = x_range[i:i + 2]
    y1, y2      = y_range[j:j + 2]
    
    z11, z12    = data_grid[j][i:i + 2]
    z21, z22    = data_grid[j + 1][i:i + 2]    
    
    inter_value = (z11 * (x2 - x) * (y2 - y) +
                    z21 * (x - x1) * (y2 - y) +
                    z12 * (x2 - x) * (y - y1) +
                    z22 * (x - x1) * (y - y1)) / ((x2 - x1) * (y2 - y1))    
 
    return inter_value

He1     = pn.RecAtom('He', 1)
Te, ne  = 10550.0, 155.0
lines   = np.array([4026.0, 4471.0, 5876.0, 6678.0])

min_den, max_den, step_den  = 0, 1000, 5 
den_interval                = np.arange(min_den, max_den, step_den)
den_interval[0]             = 1
min_tem, max_tem, step_tem  = 7000, 20000, 50 
tem_interval                = np.arange(min_tem, max_tem, step_tem)

He_emis_grid = np.empty((tem_interval.shape[0], den_interval.shape[0], lines.shape[0])) 
    
for i in range(lines.shape[0]):
    He_emis_grid[:, :, i] = He1.getEmissivity(tem_interval, den_interval, wave=lines[i], product=True)

start = timer()   
bilinear_manual_axis = bilinear_interpolator_axis(ne, Te, den_interval, tem_interval, He_emis_grid)
end = timer()
time_new = end - start
print 'new method', time_new

start = timer()   
for i in range(lines.shape[0]):
    He_emis_grid[:, :, i] = He1.getEmissivity(tem_interval, den_interval, wave=lines[i], product=True)
end = timer()
time_old = end - start
print 'Old method', time_old

print 'ratio', time_new/time_old


print bilinear_manual_axis
print He1.getEmissivity(Te, ne, wave=lines[0]), He1.getEmissivity(Te, ne, wave=lines[1]), He1.getEmissivity(Te, ne, wave=lines[2]), He1.getEmissivity(Te, ne, wave=lines[3])

# bilinear_manual_axis = bilinear_interpolator_axis(Te, ne, tem_interval, den_interval, He_emis_grid)

# inter_values = np.empty(lines.shape[0])
# for i in range(lines.shape[0]):
#     f_rec = interpolate.RectBivariateSpline(tem_interval, den_interval, He_emis_grid[:,:,i])
#     inter_values[i] = f_rec(Te, ne)[0][0]
#     
# print 'Interpolated linear', bilinear_manual_axis
# print 'Interpolated Scipy',  inter_values
# print 'True values', He1.getEmissivity(Te, ne, wave=lines[0]), He1.getEmissivity(Te, ne, wave=lines[1]), He1.getEmissivity(Te, ne, wave=lines[2])


# print 'Intervals'
# print tem_interval
# print den_interval
# 
# print
# print He_emis_grid[0,0,0]
# print He1.getEmissivity(7000, 1, wave=lines[0])
# print 
# 
# print
# print He_emis_grid[1,0,0]
# print He1.getEmissivity(7100, 1, wave=lines[0])
# print 
# 
# print
# print He_emis_grid[0,1,0]
# print He1.getEmissivity(7000, 10, wave=lines[0])
# print 


# import numpy as np
# from scipy.ndimage.interpolation import map_coordinates
# from scipy import interpolate
# from bisect import bisect_left
# 
# #Function to assign a grid value according to the coordinates
# def pressure_func(temp, den, factor = 1):
#     return factor * den * temp
# 
# def bilinear_interpolator(x, y, x_range, y_range, data_grid):
#     
#     #Manual interpolation
#     i = bisect_left(x_range, x) - 1
#     j = bisect_left(y_range, y) - 1
#     
#     x1, x2      = x_range[i:i + 2]
#     y1, y2      = y_range[j:j + 2]
#     z11, z12    = data_grid[:,:, 0][j][i:i + 2]
#     z21, z22    = data_grid[:,:, 0][j + 1][i:i + 2]
#     
#     inter_value = (z11 * (x2 - Te) * (y2 - ne) +
#                     z21 * (Te - x1) * (y2 - ne) +
#                     z12 * (x2 - Te) * (ne - y1) +
#                     z22 * (Te - x1) * (ne - y1)) / ((x2 - x1) * (y2 - y1))    
# 
#     return inter_value
# 
# def bilinear_interpolator_axis(x, y, x_range, y_range, data_grid):
#     
#     #Manual interpolation
#     i = bisect_left(x_range, x) - 1
#     j = bisect_left(y_range, y) - 1
#     
#     x1, x2      = x_range[i:i + 2]
#     y1, y2      = y_range[j:j + 2]
#     z11, z12    = data_grid[j][i:i + 2]
#     z21, z22    = data_grid[j + 1][i:i + 2]
#     
#     inter_value = (z11 * (x2 - Te) * (y2 - ne) +
#                     z21 * (Te - x1) * (y2 - ne) +
#                     z12 * (x2 - Te) * (ne - y1) +
#                     z22 * (Te - x1) * (ne - y1)) / ((x2 - x1) * (y2 - y1))    
# 
#     return inter_value
# 
# #Define the x and y ranges and the size of z
# temp_interval   = np.arange(300, 350, 10)
# den_interval    = np.arange(1.0, 1.5, 0.10)
# num_gases       = 3
# Te, ne          = 315, 1.15
# 
# #Generate the data cube and fill it with data
# data_grid = np.zeros((temp_interval.shape[0], den_interval.shape[0], num_gases)) 
# for i in range(len(temp_interval)):
#     for j in range(len(den_interval)):
#         data_grid[i,j,0] = pressure_func(1, temp_interval[i], den_interval[j]) 
# 
# #For simplicity the values along the z axis are just a factor from the first one 
# data_grid[:,:, 1] = data_grid[:,:, 0] * 2
# data_grid[:,:, 2] = data_grid[:,:, 0] * 3
# 
# f_l = interpolate.interp2d(temp_interval, den_interval, data_grid[:,:, 0], kind='linear')
# f_c = interpolate.interp2d(temp_interval, den_interval, data_grid[:,:, 0], kind='cubic')
# f_rec = interpolate.RectBivariateSpline(temp_interval, den_interval, data_grid[:,:, 0])
# bilinear_manual = bilinear_interpolator(Te, ne, temp_interval, den_interval, data_grid)
# bilinear_manual_axis = bilinear_interpolator_axis(Te, ne, temp_interval, den_interval, data_grid)
# 
# print '\n\nlinear',     f_l(Te, ne)
# print 'cubes',          f_c(Te, ne)
# print 'RectBiva',       f_rec(Te, ne)[0]
# print 'Manual inter',   bilinear_manual
# print 'True value',     ne * Te
# print 'Manual axis',    bilinear_manual_axis
# print 'True axis',      ne * Te * np.array([1,2,3])

  
# #Vector with the coordinates at which we want to interpolate. For simplicity: ((0,0,0),(0,0,1),(0,0,2))
# coord_vector = np.zeros((3,3))
# coord_vector[:,0] = 1
# coord_vector[:,1] = 1
# coord_vector[:,2] = np.arange(3)
# 
# #Perform the interpolation
# 
# print '\n\nInterpolation result', map_coordinates(data_grid, coord_vector, order=1)
# print 'Expected result', data_grid[1,1,0], data_grid[1,1,1], data_grid[1,1,2]


# import numpy as np
# from scipy.ndimage.interpolation import map_coordinates
# 
# #Function assigning the grid values as a function of x and y 
# def func(x, y):
#     return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2
# 
# #Grid of x and y
# grid_x, grid_y = np.mgrid[0:100, 0:100]
# 
# #Empty array for x, y and z
# data_grid = np.empty((grid_x.shape[0], grid_y.shape[0], 3))
# 
# #Generating random points
# points = np.random.rand(100, 2)
# values = func(points[:,0], points[:,1])
# 
# #Filling the Z axis (in this particular case all three z axis entries have the same value)
# for i in range(data_grid.shape[2]):
#     data_grid[:,:,i] = values * (i + 1.0)
#     print 'factor', (i + 1.0), data_grid[1,1,0]
# 
# print  data_grid[1,1,0]
# 
# value_array = np.empty((3,3))
# value_array[:,0] = 1
# value_array[:,1] = 1
# value_array[:,2] = np.arange(3)
# 
# print value_array
# print np.array(((1,1,0),(1,1,1),(1,1,2)))
# 
# #Interpolate at a given coordinate
# print map_coordinates(data_grid, np.array(((1,1,0),(1,1,1),(1,1,2))))
# print map_coordinates(data_grid, value_array)


# import pyneb as pn
# import numpy as np
# from scipy import interpolate
# from scipy.ndimage.interpolation import map_coordinates
# 
# He1 = pn.RecAtom('He', 1)
# Te, den = 10000.0, 100.0
# wave    = 5876.0
# lines   = np.array([4024.0, 5876.0, 6678.0])
# 
# min_den, max_den, step_den = 0, 1000, 10 
# den_interval = np.arange(min_den, max_den, step_den)
# den_interval[0] = 1
# min_tem, max_tem, step_tem = 7000, 20000, 100 
# tem_interval = np.arange(min_tem, max_tem, step_tem)
# 
# He_emis_grid = np.empty((tem_interval.shape[0], den_interval.shape[0], lines.shape[0])) 
# #He1.getEmissivity(tem_interval, den_interval, wave=wave, product=True)
# 
# print np.mgrid[0:1:100j, 0:1:200j]
# 
# for i in range(lines.shape[0]):
#     He_emis_grid[:, :, i] = He1.getEmissivity(tem_interval, den_interval, wave=wave, product=True)
# 
# print map_coordinates(He_emis_grid, coordinates = (Te - min_tem, den))


#print interpolate.griddata((tem_interval, den_interval), He_emis_grid, xi=(Te, den))

#         res = interpolate.griddata((self.temp.ravel(), self.log_dens.ravel()), enu.ravel(),
#                                    (temg, logd), method=method)

# import numpy as np
# import matplotlib.pyplot as plt
# import pyCloudy as pc
# 
# dir_ = '/home/vital/Desktop/tests_cloudy/'
# pc.config.cloudy_exe = '/home/vital/cloudy/source/cloudy.exe'
# 
# def make_model(name, radius):
#     Min = pc.CloudyInput('/home/vital/Desktop/tests_cloudy/{}_{}'.format(name, radius))
#     Min.set_BB(Teff=43600, lumi_unit='Q(H)', lumi_value=49.34)
#     Min.set_cste_density(4)
#     Min.set_radius(radius)
#     Min.set_abund(predef='ism', nograins=False)
#     Min.set_other(('Cosmic Rays Background'))
#     Min.print_input()
# 
# name = 'M1'
# for radius in np.linspace(13, 23,6):
#     make_model(name, radius)
# 
# pc.print_make_file(dir_)
# 
# pc.run_cloudy(dir_=dir_, n_proc=6, use_make=True)
# 
# Ms = pc.load_models(dir_ + '/M1_', read_emis=False)
# 
# for M in Ms:
#     print(M.model_name_s, M.out['Cloudy ends'])


# def make_varyZ(Z, folder_models):
#     Min = pc.CloudyInput('{}varyZ_{}'.format(folder_models, Z))
#     Min.set_BB(Teff=4e4, lumi_unit='Ionization parameter', lumi_value=-2)
#     Min.set_cste_density(0)
#     Min.set_stop(('zone = 1'))
#     Min.set_emis_tab(('O  3 5006.84A', 'H  1 4861.36A'))
#     Min.set_other(('metals {}'.format(Z), 
#                    'set dr 0', 
#                    'Cosmic Rays Background'))
#     Min.print_input()
# 
# for Z in np.arange(-2, 1.1, 0.25):
#     make_varyZ(Z, dir_)
# 
# pc.run_cloudy(dir_=dir_)
#  
# Ms = pc.load_models(dir_)
# Ms = sorted(Ms, key=lambda x:x.abund['O']) 
#      
# print Ms[0].emis_labels
 
# O3Hb = [M.get_emis_vol('O__3_500684A') / M.get_emis_vol('H__1_486136A') for M in Ms]
# OH = [M.abund['O'] for M in Ms]
# 
# f, ax = plt.subplots(figsize=(8,6))
# ax.plot(OH, O3Hb)
# ax.set_xlabel('log O/H')
# ax.set_ylabel(r'[OIII]/H$\beta$');
# 
# T0 = [M.T0 for M in Ms]
# f, ax = plt.subplots(figsize=(10,8))
# ax.plot(OH, np.log(T0))
# ax.set_xlabel('log O/H')
# ax.set_ylabel('log Te')
# 
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# import pyCloudy as pc
# 
# # Define verbosity to high level (will print errors, warnings and messages)
# pc.log_.level = 3
# 
# 
# # Define some parameters of the model:
# model_name      = 'Elemental grid'
# full_model_name = '{0}{1}'.format(dir_, model_name)
# 
# #Physical parameters
# dens    = 2.        #log cm-3
# Teff    = 45000.    #K
# qH      = 47.       #s-1
# r_min   = 0         #cm
# dist    = 1.26      #kpc
# 
# #These are the commands common to all the models (here only one ...)
# emis_tab = ['He 1  3888.63A',
#             'He 1  4026.20A',
#             'He 1  4471.49A',
#             'He 1  5875.64A',
#             'He 1  6678.15A',
#             'He 1  7065.22A']
# 
# # Defining the object that will manage the input file for Cloudy
# c_input = pc.CloudyInput(full_model_name)
# c_input.set_BB(Teff = Teff, lumi_unit = 'q(H)', lumi_value = qH)
# c_input.set_cste_density(dens)
# c_input.set_radius(r_in=r_min)
# c_input.set_emis_tab(emis_tab)  # better use read_emis_file(file) for long list of lines, where file is an external file.
# 
# # Tell pyCloudy where your cloudy executable is:
# pc.config.cloudy_exe = '/home/vital/cloudy/source/cloudy.exe'
# 
# pc.log_.timer('Starting Cloudy', quiet = True, calling = 'test1')
# c_input.run_cloudy()
# pc.log_.timer('Cloudy ended after seconds:', calling = 'test1')





# import                      pandas as pd
# import                      pyneb as pn
# from os                     import environ, chdir, system
# from numpy                  import log10 as nplog10, pi, power, loadtxt
# from collections            import OrderedDict
# from subprocess             import Popen, PIPE, Popen, STDOUT
# from dazer_methods          import Dazer
# from pyCloudy.utils.physics import abund_Asplund_2009
# 
# dz = Dazer()
# dz.FigConf()
# 
# diags       = pn.Diagnostics()
# O3          = pn.Atom('O', 3)
# S2, S3, S4  = pn.Atom('S', 2), pn.Atom('S', 3), pn.Atom('S', 4)
# 
# def import_popstar_data(Model_dict, den):
#     
#     FilesFolder                     = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/' 
#     
#     if den == 1:
#         TableAddressn = 'mnras0403-2012-SD1_clusterTable1_10cm3.txt'
#     elif den == 2:
#         TableAddressn = 'mnras0403-2012-SD2_clusterTable2_100cm3.txt'
#            
#     Frame_MetalsEmission            = pd.read_csv(FilesFolder + TableAddressn, delim_whitespace = True)
#     
#     nH                              = den**2  #cm^-3
#     c                               = 29979245800.0         #cm/s
#     pc_to_cm                        = 3.0856776e18          #cm/pc
#     
#     Frame_MetalsEmission['logR_cm'] = nplog10(Frame_MetalsEmission['logR'] * pc_to_cm)
#     Frame_MetalsEmission['Q']       = nplog10(power(10, Frame_MetalsEmission['logU']) * 4 * pi * c * nH * power(Frame_MetalsEmission['logR'] * pc_to_cm, 2))
# 
#     return Frame_MetalsEmission
# 
# def save_script(scriptAddress, lines_list):
#     
#     #Save list to text file
#     with open(scriptAddress, 'w') as f:
#         for line in lines_list:
#             f.write(line + '\n')
#             
#     return
# 
# def calculate_abundances(ScriptFolder, lines_file):
#      
#     SII_6716A, SII_6730A, SIII_9069A, SIII_9531A, SIII_6312A, SIV_10m  = loadtxt(ScriptFolder + lines_file, delimiter='\t', usecols=(17, 18, 19, 20, 21, 23), unpack=True)
#     
#     OIII_4959A, OIII_5007A, OIII_4363A = loadtxt(ScriptFolder + lines_file, delimiter='\t', usecols=(13, 14, 15), unpack=True)
#         
#     TOIII, NSII = diags.getCrossTemDen('[OIII] 4363/5007+', '[SII] 6731/6716', OIII_4363A/(OIII_4959A+OIII_5007A), SII_6730A/SII_6716A)
#     
#     TSIII, NSII = diags.getCrossTemDen('[SIII] 6312/9200+', '[SII] 6731/6716', SIII_6312A/(SIII_9069A+SIII_9531A), SII_6730A/SII_6716A)
#     
#     S2_abund    = S2.getIonAbundance(SII_6730A, tem=TSIII, den=NSII, wave=6731, Hbeta=1)
#     S3_abund    = S3.getIonAbundance(SIII_9531A, tem=TSIII, den=NSII, wave=9531, Hbeta=1) 
#     S4_abund    = S4.getIonAbundance(SIV_10m, tem=TOIII, den=NSII, wave=105000, Hbeta=1)
#     
#     S_abund = S2_abund + S3_abund + S4_abund
#     
#     S_abund_log = 12 + nplog10(S_abund)
#         
#     return nplog10(S_abund)
# 
# def lines_to_extract(ScriptFolder):
# 
#     #Emision lines to store
#     emission_lines_list = [
#                     'H  1  6562.81A',
#                     'H  1  4861.33A',
#                     'He 2  4685.64A',
#                     'He 2  4541.46A',
#                     'He 1  3888.63A',
#                     'He 1  4026.20A',
#                     'He 1  4471.49A',
#                     'He 1  5875.64A',
#                     'He 1  6678.15A',
#                     'He 1  7065.22A',
#                     'O  2  3726.03A',
#                     'O  2  3728.81A',
#                     'O  3  4958.91A',
#                     'O  3  5006.84A',
#                     'BLND  4363.00A',
#                     'O  1  6300.30A',
#                     'S  2  6716.44A',
#                     'S  2  6730.82A',
#                     'S  3  9068.62A',
#                     'S  3  9530.62A',
#                     'S  3  6312.06A',
#                     'S  3  18.7078m',
#                     'S  4  10.5076m',
#                     'Cl 2  9123.60A',
#                     'Cl 3  5517.71A',
#                     'Cl 3  5537.87A',
#                     'Cl 3  8433.66A',
#                     'Cl 3  8480.86A',
#                     'Cl 4  7530.54A',
#                     'Cl 4  8045.63A',
#                     'N  2  6548.05A',
#                     'N  2  6583.45A',
#                     'BLND  5755.00A',
#                     'Ar 3  7135.79A',
#                     'Ar 3  7751.11A',
#                     'Ar 4  4711.26A',
#                     'Ar 4  4740.12A'
#                          ]         
#      
#     save_script(ScriptFolder + "lines.dat", emission_lines_list)
# 
#     return
# 
# def cloudy_grid_node_script(ScriptFolder, data_dict):
#         
#     abund_database = abund_Asplund_2009.copy()    
#     
#     #Cloudy script
#     script_Lines = [#'set punch prefix {}'.format(Model_dict['Name']),
#                     'table star file="{}" log age= {} log z = {}'.format('spkroz0001z05stellar.mod', data_dict['age'], data_dict['zStars']),
#                     'Q(H) {}'.format(round(data_dict['Q'], 4)),
#                     'radius {}'.format(round(data_dict['R'], 4)),   
#                     'hden {}'.format(round(data_dict['den'])),
#                     'grains ISM',
#                     'metals and grains {}'.format(data_dict['Metals_frac']),             
#                     'CMB',
#                     'cosmic rays background',
#                     'iterate',
#                     'stop temperature 200',
#                     'element abundance aluminium -5.550',
#                     'element abundance argon -5.600',
#                     'element abundance boron -9.300',
#                     'element abundance beryllium -10.620',
#                     'element abundance carbon -3.570',
#                     'element abundance calcium -5.660',
#                     'element abundance chlorine -6.500',
#                     'element abundance cobalt -7.010',
#                     'element abundance chromium -6.360',
#                     'element abundance copper -7.810',
#                     'element abundance fluorine -7.440',
#                     'element abundance iron -4.500',
#                     'element abundance helium -1.070',
#                     'element abundance potassium -6.970',
#                     'element abundance lithium -10.950',
#                     'element abundance magnesium -4.400',
#                     'element abundance manganese -6.570',
#                     'element abundance nitrogen -4.170',
#                     'element abundance sodium -5.760',
#                     'element abundance neon -4.070',
#                     'element abundance nickel -5.780',
#                     'element abundance oxygen -3.310',
#                     'element abundance phosphorus -6.590',
#                     'element abundance sulphur -4.880',
#                     'element abundance scandium -8.850',
#                     'element abundance silicon -4.490',
#                     'element abundance titanium -7.050',
#                     'element abundance vanadium -8.070',
#                     'element abundance zinc -7.440',
#                     'save transmitted continuum file = "big_cloud_SED.txt" last',
#                     'save last radius ".rad" no hash',
#                     'save last continuum ".cont" units microns no hash',
#                     'save last physical conditions ".phy" no hash',
#                     'save last overview ".ovr" no hash',
#                     'save last heating ".heat" no hash',
#                     'save last cooling ".cool" no hash',
#                     'save last optical depth ".opd" no hash',
#                     'save last element hydrogen ".ele_H" no hash',
#                     'save last element helium ".ele_He" no hash',
#                     'save last element nitrogen ".ele_N" no hash',
#                     'save last element oxygen ".ele_O" no hash',
#                     'save last element argon ".ele_Ar" no hash',
#                     'save last element sulphur ".ele_S" no hash',
#                     'save last element chlorin ".ele_Cl" no hash',
#                     'save line list ".lin" "lines.dat" last no hash',
# #                     'save last lines emissivity ".emis" no hash',
# #                     'H  1  6562.81A',
# #                     'H  1  4861.33A',
# #                     'He 2  4685.64A',
# #                     'He 2  4541.46A',
# #                     'He 1  3888.63A',
# #                     'He 1  4026.20A',
# #                     'He 1  4471.49A',
# #                     'He 1  5875.64A',
# #                     'He 1  6678.15A',
# #                     'He 1  7065.22A',
# #                     'O  2  3726.03A',
# #                     'O  2  3728.81A',
# #                     'O  3  4958.91A',
# #                     'O  3  5006.84A',
# #                     'BLND  4363.00A',
# #                     'O  1  6300.30A',
# #                     'S  2  6716.44A',
# #                     'S  2  6730.82A',
# #                     'S  3  9068.62A',
# #                     'S  3  9530.62A',
# #                     'S  3  6312.06A',
# #                     'S  3  18.7078m',
# #                     'S  4  10.5076m',
# #                     'Cl 2  9123.60A',
# #                     'Cl 3  5517.71A',
# #                     'Cl 3  5537.87A',
# #                     'Cl 3  8433.66A',
# #                     'Cl 3  8480.86A',
# #                     'Cl 4  7530.54A',
# #                     'Cl 4  8045.63A',
# #                     'N  2  6548.05A',
# #                     'N  2  6583.45A',
# #                     'BLND  5755.00A',
# #                     'Ar 3  7135.79A',
# #                     'Ar 3  7751.11A',
# #                     'Ar 4  4711.26A',
# #                     'Ar 4  4740.12A',
# #                     'save grain extinction ".pdr_av"',
# #                     'save grain temperature ".pdr_temp"',
# #                     'save species densities ".pdr_pop"',
# #                     "SiO",
# #                     "Si+",
# #                     "Si",
# #                     "CO",
# #                     "C+",
# #                     "C",
# #                     "H2",
# #                     "H+",
# #                     "H",
# #                     "*temp",
# #                     "*AV",
# #                     "*depth",
# #                     "end",               
#                     ]
#     
#     save_script(ScriptFolder + data_dict['Name'] + '.in', script_Lines)
#        
#     return
# 
# def cloudy_grid_node_script_phi(ScriptFolder, data_dict):
#         
#     abund_database = abund_Asplund_2009.copy()    
#     
#     #Cloudy script
#     script_Lines = [#'set punch prefix {}'.format(Model_dict['Name']),
#                     'table star file="{}" log age= {} log z = {}'.format('spkroz0001z05stellar.mod', data_dict['age'], data_dict['zStars']),
#                     'phi(H) {}'.format(round(data_dict['phi'], 4)),
# #                     'radius {}'.format(round(data_dict['R'], 4)),   
#                     'hden {}'.format(round(data_dict['den_big'])),
#                     'grains ISM',
#                     'metals and grains {}'.format(data_dict['Metals_frac']),             
#                     'CMB',
#                     'cosmic rays background',
#                     'iterate',
#                     'stop temperature 10000',
#                     'element abundance aluminium -5.550',
#                     'element abundance argon -5.600',
#                     'element abundance boron -9.300',
#                     'element abundance beryllium -10.620',
#                     'element abundance carbon -3.570',
#                     'element abundance calcium -5.660',
#                     'element abundance chlorine -6.500',
#                     'element abundance cobalt -7.010',
#                     'element abundance chromium -6.360',
#                     'element abundance copper -7.810',
#                     'element abundance fluorine -7.440',
#                     'element abundance iron -4.500',
#                     'element abundance helium -1.070',
#                     'element abundance potassium -6.970',
#                     'element abundance lithium -10.950',
#                     'element abundance magnesium -4.400',
#                     'element abundance manganese -6.570',
#                     'element abundance nitrogen -4.170',
#                     'element abundance sodium -5.760',
#                     'element abundance neon -4.070',
#                     'element abundance nickel -5.780',
#                     'element abundance oxygen -3.310',
#                     'element abundance phosphorus -6.590',
#                     'element abundance sulphur -4.880',
#                     'element abundance scandium -8.850',
#                     'element abundance silicon -4.490',
#                     'element abundance titanium -7.050',
#                     'element abundance vanadium -8.070',
#                     'element abundance zinc -7.440',
#                     'save transmitted continuum file = "big_cloud_SED.txt" last',
#                     'save last radius ".rad" no hash',
#                     'save last continuum ".cont" units microns no hash',
#                     'save last physical conditions ".phy" no hash',
#                     'save last overview ".ovr" no hash',
#                     'save last heating ".heat" no hash',
#                     'save last cooling ".cool" no hash',
#                     'save last optical depth ".opd" no hash',
#                     'save last element hydrogen ".ele_H" no hash',
#                     'save last element helium ".ele_He" no hash',
#                     'save last element nitrogen ".ele_N" no hash',
#                     'save last element oxygen ".ele_O" no hash',
#                     'save last element argon ".ele_Ar" no hash',
#                     'save last element sulphur ".ele_S" no hash',
#                     'save last element chlorin ".ele_Cl" no hash',
#                     'save line list ".lin" "lines.dat" last no hash',
# #                     'save last lines emissivity ".emis" no hash',
# #                     'H  1  6562.81A',
# #                     'H  1  4861.33A',
# #                     'He 2  4685.64A',
# #                     'He 2  4541.46A',
# #                     'He 1  3888.63A',
# #                     'He 1  4026.20A',
# #                     'He 1  4471.49A',
# #                     'He 1  5875.64A',
# #                     'He 1  6678.15A',
# #                     'He 1  7065.22A',
# #                     'O  2  3726.03A',
# #                     'O  2  3728.81A',
# #                     'O  3  4958.91A',
# #                     'O  3  5006.84A',
# #                     'BLND  4363.00A',
# #                     'O  1  6300.30A',
# #                     'S  2  6716.44A',
# #                     'S  2  6730.82A',
# #                     'S  3  9068.62A',
# #                     'S  3  9530.62A',
# #                     'S  3  6312.06A',
# #                     'S  3  18.7078m',
# #                     'S  4  10.5076m',
# #                     'Cl 2  9123.60A',
# #                     'Cl 3  5517.71A',
# #                     'Cl 3  5537.87A',
# #                     'Cl 3  8433.66A',
# #                     'Cl 3  8480.86A',
# #                     'Cl 4  7530.54A',
# #                     'Cl 4  8045.63A',
# #                     'N  2  6548.05A',
# #                     'N  2  6583.45A',
# #                     'BLND  5755.00A',
# #                     'Ar 3  7135.79A',
# #                     'Ar 3  7751.11A',
# #                     'Ar 4  4711.26A',
# #                     'Ar 4  4740.12A',
# #                     'save grain extinction ".pdr_av"',
# #                     'save grain temperature ".pdr_temp"',
# #                     'save species densities ".pdr_pop"',
# #                     "SiO",
# #                     "Si+",
# #                     "Si",
# #                     "CO",
# #                     "C+",
# #                     "C",
# #                     "H2",
# #                     "H+",
# #                     "H",
# #                     "*temp",
# #                     "*AV",
# #                     "*depth",
# #                     "end",               
#                     ]
#     
#     save_script(ScriptFolder + data_dict['Name_big'] + '.in', script_Lines)
#        
#     return
# 
# def cloudy_grid_node_script_smallCloud(ScriptFolder, data_dict):
#             
#     #Cloudy script
#     script_Lines = [#'set punch prefix {}'.format(Model_dict['Name']),
#                     'table read file = "big_cloud_SED.txt" scale=1',
#                     #'ionization parameter {}'.format(Model_dict['u']),
#                     'radius {}'.format(data_dict['logR_cm'], 4),   
#                     'hden {}'.format(round(data_dict['den_small'])),
#                     'grains ISM',
#                     'metals and grains {}'.format(data_dict['Metals_frac']),             
#                     'CMB',
#                     'cosmic rays background',
#                     'iterate',
#                     #'stop temperature 200',
#                     'element abundance aluminium -5.550',
#                     'element abundance argon -5.600',
#                     'element abundance boron -9.300',
#                     'element abundance beryllium -10.620',
#                     'element abundance carbon -3.570',
#                     'element abundance calcium -5.660',
#                     'element abundance chlorine -6.500',
#                     'element abundance cobalt -7.010',
#                     'element abundance chromium -6.360',
#                     'element abundance copper -7.810',
#                     'element abundance fluorine -7.440',
#                     'element abundance iron -4.500',
#                     'element abundance helium -1.070',
#                     'element abundance potassium -6.970',
#                     'element abundance lithium -10.950',
#                     'element abundance magnesium -4.400',
#                     'element abundance manganese -6.570',
#                     'element abundance nitrogen -4.170',
#                     'element abundance sodium -5.760',
#                     'element abundance neon -4.070',
#                     'element abundance nickel -5.780',
#                     'element abundance oxygen -3.310',
#                     'element abundance phosphorus -6.590',
#                     'element abundance sulphur -4.880',
#                     'element abundance scandium -8.850',
#                     'element abundance silicon -4.490',
#                     'element abundance titanium -7.050',
#                     'element abundance vanadium -8.070',
#                     'element abundance zinc -7.440',
#                     'save transmitted continuum file = "big_cloud_SED.txt" last',
#                     'save last radius ".rad" no hash',
#                     'save last continuum ".cont" units microns no hash',
#                     'save last physical conditions ".phy" no hash',
#                     'save last overview ".ovr" no hash',
#                     'save last heating ".heat" no hash',
#                     'save last cooling ".cool" no hash',
#                     'save last optical depth ".opd" no hash',
#                     'save last element hydrogen ".ele_H" no hash',
#                     'save last element helium ".ele_He" no hash',
#                     'save last element nitrogen ".ele_N" no hash',
#                     'save last element oxygen ".ele_O" no hash',
#                     'save last element argon ".ele_Ar" no hash',
#                     'save last element sulphur ".ele_S" no hash',
#                     'save last element chlorin ".ele_Cl" no hash',
#                     'save line list ".lin" "lines.dat" last no hash',
# #                     'save last lines emissivity ".emis" no hash',
# #                     'H  1  6562.81A',
# #                     'H  1  4861.33A',
# #                     'He 2  4685.64A',
# #                     'He 2  4541.46A',
# #                     'He 1  3888.63A',
# #                     'He 1  4026.20A',
# #                     'He 1  4471.49A',
# #                     'He 1  5875.64A',
# #                     'He 1  6678.15A',
# #                     'He 1  7065.22A',
# #                     'O  2  3726.03A',
# #                     'O  2  3728.81A',
# #                     'O  3  4958.91A',
# #                     'O  3  5006.84A',
# #                     'BLND  4363.00A',
# #                     'O  1  6300.30A',
# #                     'S  2  6716.44A',
# #                     'S  2  6730.82A',
# #                     'S  3  9068.62A',
# #                     'S  3  9530.62A',
# #                     'S  3  6312.06A',
# #                     'S  3  18.7078m',
# #                     'S  4  10.5076m',
# #                     'Cl 2  9123.60A',
# #                     'Cl 3  5517.71A',
# #                     'Cl 3  5537.87A',
# #                     'Cl 3  8433.66A',
# #                     'Cl 3  8480.86A',
# #                     'Cl 4  7530.54A',
# #                     'Cl 4  8045.63A',
# #                     'N  2  6548.05A',
# #                     'N  2  6583.45A',
# #                     'BLND  5755.00A',
# #                     'Ar 3  7135.79A',
# #                     'Ar 3  7751.11A',
# #                     'Ar 4  4711.26A',
# #                     'Ar 4  4740.12A',
# #                     'save grain extinction ".pdr_av"',
# #                     'save grain temperature ".pdr_temp"',
# #                     'save species densities ".pdr_pop"',
# #                     "SiO",
# #                     "Si+",
# #                     "Si",
# #                     "CO",
# #                     "C+",
# #                     "C",
# #                     "H2",
# #                     "H+",
# #                     "H",
# #                     "*temp",
# #                     "*AV",
# #                     "*depth",
# #                     "end",               
#                     ]
#     save_script(ScriptFolder + data_dict['Name'] + '.in', script_Lines)
#        
#     return
# 
# def run_script(ScriptName, ScriptFolder, cloudy_address = '/home/vital/Cloudy/source/cloudy.exe', bins_folder = "/usr/sbin:/sbin:/home/vital/.my_bin:"):
#     
#     #Move to the script folder
#     chdir(ScriptFolder)
#     
#     #Adding the cloudy path to the environment
#     my_env = environ
#     my_env["PATH"] = bins_folder + my_env["PATH"] #This variable should be adapted to the computer
#        
#     #Preparing the command
#     Command = 'cloudy {}'.format(ScriptName[0:ScriptName.rfind('.')])
# 
#     print "--Launching command:"
#     print "  ", Command#, '@', ScriptFolder, '\n'
#     
#     #Run the command
#     p = Popen(Command, shell=True, stdout=PIPE, stderr=STDOUT, env=my_env)
# 
#     #Terminal output in terminal
#     if len(p.stdout.readlines()) > 0:
#         print '-- Code output wording\n'
#         for line in p.stdout.readlines():
#             print line
#             
#     return
# 
# #Set script name and location
# 
# ScriptFolder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/imposition_zones/'
# 
# #Dictionary to store the grid points
# Grid_Values = OrderedDict() 
# Grid_Values['age']          = ['6.0']         #['5.', '5.48','5.7','5.85','6.','6.1','6.18','6.24','6.3','6.35','6.4','6.44','6.48','6.51','6.54','6.57','6.6','6.63','6.65','6.68','6.7','6.72']
# Grid_Values['clus_mass']    = ['100000.0']    #['12000.', '20000.', '60000.', '100000.', '200000.'] 
# Grid_Values['zGas']         = ['0.004']       #['0.0001', '0.0004', '0.004', '0.008', '0.02', '0.05'] 
# Grid_Values['zStars']       = ['-2.1']        #['-2.1'] 
# 
# Grid_Values = OrderedDict() 
# Grid_Values['age']          = ['5.0']         
# Grid_Values['clus_mass']    = ['12000.0']    
# Grid_Values['zGas']         = ['0.02']       
# Grid_Values['zStars']       = ['-2.1']        
# Grid_Values['radious']      = ['8.0', '9.0', '10.0',  '10.5', '11.0',  '11.5', '12.0',  '12.5', '13.0',  '13.5', '14.0', '14.5', '15.0', '15.5', '16.0', '16.5', '17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']
# 
# #We have done this
# # ['5.0', '5.48', '6.0', '6.48', '6.72']
# # ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
# # ['0.0004', '0.004', '0.008', '0.02']
# # ['-2.1']
# #TGrid_Mass12000.0_age5.0_zStar-2.1_zGas0.02.lin
# 
# #Dictionary to store the simulations physical conditions
# Model_dict = OrderedDict()
# 
# #Set density of the model (only 10 and 100 available in grids)
# Model_dict['den_big'] = 1
# Model_dict['den_small'] = 2
#                          
# #Generate the scripts with the lines we want to print the flux
# lines_to_extract(ScriptFolder)
# 
# c = 29979245800.0         #cm/s
# pc_to_cm = 3.0856776e18   #cm/pc
# 
# Frame_MetalsEmission = import_popstar_data(Model_dict, den=Model_dict['den_big'])              
# 
# #Loop through all the conditions
# for age in Grid_Values['age']:
#     for mass in Grid_Values['clus_mass']:
#         for zGas in Grid_Values['zGas']:                                        
#             for zStar in Grid_Values['zStars']:
#                 
#                 Model_dict['Name_big']      = 'TGrid' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
#                 Model_dict['age']           = age
#                 Model_dict['zGas']          = zGas
#                 Model_dict['Metals_frac']   = str(float(zGas) / 0.02)
#                 Model_dict['zGas']          = zGas
#                 Model_dict['zStars']        = zStar
#                 
#                 index = (Frame_MetalsEmission["Z"] == float(zGas)) & (Frame_MetalsEmission["M_Msun"] == float(mass)) & (Frame_MetalsEmission["t"] == float(age))
#                 
#                 print '-Going for conditions: ', age, zGas, zStar, mass
#                 
#                 Model_dict['Q']             = Frame_MetalsEmission.loc[index, 'Q'].values[0]
#                 Model_dict['R']             = Frame_MetalsEmission.loc[index, 'logR_cm'].values[0]
#                 Model_dict['phi']           = nplog10((10.0**Model_dict['Q']) / (4 * pi * (10**Model_dict['R'])**2))
#     
#                 ScriptName = Model_dict['Name_big'] + '.in'
#                   
#                 #Generate the script
#                 cloudy_grid_node_script_phi(ScriptFolder, Model_dict)
#                       
#                 #Run the cloudy script
# #                 run_script(ScriptName, ScriptFolder)
#                 
#                 initial_sulfur_abund = calculate_abundances(ScriptFolder, Model_dict['Name_big'] + '.lin')
#                 print '--Sulfur abundance measured in initial cloud', initial_sulfur_abund, '\n'
#                  
# #                 lines_file                  = Model_dict['Name_big'] + '.lin'
# #                 
# #                 SII_6716A, SII_6730A, SIII_9069A, SIII_9531A  = loadtxt(ScriptFolder + lines_file, delimiter='\t', usecols=(17, 18, 19, 20), unpack=True)
# #                                 
# #                 S_ratio = (SII_6716A + SII_6730A) / (SIII_9069A + SIII_9531A)
# # 
# #                 U_predicted = -1.69 * S_ratio - 2.76
# # 
# #                 nH = Model_dict['den_small']**2  #cm^-3
#                 
#                 dz.data_plot(0.0, initial_sulfur_abund, label='First cloud sulfur abundance', markerstyle='o')
# 
#                  
#                 for radius in Grid_Values['radious']:
#                     Model_dict['logR_cm'] = radius
#                       
#                     Model_dict['Name'] = Model_dict['Name_big'].replace('TGrid', 'Small_Cloud') + '_rad' + radius
#                     
#                     #Generate the script
#                     cloudy_grid_node_script_smallCloud('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/imposition_zones/', Model_dict)
#                         
#                     #Run the cloudy script
#                     run_script(Model_dict['Name'] + '.in', '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/imposition_zones/')
#                       
#                     #Calculate the abundances
#                     sulfur_abund = calculate_abundances('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/imposition_zones/', Model_dict['Name'] + '.lin')
#                     
#                     dz.data_plot(radius, sulfur_abund, label='Second cloud abundance', markerstyle='o', color='red')
#                     
#                     print 'Sulfur abundance {} secondary cloud at radious {}: '.format(sulfur_abund, radius) 
# 
# dz.FigWording(r'log(radious) (cm)', r'log(S/H)', 'Evolution of sulfur abundance evolution with second cloud location')
#  
# dz.display_fig()
#                           
# print 'Data treated'