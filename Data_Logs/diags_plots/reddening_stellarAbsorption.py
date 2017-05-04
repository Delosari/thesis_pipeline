import uncertainties.unumpy as unumpy  
from dazer_methods import Dazer
from libraries.Math_Libraries.fitting_methods import LinfitLinearRegression

#Declare coding classes
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict      = dz.import_catalogue()
catalogue_df        = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
lineslog_extension  = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'
lineslog_extension2 = '_' + catalogue_dict['Datatype'] + '_linesLog_emission.txt'
dz.quick_indexing(catalogue_df)

#Reddening properties
R_v = 3.4
red_curve = 'G03'
 
#Define plot frame and colors
size_dict = {'axes.labelsize':20, 'legend.fontsize':18, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':18, 'ytick.labelsize':18}
dz.FigConf(plotSize = size_dict)
 
# Loop through files
for i in range(len(catalogue_df.index)):
      
    #Locate the files
    objName = catalogue_df.iloc[i].name
    
    if objName == 'SHOC579':
    
        fits_file           = catalogue_df.iloc[i].reduction_fits
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        lineslog_address    = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=lineslog_extension)
        lineslog_address2   = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=lineslog_extension2)
                 
        print '-- Treating {} @ {}'.format(objName, lineslog_address)
     
        #Load object data
        lineslog_frame              = dz.load_lineslog_frame(lineslog_address)
        lineslog_frame2             = dz.load_lineslog_frame(lineslog_address2)
         
        #Load reddening curve for the lines
        lines_wavelengths           = lineslog_frame.lambda_theo.values
        lines_Xx                    = dz.reddening_Xx(lines_wavelengths, red_curve, R_v)
        lines_f                     = dz.flambda_from_Xx(lines_Xx, red_curve, R_v)
        lineslog_frame['line_f']    = lines_f
     
        lines_wavelengths2          = lineslog_frame2.lambda_theo.values
        lines_Xx2                   = dz.reddening_Xx(lines_wavelengths2, red_curve, R_v)
        lines_f2                    = dz.flambda_from_Xx(lines_Xx2, red_curve, R_v)
        lineslog_frame2['line_f']   = lines_f2     
     
        #Determine recombination coefficients for several combinations
        object_data = catalogue_df.iloc[i]
        ratios_dict = dz.compare_RecombCoeffs(object_data, lineslog_frame)             
        ratios_dict2 = dz.compare_RecombCoeffs(object_data, lineslog_frame2)             
         
        cHbeta_all_MagEr, n_all_MagEr   = LinfitLinearRegression(ratios_dict['all_x'], ratios_dict['all_y'])
        trendline_all                   = cHbeta_all_MagEr * ratios_dict['all_x'] + n_all_MagEr
        cHbeta_in_MagEr, n_in_MagEr     = LinfitLinearRegression(ratios_dict['in_x'], ratios_dict['in_y'])
        trendline_in                    = cHbeta_in_MagEr * ratios_dict['in_x'] + n_in_MagEr
             
        cHbeta_all_MagEr2, n_all_MagEr2 = LinfitLinearRegression(ratios_dict2['all_x'], ratios_dict2['all_y'])
        trendline_all2                  = cHbeta_all_MagEr2 * ratios_dict2['all_x'] + n_all_MagEr2
        cHbeta_in_MagEr2, n_in_MagEr2   = LinfitLinearRegression(ratios_dict2['in_x'], ratios_dict2['in_y'])
        trendline_in2                   = cHbeta_in_MagEr2 * ratios_dict2['in_x'] + n_in_MagEr2            
                                  
        #--Blue points
        if len(ratios_dict['blue_x']) > 0:
            dz.data_plot(unumpy.nominal_values(ratios_dict['blue_x'][2:]), unumpy.nominal_values(ratios_dict['blue_y'][2:]), 'ISIS blue arm recombination ratios', markerstyle='o', color = '#0072B2',  y_error=unumpy.std_devs(ratios_dict['blue_y'][2:]))
            dz.plot_text(unumpy.nominal_values(ratios_dict['blue_x'][2:]), unumpy.nominal_values(ratios_dict['blue_y'][2:]),  ratios_dict['blue_ions'][2:], color = '#0072B2', fontsize=18)         
         
        #--Red points
        if len(ratios_dict['red_x']) > 0:
            dz.data_plot(unumpy.nominal_values(ratios_dict['red_x']), unumpy.nominal_values(ratios_dict['red_y']), 'ISIS red arm emissions', markerstyle='o', color = '#D55E00',  y_error=unumpy.std_devs(ratios_dict['red_y']))
            dz.plot_text(unumpy.nominal_values(ratios_dict['red_x']), unumpy.nominal_values(ratios_dict['red_y']),  ratios_dict['red_ions'], color = '#D55E00', fontsize=18)
          
        if len(ratios_dict['blue_x']) > 0:
            dz.data_plot(unumpy.nominal_values(ratios_dict2['blue_x'][2:]), unumpy.nominal_values(ratios_dict2['blue_y'][2:]), 'Recombination ratios (no stellar absorption)', markerstyle='X', color = '#009E73',  y_error=unumpy.std_devs(ratios_dict2['blue_y'][2:]))
        if len(ratios_dict['red_x']) > 0:
            dz.data_plot(unumpy.nominal_values(ratios_dict2['red_x'][0]), unumpy.nominal_values(ratios_dict2['red_y'][0]), 'Recombination ratios (no stellar absorption)', markerstyle='X', color = '#009E73',  y_error=unumpy.std_devs(ratios_dict2['red_y'][0]))
          
        #--Trendline
        dz.data_plot(unumpy.nominal_values(ratios_dict['in_x']), unumpy.nominal_values(trendline_in), r'First regression $c(H\beta) = {Value} \pm {Error}$'.format(Value = round(cHbeta_all_MagEr.nominal_value, 3), Error = round(cHbeta_all_MagEr.std_dev,3)), linestyle='--', color = '#0072B2')        
        dz.data_plot(unumpy.nominal_values(ratios_dict2['in_x']), unumpy.nominal_values(trendline_in2), r'Second regression $c(H\beta) = {Value} \pm {Error}$'.format(Value = round(cHbeta_all_MagEr2.nominal_value, 3), Error = round(cHbeta_all_MagEr2.std_dev,3)), linestyle='--', color = '#D55E00')        
                                  
        #Figure format
        dz.Axis.set_ylim(-0.5,0.4)
        dz.Axis.set_xlim(-0.65,0.4)

        Title       = r'Object {Codename} reddening coefficient calculation'.format(Codename = catalogue_df.loc[objName].quick_index)
        y_Title     = r'$log(I/I_{H\beta})_{th}-log(F/F_{H\beta})_{Obs}$'
        x_Title     = r'$f(\lambda)-f(\lambda_{H\beta})$'
        dz.FigWording(x_Title, y_Title, Title, loc=4)
                                     
        output_pickle = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/Images/reddening_evolution.png'
        dz.save_manager(output_pickle, save_pickle = False) 

print 'All data treated', dz.display_errors()