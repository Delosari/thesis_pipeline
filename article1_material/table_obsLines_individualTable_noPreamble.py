from dazer_methods          import Dazer
from collections            import OrderedDict
from numpy                  import concatenate, unique, round, nan
from pandas                 import read_csv, isnull, notnull
from lib.CodeTools.sigfig   import round_sig

lines_log_format_headers    = ['Ions', 'lambda_theo', 'notation']
lines_log_format_address    = '/home/vital/workspace/dazer/format/emlines_pyneb_optical_infrared.dz'
pdf_address                 = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/tables/lines_fluxes_noPreamble'
lines_df                    = read_csv(lines_log_format_address, index_col = 0, names=lines_log_format_headers, delim_whitespace = True)
  
#Generate dazer object
dz = Dazer()
   
#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
norm_factor     = 1000
  
#Treatment add quick index
dz.quick_indexing(catalogue_df)
          
#Declare data for the analisis
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'
   
#Reddening properties
R_v             = 3.4
red_curve       = 'G03_average'
cHbeta_type     = 'cHbeta_emis'
    
#Define table properties
obj_per_page    = 2
Headers         = [r'$\lambda(\AA)$'] + [ r'$EW(\AA)$', r'$F(\lambda)$', r'$I(\lambda)$']* obj_per_page
column_code     = ['line_Eqw', 'line_Flux', 'line_Int']
linformat_df    = read_csv(lines_log_format_address, names=['line_label', 'ion', 'lambda_theo', 'latex_format'], delim_whitespace=True)
linformat_df.lambda_theo = round(linformat_df.lambda_theo.values, 2)
   
#Start the table
dz.create_pdfDoc(pdf_address, pdf_type='table')

dz.pdf_insert_table(table_format='l' + 'c' * (3 * obj_per_page))

