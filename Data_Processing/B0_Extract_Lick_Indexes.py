#!/usr/bin/python

from dazer_methods import Dazer

#Create class object
dz = Dazer()
script_code     = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
log_exension    = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'

#Define operation
Catalogue_Dic           = dz.import_catalogue()
Pattern                 =  '_' + Catalogue_Dic['Datatype'] + '_linesLog_reduc.txt'

#Define table shape
Width                   = "%" + str(50+2) + "s"
HeaderSize              = 2
LickIndexesHeader       = ['Ion', 'lambda_theo', 'group_label','Wave1', 'Wave2', 'Wave3', 'Wave4', 'Wave5', 'Wave6', 'add_wide_component']
columns_format          = ['%11.6f', '%11.6f', '%11.6f','%11.6f', '%11.6f', '%11.6f', '%11.6f', '%11.6f', '%11.6f', '%11.6f']

#Loop through the objects
for i in range(len(catalogue_df.index)):

    #Object
    objName             = catalogue_df.iloc[i].name
        
    fits_file           = catalogue_df.iloc[i].reduction_fits
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    lineslog_address    = '{objfolder}{codeName}_WHT_linesLog_reduc.txt'.format(objfolder = ouput_folder, codeName=objName)

    print '-- Treating {} @ {}'.format(objName, fits_file)

    #Load the lines log
    lineslog_frame      = dz.load_lineslog_frame(lineslog_address)
    
    #Extract the information corresponding to the lines selection
    lick_icds_frame     = lineslog_frame[LickIndexesHeader]

    #Convert to string format and save to text file
    string_frame = lick_icds_frame.to_string()    
    lick_txt = '{}{}_lick_indeces.txt'.format(ouput_folder, objName)
    with open(lick_txt, 'wb') as f:
        f.write(string_frame.encode('UTF-8'))
    
print 'Data treated'

#     #Save the data frame
#     lick_txt = '{}{}_lick_indeces_text.txt'.format(ouput_folder, objName)
#     lick_icds_frame.to_csv(lick_txt, sep=' ', float_format='%.6f', columns=None, header=True, index=True)
#
# #Loop through the objects
# for i in range(len(catalogue_df.index)):
#             
#     CodeName, FileName, FileFolder = dz.Analyze_Address(FilesList[i])
#             
#     InputTextFile                   = open(FileFolder + FileName,"r")
#     TextLines                       = InputTextFile.readlines()
#     InputTextFile.close()
#     
#     OutputFileName                  = CodeName + '_LickIndexes.txt'
#     New_Folder                      = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue_SulfurRegression/Objects/' + CodeName + '/'
# 
#     OutputTextFile                  = open(New_Folder + OutputFileName,"w")
#     LickIndexesHeader_Row           = "".join(Width % m for m in LickIndexesHeader)
#     OutputTextFile.write(LickIndexesHeader_Row + "\n")
#     
#     LinesLogHeader                  = TextLines[1].split()
#     Label_Index                     = LinesLogHeader.index('Line_Label')
#     Ion_Index                       = LinesLogHeader.index('Ion')
#     TheoWave_Index                  = LinesLogHeader.index('TheoWavelength')
#     Blended_Index                   = LinesLogHeader.index('Blended_Set')
# 
#     Wave1_Index                     = LinesLogHeader.index('Wave1')
#     Wave2_Index                     = LinesLogHeader.index('Wave2')
#     Wave3_Index                     = LinesLogHeader.index('Wave3')
#     Wave4_Index                     = LinesLogHeader.index('Wave4')
#     Wave5_Index                     = LinesLogHeader.index('Wave5')
#     Wave6_Index                     = LinesLogHeader.index('Wave6')
# 
#     WC_Index                        = LinesLogHeader.index('Wide_component')
# 
#     for j in range(HeaderSize, len(TextLines)):
#         InputLine           = TextLines[j].split()     
#         Blended_Value       = InputLine[Blended_Index]
#         
#         if Blended_Value == 'None':
#             Lick_Values     = [InputLine[Label_Index], InputLine[Ion_Index], InputLine[TheoWave_Index], InputLine[Blended_Index], InputLine[Wave1_Index], InputLine[Wave2_Index], InputLine[Wave3_Index], InputLine[Wave4_Index],InputLine[Wave5_Index], InputLine[Wave6_Index], InputLine[WC_Index]]
#             OutputLine      = "".join(Width % n for n in Lick_Values)
#             OutputTextFile.write(OutputLine + "\n")
# 
#         else:
#             FirstWavelength = Blended_Value[0:Blended_Value.find('A_')+1]
#             if InputLine[Label_Index] == FirstWavelength:
#                 Lick_Values = [InputLine[Label_Index], InputLine[Ion_Index], InputLine[TheoWave_Index], InputLine[Blended_Index], InputLine[Wave1_Index], InputLine[Wave2_Index], InputLine[Wave3_Index], InputLine[Wave4_Index],InputLine[Wave5_Index], InputLine[Wave6_Index], InputLine[WC_Index]]
#                 OutputLine  = "".join(Width % m for m in Lick_Values)
#                 OutputTextFile.write(OutputLine + "\n")
#                                 
#     OutputTextFile.close() 
#                      
# print "\nAll data treated generated"
# 
# print 'This files gave an error'
# for fileuco in dz.ErrorList:
#     print fileuco[0]
#     print fileuco[1]
    

