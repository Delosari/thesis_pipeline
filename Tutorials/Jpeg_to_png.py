#!/usr/bin/env python
import matplotlib.pyplot as plt
import Code_Lib.MethodsPyplot as mp
import Code_Lib.vitools as vit
import Image

RootFolder  = "/Users/INAOE_Vital/Dropbox/Astrophysics/Data/WHT_HII_Galaxies/"
Pattern = ".jpg"
# Pattern =                 'obj08_Blue_t_z_EBV.fits'
PlotVector = None

#Find and organize files from terminal command or .py file
FilesList, PlotVector = mp.FindAndOrganize(PlotVector, Pattern, RootFolder)

#Loop through files
for i in range(len(FilesList)):
    plt.cla()
    #Store plot properties and command flags
    
    for j in range(len(FilesList[i])):
        CodeName, FileName, FileFolder, PlotVector = mp.FileAnalyzer(FilesList[i][j], PlotVector)

        Input_ImageName = FileName
        Im = Image.open(FileFolder + Input_ImageName)
        Output_ImageName = CodeName + 'png'
        Im.save(FileFolder + Output_ImageName)
        Im.close()
        
        print FileName


    print i+1, '/' , len(FilesList)

#-----------------------------------------------------------------------------------------------------

print "All plots generated"