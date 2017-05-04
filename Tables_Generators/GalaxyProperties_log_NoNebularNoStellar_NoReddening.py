import pyneb                                as pn
import numpy                                as np
from numpy                                  import power, where, ndarray, asscalar
from pylatex                                import NoEscape, Document, Section, Subsection, Tabular, MultiColumn, Table, MultiRow, Package, Figure
from ManageFlow                             import DataToTreat
from collections                            import OrderedDict, Sequence
from uncertainties.unumpy                   import uarray, nominal_values, std_devs, log10 as unum_log10
from uncertainties                          import UFloat, ufloat
from Math_Libraries.sigfig                  import round_sig
from CodeTools.PlottingManager              import myPickle
from uncertainties.umath                    import log10 as umath_log10

def colorChooser(ObsRatio, TheRatio):
     
    if (TheRatio * 0.90 < ObsRatio < TheRatio * 1.10):
        color = 'ForestGreen'
     
    elif (TheRatio * 0.75 < ObsRatio < TheRatio * 1.25):
        color = 'YellowOrange'
         
    else:
        color = 'Red'
         
    return color
 
def headers_dict_format():
 
    #This dictionary stores the format of the headers in latex
    #It also serves as a list from the defined entry keys
    header_dict             = OrderedDict()
     
    #Object header
    header_dict['object']       = 'Object ID'
     
    #Emision lines ratios
    header_dict['O3_ratio']     = r'$\frac{\left[OIII\right]5007\AA}{\left[OIII\right]4959\AA}$'
    header_dict['N2_ratio']     = r'$\frac{\left[NII\right]6584\AA}{\left[NII\right]6548\AA}$'
    header_dict['S3_ratio']     = r'$\frac{\left[SIII\right]9531\AA}{\left[SIII\right]9069\AA}$'
 
    #Physical Parameters
    header_dict['TOIII']        = r'$T_{\left[OIII\right]}$'
#     header_dict['TOII']         = r'$T_{\left[OII\right]}$'
    header_dict['TSIII']        = r'$T_{\left[SIII\right]}$'
    header_dict['TSII']         = r'$T_{\left[SII\right]}$'
    header_dict['nSII']         = r'$n_{e,\,\left[SII\right]}$'
 
    #Abundances
    header_dict['OI_HI']        = r'$12+log\left(\frac{O}{H}\right)$'
    header_dict['NI_HI']        = r'$12+log\left(\frac{N}{H}\right)$'
    header_dict['SI_HI']        = r'$12+log\left(\frac{S}{H}\right)$'
    header_dict['SI_HI_ArCorr'] = r'$12+log\left(\frac{S}{H}\right)_{Ar}$'
     
    header_dict['HeI_HI']       = r'$\frac{He}{H}$'
    header_dict['HeII_HII']     = r'$y^{+}$'
    header_dict['HeIII_HII']    = r'$y^{++}$'
     
    header_dict['Y_Inference_O']= r'$Y_{\left(\frac{O}{H}\right)}$'
    header_dict['Y_Mass_O']     = r'$Y_{\left(\frac{O}{H}\right),\,inf}$'
     
    return header_dict
 
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
        RatiosColor_dict['O3_ratio']    = colorChooser(Ratios_dict['O3_ratio'], Atom_Dict['O3_ratio'])
    else:
        Ratios_dict['O3_ratio']         = 'None'
        RatiosColor_dict['O3_ratio']    = 'Black'
         
    #Calculate Flux ratios
    if ('N2_6548A' in Lines_Dict) and ('N2_6584A' in Lines_Dict):
        Ratios_dict['N2_ratio']         = Lines_Dict['N2_6584A'] / Lines_Dict['N2_6548A']
        RatiosColor_dict['N2_ratio']    = colorChooser(Ratios_dict['N2_ratio'], Atom_Dict['N2_ratio'])
    else:
        Ratios_dict['N2_ratio']         = 'None'
        RatiosColor_dict['N2_ratio']    = 'Black'
         
    #Calculate Flux ratios
    if ('S3_9069A' in Lines_Dict) and ('S3_9531A' in Lines_Dict):
        Ratios_dict['S3_ratio']         = Lines_Dict['S3_9531A'] / Lines_Dict['S3_9069A']
        RatiosColor_dict['S3_ratio']    = colorChooser(Ratios_dict['S3_ratio'], Atom_Dict['S3_ratio'])
    else:
        Ratios_dict['S3_ratio']         = 'None'
        RatiosColor_dict['S3_ratio']    = 'Black'
         
    return Ratios_dict, RatiosColor_dict
      
