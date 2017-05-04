from numpy import nanmean, nanstd, mean
from uncertainties import ufloat
from dazer_methods import Dazer
import pandas as pd

lines_log_format_address = '/home/vital/git/Dazer/Dazer/dazer/bin/emlines_pyneb_optical_infrared.dz'
lines_log_format_headers = ['Ions', 'lambda_theo', 'notation']
lines_df = pd.read_csv(lines_log_format_address, index_col = 0, names=lines_log_format_headers, delim_whitespace = True)

print r'${{}}$'.format(lines_df.loc['H1_4861A'].notation)

#Generate dazer object
dz = Dazer()
 
#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
norm_factor     = 1000
  
#Declare data for the analisis
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'
 
#Reddening properties
R_v = 3.4
red_curve = 'G03'
cHbeta_type = 'cHbeta_reduc'
 
#Define table properties
Headers     = [r'$\lambda(\AA)$', r'$f$', r'$F(\lambda)$', r'$EW(\AA)$', r'$I(\lambda)$']
column_code = ['lambda_theo', 'line_Xx', 'line_Flux', 'line_Eqw', 'line_Int'] 
 
#Loop through objects:
for i in range(len(catalogue_df.index)):
          
    #Locate the objects
    objName      = catalogue_df.iloc[i].name
    ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
     
    if objName == '71':
                  
        #Load observational lines
        lineslog_reducAddress   = '{objfolder}{codeName}_WHT_linesLog_reduc.txt'.format(objfolder = ouput_folder, codeName=objName)
        lineslog_emisAddress    = '{objfolder}{codeName}_WHT_linesLog_emission.txt'.format(objfolder = ouput_folder, codeName=objName)
        reduc_linedf            = dz.load_lineslog_frame(lineslog_reducAddress)
        emission_linedf         = dz.load_lineslog_frame(lineslog_emisAddress)
     
        #Perform the reddening correction
        cHbeta = catalogue_df.iloc[i][cHbeta_type]
        dz.deredden_lines(reduc_linedf, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
        dz.deredden_lines(emission_linedf, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
         
        #Get Hbeta flux for normalization
        Hbeta_flux  = reduc_linedf.loc['H1_4861A'].line_Flux
        Hbeta_Int   = reduc_linedf.loc['H1_4861A'].line_Int
         
        #Generate pdf
        table_address = '{objfolder}{codeName}_WHT_linesLog_reduc'.format(objfolder = ouput_folder, codeName=objName)
        dz.create_pdfDoc(table_address, pdf_type='table')    
         
        #Set the pdf format
        dz.pdf_insert_table(Headers)
           
        for line in reduc_linedf.index.values:
            
            ion     = r'${}$'.format(lines_df.loc[line].notation) if '_w' not in line else  r'$H\alpha$'            
            row     = list(reduc_linedf.loc[line, column_code].values)
            row[2]  = row[2] / Hbeta_flux * norm_factor
            row[4]  = row[4] / Hbeta_Int * norm_factor
            row     = [r'{} {}'.format(row[0], ion)] + row[1:]
            dz.addTableRow(row, last_row = False if reduc_linedf.index[-1] != line else True)

        row = [r'$F(H\beta)$ $(erg\,cm^{-2} s^{-1} \AA^{-1})$', '', dz.format_for_table(Hbeta_flux, rounddig = 3, scientific_notation=True), '', dz.format_for_table(Hbeta_Int, rounddig = 3, scientific_notation=True)]
        dz.addTableRow(row, last_row = False)
        row = [r'$c(H\beta)$', '', cHbeta, '', '']
        dz.addTableRow(row, last_row = True)

        dz.generate_pdf()