# #!/usr/bin/python
# 
# from dazer_methods import Dazer
# 
# dz = Dazer()
# 
# #Define operation
# Catalogue_Dic           = dz.import_catalogue()
# Pattern                 =  '_' + Catalogue_Dic['Datatype'] + '_LinesLog_v3.txt'
# 
# #Define table shape
# Width                   = "%" + str(50+2) + "s"
# HeaderSize              = 2
# LickIndexesHeader       = ["Line_Label", "Ion", "TheoWavelength", "Blended_Set","Wave1", "Wave2", "Wave3", "Wave4", "Wave5", "Wave6", "Wide_component"]
# 
# #Import the text lines logs from which we generate the lick indexes
# FilesList       = dz.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
# 
# for i in range(len(FilesList)):
#         
#     CodeName, FileName, FileFolder = dz.Analyze_Address(FilesList[i])
#             
#     InputTextFile                   = open(FileFolder + FileName,"r")
#     TextLines                       = InputTextFile.readlines()
#     InputTextFile.close()
#     
#     OutputFileName                  = CodeName + '_LickIndexes.txt'
#     New_Folder                      = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue_SulfurRegression/Objects/' + CodeName + '/'
# 
#     OutputTextFile                  = open(New_Folder + OutputFileName,"w")
#     LickIndexesHeader_Row           = "".join(Width % m for m in LickIndexesHeader)
#     OutputTextFile.write(LickIndexesHeader_Row + "\n")
#     
#     LinesLogHeader                  = TextLines[1].split()
#     Label_Index                     = LinesLogHeader.index('Line_Label')
#     Ion_Index                       = LinesLogHeader.index('Ion')
#     TheoWave_Index                  = LinesLogHeader.index('TheoWavelength')
#     Blended_Index                   = LinesLogHeader.index('Blended_Set')
# 
#     Wave1_Index                     = LinesLogHeader.index('Wave1')
#     Wave2_Index                     = LinesLogHeader.index('Wave2')
#     Wave3_Index                     = LinesLogHeader.index('Wave3')
#     Wave4_Index                     = LinesLogHeader.index('Wave4')
#     Wave5_Index                     = LinesLogHeader.index('Wave5')
#     Wave6_Index                     = LinesLogHeader.index('Wave6')
# 
#     WC_Index                        = LinesLogHeader.index('Wide_component')
# 
#     for j in range(HeaderSize, len(TextLines)):
#         InputLine           = TextLines[j].split()     
#         Blended_Value       = InputLine[Blended_Index]
#         
#         if Blended_Value == 'None':
#             Lick_Values     = [InputLine[Label_Index], InputLine[Ion_Index], InputLine[TheoWave_Index], InputLine[Blended_Index], InputLine[Wave1_Index], InputLine[Wave2_Index], InputLine[Wave3_Index], InputLine[Wave4_Index],InputLine[Wave5_Index], InputLine[Wave6_Index], InputLine[WC_Index]]
#             OutputLine      = "".join(Width % n for n in Lick_Values)
#             OutputTextFile.write(OutputLine + "\n")
# 
#         else:
#             FirstWavelength = Blended_Value[0:Blended_Value.find('A_')+1]
#             if InputLine[Label_Index] == FirstWavelength:
#                 Lick_Values = [InputLine[Label_Index], InputLine[Ion_Index], InputLine[TheoWave_Index], InputLine[Blended_Index], InputLine[Wave1_Index], InputLine[Wave2_Index], InputLine[Wave3_Index], InputLine[Wave4_Index],InputLine[Wave5_Index], InputLine[Wave6_Index], InputLine[WC_Index]]
#                 OutputLine  = "".join(Width % m for m in Lick_Values)
#                 OutputTextFile.write(OutputLine + "\n")
#                                 
#     OutputTextFile.close() 
#                      
# print "\nAll data treated generated"
# 
# print 'This files gave an error'
# for fileuco in dz.ErrorList:
#     print fileuco[0]
#     print fileuco[1    
    
    
    