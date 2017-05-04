import pandas as pd
import pyfits as pf
from astroquery.simbad import Simbad
from dazer_methods import Dazer

dz = Dazer()
Catalogue_Dic   = '/home/vital/Dropbox/Astrophysics/Telescope Time/Standard_Stars/Calspec_Spectra/'
Pattern         = '.fits'
FilesList       = dz.Folder_Explorer(Pattern,  Catalogue_Dic, CheckComputer=False)
 
#Generate plot frame and colors
dz.FigConf()
 
#Loop through files
for i in range(len(FilesList)):
        
    #Analyze file address
    CodeName, FileName, FileFolder          = dz.Analyze_Address(FilesList[i])
     
    #Import fits file
    fits_file   = pf.open(FilesList[i])
    Wave        = fits_file[1].data['WAVELENGTH']
    Int         = fits_file[1].data['FLUX']
     
    fits_file.close()
     
    dz.data_plot(Wave, Int, label=FileName.replace('_', ''))
     
dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', 'Calspec library')         
dz.Axis.set_yscale('log')
dz.Axis.set_xlim(7000, 10000)
dz.display_fig()

# /home/vital/Dropbox/Astrophysics/Telescope Time/Standard_Stars/Calspec_Spectra/bd_17d4708_stisnic_006.fits

# file_address = '/home/vital/Dropbox/Astrophysics/Telescope Time/Standard_Stars/Calspec_Spectra/bd_17d4708_stisnic_006.fits'
# 
# fits_file = pf.open(file_address)
# print fits_file[1].data['WAVELENGTH']
# print fits_file[1].data['FLUX']
# 
# fits_file.close()


# #Recover objects list
# Table_Address           = '/home/vital/Dropbox/Astrophysics/Telescope Time/Standard_Stars/Calspec_list.csv'
# Candiates_frame         = pd.read_csv(Table_Address, delimiter = '; ', header = 0, index_col = 0)
# Candiates_frame['RA']   = None
# Candiates_frame['DEC']  = None
#  
#  
# for i in range(len(Candiates_frame.index)):
#    
#     name = Candiates_frame.index[i]
#    
#     result_table = Simbad.query_object(name)
#      
#     try:
#         Candiates_frame.ix[i,"RA"]  = str(result_table['RA'][0]).replace(' ',':')
#         Candiates_frame.ix[i,"DEC"] = str(result_table['DEC'][0]).replace(' ',':')
#      
#     except:
#         Candiates_frame.ix[i,"RA"]  = 'Not loaded'
#         Candiates_frame.ix[i,"DEC"] = 'Not loaded'
#  
#     print name, Candiates_frame.ix[i,"RA"], Candiates_frame.ix[i,"DEC"]
#    
# print '\nList of objects'       
# for i in range(len(Candiates_frame.index)):
#     if Candiates_frame.ix[i,"RA"] != 'Not loaded':
#         print '[{StarCode}] {RA} {DEC}'.format(StarCode = Candiates_frame.index[i].replace(' ','_').replace('+','_'), RA = Candiates_frame.ix[i,"RA"].replace(':', ' '), DEC = Candiates_frame.ix[i,"DEC"].replace(':', ' ')) 
