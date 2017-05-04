from dazer_methods import Dazer
from libraries.Math_Libraries.sigfig import round_sig

def colorChooser(ObsRatio, TheRatio):
     
    if (TheRatio * 0.95 < ObsRatio < TheRatio * 1.05):
        color = 'ForestGreen'#'green'#
     
    elif (TheRatio * 0.90 < ObsRatio < TheRatio * 1.10):
        color = 'YellowOrange'#'yellow'#
         
    else:
        color = 'BrickRed'
         
    return color

#Import library object

dz = Dazer()
dz.load_elements()

#Load observational data
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_emission_2nd.txt'
dz.quick_indexing(catalogue_df)

#Reddening properties
R_v         = 3.4
red_curve   = 'G03'
cHbeta_type = 'cHbeta_emis'

#Define data to load
ext_data        = '_emis2nd'
pdf_address     = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/objProperties_noPreamble'
  
#Headers
properties_list =   ['neSII', 'TeSIII', 'TeOIII'] 
properties_list =   map(( lambda x: x + ext_data), properties_list)
headers_format  =   ['HII Galaxy', r'$\frac{[OIII]\lambda5007\AA}{[OIII]\lambda4959\AA}$', r'$\frac{[SIII]\lambda9531\AA}{[SIII]\lambda9069\AA}$'] 
headers_format  +=  [r'$n_{e}[SII](cm^{-3})$',  r'$T_{e}[SIII](K)$',  r'$T_{e}[OIII](K)$']
headers_format  +=  [r'$T_{low}$', r'$T_{high}$']
 
#Set the pdf format
dz.pdf_insert_table(headers_format)
  
for objName in catalogue_df.loc[dz.idx_include].index:
        
    ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    lineslog_address = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=AbundancesFileExtension)
    
    #Load lines frame
    lineslog_frame = dz.load_lineslog_frame(lineslog_address)
   
    #Perform the reddening correction
    cHbeta = catalogue_df.loc[objName, cHbeta_type]
    dz.deredden_lines(lineslog_frame, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
    
    #Sulfur ratios
    if set(lineslog_frame.index) >= set(['S3_9069A','S3_9531A']): 
        s3_ratio = lineslog_frame.loc['S3_9531A'].line_Int / lineslog_frame.loc['S3_9069A'].line_Int
        s3_color = colorChooser(s3_ratio.nominal_value, dz.S3_ratio)
        s3_entry = r'\textcolor{' + s3_color + '}{' + dz.format_for_table(s3_ratio, rounddig=3)  + '}'
    else:
        s3_entry = '-'
    
    #Oxygen ratios
    if set(lineslog_frame.index) >= set(['O3_4959A','O3_5007A']): 
        O3_ratio = lineslog_frame.loc['O3_5007A'].line_Int / lineslog_frame.loc['O3_4959A'].line_Int
        O3_color = colorChooser(O3_ratio.nominal_value, dz.O3_5000_ratio)
        O3_entry = r'\textcolor{' + O3_color + '}{' + dz.format_for_table(O3_ratio, rounddig=3)  + '}'
    else:
        O3_entry = '-'        
    
    #Fill the table
    entry_name   = '{slash}href{{{url}}}{{{text}}}'.format(slash='\\',url=catalogue_df.loc[objName].SDSS_Web,text=catalogue_df.loc[objName].quick_index).replace('&','\&')
    T_low_entry  = r'$T_{e}[SIII]$' if catalogue_df.loc[objName].T_low == 'TeSIII' else r'$T_{e}[SIII] eq.16$'
    T_high_entry = r'$T_{e}[OIII]$' if catalogue_df.loc[objName].T_high == 'TeOIII' else r'$T_{e}[OIII] eq.16$'
    row          = [entry_name] + [O3_entry] + [s3_entry] + list(catalogue_df.loc[objName, properties_list].values) + [T_low_entry, T_high_entry]
    dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True, rounddig=3)
 
dz.generate_pdf(output_address=pdf_address)
 
print 'Table generated'

