from numpy import where
from uncertainties import ufloat
from dazer_methods import Dazer

#Declare objects
dz = Dazer()
 
#Define data type and location
Catalogue_Dic   = dz.import_catalogue()
Table_Name      = '_lineslog' 
log_extension   = '_log.txt'
cHbeta_type     = 'cHBeta_red'
emission_log    = '_' + Catalogue_Dic['Datatype'] + '_LinesLog_v3.txt'
# emission_log_st = '_' + Catalogue_Dic['Datatype'] + '_emission_LinesLog_v3.txt'

#Get file list
FilesList = dz.Folder_Explorer(emission_log, Catalogue_Dic['Obj_Folder'], CheckComputer=False)

#Get the dictionary with the headers format and the data
dz.EmissionLinesLog_header()
 
#Generate list of objects (Dazer should have a method for this)
for i in range(len(FilesList)):                 
     
    CodeName, FileName, FileFolder  = dz.Analyze_Address(FilesList[i])
     
    #load object data
    cHbeta                  = dz.GetParameter_ObjLog(CodeName, FileFolder, cHbeta_type, Assumption='float')     
    obj_lines_frame         = dz.load_object_frame(FileFolder, CodeName, emission_log, chbeta_coef = cHbeta_type)    
#     obj_lines_frame_star    = dz.load_object_frame(FileFolder, CodeName, emission_log_st, chbeta_coef = cHbeta_type)    
    Hbeta_Flux              = obj_lines_frame['line_Flux']['H1_4861A']
    Hbeta_Int               = obj_lines_frame['line_Int']['H1_4861A']
              
    #Generate object row of data 
    data_keys   = dz.header_dict.keys()
    Object_row  = ['None'] * len(dz.header_dict)
     
    #Establish table format
    dz.latex_header(table_address = FileFolder + CodeName + Table_Name, TitleColumn = ['', '', 'HII Galaxy', CodeName, ''])
        
    #Loop through all the emission recordings
    objlines = obj_lines_frame.index.values
    for j in range(len(objlines)):
     
        if '_w' not in objlines[j]:
            #Loop through the columns and prepare the data to store
            for k in range(len(Object_row)):
             
                thekey = data_keys[k]
                
                if thekey == 'Emission':
                    format_index    = where(dz.LinesLogFormat_dict['0'] == objlines[j])[0][0]
                    wavelength      = dz.format_for_table(obj_lines_frame.iloc[j]['TheoWavelength'], rounddig = 4)
                    ion             = dz.LinesLogFormat_dict['3'][format_index]
                    Object_row[k]   = r'${wavelength}$ ${ion}$'.format(wavelength = wavelength, ion = ion)
                     
                elif thekey == 'f_lambda':
                    Object_row[k]   = dz.format_for_table(obj_lines_frame.iloc[j]['line_f'], rounddig = 4)
             
                elif thekey == 'Eqw':
                    Eqw             = obj_lines_frame.iloc[j]['line_Int'] / ufloat(obj_lines_frame.iloc[j]['Continuum_Median'], obj_lines_frame.iloc[j]['Continuum_sigma'])
    #                 print objlines[j],  obj_lines_frame.iloc[j]['line_Int'].nominal_value,  ufloat(obj_lines_frame.iloc[j]['Continuum_Median'], obj_lines_frame.iloc[j]['Continuum_sigma']).nominal_value, Eqw.nominal_value
                    Object_row[k]   = dz.format_for_table(Eqw, rounddig = 3)
             
                elif thekey == 'Flux_undim':
                    value           = obj_lines_frame.iloc[j]['line_Flux'] * 1000.0 / Hbeta_Flux
                    Object_row[k]   = dz.format_for_table(value, rounddig = 3)
             
                elif thekey == 'Int_undim':
                    value           = obj_lines_frame.iloc[j]['line_Int'] * 1000.0 / Hbeta_Int
                    Object_row[k]   = dz.format_for_table(value, rounddig = 3)
                 
        #Insert the row
        dz.table.add_row(Object_row, escape=False)
     
    #Adding a double line for different section
    dz.table.add_hline()
     
    #Hbeta pure flux row
    IHB_Row         = [r'$I_{H\beta}$', ' ', ' ',dz.format_for_table(Hbeta_Flux, rounddig = 3, scientific_notation=True), '']
    dz.table.add_row(IHB_Row, escape=False)
    
    #c(Hbeta) Row flux row
    CHbeta_Row      = [r'$c(H\beta)$', ' ', ' ', dz.format_for_table(cHbeta, rounddig = 3), '']
    dz.table.add_row(CHbeta_Row, escape=False)
     
    dz.table_footer()
         
#     except:
#         pv.log_error(CodeName) 
 
print 'All tables generated'