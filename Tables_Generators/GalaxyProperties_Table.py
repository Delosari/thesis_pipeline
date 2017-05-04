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

    Elemental_Abundances_format                 = ['{:.5e}'] * len(Elemental_Abundances_labels)
    Ion_Abundanes_format                        = ['{:.5e}'] * len(Ion_Abundanes_labels)
    Physical_Properties_format                  = ['{:.2f}'] * len(Physical_Properties)
    Inference_Ouput_format                      = ['{:.2f}','{:.2f}','{:.5e}','{:.5f}']
    
    parameter_List                              = Elemental_Abundances + Ion_Abundanes + Physical_Properties + Inference_Ouput
    labels_List                                 = Elemental_Abundances_labels + Ion_Abundanes_labels + Physical_Properties_labels + Inference_Ouput_labels
    format_list                                 = Elemental_Abundances_format + Ion_Abundanes_format + Physical_Properties_format + Inference_Ouput_format
    
    Properties_dict = OrderedDict()
    for i in range(len(parameter_List)):
        parameter                               = parameter_List[i]
        Properties_dict[parameter]              = OrderedDict()
        Properties_dict[parameter]['label']     = labels_List[i]
        Properties_dict[parameter]['format']    = format_list[i]
        
    return Properties_dict

linesLog_Headers                            = ['Ion', 'TheoWavelength',     'WaveBrute',          'FluxBrute',          'FluxGauss',        'ErrorEL_MCMC',        'Eqw',       'ErrorEqw']
Labels_list                                 = ['Ion', r'$\lambda_{Theo}$',  r'$\lambda_{Obs}$',   r'$F_{Integrated}$',  r'$F_{Reduced}$',   r'$EW$']
Log_extension_red                           = '_WHT_LinesLog_v3.txt'  
Log_extension_dered                         = '_WHT_dered_LinesLog_v3.txt'
Log_extension_Neb                           = '_WHT_dered_Neb_LinesLog_v3.txt'
Log_extension_Stellar                       = '_WHT_dered_Neb_Stellar_LinesLog_v3.txt'
#Generate dazer object
pv                                          = myPickle()
 
#Define data type and location
Catalogue_Dic                               = DataToTreat()
Pattern                                     = Catalogue_Dic['Datatype'] + '.fits'
 
#Locate files on hard drive
FilesList                                   = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
 
#Parameters for the global output table
Table_Name                                  = 'HII_Galaxies_Properties'
Table_Folder                                = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue/Data/'
 
#Define plot frame and colors
pv.FigFormat_One(ColorConf='Night1')
  
Data_Dict                                   = OrderedDict()
Lines_Dict                                  = OrderedDict()
Properties_dict                             = Properties_Table_Data()  
parameter_List                              = Properties_dict.keys()
Address_dict                                = OrderedDict()

#Generate list of objects (Dazer should have a method for this)
for i in range(len(FilesList)):                 
    
    CodeName, FileName, FileFolder          = pv.Analyze_Address(FilesList[i])
    Data_Dict[CodeName]                     = OrderedDict()
    Lines_Dict[CodeName]                    = OrderedDict()
    
    for j in range(len(parameter_List)):
        parameter                           = parameter_List[j]
        Data_Dict[CodeName][parameter]      = pv.GetParameter_ObjLog(CodeName, FileFolder, parameter, 'string', sigfig=5, strformat= Properties_dict[parameter]['format'])
    
    for i in range(len(linesLog_Headers)):
        Code    = linesLog_Headers[i]
        if Code == 'Ion':
            Lines_Dict[CodeName][Code]     =   pv.get_ColumnData([Code], FileFolder + CodeName + Log_extension_red, datatype=str, HeaderSize = 2) 
        else: 
            Lines_Dict[CodeName][Code]     =   pv.get_ColumnData([Code], FileFolder + CodeName + Log_extension_red, HeaderSize = 2) 
            
        Lines_Dict[CodeName]['Flux Neb']        =   pv.get_ColumnData(['FluxGauss'],    FileFolder + CodeName + Log_extension_Neb, datatype=str, HeaderSize = 2) 
        Lines_Dict[CodeName]['Error Neb']       =   pv.get_ColumnData(['ErrorEL_MCMC'], FileFolder + CodeName + Log_extension_Neb, datatype=str, HeaderSize = 2) 
        Lines_Dict[CodeName]['Flux Stellar']    =   pv.get_ColumnData(['FluxGauss'],    FileFolder + CodeName + Log_extension_Stellar, datatype=str, HeaderSize = 2) 
        Lines_Dict[CodeName]['Error Stellar']   =   pv.get_ColumnData(['ErrorEL_MCMC'], FileFolder + CodeName + Log_extension_Stellar, datatype=str, HeaderSize = 2)
         
