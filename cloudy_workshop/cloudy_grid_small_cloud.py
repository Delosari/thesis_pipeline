import                      pandas as pd
import                      pyneb as pn
from os                     import environ, chdir, system
from numpy                  import log10 as nplog10, pi, power, loadtxt
from collections            import OrderedDict
from subprocess             import Popen, PIPE, Popen, STDOUT
from dazer_methods          import Dazer
from pyCloudy.utils.physics import abund_Asplund_2009

dz = Dazer()
dz.FigConf()

diags       = pn.Diagnostics()
O3          = pn.Atom('O', 3)
S2, S3, S4  = pn.Atom('S', 2), pn.Atom('S', 3), pn.Atom('S', 4)

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
    
    Frame_MetalsEmission['logR_cm'] = nplog10(Frame_MetalsEmission['logR'] * pc_to_cm)
    Frame_MetalsEmission['Q']       = nplog10(power(10, Frame_MetalsEmission['logU']) * 4 * pi * c * nH * power(Frame_MetalsEmission['logR'] * pc_to_cm, 2))

    return Frame_MetalsEmission

def save_script(scriptAddress, lines_list):
    
    #Save list to text file
    with open(scriptAddress, 'w') as f:
        for line in lines_list:
            f.write(line + '\n')
            
    return

def calculate_abundances(ScriptFolder, lines_file):
     
    SII_6716A, SII_6730A, SIII_9069A, SIII_9531A, SIII_6312A, SIV_10m  = loadtxt(ScriptFolder + lines_file, delimiter='\t', usecols=(17, 18, 19, 20, 21, 23), unpack=True)
    
    OIII_4959A, OIII_5007A, OIII_4363A = loadtxt(ScriptFolder + lines_file, delimiter='\t', usecols=(13, 14, 15), unpack=True)
        
    TOIII, NSII = diags.getCrossTemDen('[OIII] 4363/5007+', '[SII] 6731/6716', OIII_4363A/(OIII_4959A+OIII_5007A), SII_6730A/SII_6716A)
    
    TSIII, NSII = diags.getCrossTemDen('[SIII] 6312/9200+', '[SII] 6731/6716', SIII_6312A/(SIII_9069A+SIII_9531A), SII_6730A/SII_6716A)
    
    S2_abund    = S2.getIonAbundance(SII_6730A, tem=TSIII, den=NSII, wave=6731, Hbeta=1)
    S3_abund    = S3.getIonAbundance(SIII_9531A, tem=TSIII, den=NSII, wave=9531, Hbeta=1) 
    S4_abund    = S4.getIonAbundance(SIV_10m, tem=TOIII, den=NSII, wave=105000, Hbeta=1)
    
    S_abund = S2_abund + S3_abund + S4_abund
    
    S_abund_log = 12 + nplog10(S_abund)
        
    return nplog10(S_abund)

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

