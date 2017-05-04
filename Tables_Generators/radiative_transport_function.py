from collections    import OrderedDict
from numpy          import array, genfromtxt, log10 as np_log10, loadtxt, ones, searchsorted, where, zeros,power as np_power

def generate_variables():

    data_dict = OrderedDict()
    
    #General variables
    data_dict['Atomfile1']  = '/home/vital/Dropbox/Astrophysics/Papers/Radiation_Correction/OriginalCodes/Distribution/' + 'He5B.atom'
    data_dict['Atomfile2']  = '/home/vital/Dropbox/Astrophysics/Papers/Radiation_Correction/OriginalCodes/Distribution/' + 'He5B.opt'
    data_dict['cc']         = 'None'
    data_dict['and']        = 'None'
    data_dict['NSIZ']       = 29 #This is the atom size
    data_dict['AHe']        = 0.1
    data_dict['NHUGE']      = data_dict['NSIZ'] * data_dict['NSIZ']
    data_dict['n']          = zeros(data_dict['NSIZ'], order='F') 
    data_dict['l']          = zeros(data_dict['NSIZ'], order='F') 
    data_dict['g_S']        = zeros(data_dict['NSIZ'], order='F') 
    data_dict['g']          = zeros(data_dict['NSIZ'], order='F') 
    data_dict['E']          = zeros(data_dict['NSIZ'], order='F') 
        
    #Recombination
    data_dict['al'], data_dict['al4'], data_dict['b_al'] = zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F') 

    #Indirect recombination
    data_dict['alp'], data_dict['alp4'], data_dict['b_alp'], data_dict['c_alp'] = zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F') 

    #Three body recombination
    data_dict['altbr'], data_dict['altbr4'], data_dict['b_tbr'] = zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F') 
    
    #Collisional ionization
    data_dict['Cion'], data_dict['Ciona'], data_dict['Cionb'], data_dict['Cionc'] = zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F') 
    
    #A-values and wavelengths
    data_dict['A'] = zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F')
    data_dict['wave'] = zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F')
    data_dict['waveair'] = zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F')
    
    #Collision strengths
    data_dict['om'], data_dict['om4'], data_dict['bom'] = zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F'), zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F'), zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F')
     
    #Collision rates
    data_dict['c'] = zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F')
     
    #Calcualate level populations (for cases with optical depth) and grid info
    data_dict['NTg']    = 5
    data_dict['NDg']    = 5
    data_dict['NTAUg']  = 20
    
    data_dict['Tg'], data_dict['dg'], data_dict['taug'] = zeros(data_dict['NTg'], order='F'), zeros(data_dict['NDg'], order='F'), zeros(data_dict['NTAUg'], order='F')
    data_dict['pg']     = zeros((data_dict['NSIZ'], data_dict['NDg'], data_dict['NTg'], data_dict['NTAUg']), order='F') 
    data_dict['ping']   = zeros((data_dict['NSIZ'] * data_dict['NDg'] * data_dict['NTg'] * data_dict['NTAUg']), order='F') 
    
    #Rate matrix, level pops, and departure coeffs
    data_dict['r'], data_dict['pop'], data_dict['b'] = zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F'), zeros(data_dict['NSIZ'], order='F'), zeros(data_dict['NSIZ'], order='F')
    
    #escape probabilities (not used)
    data_dict['epa'], data_dict['tauc'] = zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F'), zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F')

    return data_dict

