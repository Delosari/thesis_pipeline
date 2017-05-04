#!/usr/bin/python

from Tutorials import TableMaker
from CodeTools.MethodsPyplot import Log_2_Parameter
from PipeLineMethods.ManageFlow import DataToTreat
import CodeTools.PlottingManager as plotMan

def GetDataTable(FileFolder, CodeName, DataLog_Extension):
    
    DataTable = []
    
#   ImportData_Log 
    Data_Log_Name   = FileFolder + CodeName + DataLog_Extension
    Data_Log_File   =  open(Data_Log_Name, "r")
    TextLines       = Data_Log_File.readlines()
    Data_Log_File.close()

#   Declare lists of parameters
    Ions_list              = []
    Fluxes_list            = []
    Wave_list              = []
    EqW_list               = []
    FluxError_list          = []
    EqWError_list           =[]

    #Loop through the lies         
    for k in range(HeaderSize ,len(TextLines)):
        Record_k        = TextLines[k].split()
        Ion_k           = Record_k[1]
        Wave_k          = float(Record_k[2])
        Flux_Gauss_k    = float(Record_k[4])
        EqW_k           = float(Record_k[7])
        Error_Flux_k      = float(Record_k[8])
        Error_Eqw_k       = float(Record_k[9])
        
        if Ion_k == HBeta_Ion:
            Ion_Hbeta           = Record_k[1]
            Wave_Hbeta          = float(Record_k[2])
            Flux_Gauss_Hbeta    = float(Record_k[4])
            EqW_Hbeta           = float(Record_k[7])

        Ions_list.append(           Ion_k            )
        Wave_list.append(           Wave_k           )
        Fluxes_list.append(         Flux_Gauss_k     )
        EqW_list.append(            EqW_k            )
        FluxError_list.append(      Error_Flux_k     )    
        EqWError_list.append(       Error_Eqw_k      )
        
    HBeta_list =     [Ion_Hbeta, Wave_Hbeta, Flux_Gauss_Hbeta, EqW_Hbeta]
    
    cHBeta_Galaxy = Log_2_Parameter(FileFolder, CodeName, "cHBeta")
    
#   Add data to table
    DataTable.append([Ions_list, Wave_list, Fluxes_list, EqW_list, FluxError_list, EqWError_list, HBeta_list, cHBeta_Galaxy])

    return DataTable

DataLog_Extension   = '_dr10_LinesLog_v3.txt'                    #First batch process for untreated spectra
TexTable_Extension  = '_TableSingleIntensities.tex'        #First data log for untreated spectra

# DataLog_Extension   = '_WHT_LinesLog_v3.txt'                    #First batch process for untreated spectra
# TexTable_Extension  = '_WHT_TableSingleIntensities.tex'        #First data log for untreated spectra

CatalogueFolder, DataType, Log_Format  = DataToTreat()
Pattern = DataType + '.fits'

# Importing Dazer libraries for launching the batch measurement
pv  = plotMan.myPickle()

#Find and organize files from terminal command or .py file
FilesList = pv.FindAndOrganize(Pattern, CatalogueFolder, CheckComputer=True)
            
HBeta_Ion           = "Hbeta_4_2"

HeaderSize = 2

for m in range(len(FilesList)):    
    for j in range(len(FilesList[m])):

#       Get the spectrum:              
        CodeName, FileName, FileFolder = pv.FileAnalyzer(FilesList[m][j])
    
        LineIntensity_Table = GetDataTable(FileFolder, CodeName, DataLog_Extension)
         
        Table = TableMaker.Latex_pyTable()
        
        Table.Start_TexFile(FileFolder, CodeName + TexTable_Extension)
        
        Table.Start_Table('lrrr', Title = 'Object ' + CodeName + ' line intensities ' + '$(I(H\\beta)=100$)')
        
        Table.Table_Header(['', 'Wave $(\\AA)$', '$I(\\lambda)$', 'EqW $(\\AA)$'])
        
        HBeta_Flux = LineIntensity_Table[0][6][2]
        Factor = 100
        
        for m in range(len(LineIntensity_Table[0][0])):
            Ion, Wave, Flux, EqW, Error_Flux, Error_Eqw = LineIntensity_Table[0][0][m], LineIntensity_Table[0][1][m], LineIntensity_Table[0][2][m], LineIntensity_Table[0][3][m], LineIntensity_Table[0][4][m], LineIntensity_Table[0][5][m]
            Flux_Formated       = round(Flux / HBeta_Flux * Factor, 3)
            Error_Formated      = round(Error_Flux/HBeta_Flux * Factor, 3)
            Eqw_Formated        = round(EqW, 3)
            Eqw_Error_Formated  = round(Error_Eqw, 2)
            Table.InsertTable_Row([Ion, round(Wave,0), [Flux_Formated,Error_Formated], [Eqw_Formated,Eqw_Error_Formated]])
        
        print 'Hbeta properties', LineIntensity_Table[0][6]
        print 'Hbeta flux aqui', LineIntensity_Table[0][6][2]
        print 'cHbeta', LineIntensity_Table[0][7]
        
        Table.InsertTable_Row(["", "", '', ''])
        print 'a ver que voy...', type(HBeta_Flux)
        Table.InsertTable_Row(["$I(H\\beta)$" "$(erg\,cm^{-2} s^{-1})$", HBeta_Flux, '', ''])
#         Table.InsertTable_Row(["$c(H\\beta)$", round(LineIntensity_Table[0][7], 3), '', ''])
        
        Table.Finish_Table()
        
        Table.Finish_TexFile()

        print '---File saved at ', FileFolder + CodeName + TexTable_Extension


#                       0            1         2            3            4          5                6            7
#                    Ions_list, Wave_list, Fluxes_list, EqW_list, FluxError_list, EqWError_list, HBeta_list, cHBeta_Galaxy

#                         0           1               2               3
#                     [Ion_Hbeta, Wave_Hbeta, Flux_Gauss_Hbeta, EqW_Hbeta]

        