def cloudy_grid_node_script(ScriptFolder, data_dict):
        
    abund_database = abund_Asplund_2009.copy()    
    
    #Cloudy script
    script_Lines = [#'set punch prefix {}'.format(Model_dict['Name']),
                    'table star file="{}" log age= {} log z = {}'.format('spkroz0001z05stellar.mod', data_dict['age'], data_dict['zStars']),
                    'Q(H) {}'.format(round(data_dict['Q'], 4)),
                    'radius {}'.format(round(data_dict['R'], 4)),   
                    'hden {}'.format(round(data_dict['den'])),
                    'grains ISM',
                    'metals and grains {}'.format(data_dict['Metals_frac']),             
                    'CMB',
                    'cosmic rays background',
                    'iterate',
                    'stop temperature 200',
                    'element abundance aluminium -5.550',
                    'element abundance argon -5.600',
                    'element abundance boron -9.300',
                    'element abundance beryllium -10.620',
                    'element abundance carbon -3.570',
                    'element abundance calcium -5.660',
                    'element abundance chlorine -6.500',
                    'element abundance cobalt -7.010',
                    'element abundance chromium -6.360',
                    'element abundance copper -7.810',
                    'element abundance fluorine -7.440',
                    'element abundance iron -4.500',
                    'element abundance helium -1.070',
                    'element abundance potassium -6.970',
                    'element abundance lithium -10.950',
                    'element abundance magnesium -4.400',
                    'element abundance manganese -6.570',
                    'element abundance nitrogen -4.170',
                    'element abundance sodium -5.760',
                    'element abundance neon -4.070',
                    'element abundance nickel -5.780',
                    'element abundance oxygen -3.310',
                    'element abundance phosphorus -6.590',
                    'element abundance sulphur -4.880',
                    'element abundance scandium -8.850',
                    'element abundance silicon -4.490',
                    'element abundance titanium -7.050',
                    'element abundance vanadium -8.070',
                    'element abundance zinc -7.440',
                    'save transmitted continuum file = "big_cloud_SED.txt" last',
                    'save last radius ".rad" no hash',
                    'save last continuum ".cont" units microns no hash',
                    'save last physical conditions ".phy" no hash',
                    'save last overview ".ovr" no hash',
                    'save last heating ".heat" no hash',
                    'save last cooling ".cool" no hash',
                    'save last optical depth ".opd" no hash',
                    'save last element hydrogen ".ele_H" no hash',
                    'save last element helium ".ele_He" no hash',
                    'save last element nitrogen ".ele_N" no hash',
                    'save last element oxygen ".ele_O" no hash',
                    'save last element argon ".ele_Ar" no hash',
                    'save last element sulphur ".ele_S" no hash',
                    'save last element chlorin ".ele_Cl" no hash',
                    'save line list ".lin" "lines.dat" last no hash',
#                     'save last lines emissivity ".emis" no hash',
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
#                     'Ar 4  4740.12A',
#                     'save grain extinction ".pdr_av"',
#                     'save grain temperature ".pdr_temp"',
#                     'save species densities ".pdr_pop"',
#                     "SiO",
#                     "Si+",
#                     "Si",
#                     "CO",
#                     "C+",
#                     "C",
#                     "H2",
#                     "H+",
#                     "H",
#                     "*temp",
#                     "*AV",
#                     "*depth",
#                     "end",               
                    ]
    
    save_script(ScriptFolder + data_dict['Name'] + '.in', script_Lines)
       
    return

