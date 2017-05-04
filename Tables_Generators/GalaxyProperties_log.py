import pyneb                    as pn
from pylatex                    import Tabular
from ManageFlow                 import DataToTreat
from collections                import OrderedDict
from uncertainties              import ufloat, umath
from CodeTools.PlottingManager  import myPickle

def load_Galaxy_Ratios(FileFolder, CodeName, AbundancesExtension, Atom_Dict):
        
    Ratios_dict         = OrderedDict()
    RatiosColor_dict    = OrderedDict()
     
    #List of interesting lines
    Metal_Lines         = ['O2_3726A', 'O2_3726A', 'S2_4069A', 'S2_4076A','O3_4363A', 'Ar4_4711A', 'Ar3_7136A', 'O3_4959A', 'O3_5007A', 'N2_6548A', 'N2_6584A', 'S3_9069A', 'S3_9531A'] 
    He_Lines            = ['He2_4686A'] + ['H1_3889A',  'He1_4026A',    'He1_4387A',    'He1_4471A',    'He1_4686A',    'He1_4714A',    'He1_4922A',   'He1_5876A',    'He1_6678A',   'He1_7065A',    'He1_7281A',      'He1_10830A']
     
    #Load the lines
    Lines_Dict = pv.getEmLine_FluxDict(Metal_Lines, CodeName, FileFolder, AbundancesExtension, 'Auto')
    
    #Calculate Flux ratios
    if ('O3_4959A' in Lines_Dict) and ('O3_5007A' in Lines_Dict):
        Ratios_dict['O3_ratio']         = Lines_Dict['O3_5007A'] / Lines_Dict['O3_4959A']
        RatiosColor_dict['O3_ratio']    = pv.colorChooser(Ratios_dict['O3_ratio'], Atom_Dict['O3_ratio'])
    else:
        Ratios_dict['O3_ratio']         = 'None'
        RatiosColor_dict['O3_ratio']    = 'Black'
         
    #Calculate Flux ratios
    if ('N2_6548A' in Lines_Dict) and ('N2_6584A' in Lines_Dict):
        Ratios_dict['N2_ratio']         = Lines_Dict['N2_6584A'] / Lines_Dict['N2_6548A']
        RatiosColor_dict['N2_ratio']    = pv.colorChooser(Ratios_dict['N2_ratio'], Atom_Dict['N2_ratio'])
    else:
        Ratios_dict['N2_ratio']         = 'None'
        RatiosColor_dict['N2_ratio']    = 'Black'
         
    #Calculate Flux ratios
    if ('S3_9069A' in Lines_Dict) and ('S3_9531A' in Lines_Dict):
        Ratios_dict['S3_ratio']         = Lines_Dict['S3_9531A'] / Lines_Dict['S3_9069A']
        RatiosColor_dict['S3_ratio']    = pv.colorChooser(Ratios_dict['S3_ratio'], Atom_Dict['S3_ratio'])
    else:
        Ratios_dict['S3_ratio']         = 'None'
        RatiosColor_dict['S3_ratio']    = 'Black'
         
    return Ratios_dict, RatiosColor_dict
      
def OrganizedObject_List():
         
    CleanList = ['03', '04v1', '04v2', '06', '08', '09', '10', '11', '14', '24', '27', '70', '71', 'SDSS1', 'SDSS2', 'SDSS3', '51959-092', '51991-224', '52235-602', '52319-521', '52703-612v2', 'J2225', 'SHOC036', 'SHOC575v1', 'SHOC575v2', 'SHOC579', 'SHOC588', 'SHOC593']
#     CleanList = ['SHOC579'] 
    return CleanList