#Import classes
 
def format_for_table(entry, rounddig = 4, scientific_notation = False):
        
    #Check None entry
    if entry != None:
            
        #Check string entry
        if type(entry) == str: 
            formatted_entry = entry
           
        #Case of Numerical entry
        else:
            
            #Case of an array    
            scalarVariable = True
            if isinstance(entry, (Sequence, np.ndarray)):
                
                #Confirm is not a single value array
                if len(entry) == 1:
                    entry           = entry[0]
                #Case of an array
                else:
                    scalarVariable  = False
                    formatted_entry = '_'.join(entry) # we just put all together in a "_' joined string    
            
            #Case single scalar        
            if scalarVariable:
                              
                #Case with error quantified
                if isinstance(entry, UFloat):
                    #formatted_entry = round_sig(nominal_values(entry), rounddig, scien_notation = scientific_notation) + r'$\pm$' +  round_sig(std_devs(entry), rounddig - 2, scien_notation = scientific_notation)
                    formatted_entry = 'coso'
                #Case single float
                else:
                    formatted_entry = round_sig(entry, rounddig, scien_notation = scientific_notation)
                            
    else:
        #None entry is converted to None
        formatted_entry = 'None'
        
    return formatted_entry

def OrganizedObject_List():
         
    CleanList = ['03', '04v1', '04v2', '06', '08', '09', '10', '11', '14', '24', '27', '70', '71', 'SDSS1', 'SDSS2', 'SDSS3', '51959-092', '51991-224', '52235-602', '52319-521', '52703-612v2', 'J2225', 'SHOC036', 'SHOC575v1', 'SHOC575v2', 'SHOC579', 'SHOC588', 'SHOC593']
 
    return CleanList
   
pv = myPickle()
 
#Define data type and location
Catalogue_Dic           = DataToTreat()
Pattern                 = '_log.txt'
AbundancesFileExtension = '_' + Catalogue_Dic['Datatype'] + '_dered_Neb_Stellar_LinesLog_v3.txt'
 
#Locate files on hard drive
# FilesList               = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
FilesList               = OrganizedObject_List() 

#Define plot frame and colors
pv.FigFormat_One(ColorConf = 'Night1')
 
#Get the dictionary with the headers format and the data
header_dict = headers_dict_format()
 
#Prepare PyNeb data for ratios characteristics
pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
 
Atom_Dict = dict()
O3 = pn.Atom('O', 3) 
N2 = pn.Atom('N', 2)
S3 = pn.Atom('S', 3)
 
Atom_Dict['O3_ratio'] = O3.getEmissivity(10000, 100, wave = 5007) / O3.getEmissivity(10000, 100, wave = 4959) 
Atom_Dict['N2_ratio'] = N2.getEmissivity(10000, 100, wave = 6584) / N2.getEmissivity(10000, 100, wave = 6548)
Atom_Dict['S3_ratio'] = S3.getEmissivity(10000, 100, wave = 9531) / S3.getEmissivity(10000, 100, wave = 9069)
  
#Generate object table
Table_Name  = 'Catalogue_Propertieslog_NoComponents' 
doc         = Document(Catalogue_Dic['Data_Folder'] + Table_Name, documentclass='mn2e')
 
