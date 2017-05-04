'''
Created on Jan 19, 2016

@author: vital
'''

from CodeTools.PlottingManager                  import myPickle
import pyfits

pv  = myPickle()

pv.FigFormat_One(ColorConf='Night1')
Folder  = '/home/vital/Esoreflex/data_wkf/reflex_end_products/2016-01-19T15:01:09/UVES.2009-03-13T04:00:31.835'
Pattern = 'Hen-3-847_FLUXCAL_SCI_POINT_BLUE.fits'
FilesList = pv.Folder_Explorer(Pattern, Folder, CheckComputer=False)

for i in range(len(FilesList)):

    CodeName, FileName, FileFolder = pv.Analyze_Address(FilesList[i])
    
    Wave, Flux, ExtraData                   = pv.File_to_data(FileFolder, FileName)
    
    pv.DataPloter_One(Wave, Flux,  'UVES SPECTRUM', pv.Color_Vector[2][3])
    
#     pv.SaveManager(SavingName = FileName.replace('.fits', '.png'), SavingFolder = FileFolder)

    pv.DisplayFigure()
 
    pv.ResetPlot()
    

# FitsFile = pyfits.open(FileFolder + FileName)
# 
# print 'Length', len(FitsFile)
# 
# print FitsFile[0]
# # print FitsFile[1] #Only one frame
# 
# Header_0 = FitsFile[0].header

# #Pretty standard header
# print 'The header', type(Header_0)
# 
# print 'NAXIS1', Header_0['NAXIS1'] #Header is a dictionary
# # print 'COEFF0', Header_0['COEFF0'] #Header is a dictionary #ESTE NO ESTA
# # print 'COEFF1', Header_0['COEFF1'] #Header is a dictionary #ESTE NO ESTA
# # print 'LTV1', Header_0['LTV1'] #Header is a dictionary #ESTE NO ESTA
# print 'CRVAL1', Header_0['CRVAL1'] #Header is a dictionary
# print 'CD1_1', Header_0['CD1_1'] #Header is a dictionary
# 
# # for coso in Header_0:
# #     print coso
# # print 'Bitpix', Header_0['Bitpix'] #Header is a dictionary
# 
# Data = FitsFile[0].data
# print len(Data), type(Data)

    
    

print 'Se acabo'
