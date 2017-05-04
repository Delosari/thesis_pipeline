import  pandas as pd
from    dazer_methods import Dazer
from    numpy import isnan, nan, sort, unique, zeros
 
dz = Dazer()
 
table_address   = '/home/vital/Desktop/NGC5457_CHAOSIII_regions.xlsx'
old_df          = dz.load_excel_DF(table_address)
regions_list    = pd.unique(old_df.index)
wavelength      = sort(pd.unique(old_df.wavelength)[0:-1])
physical_param  = ['C(Hbeta)', 'F(Hbeta)', 'EW(Hbeta)', 'EW(Halpha)']

#Generate the good columns
line_labels = zeros(len(wavelength)).astype(str)
for i in range(len(wavelength)):
    wave            = wavelength[i]
    ions            = unique(old_df.line_label[(old_df.wavelength == wave)].values)
    line_labels[i]  = str(wave) + '_'+ ions[0]

#Create dataframe
new_df = pd.DataFrame(columns = list(line_labels) + physical_param, index=regions_list)

#Add error column
for column in new_df.columns.values:      
    new_df.insert(new_df.columns.get_loc(column) + 1, column + '_error', nan)

#Transfer data from old df to the new
for i in range(len(old_df)):    
    region      = old_df.iloc[i].name
    wave        = old_df.iloc[i].wavelength
    check_err   = old_df.iloc[i].flux_label
    flux        = old_df.iloc[i].flux
    error       = old_df.iloc[i].flux_error
    param_label = old_df.iloc[i].line_label
    
    #Load data into the new data frame
    if pd.isnull(check_err):
        line_label  = str(wave) + '_'+ param_label
        new_df.loc[region, line_label] = flux
        new_df.loc[region, line_label + '_error'] = error
  
    elif param_label in physical_param:
        new_df.loc[region, param_label] = flux
        new_df.loc[region, param_label + '_error'] = error
  
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(table_address.replace('_regions.xlsx', '_regions_adapted.xlsx'), engine='xlsxwriter')
    
# Convert the dataframe to an XlsxWriter Excel object.
new_df.to_excel(writer, sheet_name='Sheet1')
      
# Close the Pandas Excel writer and output the Excel file.
writer.save()



# import  pandas as pd
# from    dazer_methods import Dazer
# from    numpy import isnan, nan, sort
#  
# dz = Dazer()
#  
# table_address   = '/home/vital/Desktop/NGC5194_CHAOSI_regions.xlsx'
# old_df          = dz.load_excel_DF(table_address)
# regions_list    = pd.unique(old_df.index)
# wavelength      = sort(pd.unique(old_df.wavelength)[0:-1])
# physical_param  = ['C(Hbeta)', 'F(Hbeta)', 'EW(Hbeta)', 'EW(Halpha)']
# new_df          = pd.DataFrame(columns = list(wavelength) + physical_param, index=regions_list)
# 

# 
# for column in new_df.columns.values:
#     column_name = str(column)
#     new_df.insert(new_df.columns.get_loc(column) + 1, str(column_name) + '_error', nan)
# 
# for i in range(len(old_df)):    
#     region      = old_df.iloc[i].name
#     wave        = old_df.iloc[i].wavelength
#     check_err   = old_df.iloc[i].flux_label
#     flux        = old_df.iloc[i].flux
#     error       = old_df.iloc[i].flux_error
#     line_label  = old_df.iloc[i].line_label
#      
#     #Load data into the new data frame
#     if pd.isnull(check_err):
#         new_df.loc[region, wave] = flux
#         new_df.loc[region, str(wave) + '_error'] = error
#  
#     elif line_label in physical_param:
#         new_df.loc[region, line_label] = flux
#         new_df.loc[region, line_label + '_error'] = error
#  
#   
# # Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter('/home/vital/Desktop/NGC5194_CHAOSI_regions_adapted.xlsx', engine='xlsxwriter')
#      
# # Convert the dataframe to an XlsxWriter Excel object.
# new_df.to_excel(writer, sheet_name='Sheet1')
#      
# # Close the Pandas Excel writer and output the Excel file.
# writer.save()




# #Create new dataframe with the columns error
# new_df = pd.DataFrame(columns = headers_name)
# for column in headers_name[1:]:
#     new_df.insert(new_df.columns.get_loc(column) + 1, column + '_err', nan)
#  
# #Loop through the tables rows
# for i in range(len(old_df.index)):
#     if not isinstance(old_df.iloc[i].name, float):
#          
#         obj_index = old_df.iloc[i].name
#         new_df.loc[obj_index, 'Main Name'] = old_df.loc[obj_index, 'Main Name']
#          
#         print '--', obj_index
#         #Loop through the table columns
#         for parameter in headers_name[1:]:
#          
#             cell_value     = old_df.iloc[i][parameter]
#              
#             print parameter
#             if not (pd.isnull(cell_value)) and not (cell_value == '-'): 
#                                  
#                 #Add TNII comment column
#                 if isinstance(cell_value, (str, unicode)):
#                     new_df.loc[obj_index, 'TNII comment'] = 'TOIII was chosen for all ions'
#                     nominal_value = float(cell_value.replace('*',''))        
#                     upper_limit   = float(old_df.iloc[i+1][parameter].replace('*',''))
#                     lower_limit   = float(old_df.iloc[i+2][parameter].replace('*',''))
#                     print '-- ', nominal_value, nominal_value, lower_limit
#                 else:
#                     nominal_value   = cell_value
#                     upper_limit     = old_df.iloc[i+1][parameter]
#                     lower_limit     = old_df.iloc[i+2][parameter]
#  
#                 new_df.loc[obj_index, parameter] = nominal_value
#                 new_df.loc[obj_index, parameter + '_err'] = '+{}-{}'.format(upper_limit - nominal_value, nominal_value - lower_limit)        
#  
#  
# print new_df



