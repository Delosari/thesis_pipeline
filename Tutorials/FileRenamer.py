#!/usr/bin/python

import sys
import os
import Code_Lib.vitools as vit
import Scientific_Lib.AstroMethods as astro

ArgumentsCheck, Arguments = vit.Arguments_Checker(sys.argv)

print "Initiating " + Arguments[0][Arguments[0].rfind("/")+1:len(Arguments[0])] + " task\n"

FilesList, FlagsList = vit.Arguments_Handler(ArgumentsCheck, Arguments)

if ArgumentsCheck == False:  
    Folder = "/home/vital/Desktop/Seventh_Search/"
    FilesList = vit.FilesFinder(Folder,"spec")
    FlagsList = ["-0000","-1111"]
    
for i in range(len(FilesList)):
    print i
    File = FilesList[i]
    
    ObjName, FileName, FolderName = vit.AddressAnalyzer(File)
    FileNew = FileName.replace("-","_")
    FileNewNew = FileNew.replace(".fits","_dr10.fits")
    vit.FileRenamer(File,FileName,FileNewNew)

print "se acabo"