def cloudy_grid_node_script_phi(ScriptFolder, data_dict):
        
    abund_database = abund_Asplund_2009.copy()    
    
    #Cloudy script
    script_Lines = [#'set punch prefix {}'.format(Model_dict['Name']),
                    'table star file="{}" log age= {} log z = {}'.format('spkroz0001z05stellar.mod', data_dict['age'], data_dict['zStars']),
                    'phi(H) {}'.format(round(data_dict['phi'], 4)),
#                     'radius {}'.format(round(data_dict['R'], 4)),   
                    'hden {}'.format(round(data_dict['den_big'])),
                    'grains ISM',
                    'metals and grains {}'.format(data_dict['Metals_frac']),             
                    'CMB',
                    'cosmic rays background',
                    'iterate',
                    'stop temperature 10000',
                    'element abundance aluminium -5.550',
                    'element abundance argon -5.600',
                    'element abundance boron -9.300',
                    'element abundance beryllium -10.620',
                    'element abundance carbon -3.570',
                    'element abundance calcium -5.660',
                    'element abundance chlorine -6.500',
                    'element abundance cobalt -7.010',
                    'element abundance chromium -6.360',
                    'element abundance copper -7.810',
                    'element abundance fluorine -7.440',
                    'element abundance iron -4.500',
                    'element abundance helium -1.070',
                    'element abundance potassium -6.970',
                    'element abundance lithium -10.950',
                    'element abundance magnesium -4.400',
                    'element abundance manganese -6.570',
                    'element abundance nitrogen -4.170',
                    'element abundance sodium -5.760',
                    'element abundance neon -4.070',
                    'element abundance nickel -5.780',
                    'element abundance oxygen -3.310',
                    'element abundance phosphorus -6.590',
                    'element abundance sulphur -4.880',
                    'element abundance scandium -8.850',
                    'element abundance silicon -4.490',
                    'element abundance titanium -7.050',
                    'element abundance vanadium -8.070',
                    'element abundance zinc -7.440',
                    'save transmitted continuum file = "big_cloud_SED.txt" last',
                    'save last radius ".rad" no hash',
                    'save last continuum ".cont" units microns no hash',
                    'save last physical conditions ".phy" no hash',
                    'save last overview ".ovr" no hash',
                    'save last heating ".heat" no hash',
                    'save last cooling ".cool" no hash',
                    'save last optical depth ".opd" no hash',
                    'save last element hydrogen ".ele_H" no hash',
                    'save last element helium ".ele_He" no hash',
                    'save last element nitrogen ".ele_N" no hash',
                    'save last element oxygen ".ele_O" no hash',
                    'save last element argon ".ele_Ar" no hash',
                    'save last element sulphur ".ele_S" no hash',
                    'save last element chlorin ".ele_Cl" no hash',
                    'save line list ".lin" "lines.dat" last no hash',
#                     'save last lines emissivity ".emis" no hash',
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
#                     'Ar 4  4740.12A',
#                     'save grain extinction ".pdr_av"',
#                     'save grain temperature ".pdr_temp"',
#                     'save species densities ".pdr_pop"',
#                     "SiO",
#                     "Si+",
#                     "Si",
#                     "CO",
#                     "C+",
#                     "C",
#                     "H2",
#                     "H+",
#                     "H",
#                     "*temp",
#                     "*AV",
#                     "*depth",
#                     "end",               
                    ]
    
    save_script(ScriptFolder + data_dict['Name_big'] + '.in', script_Lines)
       
    return

def cloudy_grid_node_script_smallCloud(ScriptFolder, data_dict):
            
    #Cloudy script
    script_Lines = [#'set punch prefix {}'.format(Model_dict['Name']),
                    'table read file = "big_cloud_SED.txt" scale=1',
                    #'ionization parameter {}'.format(Model_dict['u']),
                    'radius {}'.format(data_dict['logR_cm'], 4),   
                    'hden {}'.format(round(data_dict['den_small'])),
                    'grains ISM',
                    'metals and grains {}'.format(data_dict['Metals_frac']),             
                    'CMB',
                    'cosmic rays background',
                    'iterate',
                    #'stop temperature 200',
                    'element abundance aluminium -5.550',
                    'element abundance argon -5.600',
                    'element abundance boron -9.300',
                    'element abundance beryllium -10.620',
                    'element abundance carbon -3.570',
                    'element abundance calcium -5.660',
                    'element abundance chlorine -6.500',
                    'element abundance cobalt -7.010',
                    'element abundance chromium -6.360',
                    'element abundance copper -7.810',
                    'element abundance fluorine -7.440',
                    'element abundance iron -4.500',
                    'element abundance helium -1.070',
                    'element abundance potassium -6.970',
                    'element abundance lithium -10.950',
                    'element abundance magnesium -4.400',
                    'element abundance manganese -6.570',
                    'element abundance nitrogen -4.170',
                    'element abundance sodium -5.760',
                    'element abundance neon -4.070',
                    'element abundance nickel -5.780',
                    'element abundance oxygen -3.310',
                    'element abundance phosphorus -6.590',
                    'element abundance sulphur -4.880',
                    'element abundance scandium -8.850',
                    'element abundance silicon -4.490',
                    'element abundance titanium -7.050',
                    'element abundance vanadium -8.070',
                    'element abundance zinc -7.440',
                    'save transmitted continuum file = "big_cloud_SED.txt" last',
                    'save last radius ".rad" no hash',
                    'save last continuum ".cont" units microns no hash',
                    'save last physical conditions ".phy" no hash',
                    'save last overview ".ovr" no hash',
                    'save last heating ".heat" no hash',
                    'save last cooling ".cool" no hash',
                    'save last optical depth ".opd" no hash',
                    'save last element hydrogen ".ele_H" no hash',
                    'save last element helium ".ele_He" no hash',
                    'save last element nitrogen ".ele_N" no hash',
                    'save last element oxygen ".ele_O" no hash',
                    'save last element argon ".ele_Ar" no hash',
                    'save last element sulphur ".ele_S" no hash',
                    'save last element chlorin ".ele_Cl" no hash',
                    'save line list ".lin" "lines.dat" last no hash',
#                     'save last lines emissivity ".emis" no hash',
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
#                     'Ar 4  4740.12A',
#                     'save grain extinction ".pdr_av"',
#                     'save grain temperature ".pdr_temp"',
#                     'save species densities ".pdr_pop"',
#                     "SiO",
#                     "Si+",
#                     "Si",
#                     "CO",
#                     "C+",
#                     "C",
#                     "H2",
#                     "H+",
#                     "H",
#                     "*temp",
#                     "*AV",
#                     "*depth",
#                     "end",               
                    ]
    save_script(ScriptFolder + data_dict['Name'] + '.in', script_Lines)
       
    return

