from CodeTools.PlottingManager              import myPickle
from ManageFlow                             import DataToTreat
from pylatex                                import NoEscape, Document, Section, Subsection, Tabular, MultiColumn, Table, MultiRow, Package, Figure
from uncertainties                          import ufloat
from collections                            import OrderedDict
from Math_Libraries.sigfig                  import round_sig
from Astro_Libraries.Reddening_Corrections  import ReddeningLaws    

#Generate dazer object
pv                                          = myPickle()
Reddening                                   = ReddeningLaws()

#Files extension
Log_extension_red                           = '_WHT_LinesLog_v3.txt'  
Log_extension_dered                         = '_WHT_dered2nd_LinesLog_v3.txt'
Log_extension_Neb                           = '_WHT_dered2nd_Neb2nd_LinesLog_v3.txt'
Log_extension_Stellar                       = '_WHT_dered_Neb_stellar_LinesLog_v3.txt'

#Locate files on hard drive
Catalogue_Dic                               = DataToTreat()
Pattern                                     = Catalogue_Dic['Datatype'] + '.fits'
FilesList                                   = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)

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
    
    #Get Hbeta values    
    Hbeta_Flux_dered    = pv.getFlux_LinesLog(FileFolder + CodeName + Log_extension_red, 'H1_4861A')
    Hbeta_Flux_Neb      = pv.getFlux_LinesLog(FileFolder + CodeName + Log_extension_Neb, 'H1_4861A')
    Hbeta_Flux_Stellar  = pv.getFlux_LinesLog(FileFolder + CodeName + Log_extension_Stellar, 'H1_4861A')
    
    #Load c(Hbeta)
    cHbeta              = pv.GetParameter_ObjLog(CodeName, FileFolder, 'cHBeta_stellar', Assumption='float')

    #Generate the f_lambda column
    Emlines_wavelength  = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'TheoWavelength')
    f_lambdaColumn      = Reddening.Reddening_f(Emlines_wavelength, 3.2, 'Cardelli1989')
    
    #Load fluxes and their corresponding errors
    Ions                = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'Ion')
    Flux_red            = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'FluxGauss')
    Error_red           = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'ErrorEL_MCMC')
    Eqw_red             = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'Eqw')
    EqwError_red        = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'ErrorEqw')
    Flux_neb            = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_Neb, 'FluxGauss')
    Error_neb           = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_Neb, 'ErrorEL_MCMC')
    Flux_stellar        = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_Stellar, 'FluxGauss')
    Error_stellar       = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_Stellar, 'ErrorEL_MCMC')
    
    #--------------------Prepare latex file--------------------------------
 
    #Generate object row of data 
    data_keys   = pv.header_dict.keys()
    Object_row  = ['None'] * len(pv.header_dict)
     
    #Establish table format
    pv.latex_header(table_address = FileFolder + CodeName + '_lineslog')
        
    #Loop through all the emission recordings
    for j in range(len(Ions)):
    
        #Loop through the columns and prepare the data to store
        for k in range(len(Object_row)):
        
            thekey = data_keys[k]
        
            if thekey == 'Emission':
                Object_row[k] = pv.format_for_table(Emlines_wavelength[j], rounddig = 4) + ' ' + Ions[j].replace('_', '-')
                
            elif thekey == 'flambda':
                Object_row[k] = pv.format_for_table(f_lambdaColumn[j], rounddig = 3)
        
            elif thekey == 'Eqw':
                Object_row[k] = pv.format_for_table(ufloat(Eqw_red[j], EqwError_red[j]), rounddig = 3)
        
            elif thekey == 'flux':
                value = ufloat(Flux_red[j], Error_red[j]) * 1000.0 / Hbeta_Flux_dered
                Object_row[k] = pv.format_for_table(value, rounddig = 3)
        
            elif thekey == 'Ineb':
                value = ufloat(Flux_neb[j], Error_neb[j]) * 1000.0 / Hbeta_Flux_Neb
                Object_row[k] = pv.format_for_table(value, rounddig = 3)
                
            elif thekey == 'Istellar':
                value = ufloat(Flux_stellar[j], Error_stellar[j]) * 1000.0 / Hbeta_Flux_Stellar
                Object_row[k] = pv.format_for_table(value, rounddig = 3)

        #Insert the row
        pv.table.add_row(Object_row, escape=False)
    
    #Adding a double line for different section
    pv.table.add_hline()
    
    #Hbeta pure flux row
    IHB_Row         = [r'$I_{H\beta}$', ' ', ' ', pv.format_for_table(Hbeta_Flux_dered, rounddig = 3, scientific_notation=True), pv.format_for_table(Hbeta_Flux_Neb, rounddig = 3, scientific_notation=True), pv.format_for_table(Hbeta_Flux_Stellar, rounddig = 3,scientific_notation=True)]
    pv.table.add_row(IHB_Row, escape=False)
   
    #c(Hbeta) Row flux row
    CHbeta_Row      = [r'$c(H\beta)$', ' ', ' ', pv.format_for_table(cHbeta, rounddig = 3), '', '',]
    pv.table.add_row(CHbeta_Row, escape=False)
    
    pv.table_footer()
    
