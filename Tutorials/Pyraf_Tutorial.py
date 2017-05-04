'''
Created on May 18, 2015

@author: vital
'''

#Reading a Header

from pyraf import iraf
from Scientific_Lib.IrafMethods import Pyraf_Workflow 

Airmass_Key = 'AIRMASS'
ExpTime_Key = 'EXPTIME'

def outputNameGenerator(InputFile, Suffix):
    OutputFile =  InputFile[0:InputFile.find('.fits')] + '_' + Suffix + '.fits'
    return OutputFile

def get_HeaderValue(Item, Fit_Address, Digitalize = False):
    Header = iraf.imhead(Fit_Address, long='yes', Stdout=1)
    for i in range(len(Header)):
        key = Header[i].replace(' ','').split('=')[0]
        if key == Item:
            value = Header[i].replace(' ','').split('=')[1]
            value = value.split('/')[0]
            if Digitalize == True:
                return float(value)
            else:
                return value 

def printIrafCommand(Task, Attributes):
    
    keys_attrib     = Attributes.keys()
    values_attrib   = Attributes.values()

    command_String = Task
    
    for i in range(len(keys_attrib)):
        command_String = command_String + ' ' + keys_attrib[i] + '=' + values_attrib[i]

    print 'The command for', Task

def CalibrateTask(InputFile, OutputFile, senstivityCurve, Fits_Folder, airmass_value, exptime, Configuration = 'WHT', Suffix = 'Fx', fnu_units = 'no'):
    
    if OutputFile == None:
        OutputFile = outputNameGenerator(InputFile, Suffix)
    
    if Configuration == 'WHT':
        
        Observatory         = 'lapalma'
        ExtinctionFileName  = 'a_ing_ext.dat'
        
        calibrate_conf = {'input'       :Fits_Folder + InputFile,
                          'output'      :Fits_Folder + OutputFile,
                          
                          'extinct'     :'yes',
                          'flux'        :'yes',
                          'extinction'  :Fits_Folder + ExtinctionFileName,
                          'observatory' :Observatory,
                          
                          'ignoreaps'   :'yes',
                          'sensitivity' :Fits_Folder + senstivityCurve,
                          'fnu'         :fnu_units,
                          
                          'airmass'     :airmass_value,
                          'exptime'     :exptime,
                          
                          'mode'        :'ql'
                          }
            
        iraf.module.calibrate(**calibrate_conf)
    
    return OutputFile

input_spec  = 'stdBD17_wide_cr_f_a_bg_s.fits'
output_spec = 'obj70_s_c_cr_f_a_t_bg_fxW_TESTPYRAF.fits'
Folder      = '/home/vital/Desktop/Flux_Calibration_Steps/Night1_Blue/'
sens_func   = 'a_std_wideCombAll_se.fits[0]'

# Airmass_Value = get_HeaderValue(Airmass_Key, Folder + input_spec, True)
# ExpTime_Value = get_HeaderValue(ExpTime_Key, Folder + input_spec, True)
# 
# print 'Airmass measured',           Airmass_Value
# print 'Exposition time measured',   ExpTime_Value
# 
# Loquesale = CalibrateTask(input_spec, output_spec, sens_func, Folder, Airmass_Value, ExpTime_Value, 'WHT')

iraf.noao(_doprint=0)
iraf.onedspec(_doprint=0)
 
iraf.onedspec.splot(images=Folder + input_spec)


# iraf.noao(_doprint=0)
# iraf.onedspec(_doprint=0)
# 
# py_w    = Pyraf_Workflow('WHT')
# 
# standardconf = py_w.StandardAttributes('stdF34_wide_cr_f_a_bg_s.fits', 
#                                        'a_std_wideCombAll_Tutorial', 
#                                        'a_feige34_50a', 
#                                        '/home/vital/Desktop/Flux_Calibration_Steps/PyRaf_Testing/', 
#                                        1.037292, 
#                                        300.01)
# 
# iraf.onedspec.standard(**standardconf)
# iraf.onedspec.standard(input=       '/home/vital/Desktop/Flux_Calibration_Steps/PyRaf_Testing/stdF34_wide_cr_f_a_bg_s.fits',
#                        output=      '/home/vital/Desktop/Flux_Calibration_Steps/PyRaf_Testing/a_std_wideCombAll',
#                        extinction=  '/home/vital/Desktop/Flux_Calibration_Steps/PyRaf_Testing/a_ing_ext.dat',
#                        caldir=      '/home/vital/Desktop/Flux_Calibration_Steps/PyRaf_Testing/',
#                        star_name=   'a_feige34_50a',
#                        )





# input /home/vital/Desktop/Flux_Calibration_Steps/PyRaf_Testing/stdF34_wide_cr_f_a_bg_s.fits
# output /home/vital/Desktop/Flux_Calibration_Steps/PyRaf_Testing/a_std_wideCombAll
# samestar yes
# beam_switch no
# apertures ""
# bandwidth INDEF
# bandsep INDEF
# fnuzero 3.68e-20
# extinction /home/vital/Desktop/Flux_Calibration_Steps/PyRaf_Testing/a_ing_ext.dat
# caldir /home/vital/Desktop/Flux_Calibration_Steps/PyRaf_Testing/
# observatory lapalma
# interact yes
# star_name a_feige34_50a
# airmass 1.037292
# exptime 300.01
# answer yes
