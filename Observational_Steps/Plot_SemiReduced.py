#!/usr/bin/env python

from CodeTools.PlottingManager  import myPickle

#Declare code classes
pv  = myPickle()

#Declare data to treat
Catalogue_Dic   = '/home/vital/Astrodata/WHT_04_2016/FastReduction/'
Pattern         =  '-spec.fits'

#Find and organize files from terminal command or .py file
FilesList       = pv.Folder_Explorer(Pattern,  Catalogue_Dic, CheckComputer=False)

#Generate plot frame and colors
pv.FigFormat_One(ColorConf='Night1')

#Loop through files
for i in range(len(FilesList)):
    
    if '.fits_' not in FilesList[i]:
        #Analyze file address
        print 'File', FilesList[i]
        
        CodeName, FileName, FileFolder      = pv.Analyze_Address(FilesList[i])
        
        #Import fits file
        Wave, Int, ExtraData                = pv.File_to_data(FileFolder,FileName)
    
        if 'Blue' in FileName:
            Color =  pv.Color_Vector[2][2]
        if 'Red' in FileName:
            Color =  pv.Color_Vector[2][1]
    
    
        #Plot the data
        pv.DataPloter_One(Wave, Int, ' ', LineColor = Color)
        
        # Set titles and legend  
        pv.Labels_Legends_One(Plot_Title = 'Object ' + FileName)
        
        # Save data  
        pv.SaveManager(SavingName = FileName + '_Basic_Reduction', SavingFolder = FileFolder)
        
        #Clear figure for new plot    
        pv.ResetPlot()            
                
        print i+1, '/' , len(FilesList)
