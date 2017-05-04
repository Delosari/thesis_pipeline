import pyneb
from dazer_methods import Dazer
from libraries.Plotting_Libraries.dazer_plotter         import Plot_Conf

print 'Hi'

 
# import pyneb                                as pn
# from pylatex                                import NoEscape, Document, Section, Subsection, Tabular, MultiColumn, Table, MultiRow, Package, Figure
# from ManageFlow                             import DataToTreat
# from uncertainties                          import UFloat, ufloat
# from CodeTools.PlottingManager              import myPickle
# from uncertainties.umath                    import log10 as umath_log10
# from collections                            import OrderedDict
#  
# def OrganizedObject_List():
#          
#     CleanList = ['03', '04v1', '04v2', '06', '08', '09', '10', '11', '14', '24', '27', '70', '71', 'SDSS1', 'SDSS2', 'SDSS3', '51959-092', '51991-224', '52235-602', '52319-521', '52703-612v2', 'J2225', 'SHOC036', 'SHOC575v1', 'SHOC575v2', 'SHOC579', 'SHOC588', 'SHOC593']
#     return CleanList
#    
# pv = myPickle()
#  
# #Define data type and location
# Catalogue_Dic           = DataToTreat()
# Pattern                 = '_log.txt'
# AbundancesFileExtension = '_WHT_EmissionReddend_LinesLog_v3.txt'
# database_extension      = '_extandar_30000_5000_10_v2'
# globalfile_extension    = '_global_30000_5000_10_v2'
#  
# #Locate files on hard drive
# FilesList               = OrganizedObject_List() 
# 
# #Define plot frame and colors
# pv.FigFormat_One(ColorConf = 'Night1')
#  
# #Get the dictionary with the headers format and the data
# pv.galaxylog_v2_headers()
#  
# #Prepare PyNeb data for ratios characteristics
# pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
# O3 = pn.Atom('O', 3) 
# N2 = pn.Atom('N', 2)
# S3 = pn.Atom('S', 3)
# Atom_Dict = dict()
# Atom_Dict['O3_ratio'] = O3.getEmissivity(10000, 100, wave = 5007) / O3.getEmissivity(10000, 100, wave = 4959) 
# Atom_Dict['N2_ratio'] = N2.getEmissivity(10000, 100, wave = 6584) / N2.getEmissivity(10000, 100, wave = 6548)
# Atom_Dict['S3_ratio'] = S3.getEmissivity(10000, 100, wave = 9531) / S3.getEmissivity(10000, 100, wave = 9069)
#   
# #Dictionary with the variables we want to compare 
# variables_dict = OrderedDict()
# variables_dict['y_plus_inf']    = 'HeII_HII'
# variables_dict['Te_inf']        = 'TSIII'
# variables_dict['ne_inf']        = 'nSII'
# variables_dict['cHbeta_inf']    = 'cHBeta'
# 
# #Generate object table (it also works as table type)
# Table_Name  = 'Catalogue_Propertieslog' 
# pv.latex_header(Catalogue_Dic['Data_Folder'], Table_Name)
#  
# #Declare the table header
# pv.table_header(Table_Name)
# 
# #Loop through the files 
# for i in range(len(FilesList)):
#  
#     #Trick to analyse the folders in the order I want
#     CurrentFile = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue/Objects/' + FilesList[i] + '/' + FilesList[i] + '_WHT_LinesLog_v3.txt' 
#  
#     #Declare file address and logs address
#     CodeName, FileName, FileFolder  = pv.Analyze_Address(CurrentFile)
#     ObjLog_Address  = FileFolder + FileName
#     LineLog_Address = FileFolder + CodeName + '_WHT_LinesLog_v3.txt'
#      
#     #Load the data
#     Ratios_dict, RatiosColor_dict = pv.load_Galaxy_Ratios(FileFolder, CodeName, '_WHT_LinesLog_v3.txt', Atom_Dict)
#      
#     #Generate object row of data 
#     data_keys   = pv.header_dict.keys()
#     Object_row  = ['None'] * len(pv.header_dict)
#      
#     #Load the data row
#     Object_row[0] = CodeName
#     for j in range(1, len(Object_row)):
#         
#         #Current entry 
#         thekey = data_keys[j]
#         
#         #Save the cell value in the row list of elements
#         Object_row[j] = pv.galaxylog_v2_contents(thekey, Ratios_dict, RatiosColor_dict, variables_dict, CodeName, FileFolder)
#                                    
#     #Insert the row
#     pv.table.add_row(Object_row, escape=False)
#  
# #Close the table
# pv.table_footer(Table_Name)
# 
# print 'File generated'