print 'Adios'


# from CodeTools.PlottingManager              import myPickle
# from ManageFlow                             import DataToTreat
# from pylatex                                import NoEscape, Document, Section, Subsection, Tabular, MultiColumn, Table, MultiRow, Package, Figure
# from uncertainties                          import ufloat
# from collections                            import OrderedDict
# from Math_Libraries.sigfig                  import round_sig
# from Astro_Libraries.Reddening_Corrections  import ReddeningLaws    
# 
# #Generate dazer object
# pv                                          = myPickle()
# Reddening                                   = ReddeningLaws()
# 
# #Files extension
# Log_extension_red                           = '_WHT_LinesLog_v3.txt'  
# Log_extension_dered                         = '_WHT_dered2nd_LinesLog_v3.txt'
# Log_extension_Neb                           = '_WHT_dered2nd_Neb2nd_LinesLog_v3.txt'
# Log_extension_Stellar                       = '_WHT_dered_Neb_stellar_LinesLog_v3.txt'
# 
# #Headers_dictionary
# header_dict = OrderedDict()
# header_dict['Emission']                     = 'Emission line'
# header_dict['flambda']                      = r'$f(\lambda)$'
# header_dict['Eqw']                          = r'$-EW(\AA)$'
# header_dict['flux']                         = r'$F(\lambda)$'
# header_dict['Ineb']                         = r'$I_{Neb}(\lambda)$'
# header_dict['Istellar']                     = r'$I_{Stellar}(\lambda)$'
# 
# #Locate files on hard drive
# Catalogue_Dic                               = DataToTreat()
# Pattern                                     = Catalogue_Dic['Datatype'] + '.fits'
# FilesList                                   = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
#     
# #Dictionary properties
# Data_Dict                                   = OrderedDict()
# Lines_Dict                                  = OrderedDict()
# Address_dict                                = OrderedDict()
# 
# #Generate list of objects (Dazer should have a method for this)
# for i in range(len(FilesList)):                 
#     
#     #--------------------Prepare scientific data--------------------------------
#     CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
#     
#     #Get Hbeta values    
#     Hbeta_Flux_dered    = pv.getFlux_LinesLog(FileFolder + CodeName + Log_extension_red, 'H1_4861A')
#     Hbeta_Flux_Neb      = pv.getFlux_LinesLog(FileFolder + CodeName + Log_extension_Neb, 'H1_4861A')
#     Hbeta_Flux_Stellar  = pv.getFlux_LinesLog(FileFolder + CodeName + Log_extension_Stellar, 'H1_4861A')
#     
#     #Load c(Hbeta)
#     cHbeta              = pv.GetParameter_ObjLog(CodeName, FileFolder, 'cHBeta_stellar', Assumption='float')
# 
#     #Generate the f_lambda column
#     Emlines_wavelength  = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'TheoWavelength')
#     f_lambdaColumn      = Reddening.Reddening_f(Emlines_wavelength, 3.2, 'Cardelli1989')
#     
#     #Load fluxes and their corresponding errors
#     Ions                = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'Ion')
#     Flux_red            = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'FluxGauss')
#     Error_red           = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'ErrorEL_MCMC')
#     Eqw_red             = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'Eqw')
#     EqwError_red        = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_red, 'ErrorEqw')
#     Flux_neb            = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_Neb, 'FluxGauss')
#     Error_neb           = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_Neb, 'ErrorEL_MCMC')
#     Flux_stellar        = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_Stellar, 'FluxGauss')
#     Error_stellar       = pv.getColumn_LinesLog(FileFolder + CodeName + Log_extension_Stellar, 'ErrorEL_MCMC')
#     
#     #--------------------Prepare latex file--------------------------------
#     #Generate object table
#     Table_Name  = CodeName + '_lineslog' 
#     doc         = Document(FileFolder + Table_Name, documentclass='mn2e')
#     
#     #State packages to append
#     doc.packages.append(Package('preview', options=['active', 'tightpage',])) #Package to crop pdf to a figure
# 
#     #Table pre-commands
#     doc.append(NoEscape(r'\begin{table*}'))
#     doc.append(NoEscape(r'\begin{preview}')) 
#     doc.append(NoEscape(r'{\footnotesize'))
#     doc.append(NoEscape(r'\centering'))
# 
#     #Generate object row of data 
#     data_keys   = header_dict.keys()
#     Object_row  = ['None'] * len(header_dict)
#     
#     #Establish table format
#     table_format = 'l' + ''.join([' c' for s in range(len(header_dict) - 1)])
#     
#     #Loop through the data to append rows     
#     with doc.create(Tabular(table_format)) as table:
#         
#         #Declare the header
#         table.add_hline()
#         table.add_row(header_dict.values(), escape=False)
#         table.add_hline()
#         
#         #Loop through all the emission recordings
#         for j in range(len(Ions)):
#         
#             #Loop through the columns and prepare the data to store
#             for k in range(len(Object_row)):
#             
#                 thekey = data_keys[k]
#             
#                 if thekey == 'Emission':
#                     Object_row[k] = pv.format_for_table(Emlines_wavelength[j], rounddig = 4) + ' ' + Ions[j].replace('_', '-')
#                     
#                 elif thekey == 'flambda':
#                     Object_row[k] = pv.format_for_table(f_lambdaColumn[j], rounddig = 3)
#             
#                 elif thekey == 'Eqw':
#                     Object_row[k] = pv.format_for_table(ufloat(Eqw_red[j], EqwError_red[j]), rounddig = 3)
#             
#                 elif thekey == 'flux':
#                     value = ufloat(Flux_red[j], Error_red[j]) * 1000.0 / Hbeta_Flux_dered
#                     Object_row[k] = pv.format_for_table(value, rounddig = 3)
#             
#                 elif thekey == 'Ineb':
#                     value = ufloat(Flux_neb[j], Error_neb[j]) * 1000.0 / Hbeta_Flux_Neb
#                     Object_row[k] = pv.format_for_table(value, rounddig = 3)
#                     
#                 elif thekey == 'Istellar':
#                     value = ufloat(Flux_stellar[j], Error_stellar[j]) * 1000.0 / Hbeta_Flux_Stellar
#                     Object_row[k] = pv.format_for_table(value, rounddig = 3)
# 
#             #Insert the row
#             table.add_row(Object_row, escape=False)
#         
#         #Adding a double line for different section
#         table.add_hline()
#         
#         #Hbeta pure flux row
#         IHB_Row         = [r'$I_{H\beta}$', ' ', ' ', pv.format_for_table(Hbeta_Flux_dered, rounddig = 3, scientific_notation=True), pv.format_for_table(Hbeta_Flux_Neb, rounddig = 3, scientific_notation=True), pv.format_for_table(Hbeta_Flux_Stellar, rounddig = 3,scientific_notation=True)]
#         table.add_row(IHB_Row, escape=False)
#        
#         #c(Hbeta) Row flux row
#         CHbeta_Row      = [r'$c(H\beta)$', ' ', ' ', pv.format_for_table(cHbeta, rounddig = 3), '', '',]
#         table.add_row(CHbeta_Row, escape=False)
#         
#         #Close the table
#         table.add_hline()
# 
#     #Declare table footer
#     doc.append(NoEscape('}'))
#     doc.append(NoEscape(r'\end{preview}'))               
#     doc.append(NoEscape(r'\end{table*}'))
#              
#     doc.generate_pdf(clean=True)
# 
# print 'Adios'