# import  pandas              as pd
# import  numpy               as np
# import  matplotlib.pyplot   as plt
# from    dazer_methods       import Dazer
# from    matplotlib.ticker   import NullFormatter
# from    matplotlib          import rcParams
# 
# def figure_formatting():
#  
#     sizing_dict = {}
#     sizing_dict['figure.figsize'] = (12, 9)
#     sizing_dict['legend.fontsize']  = 15
#     sizing_dict['axes.labelsize']   = 20
#     sizing_dict['axes.titlesize']   = 24
#     sizing_dict['xtick.labelsize']  = 14
#     sizing_dict['ytick.labelsize']  = 14
#     rcParams.update(sizing_dict)
#     #plt.style.use('seaborn-colorblind')
# 
#     #Figure configuration
#     left, width     = 0.1, 0.65
#     bottom, height  = 0.1, 0.65
#     bottom_h        = left_h = left + width + 0.02
#     
#     rect_scatter    = [left, bottom, width, height]
#     rect_histx      = [left, bottom_h, width, 0.2]
#     rect_histy      = [left_h, bottom, 0.2, height]
#     
#     Fig             = plt.figure(1)
#     axScatter       = plt.axes(rect_scatter)
#     axHistx         = plt.axes(rect_histx)
#     axHisty         = plt.axes(rect_histy)
#     axHistx.xaxis.set_major_formatter(NullFormatter())  #No x ticks labels
#     axHisty.yaxis.set_major_formatter(NullFormatter())  #No x ticks labels 
#     
#     return Fig, axScatter, axHistx, axHisty
# 
# def histogram_bining(binsize, data):
#     
#     min_data, max_data = np.min(data), np.max(data)
#     num_bins = np.floor((max_data - min_data) / binsize)
#     
#     return num_bins, min_data, max_data
# 
# #Import plotting class
# 
# def hist_scattering_plot(x_data, y_data, label_data):
#     
#     #Bining for histograms
#     num_x_bins, min_x_data, max_x_data = histogram_bining(500, x_data) 
#     num_y_bins, min_y_data, max_y_data = histogram_bining(1000, y_data)
#     
#     #Make plots
#     axScatter.scatter(x_data, y_data, label=label_data)
#     axHistx.hist(x_data, bins=num_x_bins)
#     axHisty.hist(y_data, bins=num_y_bins, orientation='horizontal')
#     
#     return
# 
# def axis_formatting(x_lim_min, x_lim_max, y_lim_min, y_lim_max, x_label, y_label):
#     
#     axScatter.set_xlim(x_lim_min, x_lim_max)
#     axScatter.set_ylim(y_lim_min, y_lim_max)
#     axHistx.set_xlim(x_lim_min, x_lim_max)
#     axHisty.set_ylim(y_lim_min, y_lim_max)
#     
#     axScatter.set_xlabel(x_label)
#     axScatter.set_ylabel(y_label)
#     axHistx.set_title('Planetary nebula selection with error quantification on electron parameters')
#     
#     axScatter.legend(loc='best')
#     
#     return
# 
# dz = Dazer()
# 
# Fig, axScatter, axHistx, axHisty = figure_formatting()
# 
# #Load PN database
# table_address   = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Master_table.xlsx'
# pn_df           = pd.read_excel(table_address, index_col=0, header=0)
# 
# #Index data for plot
# idcs_temp_den   = (pn_df.neSII.notnull()) & (pn_df.neSII.notnull()) & (pn_df.TOIII.notnull()) & (pn_df.TOIII.notnull())
# neSII           = pn_df.loc[idcs_temp_den].neSII
# TOIII           = pn_df.loc[idcs_temp_den].TOIII
# hist_scattering_plot(neSII, TOIII, r'$T_{e}[OIII]$ - $n_{e}[SII]$')
# 
# idcs_temp_den   = (pn_df.neSII.notnull()) & (pn_df.neSII.notnull()) & (pn_df.TSIII.notnull()) & (pn_df.TSIII.notnull())
# neSII           = pn_df.loc[idcs_temp_den].neSII
# TSIII           = pn_df.loc[idcs_temp_den].TSIII
# hist_scattering_plot(neSII, TSIII, r'$T_{e}[SIII]$ - $n_{e}[SII]$')
# 
# xlabel, ylabel = r'Density $(cm^{-3}$)', r'Temperature (K)'
# axis_formatting(x_lim_min=0, x_lim_max=30000, y_lim_min=2000, y_lim_max=50000, x_label=xlabel, y_label=ylabel)
# 
# plt.show()

