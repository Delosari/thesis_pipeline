import pandas as pd
from os             import environ, chdir, system
from numpy          import log10 as nplog10, pi, power
from collections    import OrderedDict
from subprocess     import Popen, PIPE, Popen, STDOUT
from pyCloudy.utils.physics import abund_Asplund_2009

def import_popstar_data(Model_dict):
    
    FilesFolder                     = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/teporingos/' 
    
    if Model_dict['den'] == 1:
        TableAddressn = 'mnras0403-2012-SD1_clusterTable1_10cm3.txt'
    elif Model_dict['den'] == 2:
        TableAddressn = 'mnras0403-2012-SD2_clusterTable2_100cm3.txt'
        
    print 'Popstar table is', TableAddressn

   
    Frame_MetalsEmission            = pd.read_csv(FilesFolder + TableAddressn, delim_whitespace = True)
    
    nH                              = Model_dict['den']**2  #cm^-3
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
Grid_Values['age']          = ['6.0']         
Grid_Values['clus_mass']    = ['12000.0']    
Grid_Values['zGas']         = ['0.004']       
Grid_Values['zStars']       = ['-2.1']        

#We have done this
# ['5.0', '5.48', '6.0', '6.48', '6.72']
# ['12000.0', '20000.0', '60000.0', '100000.0', '200000.0']
# ['0.0004', '0.004', '0.008', '0.02']
# ['-2.1']

#Dictionary to store the simulations physical conditions
Model_dict = OrderedDict()

#Set density of the model (only 10 and 100 available in grids)
Model_dict['den'] = 2

#Data from popstar
Frame_MetalsEmission = import_popstar_data(Model_dict)              
                         
#Generate the scripts with the lines we want to print the flux
lines_to_extract(ScriptFolder)
 
#Loop through all the conditions
for age in Grid_Values['age']:
    for mass in Grid_Values['clus_mass']:
        for zGas in Grid_Values['zGas']:                                        
            for zStar in Grid_Values['zStars']:
                
                Model_dict['Name']          = 'SmallCloud' + '_Mass' + mass + '_age'+ age + '_zStar' + zStar + '_zGas' + zGas
                Model_dict['age']           = age
                Model_dict['zGas']          = zGas
                Model_dict['Metals_frac']   = str(float(zGas) / 0.02)
                Model_dict['zGas']          = zGas
                Model_dict['zStars']        = zStar
                
                index = (Frame_MetalsEmission["Z"] == float(zGas)) & (Frame_MetalsEmission["M_Msun"] == float(mass)) & (Frame_MetalsEmission["t"] == float(age))
                
                print '-Going for conditions: ', age, zGas, zStar, mass
                
                Model_dict['Q']             = Frame_MetalsEmission.loc[index, 'Q'].values[0]
                Model_dict['R']             = Frame_MetalsEmission.loc[index, 'logR_cm'].values[0]
    
                ScriptName = Model_dict['Name'] + '.in'
                 
                #Generate the script
                cloudy_grid_node_script(ScriptFolder, Model_dict)
                     
                #Run the cloudy script
#                 run_script(ScriptName, ScriptFolder)
                
print 'Data treated'