def run_script(ScriptName, ScriptFolder, cloudy_address = '/home/vital/Cloudy/source/cloudy.exe', bins_folder = "/usr/sbin:/sbin:/home/vital/.my_bin:"):
    
    #Move to the script folder
    chdir(ScriptFolder)
    
    #Adding the cloudy path to the environment
    my_env = environ
    my_env["PATH"] = bins_folder + my_env["PATH"] #This variable should be adapted to the computer
       
    #Preparing the command
    Command = 'cloudy {}'.format(ScriptName[0:ScriptName.rfind('.')])

    print "--Launching command:"
    print "  ", Command#, '@', ScriptFolder, '\n'
    
    #Run the command
    p = Popen(Command, shell=True, stdout=PIPE, stderr=STDOUT, env=my_env)

    #Terminal output in terminal
    if len(p.stdout.readlines()) > 0:
        print '-- Code output wording\n'
        for line in p.stdout.readlines():
            print line
            
    return

#Set script name and location

ScriptFolder = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/imposition_zones/'

#Dictionary to store the grid points
Grid_Values = OrderedDict() 
Grid_Values['age']          = ['6.0']         #['5.', '5.48','5.7','5.85','6.','6.1','6.18','6.24','6.3','6.35','6.4','6.44','6.48','6.51','6.54','6.57','6.6','6.63','6.65','6.68','6.7','6.72']
Grid_Values['clus_mass']    = ['100000.0']    #['12000.', '20000.', '60000.', '100000.', '200000.'] 
Grid_Values['zGas']         = ['0.004']       #['0.0001', '0.0004', '0.004', '0.008', '0.02', '0.05'] 
Grid_Values['zStars']       = ['-2.1']        #['-2.1'] 

Grid_Values = OrderedDict() 
Grid_Values['age']          = ['5.0']         
Grid_Values['clus_mass']    = ['12000.0']    
Grid_Values['zGas']         = ['0.02']       
Grid_Values['zStars']       = ['-2.1']        
Grid_Values['radious']      = ['8.0', '9.0', '10.0',  '10.5', '11.0',  '11.5', '12.0',  '12.5', '13.0',  '13.5', '14.0', '14.5', '15.0', '15.5', '16.0', '16.5', '17.0', '17.5', '18.0', '18.5', '19.0', '19.5', '20.0']

#We have done this
# ['5.0', '5.48', '6.0', '6.48', '6.72']
# ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
# ['0.0004', '0.004', '0.008', '0.02']
# ['-2.1']
#TGrid_Mass12000.0_age5.0_zStar-2.1_zGas0.02.lin