for obj_group in [['8', 'SHOC579']]:
                 
    group_dict = OrderedDict()
        
    #Make dict with all the objects lines dataframes
    for obj in obj_group:
        ouput_folder            = '{}{}/'.format(catalogue_dict['Obj_Folder'], obj)
        linelog_reducAddress    = '{objfolder}{codeName}_WHT_linesLog_reduc.txt'.format(objfolder = ouput_folder, codeName=obj)
        linelog_emisAddress     = '{objfolder}{codeName}_WHT_linesLog_emission_2nd.txt'.format(objfolder = ouput_folder, codeName=obj)
        reduc_linedf            = dz.load_lineslog_frame(linelog_reducAddress)
        emission_linedf         = dz.load_lineslog_frame(linelog_emisAddress)
      
        cHbeta = catalogue_df.loc[obj, cHbeta_type]
        dz.deredden_lines(reduc_linedf, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
        dz.deredden_lines(emission_linedf, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
            
        group_dict[str(obj) + '_df']        = reduc_linedf
        group_dict[str(obj) + '_dfemis']    = emission_linedf
            
        group_dict[str(obj) + '_Hbeta_F']   = emission_linedf.loc['H1_4861A'].line_Flux
        group_dict[str(obj) + '_Hbeta_I']   = emission_linedf.loc['H1_4861A'].line_Int
                
        #Create array with all the lines observed from all objects 
        if obj == obj_group[0]:
            lambdas_array = emission_linedf['lambda_theo'].values
        else:
            lambdas_i = emission_linedf['lambda_theo'].values
            lambdas_array = concatenate((lambdas_array, lambdas_i))
        
    #Short array and remove repeated entries    
    lambdas_array = unique(lambdas_array)
      
    #Insert the row with the names
    row_objs = ['']
    for idx in range(obj_per_page):
        objName     = catalogue_df.loc[obj_group[idx], 'quick_index']
        row_objs    += ['', objName, '']
    dz.addTableRow(row_objs, last_row = False)
      
    #Add the parameters row
    dz.addTableRow(Headers, last_row = True)
      
    #Loop through the observed lines an ad them to the table
    for wave in lambdas_array:
      
        if wave in linformat_df['lambda_theo'].values:
            idx_label   = (linformat_df['lambda_theo'] == wave)
            ion         = linformat_df.loc[idx_label, 'latex_format'].values[0]
            label       = linformat_df.loc[idx_label, 'line_label'].values[0]
            line_label  = r'{} ${}$'.format(int(round(wave,0)), ion)
            row         = [line_label]
                                            
            for obj in obj_group:
                row_i   = ['-'] * 3 #By default empty cells
                if label in group_dict[str(obj) + '_dfemis'].index:            
                    row_i           = list(group_dict[str(obj) + '_dfemis'].loc[label, column_code].values)
                    
                    #Special treatment for the equivalent length: Using flux 
                    continua_reduc  = group_dict[str(obj) + '_df'].loc[label, 'con_dered']
                    Eqw_special     = row_i[2] / continua_reduc
                    
                    if Eqw_special >= 5.0:
                        rounddig = 3
                        rounddig_er = 3 
                    else:
                        rounddig = 1
                        rounddig_er = 1
                    
                    row_i[0]        = dz.format_for_table(Eqw_special, rounddig = rounddig, rounddig_er=rounddig_er)
                    
                    row_i[1]        = row_i[1] / group_dict[str(obj) + '_Hbeta_F'] * norm_factor
                    row_i[2]        = row_i[2] / group_dict[str(obj) + '_Hbeta_I'] * norm_factor
                         
                row = row + row_i     

            dz.addTableRow(row, last_row = False)
           
        else:
            print 'ESTA FALLA', wave
            
    dz.table.add_hline()
      
    #Add bottom rows with the Hbeta flux and reddening
    row_F, row_cHbeta = [r'$I(H\beta)$'], [r'$c(H\beta)$']
    row_clean = ['$(erg\,cm^{-2} s^{-1} \AA^{-1})$'] + [''] * len(obj_group) * 3
    for obj in obj_group:
        #row_F       += ['', dz.format_for_table(group_dict[str(obj) + '_Hbeta_F'], rounddig = 2, scientific_notation=True), dz.format_for_table(group_dict[str(obj) + '_Hbeta_I'], rounddig = 2, scientific_notation=True)]
        row_F       += ['', dz.format_for_table(group_dict[str(obj) + '_Hbeta_F'], rounddig = 2, scientific_notation=True), dz.format_for_table(group_dict[str(obj) + '_Hbeta_I'], rounddig = 2, scientific_notation=True)]
        cHbeta_reduc, cHbeta_emis = catalogue_df.loc[obj, 'cHbeta_reduc'], catalogue_df.loc[obj, 'cHbeta_emis'] 
        
        cHbeta_reduc_entry  = '{}$\pm${}'.format(round_sig(cHbeta_reduc.nominal_value, 2, scien_notation=False), round_sig(cHbeta_reduc.std_dev, 1, scien_notation=False))
        cHbeta_emis_entry   = '{}$\pm${}'.format(round_sig(cHbeta_emis.nominal_value, 2, scien_notation=False), round_sig(cHbeta_emis.std_dev, 1, scien_notation=False))
        #row_cHbeta  += ['', cHbeta_reduc_entry, cHbeta_emis_entry]
        row_cHbeta  += ['', cHbeta_emis_entry, '']
        print cHbeta_emis_entry
        
        
    dz.addTableRow(row_F, last_row = False)
    dz.addTableRow(row_clean, last_row = False)
    dz.addTableRow(row_cHbeta, last_row = True) 
    dz.table.add_hline()
   
dz.generate_pdf()


# from numpy import nanmean, nanstd, mean, concatenate, unique, sum, round, nan
# from uncertainties  import ufloat
# from dazer_methods  import Dazer
# from collections    import OrderedDict
# import pandas       as pd
# from pylatex        import Document, Figure, NewPage, NoEscape, Package, Tabular, Section, Tabu, Table
#   
# lines_log_format_headers    = ['Ions', 'lambda_theo', 'notation']
# lines_log_format_address    = '/home/vital/workspace/dazer/format/emlines_pyneb_optical_infrared.dz'
# pdf_address                 = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/lines_fluxes_noPreamble'
# lines_df                    = pd.read_csv(lines_log_format_address, index_col = 0, names=lines_log_format_headers, delim_whitespace = True)
#   
# #Generate dazer object
# dz = Dazer()
#    
# #Load catalogue dataframe
# catalogue_dict  = dz.import_catalogue()
# catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
# norm_factor     = 1000
#   
# #Treatment add quick index
# catalogue_df['quick_idx'] = nan
# counter_idx = 1
# for obj in catalogue_df.index:
#     if pd.isnull(catalogue_df.loc[obj,'Ignore_article']):
#         if pd.notnull(catalogue_df.loc[obj,'Favoured_ref']):
#             catalogue_df.loc[obj,'quick_idx'] = catalogue_df.loc[obj,'Favoured_ref']
#         else:
#             catalogue_df.loc[obj,'quick_idx'] = str(counter_idx)
#             counter_idx += 1
#           
# #Declare data for the analisis
# AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'
#    
# #Reddening properties
# R_v             = 3.4
# red_curve       = 'G03'
# cHbeta_type     = 'cHbeta_reduc'
#     
# #Define table properties
# obj_per_page    = 2
# Headers         = [r'$\lambda(\AA)$'] + [ r'$EW(\AA)$', r'$F(\lambda)$', r'$I(\lambda)$']* obj_per_page
# column_code     = ['line_Eqw', 'line_Flux', 'line_Int']
# linformat_df    = pd.read_csv(lines_log_format_address, names=['line_label', 'ion', 'lambda_theo', 'latex_format'], delim_whitespace=True)
# linformat_df.lambda_theo = round(linformat_df.lambda_theo.values, 2)
#    
# #Start the table
# # dz.create_pdfDoc(pdf_address, pdf_type='table')
# 
# # dz.pdf_insert_longtable(table_format='l' + 'c' * (3 * obj_per_page))
# dz.pdf_insert_table(table_format='l' + 'c' * (3 * obj_per_page))
# # for obj_group in zip(*[iter(catalogue_df.index)]*obj_per_page):
# for obj_group in [['8', 'SHOC579']]:
#                  
#     group_dict = OrderedDict()
#         
#     #Load object fluxes
#     for obj in obj_group:
#         ouput_folder            = '{}{}/'.format(catalogue_dict['Obj_Folder'], obj)
#         linelog_reducAddress    = '{objfolder}{codeName}_WHT_linesLog_reduc.txt'.format(objfolder = ouput_folder, codeName=obj)
#         linelog_emisAddress     = '{objfolder}{codeName}_WHT_linesLog_emission.txt'.format(objfolder = ouput_folder, codeName=obj)
#         reduc_linedf            = dz.load_lineslog_frame(linelog_reducAddress)
#         emission_linedf         = dz.load_lineslog_frame(linelog_emisAddress)
#       
#         cHbeta = catalogue_df.loc[obj, cHbeta_type]
#         dz.deredden_lines(reduc_linedf, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
#         dz.deredden_lines(emission_linedf, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
#             
#         group_dict[str(obj) + '_df']        = reduc_linedf
#         group_dict[str(obj) + '_dfemis']    = emission_linedf
#             
#         group_dict[str(obj) + '_Hbeta_F']   = reduc_linedf.loc['H1_4861A'].line_Flux
#         group_dict[str(obj) + '_Hbeta_I']   = reduc_linedf.loc['H1_4861A'].line_Int
#             
#         #Object lengths 
#         if obj == obj_group[0]:
#             lambdas_array = reduc_linedf['lambda_theo'].values
#         else:
#             lambdas_i = reduc_linedf['lambda_theo'].values
#             lambdas_array = concatenate((lambdas_array, lambdas_i))
#         
#     #Short array and remove repeated entries    
#     lambdas_array = unique(lambdas_array)
#       
#     #Insert the row with the names
#     row_objs = ['']
#     for idx in range(obj_per_page):
#         objName     = catalogue_df.loc[obj_group[idx],'quick_idx']
#         row_objs    += ['', objName, '']
#         #dz.table.add_hline(start=2+(idx)*3, end=4+(idx)*3)
#     dz.addTableRow(row_objs, last_row = False)
#       
#     #Add the parameters row
#     dz.addTableRow(Headers, last_row = True)
#       
#     #Loop through the lines
#     for wave in lambdas_array:
#       
#         if wave in linformat_df['lambda_theo'].values:
#             idx_label   = (linformat_df['lambda_theo'] == wave)
#             ion         = linformat_df.loc[idx_label, 'latex_format'].values[0]
#             label       = linformat_df.loc[idx_label, 'line_label'].values[0]
#             line_label  = r'{} ${}$'.format(wave, ion)
#             row         = [line_label]
#                                             
#             for obj in obj_group:
#                 row_i   = ['-'] * 3
#                 if label in group_dict[str(obj) + '_df'].index:            
#                     row_i       = list(group_dict[str(obj) + '_df'].loc[label, column_code].values)
#                     row_i[1]    = row_i[1] / group_dict[str(obj) + '_Hbeta_F'] * norm_factor
#                     row_i[2]    = row_i[2] / group_dict[str(obj) + '_Hbeta_I'] * norm_factor
#                          
#                 row = row + row_i     
#             print len(row), row
#             dz.addTableRow(row, last_row = False)
#            
#         else:
#             print 'ESTA FALLA', wave
#     dz.table.add_hline()
#       
#     #Add rows for with the Hbeta flux and reddening
#     #row_F, row_cHbeta = [r'$F(H\beta)$ $(erg\,cm^{-2} s^{-1} \AA^{-1})$'], [r'$c(H\beta)$']
#     row_F, row_cHbeta = [r'$F(H\beta)$'], [r'$c(H\beta)$']
#     row_clean = ['$(erg\,cm^{-2} s^{-1} \AA^{-1})$'] + [''] * len(obj_group) * 3
#     for obj in obj_group:
#         row_F       += ['', dz.format_for_table(group_dict[str(obj) + '_Hbeta_F'], rounddig = 2, scientific_notation=True), dz.format_for_table(group_dict[str(obj) + '_Hbeta_I'], rounddig = 2, scientific_notation=True)]
#         row_cHbeta  += ['', catalogue_df.loc[obj, 'cHbeta_reduc'], catalogue_df.loc[obj, 'cHbeta_emis']]
#            
#     dz.addTableRow(row_F, last_row = False)
#     dz.addTableRow(row_clean, last_row = False)
#     dz.addTableRow(row_cHbeta, last_row = True) 
#     dz.table.add_hline()
#    
# dz.generate_pdf(output_address=pdf_address)