# import  pandas as pd
# from    dazer_methods import Dazer
# from    numpy import isnan, nan
# 
# dz = Dazer()
# 
# table_address   = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Database/4_Gorny/table_tempDen.xlsx'
# old_df          = dz.load_excel_DF(table_address)
# headers_name    = old_df.columns
# 
# #Create new dataframe with the columns error
# new_df = pd.DataFrame(columns = headers_name)
# for column in headers_name[1:]:
#     new_df.insert(new_df.columns.get_loc(column) + 1, column + '_err', nan)
# 
# #Loop through the tables rows
# for i in range(len(old_df.index)):
#     if not isinstance(old_df.iloc[i].name, float):
#         
#         obj_index = old_df.iloc[i].name
#         new_df.loc[obj_index, 'Main Name'] = old_df.loc[obj_index, 'Main Name']
#         
#         print '--', obj_index
#         #Loop through the table columns
#         for parameter in headers_name[1:]:
#         
#             cell_value     = old_df.iloc[i][parameter]
#             
#             print parameter
#             if not (pd.isnull(cell_value)) and not (cell_value == '-'): 
#                                 
#                 #Add TNII comment column
#                 if isinstance(cell_value, (str, unicode)):
#                     new_df.loc[obj_index, 'TNII comment'] = 'TOIII was chosen for all ions'
#                     nominal_value = float(cell_value.replace('*',''))        
#                     upper_limit   = float(old_df.iloc[i+1][parameter].replace('*',''))
#                     lower_limit   = float(old_df.iloc[i+2][parameter].replace('*',''))
#                     print '-- ', nominal_value, nominal_value, lower_limit
#                 else:
#                     nominal_value   = cell_value
#                     upper_limit     = old_df.iloc[i+1][parameter]
#                     lower_limit     = old_df.iloc[i+2][parameter]
# 
#                 new_df.loc[obj_index, parameter] = nominal_value
#                 new_df.loc[obj_index, parameter + '_err'] = '+{}-{}'.format(upper_limit - nominal_value, nominal_value - lower_limit)        
# 
# 
# print new_df
# 
# # Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter('/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Database/4_Gorny/table_tempDen_adjusted.xlsx', engine='xlsxwriter')
# 
# # Convert the dataframe to an XlsxWriter Excel object.
# new_df.to_excel(writer, sheet_name='Sheet1')
# 
# # Close the Pandas Excel writer and output the Excel file.
# writer.save()

# import  pandas as pd
# from    dazer_methods import Dazer
# from    numpy import isnan, nan
#   
# dz = Dazer()
#   
# table_address   = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Database/2_Henry/table_den_Temp.xlsx'
# #table_address   = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Database/3_Milingo/table_temden.xlsx'
# old_df          = dz.load_excel_DF(table_address)
# headers_name    = old_df.columns
# objects_list    = pd.unique(old_df.index.values)
# headers_name    = pd.unique(old_df.Param.values)
#   
# #Create new dataframe with the columns error
# new_df = pd.DataFrame(columns = headers_name)
# for column in headers_name:
#     new_df.insert(new_df.columns.get_loc(column) + 1, column + '_err', nan)
# new_df['Comments'] = nan
# 
# #Loop through the tables rows
# for i in range(len(old_df.index)):
#          
#     #Check if magnitude was measured
#     if not pd.isnull(old_df.iloc[i].mag): 
#      
#         objID       = old_df.iloc[i].name
#         parmID      = old_df.iloc[i].Param
#         magParam    = old_df.iloc[i].mag
#         errParam    = old_df.iloc[i].error
#         comentParam = old_df.iloc[i].den
#         
#         #Add the parameter
#         new_df.loc[objID, parmID] = magParam
#         new_df.loc[objID, parmID + '_err'] = errParam
#          
#         #Include the comment if observed:
#         if not pd.isnull(comentParam):
#             
#             new_comment = '({} {})'.format(parmID, comentParam)
#             
#             #Check if a comment was already there
#             if pd.isnull(new_df.loc[objID].Comments):
#                 new_df.loc[objID, 'Comments']   = new_comment
#             else:
#                 previous_comment                = new_df.loc[objID, 'Comments'] + ' ' + new_comment
#                 new_df.loc[objID, 'Comments']   = previous_comment
#                 
# # Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter(table_address.replace('.xlsx', '_adjusted.xlsx'), engine='xlsxwriter')
#   
# # Convert the dataframe to an XlsxWriter Excel object.
# new_df.to_excel(writer, sheet_name='Sheet1')
#   
# # Close the Pandas Excel writer and output the Excel file.
# writer.save()



    