#!/usr/bin/python

from numpy import median, searchsorted, mean
import CodeTools.PlottingManager as plotMan
from PipeLineMethods.ManageFlow import DataToTreat

def LM_CalciumTriplet_Bands(TheoWave):
    
    if TheoWave == 8498:
        Wave1 = 8447.50
        Wave2 = 8462.50
        Wave3 = 8483.00
        Wave4 = 8513.00
        Wave5 = 8842.50
        Wave6 = 8857.50
    
    elif TheoWave == 8542:
        Wave1 = 8447.50
        Wave2 = 8462.50
        Wave3 = 8527.00
        Wave4 = 8557.00
        Wave5 = 8842.50
        Wave6 = 8857.50
        
    elif TheoWave == 8662:
        Wave1 = 8447.50
        Wave2 = 8462.50
        Wave3 = 8647.00
        Wave4 = 8677.00
        Wave5 = 8842.50
        Wave6 = 8857.50
    
    WaveValues = ((Wave1, Wave2), (Wave3, Wave4), (Wave5, Wave6))
    
    return WaveValues

def ExtractSubRegion(TotalWavelen, TotalInten, Wlow, Whigh):

    indmin, indmax = searchsorted(TotalWavelen, (Wlow, Whigh))
    indmax = min(len(TotalWavelen)-1, indmax)
    
    PartialWavelength = TotalWavelen[indmin:indmax]
    PartialIntensity = TotalInten[indmin:indmax]
    
    return PartialWavelength, PartialIntensity

Pv  = plotMan.myPickle()

CatalogueFolder, DataType, Log_Format  = DataToTreat()
Pattern = DataType + '.fits'

#Find and organize files from terminal command or .py file
FilesList = Pv.FindAndOrganize(Pattern, CatalogueFolder, CheckComputer=True)

#Generate plot frame and colors
Pv.FigFormat_One(ColorConf='Night1')

#Loop through files
for m in range(len(FilesList)):
    for j in range(len(FilesList[m])):
            
        CodeName, FileName, FileFolder = Pv.FileAnalyzer(FilesList[m][j])
        Wave, Int, ExtraData  = Pv.File2Data(FileFolder,FileName)
        
        BlueBump_Wave,  BlueBump_Int      = ExtractSubRegion(Wave, Int, 4600,4680)          #The bump is at 
        RedBump_Wave, RedBump_Int     = ExtractSubRegion(Wave, Int, 5650,5910)              #The bump is at 5808
        OxygenVI_Wave, OxygenVI_Int     = ExtractSubRegion(Wave, Int, 3750,3860)
                    
        #Blue bump region
        if (Wave[0] < 4620) and (4720 < Wave[-1]):
            Label1 = CodeName + ' spectrum'    
            Pv.DataPloter_One(BlueBump_Wave, BlueBump_Int, Label1, Pv.Color_Vector[2][2])
            Pv.Labels_Legends_One(Plot_Title = 'Object ' + CodeName + ' Blue Bump Region',Plot_xlabel= r'Wavelength $(\AA)$', Plot_ylabel='Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$')
            Pv.SaveManager(SavingName ='B4_' + CodeName + '_Blue_Bump_Region', SavingFolder = FileFolder, ForceSave = True)
        
            Pv.ResetPlot()       
        
        #Red bump region
        if (Wave[0] < 5820) and (5900 < Wave[-1]):
            Label1 = CodeName + ' spectrum'    
            Pv.DataPloter_One(RedBump_Wave, RedBump_Int, Label1, Pv.Color_Vector[2][1])
            Pv.Labels_Legends_One(Plot_Title = 'Object ' + CodeName + ' Red Bump Region',Plot_xlabel= r'Wavelength $(\AA)$', Plot_ylabel='Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$')
            Pv.SaveManager(SavingName ='B5_' + CodeName + '_Red_Bump_Region', SavingFolder = FileFolder, ForceSave = True)

            Pv.ResetPlot()
        
        #OxygenVI region
        if (Wave[0] < 3790) and (4720 < Wave[-1]):
            Label1 = CodeName + ' spectrum'    
            Pv.DataPloter_One(OxygenVI_Wave, OxygenVI_Int, Label1, Pv.Color_Vector[2][3])
            Pv.Labels_Legends_One(Plot_Title = 'Object ' + CodeName + ' Oxygen VI Bump Region',Plot_xlabel= r'Wavelength $(\AA)$', Plot_ylabel='Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$')
            Pv.SaveManager(SavingName ='B6_' + CodeName + '_OxygenVI_Bump_Region', SavingFolder = FileFolder, ForceSave = True)
        
            Pv.ResetPlot()
                 
print "\nAll data treated generated"