doc.packages.append(Package('preview', options=['active', 'tightpage',])) #Package to crop pdf to a figure
doc.packages.append(Package('color', options=['usenames', 'dvipsnames',])) #Package to crop pdf to a figure
doc.packages.append(Package('geometry', options=['pass', 'paperwidth=30in', 'paperheight=11in', ])) #Package to crop pdf to a figure
 
#Table pre-commands
doc.append(NoEscape(r'\begin{table*}[h]'))
doc.append(NoEscape(r'\begin{preview}')) 
doc.append(NoEscape(r'{\footnotesize'))
doc.append(NoEscape(r'\centering'))
 
#Establish table format
table_format = 'l' + ''.join([' c' for s in range(len(header_dict) - 1)])
  
List_Objects = []
 
#Generate the table    
with doc.create(Tabular(table_format)) as table:
 
    #Declare the header
    table.add_hline()
    table.add_row(header_dict.values(), escape=False)
    table.add_hline()
 
    #Loop through the files 
    for i in range(len(FilesList)):
     
        #Trick to analyse the folders in the order I want
        CurrentFile = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue/Objects/' + FilesList[i] + '/' + FilesList[i] + '_WHT_LinesLog_v3.txt' 
     
        #Analyze file address
        CodeName, FileName, FileFolder  = pv.Analyze_Address(CurrentFile)
        
        List_Objects.append(CodeName)
         
        #Declare logs address
        ObjLog_Address      = FileFolder + FileName
        LineLog_Address     = FileFolder + CodeName + '_WHT_LinesLog_v3.txt'
         
        #Load the data
        Ratios_dict, RatiosColor_dict = load_Galaxy_Ratios(FileFolder, CodeName, AbundancesFileExtension, Atom_Dict)
         
        #Generate object row of data 
        data_keys   = header_dict.keys()
        Object_row  = ['None'] * len(header_dict)
         
        #Load the data row
        Object_row[0] = CodeName
        for j in range(1, len(Object_row)):
             
            thekey = data_keys[j]
                                     
            #Treatment for the line ratios
            if thekey in ['O3_ratio', 'N2_ratio', 'S3_ratio']:
                value = format_for_table(Ratios_dict[thekey])
                color = RatiosColor_dict[thekey]
                Object_row[j] = r'\textcolor{' + color + '}{' + value + '}'
             
            #Treatment for the physical conditions
            elif thekey in ['TOIII', 'TOII', 'TSIII', 'TSII', 'nSII']:
                value           = pv.GetParameter_ObjLog(CodeName, FileFolder, thekey, 'string', sigfig=5, strformat= '{:.2f}')
                Object_row[j]   = value
 
            #Treatment for metallic abundances
            elif thekey in ['OI_HI', 'NI_HI', 'SI_HI', 'SI_HI_ArCorr', 'nSII']:
                value               = pv.GetParameter_ObjLog(CodeName, FileFolder, thekey, 'float')
                if value != None:
                    abund_log           = 12 + umath_log10(value)
                    formated_abundance = format_for_table(abund_log)
                else:
                    formated_abundance = None
                Object_row[j] = formated_abundance
 
            #Treatment for Helium abundances
            elif thekey in ['HeI_HI', 'HeII_HII', 'HeIII_HII', 'Y_Inference_O', 'Y_Mass_O']:
                value = pv.GetParameter_ObjLog(CodeName, FileFolder, thekey, 'float')
                if value != None:
                    formated_abundance = format_for_table(value, 3)
                else:
                    formated_abundance = None
                Object_row[j] = formated_abundance
            else:
                Object_row[j] = '0.0000'
                 
        #Insert the row
        table.add_row(Object_row, escape=False)
     
    table.add_hline()
     
#Close the preview
doc.append(NoEscape('}'))
doc.append(NoEscape(r'\end{preview}'))               
doc.append(NoEscape(r'\end{table*}'))  
     
#Generate the document
# doc.generate_tex()
doc.generate_pdf(clean=False)
 
print 'File generated'