#Dictionary to store the simulations physical conditions
Model_dict = OrderedDict()

#Set density of the model (only 10 and 100 available in grids)
Model_dict['den_big'] = 1
Model_dict['den_small'] = 2
                         
#Generate the scripts with the lines we want to print the flux
lines_to_extract(ScriptFolder)

c = 29979245800.0         #cm/s
pc_to_cm = 3.0856776e18   #cm/pc

Frame_MetalsEmission = import_popstar_data(Model_dict, den=Model_dict['den_big'])              

#Loop through all the conditions
for age in Grid_Values['age']:
    for mass in Grid_Values['clus_mass']:
        for zGas in Grid_Values['zGas']:                                        
            for zStar in Grid_Values['zStars']:
                
                Model_dict['Name_big']      = 'TGrid' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
                Model_dict['age']           = age
                Model_dict['zGas']          = zGas
                Model_dict['Metals_frac']   = str(float(zGas) / 0.02)
                Model_dict['zGas']          = zGas
                Model_dict['zStars']        = zStar
                
                index = (Frame_MetalsEmission["Z"] == float(zGas)) & (Frame_MetalsEmission["M_Msun"] == float(mass)) & (Frame_MetalsEmission["t"] == float(age))
                
                print '-Going for conditions: ', age, zGas, zStar, mass
                
                Model_dict['Q']             = Frame_MetalsEmission.loc[index, 'Q'].values[0]
                Model_dict['R']             = Frame_MetalsEmission.loc[index, 'logR_cm'].values[0]
                Model_dict['phi']           = nplog10((10.0**Model_dict['Q']) / (4 * pi * (10**Model_dict['R'])**2))
    
                ScriptName = Model_dict['Name_big'] + '.in'
                  
                #Generate the script
                cloudy_grid_node_script_phi(ScriptFolder, Model_dict)
                      
                #Run the cloudy script
#                 run_script(ScriptName, ScriptFolder)
                
                initial_sulfur_abund = calculate_abundances(ScriptFolder, Model_dict['Name_big'] + '.lin')
                print '--Sulfur abundance measured in initial cloud', initial_sulfur_abund, '\n'
                 
#                 lines_file                  = Model_dict['Name_big'] + '.lin'
#                 
#                 SII_6716A, SII_6730A, SIII_9069A, SIII_9531A  = loadtxt(ScriptFolder + lines_file, delimiter='\t', usecols=(17, 18, 19, 20), unpack=True)
#                                 
#                 S_ratio = (SII_6716A + SII_6730A) / (SIII_9069A + SIII_9531A)
# 
#                 U_predicted = -1.69 * S_ratio - 2.76
# 
#                 nH = Model_dict['den_small']**2  #cm^-3
                
                dz.data_plot(0.0, initial_sulfur_abund, label='First cloud sulfur abundance', markerstyle='o')

                 
                for radius in Grid_Values['radious']:
                    Model_dict['logR_cm'] = radius
                      
                    Model_dict['Name'] = Model_dict['Name_big'].replace('TGrid', 'Small_Cloud') + '_rad' + radius
                    
                    #Generate the script
                    cloudy_grid_node_script_smallCloud('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/imposition_zones/', Model_dict)
                        
                    #Run the cloudy script
                    run_script(Model_dict['Name'] + '.in', '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/imposition_zones/')
                      
                    #Calculate the abundances
                    sulfur_abund = calculate_abundances('/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/imposition_zones/', Model_dict['Name'] + '.lin')
                    
                    dz.data_plot(radius, sulfur_abund, label='Second cloud abundance', markerstyle='o', color='red')
                    
                    print 'Sulfur abundance {} secondary cloud at radious {}: '.format(sulfur_abund, radius) 

dz.FigWording(r'log(radious) (cm)', r'log(S/H)', 'Evolution of sulfur abundance evolution with second cloud location')
 
dz.display_fig()
                          
print 'Data treated'