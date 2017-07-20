import os
import numpy    as np
import pyneb    as pn
import pandas   as pd
import pyCloudy as pc
import matplotlib.pyplot as plt
from collections import OrderedDict
from pyCloudy.utils.physics import abund_Asplund_2009
from sympy.physics.units import luminosity
from pyCloudy.utils.astro import conv_arc
from dazer_methods import Dazer

dz = Dazer()
dz.FigConf()

diags       = pn.Diagnostics()
O3          = pn.Atom('O', 3)
S2, S3, S4  = pn.Atom('S', 2), pn.Atom('S', 3), pn.Atom('S', 4)

def lines_to_extract(ScriptFolder):

    #Emision lines to store
    emission_lines_list = [
                    'H  1  6562.81A',
                    'H  1  4861.33A',
                    'He 2  4685.64A',
                    'He 2  4541.46A',
                    'He 1  3888.63A',
                    'He 1  4026.20A',
                    'He 1  4471.49A',
                    'He 1  5875.64A',
                    'He 1  6678.15A',
                    'He 1  7065.22A',
                    'O  2  3726.03A',
                    'O  2  3728.81A',
                    'O  3  4958.91A',
                    'O  3  5006.84A',
                    'BLND  4363.00A',
                    'O  1  6300.30A',
                    'S  2  6716.44A',
                    'S  2  6730.82A',
                    'S  3  9068.62A',
                    'S  3  9530.62A',
                    'S  3  6312.06A',
                    'S  3  18.7078m',
                    'S  4  10.5076m',
                    'Cl 2  9123.60A',
                    'Cl 3  5517.71A',
                    'Cl 3  5537.87A',
                    'Cl 3  8433.66A',
                    'Cl 3  8480.86A',
                    'Cl 4  7530.54A',
                    'Cl 4  8045.63A',
                    'N  2  6548.05A',
                    'N  2  6583.45A',
                    'BLND  5755.00A',
                    'Ar 3  7135.79A',
                    'Ar 3  7751.11A',
                    'Ar 4  4711.26A',
                    'Ar 4  4740.12A'
                         ]         
    save_script(ScriptFolder + "lines.dat", emission_lines_list)

    return


#Simulation folder

def save_script(scriptAddress, lines_list):
    
    #Save list to text file
    with open(scriptAddress, 'w') as f:
        for line in lines_list:
            f.write(line + '\n')
            
    return

def import_popstar_data(Model_dict, den):
    
    FilesFolder                     = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/' 
    
    if den == 1:
        TableAddressn = 'mnras0403-2012-SD1_clusterTable1_10cm3.txt'
    elif den == 2:
        TableAddressn = 'mnras0403-2012-SD2_clusterTable2_100cm3.txt'
           
    Frame_MetalsEmission            = pd.read_csv(FilesFolder + TableAddressn, delim_whitespace = True)
    
    nH                              = den**2  #cm^-3
    c                               = 29979245800.0         #cm/s
    pc_to_cm                        = 3.0856776e18          #cm/pc
    
    Frame_MetalsEmission['logR_cm'] = np.log10(Frame_MetalsEmission['logR'] * pc_to_cm)
    Frame_MetalsEmission['Q']       = np.log10(np.power(10, Frame_MetalsEmission['logU']) * 4 * np.pi * c * nH * np.power(Frame_MetalsEmission['logR'] * pc_to_cm, 2))
    
    return Frame_MetalsEmission

#Folder where we run/save data

def make_mask_slit(arcsec, M_sphere, ap_center=[0., 0.], ap_size=[1., 1.]):
    """
    This returns a mask (values between 0. and 1.) to be multiplied to the image to take the flux passing through an aperture.
    An pc.C3D object named M_sphere must exist outside theis function
    """

    x_arc = arcsec(M_sphere.cub_coord.x_vec)
    y_arc = arcsec(M_sphere.cub_coord.y_vec)
    z_arc = arcsec(M_sphere.cub_coord.z_vec)
        
    X, Y = np.meshgrid(y_arc, x_arc)
    bool_mask = ((X > ap_center[0] - ap_size[0]/2.) & 
            (X <= ap_center[0] + ap_size[0]/2.) & 
            (Y > ap_center[1] - ap_size[1]/2.) & 
            (Y <= ap_center[1] + ap_size[1]/2.))
        
    mask = np.zeros_like(X)
    mask[bool_mask] = 1.0
    return mask

