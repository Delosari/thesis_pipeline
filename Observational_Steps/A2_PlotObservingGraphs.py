#!/usr/bin/python

from os.path                        import isfile
from PipeLineMethods.ManageFlow     import DataToTreat
import CodeTools.PlottingManager    as plotMan

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
                            
        #Blue bump region
        if isfile(FileFolder + CodeName + '_FC.png'):
            Pv.DataPloter_One(BlueBump_Wave, BlueBump_Int, Label1, Pv.Color_Vector[2][2])
            Pv.Labels_Legends_One(Plot_Title = 'Object ' + CodeName + ' Blue Bump Region',Plot_xlabel= r'Wavelength $(\AA)$', Plot_ylabel='Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$')
            Pv.SaveManager(SavingName ='A2_' + CodeName + '_Blue_Bump_Region', SavingFolder = FileFolder, ForceSave = True)
        
            Pv.ResetPlot()       
        
        #Red bump region
        if (Wave[0] < 5820) and (5900 < Wave[-1]):
            Label1 = CodeName + ' spectrum'    
            Pv.DataPloter_One(RedBump_Wave, RedBump_Int, Label1, Pv.Color_Vector[2][1])
            Pv.Labels_Legends_One(Plot_Title = 'Object ' + CodeName + ' Red Bump Region',Plot_xlabel= r'Wavelength $(\AA)$', Plot_ylabel='Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$')
            Pv.SaveManager(SavingName ='A3_' + CodeName + '_Red_Bump_Region', SavingFolder = FileFolder, ForceSave = True)

            Pv.ResetPlot()
        
        #OxygenVI region
        if (Wave[0] < 3790) and (4720 < Wave[-1]):
            Label1 = CodeName + ' spectrum'    
            Pv.DataPloter_One(OxygenVI_Wave, OxygenVI_Int, Label1, Pv.Color_Vector[2][3])
            Pv.Labels_Legends_One(Plot_Title = 'Object ' + CodeName + ' Oxygen VI Bump Region',Plot_xlabel= r'Wavelength $(\AA)$', Plot_ylabel='Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$')
            Pv.SaveManager(SavingName ='A4_' + CodeName + '_OxygenVI_Bump_Region', SavingFolder = FileFolder, ForceSave = True)
        
            Pv.ResetPlot()
                 
print "\nAll data treated generated"