#Get alphabetically ordered list of dictionary:
HII_Galaxy_List = Data_Dict.keys()
HII_Galaxy_List.sort()

#Generate Document
doc = Document(Table_Folder+ Table_Name)

doc.packages.append(Package('geometry', options=['tmargin=2cm', 'lmargin=1cm', 'rmargin=1cm','bmargin=2cm']))
doc.packages.append(Package('floatrow'))
doc.preamble.append(r'\DeclareFloatFont{huge}{\huge}')
doc.preamble.append(r'\floatsetup[table]{font=huge}')

# doc.append(r'\DeclareFloatFont{tiny}{\tiny}')
# doc.append(r'\floatsetup[table]{font=tiny}')

#Main section manuscript
with doc.create(Section('HII Galaxies properties:')):
    
    for i in range(len(HII_Galaxy_List)):
        Galaxy = HII_Galaxy_List[i]
        
        with doc.create(Subsection('Galaxy ' + Galaxy)):
            with doc.create(Table('|c|c|')) as table:
                for parameter in parameter_List:                    
                    Label   = Properties_dict[parameter]['label']
                    value   = str(Data_Dict[Galaxy][parameter])
                    table.add_hline()
                    table.add_row((Label, value))

            doc.append(r'\newpage')
            doc.append(r'\tiny')
            
            with doc.create(Table('|c|c|c|c|c|c|c|c|')) as table:
#                 List_Headers = Lines_Dict[CodeName].keys() + [r'$F_{Nebular}$', r'$F_{Stellar}$']
                List_Lines  = Lines_Dict[CodeName]['Ion'] 
                table.add_hline()
                table.add_row(Labels_list + [r'$F_{Nebular}$', r'$F_{Stellar}$'])    
                
                for j in range(len(List_Lines)):                 
                    Column1 =   Lines_Dict[CodeName]['Ion'][j].replace('_', '-')
                    Column2 =   round_sig(Lines_Dict[CodeName]['TheoWavelength'][j], 5)
                    Column3 =   round_sig(Lines_Dict[CodeName]['WaveBrute'][j], 5)
                    Column4 =   round_sig(Lines_Dict[CodeName]['FluxBrute'][j], 4)
                    Column5 =   round_sig(Lines_Dict[CodeName]['FluxGauss'][j], 3) + r'$\pm$' + round_sig(Lines_Dict[CodeName]['ErrorEL_MCMC'][j], 3)
                    Column6 =   round_sig(Lines_Dict[CodeName]['Eqw'][j], 2, scien_notation=False) + r'$\pm$' + round_sig(Lines_Dict[CodeName]['ErrorEqw'][j], 3, scien_notation=False)
                    Column7 =   round_sig(Lines_Dict[CodeName]['Flux Neb'][j], 3) + r'$\pm$' + round_sig(Lines_Dict[CodeName]['Error Neb'][j], 3)
                    Column8 =   round_sig(Lines_Dict[CodeName]['Flux Stellar'][j], 3) + r'$\pm$' + round_sig(Lines_Dict[CodeName]['Error Neb'][j], 3)
                    
                    table.add_hline()
                    table.add_row((Column1,Column2,Column3,Column4,Column5,Column6,Column7,Column8))                    
    
#             with doc.create(Subsection(r'$\chi^{2}$ plots:')):
#                 with doc.create(Figure(position='h!')) as kitten_pic:
#                     kitten_pic.add_image('docs/static/kitten.jpg', width='120px')
#                     kitten_pic.add_caption('Look it\'s on its back')    
    
    
    
    doc.append(r'\newpage')
    
doc.generate_pdf(clean=True)