def make_mask_circle(arcsec, M_sphere):

    x_arc = arcsec(M_sphere.cub_coord.x_vec)
    y_arc = arcsec(M_sphere.cub_coord.y_vec)
    z_arc = arcsec(M_sphere.cub_coord.z_vec)

    X, Y = np.meshgrid(y_arc, x_arc)
    
    mask_center     = (0.25**2>(X-0)**2+(Y-0)**2)
    mask_sideA      = (0.20**2>(X-0.75)**2+(Y+0.25)**2)
    mask_sideB      = (0.20**2>(X+0.65)**2+(Y-0.10)**2)
    mask_sideC      = (0.10**2>(X+0.45)**2+(Y+0.30)**2)
    mask_sideD      = (0.10**2>(X-0.35)**2+(Y-0.30)**2)
    mask_sideE      = (0.20**2>(X-0.35)**2+(Y+0.65)**2)
    
    mask_circle     = np.zeros_like(X)
    mask_circle[mask_sideE | mask_sideD | mask_sideC | mask_sideB |mask_sideA | mask_center] = 1.0
#     mask_circle[mask_center] = 1.0

    return mask_circle

def extract_fluxes_pure_slits(grid_data, mask):
    
    lin_dict = OrderedDict()
    
    # Hbeta is computed for the whole object and throught the aperture
    lin_dict['Hb_tot']    = (grid_data.get_emis('H__1_486133A')*grid_data.cub_coord.cell_size).sum()
    lin_dict['Hb_slit']   = ((grid_data.get_emis('H__1_486133A')*grid_data.cub_coord.cell_size).sum(1) * mask).sum()
    
    for label in grid_data.m[0].emis_labels:
        I_tot = (grid_data.get_emis(label).sum()*grid_data.cub_coord.cell_size) / lin_dict['Hb_tot']
        I_slit = ((grid_data.get_emis(label).sum(1) * mask).sum()*grid_data.cub_coord.cell_size) / lin_dict['Hb_slit']
        lin_dict[label + '_slit'] = I_slit
        lin_dict[label + '_tot'] = I_tot
        #print('line: {0:12s} I/Ib Total: {1:6.4f} I/Ib Slit: {2:6.4f} Delta: {3:4.1f}%'.format(label, I_tot, I_slit, (I_slit-I_tot)/I_tot*100))
    
    return lin_dict

def extract_fluxes_combSlits(grid_dataB, grid_dataS, maskB, maskS):
    
    lin_dict = OrderedDict()
    
    # Hbeta is computed for the whole object and throught the aperture
    Hb_slit_big = ((grid_dataB.get_emis('H__1_486133A') * grid_dataB.cub_coord.cell_size).sum(1) * maskB).sum()
    Hb_slit_small = ((grid_dataS.get_emis('H__1_486133A') * grid_dataS.cub_coord.cell_size).sum(1) * maskS).sum()
    
    lin_dict['Hb_comb'] = Hb_slit_big, Hb_slit_small
        
    for label in grid_dataB.m[0].emis_labels:
        I_big = ((grid_dataB.get_emis(label).sum(1) * maskB).sum()*grid_dataB.cub_coord.cell_size) / Hb_slit_big
        I_small = ((grid_dataS.get_emis(label).sum(1) * maskS).sum()*grid_dataS.cub_coord.cell_size) / Hb_slit_small
        lin_dict[label + '_comb'] = I_big + I_small
        #print label, I_big, I_small
        #print('line: {0:12s} I/Ib Total: {1:6.4f} I/Ib Slit: {2:6.4f} Delta: {3:4.1f}%'.format(label, I_tot, I_slit, (I_slit-I_tot)/I_tot*100))
    
    return lin_dict

