from CodeTools.PlottingManager              import myPickle
from PipeLineMethods.ManageFlow             import DataToTreat
from pylatex import Document, Section, Subsection, Tabular, MultiColumn, Table, MultiRow
from numpy import power    
    

    
# print 'Flujo limpio'
# print He_Flux3889
#     
# print 'A ver las partes'
# print (Flux_dict[He3889blended_label] / Flux_dict[HBeta_label] + Flux_H8)
# print ((EqW_dict[He3889_label] + a_H) / EqW_dict[He3889_label])
# print (0.104 * power(T_4, 0.046))
# print (power(10 ,-flambda_dict[He3889_label] * cHbeta))  


#Generate dazer object
pv                                          = myPickle()
 
#Define data type and location
Catalogue_Dic                               = DataToTreat()
Pattern                                     = Catalogue_Dic['Datatype'] + '.fits'
 
#Locate files on hard drive
FilesList                                   = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
 
#Parameters for the global output table
Table_Name                                  = 'cHbeta_Coefficients'
Table_Folder                                = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue/Data/'
 
#Define plot frame and colors
pv.FigFormat_One(ColorConf='Night1')
  
#Data_Dict
cHbeta_dict = {}
  
#Loop through files only if we are dealing the WHT data and only scientific objects:
if Catalogue_Dic['Datatype'] == 'WHT':
    for i in range(len(FilesList)):
                 
        #Analyze file address
        CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
     
        #Import cHbeta coefficient
        cHbeta_dict[CodeName]           = pv.GetParameter_ObjLog(CodeName, FileFolder, 'cHBeta')
 
doc     = Document(Table_Folder+ Table_Name)
 
with doc.create(Subsection('Table of something')):
    with doc.create(Table('|c|c|')) as table:
        for i in range(len(cHbeta_dict)):
            Key = str(cHbeta_dict.keys()[i])
            value = str(cHbeta_dict.values()[i].nominal_value)
            print 'Ahoratoca', Key, value
            table.add_hline()
            table.add_row((Key, value))
 
doc.generate_pdf(clean=True)