def import_atomData(dict_data):
    
    #Treating data from first file, first part
    file_address    = dict_data['Atomfile1'] + 'A'
    
    nd,ld,g_Sd      = loadtxt(file_address, dtype=int, skiprows = 3, usecols=[0,1,2], unpack = True)    
    Ed, al4d,b_ald, alp4d, b_alpd, c_alpd, altbr4d, b_tbrd, Cionad, Cionbd, Cioncd = loadtxt(file_address, skiprows = 3, usecols=range(3, 14), unpack = True)
    
    for i in range(dict_data['NSIZ']):
        
        #In our case we substract 1 because in python arrays are numbered starting at 0
        k                           = (2 * (nd[i]*(nd[i]-1)/2 + ld[i]) + (3-g_Sd[i])/2) - 1
        dict_data['n'][k]            = nd[i]
        dict_data['l'][k]            = ld[i]
        dict_data['g_S'][k]          = g_Sd[i]
        dict_data['E'][k]            = Ed[i]
        dict_data['al4'][k]          = al4d[i]
        dict_data['b_al'][k]         = b_ald[i]
        dict_data['alp4'][k]         = alp4d[i]
        dict_data['b_alp'][k]        = b_alpd[i]
        dict_data['c_alp'][k]        = c_alpd[i]
        dict_data['altbr4'][k]       = altbr4d[i]
        dict_data['b_tbr'][k]        = b_tbrd[i]
        dict_data['Ciona'][k]        = Cionad[i]
        dict_data['Cionb'][k]        = Cionbd[i]
        dict_data['Cionc'][k]        = Cioncd[i]
        dict_data['g'][k]            = g_Sd[i]*(2*ld[i]+1)
    
    #Treating data from first file, second part
    file_address = dict_data['Atomfile1'] + 'B'
    
    nl,ll,isl,nu,lu,isu = loadtxt(file_address, dtype=int, skiprows = 3, usecols=[0,1,2,3,4,5], unpack = True)
    wav, Ak, om4k, bk   = loadtxt(file_address, skiprows = 3, usecols=[6,7,8,9], unpack = True)   
    
    for i in range(dict_data['NHUGE']):
        
        #In our case we substract 1 because in python arrays are numbered starting at 0
        kl = (2 * (nl*(nl-1)/2 + ll) + (3-isl)/2) - 1
        ku = (2 * (nu*(nu-1)/2 + lu) + (3-isu)/2) - 1
        
        dict_data['A'][kl,ku]     = Ak
        dict_data['om4'][kl,ku]   = om4k
        dict_data['om4'][ku,kl]   = om4k
        dict_data['bom'][kl,ku]   = bk
        dict_data['bom'][ku,kl]   = bk
        dict_data['wave'][kl,ku]  = wav
       
    #Treating data from second file
    file_address    = dict_data['Atomfile2'] + 'A'
    #Reading this line base file is dangerous, try with columns
    #Tg                  = genfromtxt(file_address, skip_header=3, skip_footer=5, usecols=[0,1,2,3,4])  
    #dg                  = genfromtxt(file_address, skip_header=4, skip_footer=6, usecols=[0,1,2,3,4])  
    #taug                = genfromtxt(file_address, skip_header=4, skip_footer=6, usecols=[0,1,2,3,4])      
    dict_data['Tg']     = array([5.000e+03, 8.000e+03, 1.000e+04, 1.500e+04, 2.000e+04], order='F')
    dict_data['dg']     = array([1.000e+00, 1.000e+02, 1.000e+04, 1.000e+06, 1.000e+08], order='F')
    dict_data['taug']   = array([0.0,   0.1,   0.5,   1.0,   1.5,  2.0,   3.0,   4.0,   5.0,   7.5,   10.0,  20.0,  30.0,  40.0,  50.0,  60.0,  70.0,  80.0,  90.0, 100.0], order='F')

    file_address        = dict_data['Atomfile2'] + 'B'

    #Entry sizes
    Data_Dict['NEN']    = 5
    Data_Dict['NROWS']  = Data_Dict['NTg'] * Data_Dict['NDg'] * Data_Dict['NTAUg'] * Data_Dict['NSIZ'] / Data_Dict['NEN']

    arr = array(list(import_levelspopulation_file(file_address)))

    Data_Dict['ping']   = arr.reshape((Data_Dict['NSIZ'], Data_Dict['NDg'], Data_Dict['NTg'], Data_Dict['NTAUg']), order='F')

    return 

def aircalc(dict_data):
    
    #Formula 3 from ApJ Supp 1991 77, 119 Morton, D.C.
    for i in range(dict_data['NSIZ']):
        for j in range(dict_data['NSIZ']):
            if dict_data['wave'][i,j] > 2000:
                sig = 1e4 / dict_data['wave'][i,j]
                fac = 6.4328e-5+2.94981e-2 / (146-sig*sig) + 2.5540e-4/(41-sig*sig)
                dict_data['waveair'][i,j] = dict_data['wave'][i,j]/(1+fac)
