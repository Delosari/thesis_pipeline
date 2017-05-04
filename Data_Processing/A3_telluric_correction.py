from dazer_methods import Dazer
from pandas import read_csv
from uncertainties import ufloat
from numpy import array, median, searchsorted, max, where, ones, mean
from astropy.io import fits
from DZ_observation_reduction import spectra_reduction
 
def Emission_Threshold(LineLoc, TotalWavelen, TotalInten, BoxSize = 70):
      
    #Use this method to determine the box and location of the emission lines
    Bot                 = LineLoc - BoxSize
    Top                 = LineLoc + BoxSize
      
    indmin, indmax      = searchsorted(TotalWavelen, (Bot, Top))
    if indmax > (len(TotalWavelen)-1):
        indmax = len(TotalWavelen)-1
      
    PartialWavelength   = TotalWavelen[indmin:indmax]
    PartialIntensity    = TotalInten[indmin:indmax]
      
    Bot                 = LineLoc - 2
    Top                 = LineLoc + 2
      
    indmin, indmax      = searchsorted(PartialWavelength, (Bot, Top))
      
    LineHeight          = max(PartialIntensity[indmin:indmax])
    LineExpLoc          = median(PartialWavelength[where(PartialIntensity == LineHeight)])
            
    return PartialWavelength, PartialIntensity, LineHeight, LineExpLoc
  
def region_indeces(wave_min, wave_max, wavenlength_range):
      
    low_trim, up_trim   = searchsorted(wavenlength_range, [wave_min, wave_max])
    indeces_array       = array(range(low_trim, up_trim))
      
    return indeces_array
  
dz = Dazer()
dz_reduc = spectra_reduction()
 
script_code = dz.get_script_code()
lickIndcs_extension = '_lick_indeces.txt'
  
#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
  
SIII_theo = 2.469
H7_H8_ratio_theo = 1.98
 
#Set figure format
size_dict = {'figure.figsize': (16, 10), 'axes.labelsize':12, 'legend.fontsize':12}
dz.FigConf(plotStyle='seaborn-colorblind', plotSize = size_dict, Figtype = 'Grid_size', n_columns = 1, n_rows = 2)
#dz.FigConf(plotStyle='seaborn-colorblind', Figtype = 'Grid_size', n_columns = 1, n_rows = 2)
  
#Sulfur lines to plot
lines_interest = ['S3_9069A','S3_9531A', 'H1_9015A', 'H1_9229A', 'H1_9546A']
 