def plotting_the_mask(masks, arcsec, M_sphere):

    x_arc = arcsec(M_sphere.cub_coord.x_vec)
    y_arc = arcsec(M_sphere.cub_coord.y_vec)
    z_arc = arcsec(M_sphere.cub_coord.z_vec)

    X, Y = np.meshgrid(y_arc, x_arc)
    
    #New data                   
    dz.Axis.imshow(bigCloud_sphere.get_emis('S__3_906862A').sum(0))
    np.sum(masks)
    
    mask_contour = np.zeros_like(X)
    mask_contour[masks] = 1.0
    
    #print bigCloud_sphere.get_emis('S__4_105070M').sum(0)* masks
    
    dz.Axis.contour(mask_contour, colors='orange', linewidths=0.5)

    dz.FigWording(r'x', r'y', r'Artificial slit superposition on pyCloudy emissivity sphere ' + r'($[SIII]9069\AA$)')
     
    dz.display_fig()

   
#     for mask in masks:
#         plt.contour(mask)
       
    #plt.colorbar()
    #dz.display_fig()

    return
    
def calculate_abundances(lines_dict, extensions = ['tot', 'slit']):
    
    abun_dict = OrderedDict()
    
    for ext in extensions:
        Hbeta                               = lines_dict['Hb_' + ext]
        SII_6716A, SII_6730A                = lines_dict['S__2_671644A' + '_' + ext], lines_dict['S__2_673082A' + '_' + ext]
        SIII_9069A, SIII_9531A, SIII_6312A  = lines_dict['S__3_906862A' + '_' + ext], lines_dict['S__3_953062A' + '_' + ext], lines_dict['S__3_631206A' + '_' + ext]
        SIV_10m                             = lines_dict['S__4_105070M' + '_' + ext]
        OIII_4959A, OIII_5007A, OIII_4363A  = lines_dict['O__3_495891A' + '_' + ext], lines_dict['O__3_500684A' + '_' + ext], lines_dict['BLND_436300A' + '_' + ext]
                
        TOIII, NSII = diags.getCrossTemDen('[OIII] 4363/5007+', '[SII] 6731/6716', OIII_4363A/(OIII_4959A+OIII_5007A), SII_6730A/SII_6716A)
        
        TSIII, NSII = diags.getCrossTemDen('[SIII] 6312/9200+', '[SII] 6731/6716', SIII_6312A/(SIII_9069A+SIII_9531A), SII_6730A/SII_6716A)
    
        S2_abund    = S2.getIonAbundance(SII_6730A, tem=TSIII, den=NSII, wave=6731, Hbeta=1)
        S3_abund    = S3.getIonAbundance(SIII_9531A, tem=TSIII, den=NSII, wave=9531, Hbeta=1) 
        S4_abund    = S4.getIonAbundance(SIV_10m, tem=TOIII, den=NSII, wave=105000, Hbeta=1)
        
        S_abund = S2_abund + S3_abund + S4_abund
        
        S_abund_log = 12 + np.log10(S_abund)
        
        abun_dict['S_' + ext] = np.log10(S_abund)
            
    return abun_dict

simu_folder = '/home/vital/Dropbox/Astrophysics/Seminars/TestingPycloudy/'

#Constant for the calculations
c           = 29979245800.0  #cm/s
pc_to_cm    = 3.0856776e18   #cm/pc
dist_big    = 3.888e21 * 600  #cm
cube_size   = 201

pc.config.cloudy_exe = '/home/vital/Cloudy/source/cloudy.exe'

Grid_Values = OrderedDict() 
Grid_Values['age']          = ['5.0']         
Grid_Values['clus_mass']    = ['12000.0']    
Grid_Values['zGas']         = ['0.02']       
Grid_Values['zStars']       = ['-2.1']        
# Grid_Values['radious']    = ['8.0', '9.0', '10.0',  '10.5', '11.0',  '11.5', '12.0',  '12.5', '13.0',  '13.5', '14.0', '14.5', '15.0', '15.5', '16.0', '16.5', '17.0', '17.5', '18.0']
Grid_Values['radious']      = ['8.0', '9.0', '10.0',  '10.5', '11.0',  '11.5', '12.0',  '12.5', '13.0',  '13.5', '14.0', '14.5', '15.5', '16.0', '16.5', '17.0', '17.5', '18.0']