#                 print dict_data['wave'][i,j], dict_data['waveair'][i,j]
                    
    return

def manage_warnings(check_type, data_dict):
    
    if check_type == 'Atomic levels number':
        nsizck = data_dict['nlev'] * (data_dict['nlev'] + 1) - 1
        if nsizck != data_dict['NSIZ']:
            print '-WARNING: Need to change NSIZ in code'
    
    elif check_type == 'Atomic levels number':
        if (data_dict['t4'] > 2) or (data_dict['t4'] > 0.5):
            print '-WARNING: Input temperature is out of bounds'
            print '-WARNING: Must have 5000< T< 20000 K to use this code'
            
        if (data_dict['den'] > 1e8):
            print '-WARNING: Input density too high!'
            print '-WARNING: Must have n_e < 10^8 cm-3 to use this code'

        if (data_dict['tau3889'] > 100) or (data_dict['tau3889'] < 0):
            print '-WARNING: Bad value of optical depth'
            print '-WARNING: Must be between 0 and 100'

    elif check_type == 'Check coordinates':
        if (data_dict['ilo'] == 0) or (data_dict['ilo'] == data_dict['NDg']):
            print '-WARNING: Bad ilo'
            print data_dict['ilo'], data_dict['NDg']
            
        if (data_dict['jlo'] == 0) or (data_dict['jlo'] == data_dict['NTg']):
            print '-WARNING: Bad jlo'
            print data_dict['jlo'], data_dict['NTg']

        if (data_dict['klo'] == 0) or (data_dict['klo'] == data_dict['NTaug']):
            print '-WARNING: Bad value klo'
            print data_dict['klo'], data_dict['NTAUg']
        
        if (data_dict['tj'] < 0) or (data_dict['tj'] > 1.0):
            print '-WARNING: Bad si'
            print data_dict['tj']       
        
        if (data_dict['uk'] < 0) or (data_dict['uk'] > 1.0):
            print '-WARNING: Bad uk'
            print data_dict['uk']        

# !c     Nudge values slightly if we are
# !c     right on edge of interpoation boundary
#       if (t4.gt.1.9900) then
#          t4=1.99
#       end if
#       if (den.gt.0.99e8) then
#          den=0.99e8
#       endif
#       if (tau3889.gt.99.) then
#          tau3889=99
#       endif
#       if (t4.lt.0.5005) then
#          t4=0.5002
#       endif
#       if (den.lt.2.0) then
#          den=2.
#       endif
#       if (tau3889.lt.0.001) then
#          tau3889=0.001
#       endif
    
    return

def tau_epmake(tau584, tau3889, data_dict):
    
    #Declare physical parameters
    nT                  = data_dict['NTg']    #5
    nS                  = data_dict['NDg']    #5
    a                   = data_dict['A']
    lambda_value        = data_dict['wave']
    tau                 = zeros((data_dict['NSIZ'], data_dict['NSIZ']), order='F')
    epa                 = ones((data_dict['NSIZ'], data_dict['NSIZ']), order='F')

    print 'Siguiente'
    for i in range(data_dict['NSIZ']):
        for j in range(data_dict['NSIZ']):
            print a[i,j], lambda_value[i,j]

    if tau584 != 0:
        for i in range(2, nS + 1):                                  #In this code we do the + 1 since it is a python code
            k           = (2 * (i * (i-1)/ 2+1) + 1) - 1            #In this code we do the - 1 since it is a python code
            tau[1,k]    = tau584 * a[1,k]/a[1,5] * (lambda_value[1,k]/lambda_value[1,5])**3
            epa[1,k]    = 1.72 / (tau[1,k] + 1.72)

    if tau3889 != 0:
        for i in range(2, nT + 1):                                  #In this code we do the + 1 since it is a python code
            k           = (2 * (i * (i-1)/ 2+1) + 0) - 1            #In this code we do the - 1 since it is a python code
            tau[2,k]    = tau3889 * a[2,k]/a[2,8] * (lambda_value[2,k]/lambda_value[2,8])**3
            epa[2,k]    = 1.72 / (tau[2,k] + 1.72)
            
    data_dict['tauc']   = tau
    data_dict['epa']    = epa
    