for i in range(len(catalogue_df.index)):
 
    print '\n-- Treating {} @ {}'.format(catalogue_df.iloc[i].name, catalogue_df.iloc[i].Red_file)
 
    codeName            = catalogue_df.iloc[i].name
    fits_file           = catalogue_df.iloc[i].Red_file
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], codeName) 
                         
    #Get object
    objName = codeName
    redshift_factor = 1 + catalogue_df.iloc[i].z_Red 
     
    #Spectrum data
    wave_obs, flux_obs, header_0_obs = dz.get_spectra_data(fits_file)
    lick_idcs_df                    = read_csv(ouput_folder + codeName + lickIndcs_extension, delim_whitespace = True, header = 0, index_col = 0, comment='L') #Dirty trick to avoid the Line_label row
    wave_join, wave_max             = catalogue_df.loc[codeName].join_wavelength, catalogue_df.loc[codeName].Wmax_Red
    idx_obj_join, idx_obj_max_Red   = searchsorted(wave_obs, [wave_join, wave_max])
    len_red_region                  = idx_obj_max_Red - idx_obj_join
             
    #Load reduction dataframe
    reduction_folder = catalogue_df.loc[codeName].obsfolder
    dz_reduc.declare_catalogue(reduction_folder, verbose=False)
      
    #Load telluric star files
    idcs_stars      = (dz_reduc.reducDf.reduc_tag == 'norm_narrow')
    Files_Folders   = dz_reduc.reducDf.loc[idcs_stars, 'file_location'].values
    Files_Names     = dz_reduc.reducDf.loc[idcs_stars, 'file_name'].values
    objects         = dz_reduc.reducDf.loc[idcs_stars, 'frame_tag'].values
      
    #Declare star for telluric correction
    favoured_star = catalogue_df.iloc[i].telluric_star
     
    #Case we can (and we want) to perform the telluric correction:        
    if (len(objects) > 0) and (favoured_star != 'None'):
           
        star_dict = {}
        for i in range(len(objects)):
            wave_star, flux_star, header_0_star = dz.get_spectra_data(Files_Folders[i] + Files_Names[i])
            idx_print_low, idx_print_high       = searchsorted(wave_star,[9000, 9650])
            idx_join_region                     = searchsorted(wave_star,[wave_join])
             
            if len(flux_star) == 2:
                flux_star = flux_star[0][0]
                 
            star_dict[objects[i]+'_wave'], star_dict[objects[i]+'_flux'] = wave_star, flux_star
            star_dict[objects[i]+'_idx_join'] = idx_join_region
                          
            dz.data_plot(wave_star, flux_star, label=objects[i], graph_axis=dz.ax2)
           
        obj_red_region = array(range(idx_obj_join,idx_obj_join + len_red_region))
        mean_flux = mean(flux_obs)
     
        #Loop through the diagnostic lines   
        obj_dict = {}
        for line in lines_interest:
            if line in lick_idcs_df.index:
     
                dz.Current_Label    = lick_idcs_df.loc[line].name
                dz.Current_Ion      = lick_idcs_df.loc[line].Ion
                dz.Current_TheoLoc  = redshift_factor * lick_idcs_df.loc[line].lambda_theo
                selections          = redshift_factor * lick_idcs_df.loc[line][3:9].values
                      
                #Measure the line intensity
                line_fit_orig = dz.measure_line(wave_obs, flux_obs, selections, None, 'lmfit', store_data = False)
                      
                #Area to plot
                subwave, subflux, lineHeight, LineExpLoc = Emission_Threshold(dz.Current_TheoLoc, wave_obs, flux_obs)    
                obj_dict[line + '_x_reduc']        = line_fit_orig['x_resample']
                obj_dict[line + '_y_reduc']        = line_fit_orig['y_resample']
                obj_dict[line + '_flux_reduc']     = line_fit_orig['flux_intg']
                obj_dict[line + '_fluxEr_reduc']   = line_fit_orig['flux_intg_er']
                obj_dict[line + '_Peak']           = line_fit_orig['A0']
                obj_dict[line + '_continuum']      = line_fit_orig['zerolev_mean']
                obj_dict[line + '_Emis_reduc']     = ufloat(line_fit_orig['flux_intg'], line_fit_orig['flux_intg_er'])
     
        #Measure the lines after the telluric correction for each case 
        for star in objects:
            star_red_region = array(range(star_dict['{}_idx_join'.format(star)], star_dict['{}_idx_join'.format(star)] + len_red_region))
            wave_tell, flux_tell = wave_obs, flux_obs / star_dict[star + '_flux']
     
            for line in lines_interest:
       
                if line in lick_idcs_df.index:
     
                    dz.Current_Label    = lick_idcs_df.loc[line].name
                    dz.Current_Ion      = lick_idcs_df.loc[line].Ion
                    dz.Current_TheoLoc  = redshift_factor * lick_idcs_df.loc[line].lambda_theo
                    selections          = redshift_factor * lick_idcs_df.loc[line][3:9].values
     
                    line_fit_tell = dz.measure_line(wave_tell, flux_tell, selections, None, 'lmfit', store_data = False)
                    obj_dict[line + '_x_telluc_' + star]       = line_fit_tell['x_resample']
                    obj_dict[line + '_y_telluc_' + star]       = line_fit_tell['y_resample']
                    obj_dict[line + '_flux_telluc_' + star]    = line_fit_tell['flux_intg']
                    obj_dict[line + '_fluxEr_telluc_' + star]  = line_fit_tell['flux_intg_er']
                    obj_dict[line + '_Emis_telluc_' + star]    = ufloat(line_fit_tell['flux_intg'], line_fit_tell['flux_intg_er'])
             
            #Save the corrected flux from the favoured star
            if star == favoured_star:
                obj_dict['corrected_flux'] = flux_tell
                obj_dict['corrected_wave'] = wave_tell
                obj_dict['corrected_header'] = header_0_obs
                 
        #Data sulfur lines
        label_reduc, label_telluc = None, None
        if ('S3_9069A' in lick_idcs_df.index) and ('S3_9531A' in lick_idcs_df.index):      
     
            #Flux ratio from original object
            rapport_orig    = obj_dict['S3_9531A_Emis_reduc'] / obj_dict['S3_9069A_Emis_reduc']
            divergence_orig = r'$\rightarrow$ ${diff}$%'.format(diff = round((1 - SIII_theo/rapport_orig.nominal_value), 3) * 100)
            ratio_SIII      = '{:L}'.format(rapport_orig)
            SIII9069        = '{:L}'.format(ufloat(obj_dict['S3_9069A_flux_reduc'], obj_dict['S3_9069A_fluxEr_reduc']))
            SIII9561        = '{:L}'.format(ufloat(obj_dict['S3_9531A_flux_reduc'], obj_dict['S3_9531A_fluxEr_reduc']))
            label_reduc     = r'4) Before: $\frac{{[SIII]\lambda9561\AA}}{{[SIII]\lambda9069\AA}}=\frac{{{SIII9561}}}{{{SIII9069}}}={ratio_SIII}$ {divergence}'.format(                                                                                                                                                 
                            SIII9561=SIII9561, SIII9069=SIII9069, ratio_SIII=ratio_SIII, divergence=divergence_orig)     
                
            #Flux ratio from from favoured star               
            rapport         = obj_dict['S3_9531A_Emis_telluc_' + favoured_star] / obj_dict['S3_9069A_Emis_telluc_' + favoured_star]
            divergence      = r'$\rightarrow$ ${diff}$%'.format(diff = round((1 - SIII_theo/rapport.nominal_value), 3) * 100)
            ratio_SIII      = '{:L}'.format(rapport)
            SIII9069        = '{:L}'.format(ufloat(obj_dict['S3_9069A_flux_telluc_' + favoured_star], obj_dict['S3_9069A_fluxEr_telluc_' + favoured_star]))
            SIII9561        = '{:L}'.format(ufloat(obj_dict['S3_9531A_flux_telluc_' + favoured_star], obj_dict['S3_9531A_fluxEr_telluc_' + favoured_star]))
            label_telluc    = r'5) After: $\frac{{[SIII]\lambda9561\AA}}{{[SIII]\lambda9069\AA}}=\frac{{{SIII9561}}}{{{SIII9069}}}={ratio_SIII}$ {divergence} ({star})'.format(                                                                                                                                                 
                            SIII9561=SIII9561, SIII9069=SIII9069, ratio_SIII=ratio_SIII, divergence=divergence, star = favoured_star)             
           
            label_telluric = r'2) Sulfur corrected ratio ({}): {}% $\Rightarrow$'.format(SIII_theo, round(1 - SIII_theo/rapport_orig.nominal_value, 3) * 100)
            for star in objects:
                rapport = obj_dict['S3_9531A_Emis_telluc_'+star] / obj_dict['S3_9069A_Emis_telluc_'+star]
                divergence = round((1 - SIII_theo/rapport.nominal_value), 3) * 100 
                label_telluric += r' ${}$% ({}),'.format(round(divergence, 3), star)
           
        #Data from Hpas7 and Hpas8 lines
        label_Hpas = None
        if ('H1_9015A' in lick_idcs_df.index) and ('H1_9546A' in lick_idcs_df.index):
            #label_Hpas = r'3) $\frac{H7_{Pas}\lambda9546\AA}{H8_{Pas}\lambda9229\AA} = $'
            label_Hpas = r'3) Hydrogen corrected ratio ({}): '.format(H7_H8_ratio_theo)
     
            #Original
            rapport = obj_dict['H1_9546A_Emis_reduc'] / obj_dict['H1_9015A_Emis_reduc']
            divergence = round((1 - H7_H8_ratio_theo/rapport.nominal_value), 3) * 100 
            label_Hpas += r'${}$%$\Rightarrow$'.format(divergence)
            HIratio_extension = r' $|$  $\frac{{H7_{{Pas}}\lambda9546\AA}}{{H8_{{Pas}}\lambda9229\AA}} =$ {}%'.format(round(divergence, 3)) 
             
            ratio_H_favoured = ''
            for star in objects:
                rapport = obj_dict['H1_9546A_Emis_telluc_'+star] / obj_dict['H1_9015A_Emis_telluc_'+star]
                divergence = round((1 - H7_H8_ratio_theo/rapport.nominal_value), 3) * 100 
                label_Hpas += r' ${}$% ({}),'.format(round(divergence, 3), star)
                if star == favoured_star:
                    ratio_H_favoured = rapport
                    HIratio_extension_tell = r' $|$  $\frac{{H7_{{Pas}}\lambda9546\AA}}{{H8_{{Pas}}\lambda9229\AA}} =$ {}% ({})'.format(round(divergence, 3), star) 
                                       
        #Plot before and after telluric correction
        dz.data_plot(wave_obs[region_indeces(wave_join, wave_max, wave_obs)], flux_obs[region_indeces(wave_join, wave_max, wave_obs)], label='1) Observed spectrum', linestyle='step', graph_axis=dz.ax1)
        dz.data_plot(wave_tell, flux_tell, label=label_telluric, linestyle='step', graph_axis=dz.ax1)
         
        if label_Hpas is not None:
            dz.ax1.autoscale(enable=False)
            x, y = array([9229.0, 9546.0]) * redshift_factor, ones(2) * mean_flux
            dz.data_plot(x, y, label_Hpas, markerstyle='o', graph_axis=dz.ax1, color=dz.colorVector['olive'])    
     
        if label_telluc is not None:
            dz.data_plot(obj_dict['S3_9069A_x_telluc_' + favoured_star], obj_dict['S3_9069A_y_telluc_' + favoured_star], label=label_telluc + HIratio_extension_tell, color=dz.colorVector['pink'], graph_axis=dz.ax1)
            dz.data_plot(obj_dict['S3_9531A_x_telluc_' + favoured_star], obj_dict['S3_9531A_y_telluc_' + favoured_star], label=label_telluc + HIratio_extension_tell, color=dz.colorVector['pink'], graph_axis=dz.ax1)
           
        if label_reduc is not None:
            dz.data_plot(obj_dict['S3_9069A_x_reduc'], obj_dict['S3_9069A_y_reduc'], label=label_reduc + HIratio_extension, color=dz.colorVector['cyan'], graph_axis=dz.ax1)
            dz.data_plot(obj_dict['S3_9531A_x_reduc'], obj_dict['S3_9531A_y_reduc'], label=label_reduc + HIratio_extension, color=dz.colorVector['cyan'], graph_axis=dz.ax1)
         
        dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', r'Object {} Telluric correction ({} star)'.format(codeName, favoured_star), loc='upper left', graph_axis=dz.ax1, sort_legend=True) 
        dz.FigWording(r'Wavelength $(\AA)$', 'Normalized flux', '', loc='lower center', graph_axis=dz.ax2, ncols_leg=4) 
         
        dz.ax2.set_ylim(0.2,1.25)
        if 'S3_9531A_continuum' in obj_dict:
            dz.ax1.set_ylim(-2 * obj_dict['S3_9531A_continuum'], 1.1 * obj_dict['S3_9531A_Peak'])
        else:
            dz.ax1.set_ylim(0.005 * mean_flux, 20 * mean_flux)
           
 
        output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=script_code, objCode=objName, ext='Telluric correction')
        dz.save_manager(output_pickle, save_pickle = True)
       
         
        #Save the fits file
        telluric_fits_address = fits_file.replace('.fits', '_tell.fits')
        catalogue_df.loc[codeName, 'tellRed_file'] = telluric_fits_address
         
        fits.writeto(telluric_fits_address, data = obj_dict['corrected_flux'], header = obj_dict['corrected_header'], overwrite = True)
                 
    #In this case the telluric correction is not performed    
    else:
        print '-- Not applying telluric correction'.format(codeName)
        catalogue_df.loc[codeName, 'tellRed_file'] = None
      
    #Reset all the axis    
    dz.ax1.cla()
    dz.ax2.cla()    
    dz.reset_fig()
             
#Save the catalogue dataframe
dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx', df_sheet_format = 'catalogue_data')



        



