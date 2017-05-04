'''
Created on Nov 15, 2015

@author: vital
'''
from CodeTools.PlottingManager              import myPickle
from PipeLineMethods.ManageFlow             import DataToTreat
from pylatex                                import Document, Section, Subsection, Tabular, MultiColumn, Table, MultiRow, Package, Figure
from numpy                                  import power    
from collections                            import OrderedDict
from Math_Libraries.sigfig                  import round_sig

#Table format
def Properties_Table_Data():
    
    #You should be able to generate a nice table format mechanism from this...
    #Text file which includes one column parameter, one column latex format, one column string format for floats
    
    #List Variables
    Elemental_Abundances                        = ['OI_HI','NI_HI','SI_HI','SI_HI_ArCorr','HeI_HI','Y_Mass_O']
    Ion_Abundanes                               = ['OII_HII', 'OII_HII_3279A', 'OII_HII_7319A', 'OIII_HII', 'NI_OI', 'NII_HII', 'SII_HII', 'SIII_HII', 'SIV_HII', 'HeII_HII', 'HeIII_HII']
    Physical_Properties                         = ['TOII', 'TOIII', 'TNII', 'TSII', 'TSIII', 'nSII']
    Inference_Ouput                             = ['ne_Inference','Te_Inference','y_plus_Inference','Y_Inference_O']

    Elemental_Abundances_labels                 = [r'$\frac{O}{H}$',r'$\frac{N}{H}$',r'$\frac{S}{H}$',r'$(\frac{S}{H})_{ArCor}$',r'$\frac{He}{H}$',r'$Y_{\frac{O}{H}}$']
    Ion_Abundanes_labels                        = [r'$(\frac{O^{1+}}{H^{1+}})$', r'$(\frac{O^{1+}}{H^{1+}})_{3279}$', r'$(\frac{O^{1+}}{H^{1+}})_{7319}$', r'$(\frac{O^{2+}}{H^{1+}})$', r'$\frac{N}{O}$', r'$(\frac{N^{1+}}{H^{1+}})$', r'$(\frac{S^{1+}}{H^{1+}})$', r'$(\frac{S^{2+}}{H^{1+}})$', r'$(\frac{S^{3+}}{H^{1+}})$', r'$(\frac{He^{1+}}{H^{1+}})$', r'$(\frac{He^{2+}}{H^{1+}})$']
    Physical_Properties_labels                  = [r'$T_{[OII]}$', r'$T_{[OIII]}$', r'$T_{[NII]}$', r'$T_{[SII]}$', r'$T_{[SIII]}$', r'$ne_{[SII]}$']
    Inference_Ouput_labels                      = [r'$ne_{Bayes}$',r'$Te_{Bayes}$',r'$(\frac{He^{1+}}{H^{1+}})$',r'$Y_{\frac{O}{H}}$']

    Elemental_Abundances_format                 = ['{:.3e}'] * len(Elemental_Abundances_labels)
    Ion_Abundanes_format                        = ['{:.3e}'] * len(Ion_Abundanes_labels)
    Physical_Properties_format                  = ['{:.2f}'] * len(Physical_Properties)
    Inference_Ouput_format                      = ['{:.2f}','{:.2f}','{:.3f}','{:.3f}']
    
    parameter_List                              = Elemental_Abundances + Ion_Abundanes + Physical_Properties + Inference_Ouput
    labels_List                                 = Elemental_Abundances_labels + Ion_Abundanes_labels + Physical_Properties_labels + Inference_Ouput_labels
    format_list                                 = Elemental_Abundances_format + Ion_Abundanes_format + Physical_Properties_format + Inference_Ouput_format
    
    Properties_dict = OrderedDict()
    for i in range(len(parameter_List)):
        parameter = parameter_List[i]
        Properties_dict[parameter] = OrderedDict()
        Properties_dict[parameter]['label']     = labels_List[i]
        Properties_dict[parameter]['format']    = format_list[i]
        
    return Properties_dict

#Generate dazer object

pv                                          = myPickle()
 
#Define data type and location
Catalogue_Dic                               = DataToTreat()
Pattern                                     = Catalogue_Dic['Datatype'] + '.fits'
 
#Locate files on hard drive
FilesList                                   = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
 
#Parameters for the global output table
Table_Name                                  = 'Cataloge_properties_log'
Table_Folder                                = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue/Data/'
 
#Define plot frame and colors
pv.FigFormat_One(ColorConf='Night1')
  
Data_Dict                                   = OrderedDict()
Properties_dict                             = Properties_Table_Data()  
parameter_List                              = Properties_dict.keys()
Address_dict                                = OrderedDict()

#Generate list of objects (Dazer should have a method for this)
for i in range(len(FilesList)):                 
    
    CodeName, FileName, FileFolder          = pv.Analyze_Address(FilesList[i])
    Data_Dict[CodeName]                     = OrderedDict()
    
    for j in range(len(parameter_List)):
        parameter                           = parameter_List[j]
        Data_Dict[CodeName][parameter]      = pv.GetParameter_ObjLog(CodeName, FileFolder, parameter, 'string', sigfig=4, strformat= Properties_dict[parameter]['format'])
             
#Get alphabetically ordered list of dictionary:
HII_Galaxy_List = Data_Dict.keys()
HII_Galaxy_List.sort()

#Generate Document
doc = Document(Table_Folder+ Table_Name)
doc.packages.append(Package('geometry', options=['tmargin=2cm', 'lmargin=1cm', 'rmargin=1cm','bmargin=2cm']))
doc.packages.append(Package('preview', options=['active', 'tightpage',]))

#Define font size
doc.append(r'\tiny')

#String with the columns format : |c|c|c|
columns_latexformat = '|c'*(len(HII_Galaxy_List) +1) + '|'
print columns_latexformat
print len(HII_Galaxy_List)
print len(HII_Galaxy_List) +1
#Generate table
doc.append(r'\begin{preview}')               
with doc.create(Table(columns_latexformat)) as table:
    
    Table_Headers = ['Parameter'] + HII_Galaxy_List
    table.add_hline()
    table.add_row(Table_Headers)
    
    for parameter in parameter_List:       
        row_list    = []
        Label       = Properties_dict[parameter]['label']
        row_list.append(Properties_dict[parameter]['label'])

        for Galaxy in HII_Galaxy_List:    
            value   = str(Data_Dict[Galaxy][parameter])
            row_list.append(value)
            
        table.add_hline()
        table.add_row(row_list)
        
table.add_hline()
doc.append(r'\end{preview}')               
doc.generate_pdf(clean=True)