#     for i in range(data_dict['NSIZ']):
#         for j in range(data_dict['NSIZ']):
#             print epa[i,j], tau[i,j]
            
    return

def hunt_check(my_array, target_value):
    
    #Case the exact value is in array
    if target_value in my_array:
        idx = where(my_array==target_value)[0][0]
    else:
        if (target_value < my_array[0]):
            idx = 0
        elif (my_array[-1] < target_value):
            idx = -1
        else:
            idx = searchsorted(my_array, target_value) - 1
            
    return idx

def import_levelspopulation_file(filename):
    with open(filename) as f_input:
        lines = f_input.readlines()
        for i in range(3, len(lines)):
            line = lines[i].split(',')
            del line[-1]
            for val in line:
                yield float(val)

Data_Dict = generate_variables()

#Declare number of levels (This is right for the He5.atom file)
Data_Dict['nlev'] = 5
manage_warnings('Atomic levels number', Data_Dict)

#Import the data from the data files:
import_atomData(Data_Dict)

#Convert from air to space wavelength
aircalc(Data_Dict)

#Convert density and temperature to log values
Data_Dict['Tg'] = np_log10(Data_Dict['Tg'])
Data_Dict['dg'] = np_log10(Data_Dict['dg'])

print Data_Dict['Tg']
print Data_Dict['dg']

#Declare physical conditions you want to treat
T       = 10000
den     = 100
tau3889 = 1.06

#Convert input data
Data_Dict['t4']         = T / 1e4
Data_Dict['den']        = den
Data_Dict['tau3889']    = tau3889
Data_Dict['denHe']      = Data_Dict['AHe'] * den
Data_Dict['tau584']     = 0


print Data_Dict['t4']
print Data_Dict['denHe']
print Data_Dict['tau584']
print 
print 

#Check bounds
manage_warnings('Check input bounds', Data_Dict)

#Calculate the cape probabilities
tau_epmake(Data_Dict['tau584'], tau3889, Data_Dict)

#Declare emission line to compute
isu = 3
nu  = 4
lu  = 2
nl  = 2
ll  = 1
kl  = 2 * (nl * (nl-1)/2 + ll) + (3-isu)/2
ku  = 2 * (nu * (nu-1)/2 + lu) + (3-isu)/2

#Interpolate from table
iss = isu / 2
ku2 = iss * (Data_Dict['NSIZ'] + 1)/2 + nu * (nu-1)/2 + lu

#Interpolation coordinates
tl  = np_log10(Data_Dict['t4'])+4.0
dl  = np_log10(den)
op  = tau3889

ilo =   hunt_check(Data_Dict['dg'], dl)
jlo =   hunt_check(Data_Dict['Tg'], tl)
klo =   hunt_check(Data_Dict['dg'], op)
si  =   (dl-Data_Dict['dg'][ilo])   / (Data_Dict['dg'][ilo+1]-Data_Dict['dg'][ilo])
tj  =   (tl-Data_Dict['Tg'][jlo])   / (Data_Dict['Tg'][jlo+1]-Data_Dict['Tg'][jlo])
uk  =   (op-Data_Dict['taug'][klo]) / (Data_Dict['taug'][klo+1]-Data_Dict['taug'][klo])

Data_Dict['ilo'] = ilo
Data_Dict['jlo'] = jlo
Data_Dict['klo'] = klo
Data_Dict['si']  = si
Data_Dict['tj']  = tj
Data_Dict['uk']  = uk

#Check the coordinates calculation
manage_warnings('Check coordinates', Data_Dict)

#Need to include density multiplications since precomputed level populations do not have density divided out...
dd1     = np_power(10, Data_Dict['dg'][ilo])
dd1     = dd1 * dd1 * Data_Dict['AHe']
dd2     = np_power(10, Data_Dict['dg'][ilo + 1])
dd2     = dd2 * dd2 * Data_Dict['AHe']
       
