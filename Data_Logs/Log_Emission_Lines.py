from CodeTools.PlottingManager              import myPickle
from ManageFlow                             import DataToTreat
from uncertainties                          import ufloat
from collections                            import OrderedDict
from Math_Libraries.sigfig                  import round_sig
from Astro_Libraries.Reddening_Corrections  import ReddeningLaws    
from numpy                                  import where
from Math_Libraries.sigfig                  import round_sig
 
#Generate dazer object
pv                                          = myPickle()
Reddening                                   = ReddeningLaws()
 
#Locate files on hard drive
Catalogue_Dic                               = DataToTreat()
Pattern                                     = Catalogue_Dic['Datatype'] + '.fits'
FilesList                                   = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
 
#Files extension
Log_extension                               = '_' + Catalogue_Dic['Datatype'] + '_EmissionFlux_LinesLog_v3.txt'   
# Log_extension_dered                         = '_WHT_dered2nd_LinesLog_v3.txt'
# Log_extension_Neb                           = '_WHT_dered2nd_Neb2nd_LinesLog_v3.txt'
# Log_extension_Stellar                       = '_WHT_dered_Neb_stellar_LinesLog_v3.txt'
 
#Get the dictionary with the headers format and the data
pv.EmissionLinesLog_header()
 
#Dictionary properties
Data_Dict                                   = OrderedDict()
Lines_Dict                                  = OrderedDict()
Address_dict                                = OrderedDict()
 
#Generate list of objects (Dazer should have a method for this)
for i in range(len(FilesList)):                 
     
    #--------------------Prepare scientific data--------------------------------
    CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
     
    cHbeta_mag              = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter = 'cHBeta_stellar', Assumption = 'cHbeta_min')
     
    print 'Chbeta', cHbeta_mag
    print round_sig(cHbeta_mag.std_dev, 3)
     
    #Load lines data
    lineslog_dict           = pv.load_object_lines(FileFolder, CodeName, Log_extension = Log_extension)
    lineslog_dered_dict     = pv.load_object_lines(FileFolder, CodeName, Log_extension = Log_extension, chbeta_coef=cHbeta_mag)
    #lineslog_neb_dict       = pv.load_object_lines(FileFolder, CodeName, Log_extension = Log_extension_Neb)
    #lineslog_stellar_dict   = pv.load_object_lines(FileFolder, CodeName, Log_extension = Log_extension_Stellar)
     
         
#     for i in range(len(lineslog_dered_dict['Line_Label'])):
#         print lineslog_dered_dict['Line_Label'][i], lineslog_dered_dict['Eqw'][i], lineslog_dered_dict['f_lambda'][i]     
     
    #Get Hbeta values
    Hbeta_Flux              = pv.get_line_value(lineslog_dict, 'H1_4861A', variable_out = 'Flux')
    Hbeta_Flux_dered        = pv.get_line_value(lineslog_dered_dict, 'H1_4861A', variable_out = 'Flux')
    #Hbeta_Flux_Neb          = pv.get_line_value(lineslog_neb_dict, 'H1_4861A', variable_out = 'Flux')
    #Hbeta_Flux_Stellar      = pv.get_line_value(lineslog_stellar_dict, 'H1_4861A', variable_out = 'Flux')
         
    #--------------------Prepare latex file--------------------------------
    #Generate object row of data 
    data_keys   = pv.header_dict.keys()
    Object_row  = ['None'] * len(pv.header_dict)
     
    #Establish table format
    pv.latex_header(table_address = FileFolder + CodeName + '_lines_table', TitleColumn = ['', '', 'HII Galaxy', CodeName, ''])
         
    #Loop through all the emission recordings
    for j in range(len(lineslog_dict['Line_Label'])):
     
        #Loop through the columns and prepare the data to store
        for k in range(len(Object_row)):
         
            thekey = data_keys[k]
         
            if thekey == 'Emission':
                format_index    = where(pv.LinesLogFormat_dict['0'] == lineslog_dict['Line_Label'][j])[0][0]
                wavelength      = pv.format_for_table(lineslog_dict['TheoWavelength'][j], rounddig = 4)
                ion             = pv.LinesLogFormat_dict['3'][format_index]
                Object_row[k]   = r'${wavelength}$ ${ion}$'.format(wavelength = wavelength, ion = ion)
                 
            elif thekey == 'f_lambda':
                Object_row[k] = pv.format_for_table(lineslog_dered_dict['f_lambda'][j], rounddig = 4)
         
            elif thekey == 'Eqw':
                Object_row[k] = pv.format_for_table(lineslog_dict['Eqw'][j], rounddig = 3)
         
            elif thekey == 'Flux_undim':
                value = lineslog_dict['Flux'][j] * 1000.0 / Hbeta_Flux
                Object_row[k] = pv.format_for_table(value, rounddig = 3)
         
            elif thekey == 'Int_undim':
                value = lineslog_dered_dict['Flux'][j] * 1000.0 / Hbeta_Flux_dered
                Object_row[k] = pv.format_for_table(value, rounddig = 3)
                 
            #elif thekey == 'Istellar':
                #value = ufloat(Flux_stellar[j], Error_stellar[j]) * 1000.0 / Hbeta_Flux_Stellar
                #Object_row[k] = pv.format_for_table(value, rounddig = 3)
 
        #Insert the row
        pv.table.add_row(Object_row, escape=False)
     
    #Adding a double line for different section
    pv.table.add_hline()
     
    #Hbeta pure flux row
    IHB_Row         = [r'$I_{H\beta}$', ' ', ' ',pv.format_for_table(Hbeta_Flux, rounddig = 3, scientific_notation=True), '']
    pv.table.add_row(IHB_Row, escape=False)
    
    #c(Hbeta) Row flux row
    CHbeta_Row      = [r'$c(H\beta)$', ' ', ' ', pv.format_for_table(cHbeta_mag, rounddig = 3), '']
    pv.table.add_row(CHbeta_Row, escape=False)
     
    pv.table_footer()
         
#     except:
#         pv.log_error(CodeName) 
 
print 'All tables generated'