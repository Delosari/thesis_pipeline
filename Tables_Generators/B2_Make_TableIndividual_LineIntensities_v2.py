#!/usr/bin/python

from    numpy                                       import where
from    Tutorials                                   import TableMaker
from    PipeLineMethods.ManageFlow                  import DataToTreat

import  CodeTools.PlottingManager                   as plotMan
from    CodeTools.File_Managing_Tools               import Tables_Txt

# Importing data manager
pv  = plotMan.myPickle()
tm  = Tables_Txt()

#Declaring lines log to treat
DataLog_Extension                       = '_dr10_LinesLog_v3.txt'                    #First batch process for untreated spectra
TexTable_Extension                      = '_TableSingleIntensities.tex'              #First data log for untreated spectra
# DataLog_Extension                       = '_WHT_LinesLog_v3.txt'                   #First batch process for untreated spectra
# TexTable_Extension                      = '_WHT_TableSingleIntensities.tex'        #First data log for untreated spectra

#Load the files
CatalogueFolder, DataType, Log_Format   = DataToTreat()
Pattern                                 = DataType + '.fits'

#Find and organize files from terminal command or .py file
FilesList                               = pv.FindAndOrganize(Pattern, CatalogueFolder, CheckComputer=True)

#Default header size
HeaderSize                              = 2

#Emision line to normalized
HBeta_Ion                               = "Hbeta_4_2"

for m in range(len(FilesList)):    
    for j in range(len(FilesList[m])):

#       Get the spectrum:              
        CodeName, FileName, FileFolder = pv.FileAnalyzer(FilesList[m][j])
    
        #Load data from table
        tm.select_Table(FileFolder + CodeName + DataLog_Extension, HeaderSize = HeaderSize, loadheaders_check = True)
        EmissionLine                                = tm.get_ColumnData(['Ion'], HeaderSize, datatype = str) 
        Wavelength, Flux, Eqw, FluxError, EqwError  = tm.get_ColumnData(['WaveGauss', 'FluxGauss', 'Eqw', 'ErrorEL_MCMC', 'ErrorEqw'], HeaderSize = HeaderSize)
        
        #Generate the latex file 
        Table = TableMaker.Latex_pyTable()
        Table.Start_TexFile(FileFolder, CodeName + TexTable_Extension)
        Table.Start_Table('lrrr', Title = 'Object ' + CodeName + ' line intensities ' + '$(I(H\\beta)=100$)')
        Table.Table_Header(['', 'Wave $(\\AA)$', '$I(\\lambda)$', 'EqW $(\\AA)$'])
        
        # Get normalization Emissionline:
        Hbeta_index = where(EmissionLine == HBeta_Ion)
        HBeta_Flux  = float(Flux[Hbeta_index])
        Factor      = 100
        
        for k in range(len(EmissionLine)):
            Flux_Formated       = round(Flux[k]         /   HBeta_Flux * Factor, 3)
            Error_Formated      = round(FluxError[k]    /   HBeta_Flux * Factor, 3)
            Eqw_Formated        = round(Eqw[k]          ,   3)
            Eqw_Error_Formated  = round(EqwError[k]     ,   2)
            Table.InsertTable_Row([EmissionLine[k]      ,   round(Wavelength[k],0)   ,   [Flux_Formated,Error_Formated],    [Eqw_Formated,Eqw_Error_Formated]])
        
        Table.InsertTable_Row(["", "", '', ''])
        Table.InsertTable_Row(["$I(H\\beta)$" "$(erg\,cm^{-2} s^{-1})$", HBeta_Flux, '', ''])
        
        Table.Finish_Table()
        
        Table.Finish_TexFile()

        print '---File saved at ', FileFolder + CodeName + TexTable_Extension
        