#Trilinear interpolation (8 vertices)
v1      = (1-si) * (1-tj) * (1-uk) * Data_Dict['pg'][ku2, ilo, jlo, klo]
v2      = si * (1-tj) * (1-uk) * Data_Dict['pg'][ku2, ilo+1, jlo, klo]
v3      = (1-si) * tj * (1-uk) * Data_Dict['pg'][ku2, ilo, jlo+1, klo]
v4      = si  *  tj   * (1-uk) * Data_Dict['pg'][ku2, ilo+1, jlo+1, klo]
v5      = (1-si) * (1-tj) * uk * Data_Dict['pg'][ku2, ilo, jlo  , klo+1]
v6      = si * (1-tj) *  uk  * Data_Dict['pg'][ku2,ilo+1,jlo  ,klo+1]
v7      = (1-si) *  tj  *  uk  * Data_Dict['pg'][ku2,ilo  ,ilo+1,klo+1]
v8      = si *  tj  *  uk  * Data_Dict['pg'][ku2,ilo+1,jlo+1,klo+1]
uppop   = (1e10/dd1) * (v1+v3+v5+v7) + (1e10/dd2) * (v2+v4+v6+v8)
uppop   = uppop * (den * Data_Dict['denHe']/1e10)

# Metastable population
ku2     = 16
v1      = (1-si) * (1-tj) * (1-uk) * Data_Dict['pg'][ku2, ilo, jlo, klo]
v2      = si * (1-tj) * (1-uk) * Data_Dict['pg'][ku2, ilo+1, jlo, klo]
v3      = (1-si) * tj * (1-uk) * Data_Dict['pg'][ku2, ilo, jlo+1, klo]
v4      = si * tj * (1-uk) * Data_Dict['pg'][ku2, ilo+1, jlo+1, klo]
v5      = (1-si) * (1-tj) *  uk * Data_Dict['pg'][ku2, ilo, jlo, klo+1]
v6      = si * (1-tj) *  uk * Data_Dict['pg'][ku2, ilo+1, jlo, klo+1]
v7      = (1-si)* tj * uk * Data_Dict['pg'][ku2, ilo, ilo+1, klo+1]
v8      = si * tj * uk * Data_Dict['pg'][ku2, ilo+1, jlo+1, klo+1]
popmet  = (1e10/dd1) * (v1+v3+v5+v7) + (1e10/dd2) * (v2+v4+v6+v8)
popmet  = popmet * (den * Data_Dict['denHe']/1e10)

#Calculate emissivity
#Modify A value by escape probability...

Aval    = Data_Dict['A'][kl,ku] * Data_Dict['epa'][kl,ku]
hnu     = 1.986302e-8 / Data_Dict['wave'][kl,ku]
emis    = hnu * Aval * uppop/den/Data_Dict['denHe']

print 'Aval', Aval
print 'hnu', hnu
print 'emis', emis

print 'interpolation coeff', ilo, jlo, klo
print '------', si, tj, uk
print 'Wavelength(Air) =', Data_Dict['waveair'][kl,ku], 'A 4*pi*j/(n_e*n_He+)=', emis
print 'N(2^3S)/n_Hn_He+=', popmet / Data_Dict['denHe']
print 'Escape probability', Data_Dict['tauc'][kl,ku]
print 'Esape probability', Data_Dict['epa'][kl,ku]

print 'Data treated'


#       Aval=A(kl,ku)*epa(kl,ku)
#       hnu=1.986302e-8/wave(kl,ku)
#       emis=hnu*Aval*uppop/den/denHe
#       write(6,6010)
#       write(6,6007) waveair(kl,ku), emis
#       print *, 'interpolation coeff', ilo, jlo, klo
#       print *, ' ------', si, tj, uk
#       write(6,6008) popmet/denHe
#       write(6,6006) tauc(kl,ku)
#       write(6,6009) epa(kl,ku)
#       write(6,6010)
# 
#  6010 format('----------------------------------------')
#  6007 format(' Wavelength(Air)=',f12.2, ' A   4*pi*j/(n_e*n_He+)=',1pe12.3)
#  6008 format(' N(2^3S)/n_Hn_He+=', 1pe12.3)
#  6009 format(' Escape probability...', 1pe12.3)
#  6006 format(' Optical depth in line', 1pe12.3)




