#Define density of the clouds (only 10 and 100 available in grids)
Grid_Values['den_big']      = 1
Grid_Values['den_small']    = 2
transmitted_ext             = '_transmitted_SED.txt'
                         
#Generate the scripts with the lines we want to print the flux
lines_to_extract(simu_folder)

#Get physical data from Manjon tables
df_Popstar = import_popstar_data(Grid_Values, den=Grid_Values['den_big'])              

#Loop through all the conditions
Model_dict = OrderedDict() 
for age in Grid_Values['age']:
    for mass in Grid_Values['clus_mass']:
        for zGas in Grid_Values['zGas']:                                        
            for zStar in Grid_Values['zStars']:
                
                #Script name root
                name_big = 'bigCloud' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
                name_big_trasnmit = name_big + transmitted_ext
                
                #Index grid point in popstar
                index       = (df_Popstar["Z"] == float(zGas)) & (df_Popstar["M_Msun"] == float(mass)) & (df_Popstar["t"] == float(age))
                
                #Physical parameters
                Q_H         = df_Popstar.loc[index, 'Q'].values[0]
                logR        = df_Popstar.loc[index, 'logR_cm'].values[0]
                phi_H       = np.log10((10.0**Q_H) / (4 * np.pi * (10**logR)**2))
                SED_params  = ('log age = {}'.format(age), 'log z = {}'.format(float(Grid_Values['zStars'][0])))
                metals_frac = str(float(zGas) / 0.02)
                
                #Generate the big cloud script
                bigCloud_sim = pc.CloudyInput(simu_folder + name_big)    
                bigCloud_sim.set_star('table stars "spkroz0001z05stellar.mod"', SED_params = SED_params, lumi_unit = 'phi(H)', lumi_value = phi_H)            
                bigCloud_sim.set_radius(r_in=logR)
                bigCloud_sim.set_cste_density(Grid_Values['den_big'])
                bigCloud_sim.set_abund(ab_dict = abund_Asplund_2009.copy(), metalsgrains = metals_frac)
                bigCloud_sim.set_stop(('temperature  8000.0'))
                bigCloud_sim.set_other(('grains ISM'))
                bigCloud_sim.set_distance(dist=dist_big/pc_to_cm/1000, unit='kpc', linear=True)
                bigCloud_sim.set_other(('cosmic rays background'))
                bigCloud_sim.set_other(('CMB'))
                bigCloud_sim.set_iterate(2)
                bigCloud_sim.set_other(('save last transmitted continuum file = "{}"'.format(transmitted_ext)))
                bigCloud_sim.read_emis_file('lines.dat')
                
                bigCloud_sim.print_input(to_file = True, verbose = False)
                                       
                #Display input code
                bigCloud_sim.print_input(verbose=False)
                
                #Run the model
                #bigCloud_sim.run_cloudy(dir_=simu_folder)
                
                #Read the simulation data
                bigCloud_output = pc.CloudyModel(simu_folder + name_big, read_emis=True)
                #bigCloud_output.print_stats()
                
                #Generate 3D grid
                bigCloud_sphere = pc.C3D(bigCloud_output, dims=cube_size, center=True, n_dim=1)
                 
                arcsec          = lambda cm: conv_arc(dist=dist_big/pc_to_cm/1000, dist_proj=cm)
                mask            = make_mask_slit(arcsec, bigCloud_sphere, ap_center=[0, 0], ap_size=[50, 1.5]) #ap_size=[50, 1.5]
                mask_cirleB     = make_mask_circle(arcsec, bigCloud_sphere) #ap_size=[50, 1.5]
                mask_big        = ~np.logical_not(mask) & np.logical_not(mask_cirleB)
                mask_small      = ~np.logical_not(mask_cirleB)
                
                #plotting_the_mask(mask_big, arcsec, bigCloud_sphere)
                
                #Calculate abundance
                big_lines_dict = extract_fluxes_pure_slits(bigCloud_sphere, mask_big)
                big_abund_dict = calculate_abundances(big_lines_dict)
                     
                print 'Big abund', big_abund_dict['S_tot'], big_abund_dict['S_slit'] 
                 
                dz.data_plot(0.0, big_abund_dict['S_slit'], label = 'First cloud abundance', markerstyle = 'o')
 
                #Plot area and mask
                #plotting_the_mask(mask_small, arcsec, bigCloud_sphere)
                 
                for radius in Grid_Values['radious']:
                      
                    #Script root name
                    name_small      = name_big.replace('bigCloud', 'smallCloud') + '_rad{}'.format(radius)
                    print '-----Running small model: {}'.format(name_small)
                                                                 
                    #Name for input radiation file
                    input_SED_line  = 'table read file = "{}"'.format(name_big_trasnmit) 
                       
                    dist_small = (dist_big - 10**float(radius))/pc_to_cm/1000
                       
                    smallCloud_sim  = pc.CloudyInput(simu_folder + name_small) 
                    smallCloud_sim.set_star(input_SED_line, SED_params=('scale={}'.format(1)),  lumi_unit = '//', lumi_value = 0.0)            
                    smallCloud_sim.set_radius(r_in=float(radius))
                    smallCloud_sim.set_distance(dist=dist_small, unit='kpc', linear=True)
                    smallCloud_sim.set_cste_density(Grid_Values['den_small'])
                    smallCloud_sim.set_abund(ab_dict = abund_Asplund_2009.copy(), metalsgrains = metals_frac)
                    smallCloud_sim.set_other(('grains ISM'))
                    smallCloud_sim.set_other(('cosmic rays background'))
                    smallCloud_sim.set_other(('CMB'))
                    smallCloud_sim.set_iterate(2)                                           
                    smallCloud_sim.read_emis_file('lines.dat')                                             
     
                    #Display input code
                    smallCloud_sim.print_input(verbose=False)
     
                    #Run the model
                    #smallCloud_sim.run_cloudy(dir_=simu_folder[0:-1])
                         
                    #Read the simulation data
                    smallCloud_output = pc.CloudyModel(simu_folder + name_small)
                    #smallCloud_output.print_stats()
                          
                    smallCloud_sphere = pc.C3D(smallCloud_output, dims=cube_size, center=True, n_dim=1)
  
                    arcsec          = lambda cm: conv_arc(dist=dist_small, dist_proj=cm)
                    mask_cirleB     = make_mask_circle(arcsec, smallCloud_sphere) #ap_size=[50, 1.5]
                    mask_small      = ~np.logical_not(mask_cirleB)                    
                      
                    #Calculate abundance
                    small_lines_dict = extract_fluxes_combSlits(bigCloud_sphere, smallCloud_sphere, mask_big, mask_small)
                    small_abund_dict = calculate_abundances(small_lines_dict, extensions=['comb'])
                    print 'Small abund rad {}'.format(radius), small_abund_dict['S_comb']
                    dz.data_plot(float(radius), small_abund_dict['S_comb'], label = 'Secondary clouds abundance', color='red', markerstyle = 'o')
 
#                     arcsec          = lambda cm: conv_arc(dist=dist_small, dist_proj=cm)
#                     mask_cirleB     = make_mask_circle(arcsec, smallCloud_sphere) #ap_size=[50, 1.5]
#                     mask_small      = ~np.logical_not(mask_cirleB)
#                      
#                     #Calculate abundance
#                     small_lines_dict = extract_fluxes_pure_slits(smallCloud_sphere)
#                     small_abund_dict = calculate_abundances(small_lines_dict)
                      
   
#                     print 'Small abund rad {}'.format(radius), small_abund_dict['S_tot'], small_abund_dict['S_slit'] 


dz.FigWording(r'log(radious) (cm)', r'log(S/H)', 'Sulfur abundance evolution with high density clumps')
 
dz.display_fig()


print 'Data generated'          
                
