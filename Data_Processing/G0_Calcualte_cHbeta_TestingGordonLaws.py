import uncertainties.unumpy as unumpy  
from dazer_methods import Dazer
from lib.Math_Libraries.fitting_methods import LinfitLinearRegression

#Declare coding classes
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict      = dz.import_catalogue()
catalogue_df        = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
lineslog_extension  = '_' + catalogue_dict['Datatype'] + '_linesLog_emission.txt'

#Reddening properties
R_v = 3.4
redding_laws = ['G03_average', 'G03_bar', 'G03_supershell']

#Set figure format
dz.FigConf()

# Loop through files

for j in range(len(redding_laws)):
    
    redding_law = redding_laws[j]

    for i in range(len(catalogue_df.index)):
          
        #Locate the files
        objName             = catalogue_df.iloc[i].name
        fits_file           = catalogue_df.iloc[i].reduction_fits
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        lineslog_address    = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=lineslog_extension)
                 
        print '-- Treating {} @ {}'.format(objName, lineslog_address)
     
        #Load object data
        lineslog_frame          = dz.load_lineslog_frame(lineslog_address)
         
        #Load reddening curve for the lines
        lines_wavelengths           = lineslog_frame.lambda_theo.values
        lines_Xx                    = dz.reddening_Xx(lines_wavelengths, redding_law, R_v)
        lines_f                     = dz.flambda_from_Xx(lines_Xx, redding_law, R_v)
        lineslog_frame['line_f']    = lines_f
     
        #Determine recombination coefficients for several combinations
        object_data = catalogue_df.iloc[i]
        ratios_dict = dz.compare_RecombCoeffs(object_data, lineslog_frame)             
               
        cHbeta_all_MagEr, n_all_MagEr   = LinfitLinearRegression(ratios_dict['all_x'], ratios_dict['all_y'])
        trendline_all                   = cHbeta_all_MagEr * ratios_dict['all_x'] + n_all_MagEr
        cHbeta_in_MagEr, n_in_MagEr     = LinfitLinearRegression(ratios_dict['in_x'], ratios_dict['in_y'])
        trendline_in                    = cHbeta_in_MagEr * ratios_dict['in_x'] + n_in_MagEr
                              
#         #--Blue points
#         if len(ratios_dict['blue_x']) > 0:
#             dz.data_plot(unumpy.nominal_values(ratios_dict['blue_x']), unumpy.nominal_values(ratios_dict['blue_y']), 'blue arm emissions', markerstyle='o', color = '#0072B2',  y_error=unumpy.std_devs(ratios_dict['blue_y']))
#             dz.plot_text(unumpy.nominal_values(ratios_dict['blue_x']), unumpy.nominal_values(ratios_dict['blue_y']),  ratios_dict['blue_ions'], color = '#0072B2')
#          
#         #--Red points
#         if len(ratios_dict['red_x']) > 0:
#             dz.data_plot(unumpy.nominal_values(ratios_dict['red_x']), unumpy.nominal_values(ratios_dict['red_y']), 'red arm emissions', markerstyle='o', color = '#D55E00',  y_error=unumpy.std_devs(ratios_dict['red_y']))
#             dz.plot_text(unumpy.nominal_values(ratios_dict['red_x']), unumpy.nominal_values(ratios_dict['red_y']),  ratios_dict['red_ions'], color = '#D55E00')
#           
#         #--Outside points
#         if ratios_dict['out_x'] is not None:
#             dz.data_plot(unumpy.nominal_values(ratios_dict['out_x']), unumpy.nominal_values(ratios_dict['out_y']), 'Invalid  emissions', markerstyle='o', color = '#009E73',  y_error=unumpy.std_devs(ratios_dict['out_y']))
#             dz.plot_text(unumpy.nominal_values(ratios_dict['out_x']), unumpy.nominal_values(ratios_dict['out_y']),  ratios_dict['out_ions'], color = '#009E73')
#           
#         #--Trendline
#         dz.data_plot(unumpy.nominal_values(ratios_dict['in_x']), unumpy.nominal_values(trendline_in), 'Valid points regression', linestyle='--', color = 'black')        
#          
#         #Store reddening coefficient
        catalogue_df.loc[objName, 'cHbeta_{}'.format(redding_law)] = cHbeta_in_MagEr
          
dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx', df_sheet_format = 'catalogue_data')
 
print 'All data treated', dz.display_errors()

