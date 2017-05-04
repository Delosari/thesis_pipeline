from dazer_methods import Dazer
from numpy import mean as np_mean, std, sum as np_sum
from uncertainties import ufloat

#Declare dazer object
dz = Dazer()

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations_BackUp/WHT_Galaxies_properties.xlsx')
lineslog_extension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'           #First data log for reduced spectra

#Define plot frame and colors
dz.FigConf()

#Redshift we have now
dz.create_pdfDoc('{objFolder}redshift_measurement'.format(objFolder=catalogue_dict['Data_Folder']))
table_headers = ['HII galaxy', r'z Blue SDSS', r'z Blue Peak', r'z Blue $\mu$', r'Calculation difference $(\%)$',
                  r'z Red SDSS', r'z Red Peak', r'z Red $\mu$', 'Calculation difference $(\%)$']

dz.pdf_insert_table(table_headers)

#Loop through files
for i in range(len(catalogue_df.index)):
    
    #print '-- Treating {} @ {}'.format(catalogue_df.iloc[i].name, catalogue_df.iloc[i].reduction_fits)
    
    #Locate the objects
    objName         = catalogue_df.iloc[i].name
    
    if objName not in ['coso']:
    
        ouput_folder    = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        fits_file       = catalogue_df.iloc[i].reduction_fits
        
        #Get previous redshifts
        z_blue      = catalogue_df.iloc[i].z_Blue       
        z_red       = catalogue_df.iloc[i].z_Red
        matchLambda = catalogue_df.iloc[i].join_wavelength
        
        #Load lines dataframe
        lineslog_address    = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=lineslog_extension)
        lineslog_frame      = dz.load_lineslog_frame(lineslog_address)
        idx_dict = {}
        idx_dict['blue']    = (lineslog_frame.lambda_theo < matchLambda)
        idx_dict['red']     = (lineslog_frame.lambda_theo > matchLambda) 
        idx_dict['z_blue']  = z_blue
        idx_dict['z_red']   = z_red
            
        #Case we only have so few lines
        if (idx_dict['blue'].sum() > 2) and (idx_dict['red'].sum() > 2):
                    
            for color in ['blue', 'red']:
                
                lines_idx       = idx_dict[color]
                z_old           = idx_dict['z_{}'.format(color)]
                
                lambda_theo     = lineslog_frame.loc[lines_idx].lambda_theo.values
                lambda_obs      = lineslog_frame.loc[lines_idx].lambda_obs.values * (1 + z_old)
                mu_obs          = lineslog_frame.loc[lines_idx].mu.values * (1 + z_old)
                eqw_obs         = lineslog_frame.loc[lines_idx].eqw.values
                        
                #Calculation from the peak
                z_i_array       = (lambda_obs - lambda_theo)/lambda_theo
                mean_value      = np_sum(z_i_array * eqw_obs) / np_sum(eqw_obs)
                std_dev         = std(z_i_array)
                catalogue_df.loc[objName, 'z_{}_obs'.format(color)] = ufloat(mean_value, std_dev) 
                catalogue_df.loc[objName, 'z_{}_obs_percentage'.format(color)] = (mean_value - z_old) / z_old * 100
                
    #                 for j in range(len(lambda_theo)):
    #                     old_fit = lambda_obs[j] / (1 + z_old)
    #                     new_fit = lambda_obs[j] / (1 + mean_value)
    #                     print lambda_theo[j], ':', old_fit, (1-old_fit/lambda_theo[j]) * 100, new_fit, (1-new_fit/lambda_theo[j]) * 100
                
                #Calculation from the gaussian fit
                z_i_array       = (mu_obs - lambda_theo)/lambda_theo
                mean_value      = np_sum(z_i_array * eqw_obs) / np_sum(eqw_obs)
                std_dev         = std(z_i_array)            
                catalogue_df.loc[objName, 'z_{}_mu'.format(color)] = ufloat(mean_value, std_dev) 
                catalogue_df.loc[objName, 'z_{}_mu_percentage'.format(color)] = (mean_value - z_old) / z_old * 100
            
            #Percentage difference between old and new:
            blue_percentage_entry = '{0:.2f}, {0:.2f}'.format(catalogue_df.loc[objName, 'z_blue_obs_percentage'], catalogue_df.loc[objName, 'z_blue_mu_percentage'])
            red_percentage_entry = '{0:.2f}, {0:.2f}'.format(catalogue_df.loc[objName, 'z_red_obs_percentage'], catalogue_df.loc[objName, 'z_red_mu_percentage'])
    
            row = [objName.replace('_','-'), z_blue, catalogue_df.loc[objName, 'z_blue_obs'], catalogue_df.loc[objName, 'z_blue_mu'], blue_percentage_entry, z_red, catalogue_df.loc[objName, 'z_red_obs'], catalogue_df.loc[objName, 'z_red_mu'], red_percentage_entry]     
                 
            dz.addTableRow(row, last_row = False if i < len(catalogue_df.index) - 1 else True)
        
        try:
            print objName, round(catalogue_df.loc[objName, 'z_blue_obs'].std_dev,6), round(catalogue_df.loc[objName, 'z_red_obs'].std_dev, 6)
        except:
            print objName, round(catalogue_df.loc[objName, 'z_blue_mu']), catalogue_df.loc[objName, 'z_blue_obs']

dz.generate_pdf()            
            
            