def table_key_format(key, Ratios_dict):

    #Treatment for the line ratios
    if key in ['O3_ratio', 'N2_ratio', 'S3_ratio']:
        
        value                       = pv.format_for_table(Ratios_dict[key])
        
        if value != None:
            color                   = RatiosColor_dict[key]
            formated_abundance      = pv.format_for_table(value)
            formated_abundance      = r'\textcolor{' + color + '}{' + formated_abundance + '}'
        else:
            formated_abundance  = None
     
    #Treatment for the physical conditions
    elif key in ['TOIII', 'TOII', 'TSIII', 'TSII', 'nSII', 'cHBeta_stellar']:
        
        value                       = pv.GetParameter_ObjLog(CodeName, FileFolder, key, 'string', sigfig=5, strformat= '{:.2f}')
        
        if value != None:
            formated_abundance      = pv.format_for_table(value)
        else:
            formated_abundance      = None
    
    #Treatment for metallic abundances
    elif key in ['OI_HI', 'NI_HI', 'SI_HI', 'SI_HI_ArCorr']:
        
        value                       = pv.GetParameter_ObjLog(CodeName, FileFolder, key, 'float')
        
        if value != None:
            abund_log               = 12 + umath.log10(value)
            formated_abundance      = pv.format_for_table(abund_log)
        else:
            formated_abundance      = None
    
    #Treatment for Helium abundances
    elif key in ['HeI_HI', 'HeII_HII', 'HeIII_HII', 'Y_Mass_O', 'Y_Inference_O', 'Y_Mass_S', 'Y_Inference_S']:
       
        value                       = pv.GetParameter_ObjLog(CodeName, FileFolder, key, 'float')

        if value != None:
            formated_abundance      = pv.format_for_table(value, 3)
        else:
            formated_abundance      = None
                
    #Treatment for the inference parameters
    elif key in ['y_plus_inf','Te_inf','ne_inf','cHbeta_inf','ftau_inf','Xi_inf']:
        
        value                       = pv.GetParameter_ObjLog(CodeName, FileFolder, key, 'float')
        

        
        if value != None:
            error_type              = key[0:key.find('_inf')] + '_SD'
            error                   = pv.GetParameter_ObjLog(CodeName, FileFolder, error_type, 'float')
            value                   = ufloat(value,error)
            color                   = pv.colorEvaluator(key, value, CodeName, FileFolder)                   
            formated_abundance      = pv.format_for_table(value, 3)
            formated_abundance      = r'\textcolor{' + color + '}{' + formated_abundance + '}'
        else:
            formated_abundance      = None   

    else:
        formated_abundance = 'NotFound'

    return formated_abundance

pv = myPickle()
 
#Define data type and location
Catalogue_Dic               = DataToTreat()
Pattern                     = '_log.txt'
# AbundancesFileExtension     = '_WHT_EmissionReddend_LinesLog_v3.txt'
# database_extension          = '_extandar_30000_5000_10_v2'
# globalfile_extension        = '_global_30000_5000_10_v2'
 
#Locate files on hard drive
FilesList                   = OrganizedObject_List() 

#Define plot frame and colors
pv.FigFormat_One(ColorConf  = 'Night1')
 
#Get the dictionary with the headers format and the data
header_dict                 = pv.dazer_GalaxyPropertiesHeader()
 
#--------------------------Prepare PyNeb data for ratios characteristics--------------------------
Atom_Dict = dict()
pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
O3 = pn.Atom('O', 3) 
N2 = pn.Atom('N', 2)
S3 = pn.Atom('S', 3)
Atom_Dict['O3_ratio'] = O3.getEmissivity(10000, 100, wave = 5007) / O3.getEmissivity(10000, 100, wave = 4959) 
Atom_Dict['N2_ratio'] = N2.getEmissivity(10000, 100, wave = 6584) / N2.getEmissivity(10000, 100, wave = 6548)
Atom_Dict['S3_ratio'] = S3.getEmissivity(10000, 100, wave = 9531) / S3.getEmissivity(10000, 100, wave = 9069)

#--------------------------Start to generate the document--------------------------

#Generate object table
pv.dazer_tableFormat('Galaxies_summary', Catalogue_Dic['Data_Folder'], header_dict)

#Generate the table    
with pv.doc.create(Tabular(pv.table_format)) as table:
 
    #Declare the header
    pv.dazer_tableHeader(table, header_dict)

    #Loop through the files 
    for i in range(len(FilesList)):
     
        #Trick to analyse the folders in the order I want
        CurrentFile = Catalogue_Dic['Obj_Folder'] + FilesList[i] + '/' + FilesList[i] + '_WHT_EmissionFlux_LinesLog_v3.txt' 
     
        print 'Current file', CurrentFile
     
        #Analyze file address
        CodeName, FileName, FileFolder  = pv.Analyze_Address(CurrentFile)
                 
        #Declare logs address
        ObjLog_Address      = FileFolder + FileName
         
        #Load the data
        Ratios_dict, RatiosColor_dict = load_Galaxy_Ratios(FileFolder, CodeName, '_WHT_EmissionFlux_LinesLog_v3.txt', Atom_Dict)
         
        #Generate object row of data 
        data_keys   = header_dict.keys()
        Object_row  = ['None'] * len(header_dict)
         
        #Load the data row
        Object_row[0] = CodeName
        for j in range(1, len(Object_row)):
                         
            Object_row[j] = table_key_format(data_keys[j], Ratios_dict)
                                        
        #Insert the data row
        table.add_row(Object_row, escape=False)
    
    #Insert final double line
    table.add_hline()
    
#Save the file
pv.dazer_tableCloser()
     
print 'Table generated'