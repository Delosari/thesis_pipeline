from matplotlib import pyplot as plt
from dazer_methods import Dazer
from uncertainties import ufloat
from numpy import searchsorted, ceil as np_ceil, interp, random,  nanmean, nanstd, median
from pylatex import Math, NoEscape, Section
from os.path import isfile

#Create class object
dz = Dazer()

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_dataframe(catalogue_dict['dataframe'])

#Grid configuration
n_columns = 4.0
sizing_dict = {'xtick.labelsize' : 8, 'ytick.labelsize' : 10, 'axes.titlesize':14}

#Declare data for the analisis
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'
cHbeta_type = 'cHbeta_reduc'

#Atoms for the abundances
MC_length = 500
dz.load_elements()
oxygen_emision = ['O2_3726A', 'O3_4363A', 'O3_4959A', 'O3_5007A', 'O2_7330A'] 
nitrogen_emision = ['N2_6548A', 'N2_6584A'] 
sulfur_emision = ['S2_6716A', 'S3_6312A', 'S3_9069A', 'S3_9531A'] 

Te = random.normal(10000, 2000, size = MC_length)
ne = random.normal(100, 20, size = MC_length)

dz.create_pdfDoc('/home/vital/Desktop/example_line_abundances')

#Loop through the objects
for i in range(len(catalogue_df.index)):
 
    #Object
    objName         = catalogue_df.iloc[i].name
    
    print 'Treating object: ', objName
        
    #Locate the files
    ouput_folder    = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    fits_reduc      = catalogue_df.iloc[i].reduction_fits
    fits_emission   = catalogue_df.iloc[i].stellar_fits
    fits_stellar    = ouput_folder + objName + '_StellarContinuum.fits'
    lineslog_address  = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=AbundancesFileExtension)
    
    if isfile(fits_stellar):
#     if i < 3:
        
        #Extract observational data
        wave_reduc, flux_reduc, header_0_reduc      = dz.get_spectra_data(fits_reduc)
        wave_emis, flux_emis, header_emis           = dz.get_spectra_data(fits_emission)
        wave_stellar, flux_stellar, header_stellar  = dz.get_spectra_data(fits_stellar)
        reduc_lineslog_df                           = dz.load_lineslog_frame(lineslog_address)
                
        #Perform the reddening correction
        cHbeta = catalogue_df.iloc[i][cHbeta_type]
        dz.deredden_lines(cHbeta, reduc_lineslog_df)
        
        #Measure Hbeta flux
        Hbeta_wavelengths = reduc_lineslog_df.loc['H1_4861A', ['Wave1', 'Wave2', 'Wave3', 'Wave4', 'Wave5', 'Wave6']].values
        Hbeta_dist = random.normal(reduc_lineslog_df.loc['H1_4861A'].line_Int.nominal_value, reduc_lineslog_df.loc['H1_4861A'].line_Int.std_dev, MC_length)
        
        #Insert new section in pdf
        with dz.pdfDoc.create(Section('HII Galaxy: {}'.format(objName))):
            
            dz.add_page()
            
            #------Plot Oxygen lines 
            element_lines = reduc_lineslog_df.loc[(reduc_lineslog_df.index.isin(oxygen_emision))].index.values
            if len(element_lines) > 0: 
                dz.FigConf(plotStyle='seaborn-colorblind', Figtype = 'grid', plotSize = sizing_dict, 
                   n_columns = int(len(element_lines)), n_rows = int(np_ceil(len(element_lines)/n_columns)))
                         
                for j in range(len(element_lines)):    
                     
                    #Define plotting regions
                    regions_wavelengths = reduc_lineslog_df.loc[element_lines[j], ['Wave1', 'Wave2', 'Wave3', 'Wave4', 'Wave5', 'Wave6']].values
                    idcs_obj, idcs_stellar = searchsorted(wave_reduc, regions_wavelengths), searchsorted(wave_stellar, regions_wavelengths)
                    subwave_solar, subFlux_solar = wave_stellar[idcs_stellar[0]:idcs_stellar[5]], flux_stellar[idcs_stellar[0]:idcs_stellar[5]]
                    subWwave, subFlux = wave_reduc[idcs_obj[0]:idcs_obj[5]], flux_reduc[idcs_obj[0]:idcs_obj[5]]
                    subWwave_emis, subFlux_emis = wave_emis[idcs_obj[0]:idcs_obj[5]], flux_emis[idcs_obj[0]:idcs_obj[5]]
                    dz.data_plot(subWwave, subFlux, label='', linestyle='step', graph_axis=dz.Axis[j])   
                    dz.data_plot(subwave_solar, subFlux_solar, label='', linestyle='step', graph_axis=dz.Axis[j])
                
                    dz.FigWording(xlabel='', ylabel='', title=element_lines[j], graph_axis=dz.Axis[j])
                
                plt.tight_layout()
                dz.fig_to_pdf(label='{} oxygen lines'.format(objName.replace('_','-')), add_page=True)
                dz.reset_fig()
            
            #------Plot Nitrogen lines
            element_lines = reduc_lineslog_df.loc[(reduc_lineslog_df.index.isin(nitrogen_emision))].index.values
            if len(element_lines) > 0: 
                dz.FigConf(plotStyle='seaborn-colorblind', Figtype = 'grid', plotSize = sizing_dict, 
                   n_columns = int(len(element_lines)), n_rows = int(np_ceil(len(element_lines)/n_columns)))
                 
                for j in range(len(element_lines)):    
                     
                    #Define plotting regions
                    regions_wavelengths = reduc_lineslog_df.loc[element_lines[j], ['Wave1', 'Wave2', 'Wave3', 'Wave4', 'Wave5', 'Wave6']].values
                    idcs_obj, idcs_stellar = searchsorted(wave_reduc, regions_wavelengths), searchsorted(wave_stellar, regions_wavelengths)
                    subwave_solar, subFlux_solar = wave_stellar[idcs_stellar[0]:idcs_stellar[5]], flux_stellar[idcs_stellar[0]:idcs_stellar[5]]
                    subWwave, subFlux = wave_reduc[idcs_obj[0]:idcs_obj[5]], flux_reduc[idcs_obj[0]:idcs_obj[5]]
                    subWwave_emis, subFlux_emis = wave_emis[idcs_obj[0]:idcs_obj[5]], flux_emis[idcs_obj[0]:idcs_obj[5]]
                    dz.data_plot(subWwave, subFlux, label='', linestyle='step', graph_axis=dz.Axis[j])   
                    dz.data_plot(subwave_solar, subFlux_solar, label='', linestyle='step', graph_axis=dz.Axis[j])
                    
                    #Get the good region
                    PartialWavelength, PartialIntensity, LineHeight, LineExpLoc = dz.Emission_Threshold(reduc_lineslog_df.loc[element_lines[j]].lambda_theo, wave_reduc, flux_reduc)
                    dz.Axis[j].set_ylim(median(subFlux_emis/10), LineHeight*2)
                    dz.FigWording(xlabel='', ylabel='', title=element_lines[j], graph_axis=dz.Axis[j])
                
                #Label with theoretical flux:
                target_lines = ['N2_6548A', 'N2_6584A']
                if reduc_lineslog_df.index.isin(target_lines).sum() == len(target_lines):
                    ratio = reduc_lineslog_df.loc['N2_6584A'].line_Int / reduc_lineslog_df.loc['N2_6548A'].line_Int
                    label = 'Galaxy {}: nitrogen lines observed ratio: ${:L}$'.format(objName.replace('_','-'), ratio)
                    label = NoEscape(label)
                else:
                    label = (r'Galaxy {}: Nitrogen lines:'.format(objName.replace('_','-')))
                    for k in range(len(element_lines)):
                        label_line = ' {} ${:L}$ '.format(element_lines[k].replace('_',' '), reduc_lineslog_df.loc[element_lines[k]].line_Int)
                        label += label_line
                    label = NoEscape(label)
                    
                plt.tight_layout()
                dz.fig_to_pdf(label=label, add_page=True)
                dz.reset_fig()
            
            #------Plot Sulfur lines
            element_lines = reduc_lineslog_df.loc[(reduc_lineslog_df.index.isin(sulfur_emision))].index.values
            if len(element_lines) > 0: 
                dz.FigConf(plotStyle='seaborn-colorblind', Figtype = 'grid', plotSize = sizing_dict, 
                   n_columns = int(n_columns), n_rows = int(np_ceil(len(element_lines)/n_columns)))
                         
                for j in range(len(element_lines)):    
                     
                    #Define plotting regions
                    regions_wavelengths = reduc_lineslog_df.loc[element_lines[j], ['Wave1', 'Wave2', 'Wave3', 'Wave4', 'Wave5', 'Wave6']].values
                    idcs_obj, idcs_stellar = searchsorted(wave_reduc, regions_wavelengths), searchsorted(wave_stellar, regions_wavelengths)
                    subwave_solar, subFlux_solar = wave_stellar[idcs_stellar[0]:idcs_stellar[5]], flux_stellar[idcs_stellar[0]:idcs_stellar[5]]
                    subWwave, subFlux = wave_reduc[idcs_obj[0]:idcs_obj[5]], flux_reduc[idcs_obj[0]:idcs_obj[5]]
                    subWwave_emis, subFlux_emis = wave_emis[idcs_obj[0]:idcs_obj[5]], flux_emis[idcs_obj[0]:idcs_obj[5]]
                    dz.data_plot(subWwave, subFlux, label='', linestyle='step', graph_axis=dz.Axis[j])   
                    dz.data_plot(subwave_solar, subFlux_solar, label='', linestyle='step', graph_axis=dz.Axis[j])
                    
                    dz.FigWording(xlabel='', ylabel='', title=element_lines[j], graph_axis=dz.Axis[j])
                
                #Label with theoretical flux:
                target_lines = ['S3_9069A', 'S3_9531A']
                if reduc_lineslog_df.index.isin(target_lines).sum() == len(target_lines):
                    ratio = reduc_lineslog_df.loc['S3_9531A'].line_Int / reduc_lineslog_df.loc['S3_9069A'].line_Int
                    label = NoEscape(r'Galaxy {}: sulfur lines observed ratio: ${:L}$'.format(objName.replace('_','-'), ratio))
                else:
                    label = (r'Galaxy {}: Sulfur lines:')
                    for j in range(len(element_lines)):
                        label_line = ' {} ${:L}$ '.format(element_lines[j].replace('_',' '), reduc_lineslog_df.loc[element_lines[j]].line_Int)
                        label += label_line
                    label = NoEscape(label)
                    
                plt.tight_layout()
                dz.fig_to_pdf(label=label, add_page=True)
                dz.reset_fig()   
            
            #Plot Helium lines
            idcs_helium     = reduc_lineslog_df.Ion.str.contains('HeI') & (reduc_lineslog_df.Ion != 'HeI_8446')
            lines_labels    = reduc_lineslog_df.loc[idcs_helium].index.values
            n_lines         = lines_labels.shape[0]
            if n_lines > 0:
                dz.FigConf(plotStyle='seaborn-colorblind', Figtype = 'grid', plotSize = sizing_dict, 
                           n_columns = int(n_columns), n_rows = int(np_ceil(n_lines/n_columns)))
                
                for j in range(n_lines):
                    
                    #Define plotting regions
                    regions_wavelengths = reduc_lineslog_df.loc[lines_labels[j], ['Wave1', 'Wave2', 'Wave3', 'Wave4', 'Wave5', 'Wave6']].values
                    idcs_obj, idcs_stellar = searchsorted(wave_reduc, regions_wavelengths), searchsorted(wave_stellar, regions_wavelengths)
                    subWwave, subFlux = wave_reduc[idcs_obj[0]:idcs_obj[5]], flux_reduc[idcs_obj[0]:idcs_obj[5]]
                    subWwave_emis, subFlux_emis = wave_emis[idcs_obj[0]:idcs_obj[5]], flux_emis[idcs_obj[0]:idcs_obj[5]]
                    subwave_solar, subFlux_solar = wave_stellar[idcs_stellar[0]:idcs_stellar[5]], flux_stellar[idcs_stellar[0]:idcs_stellar[5]]
                    interFlux_solar = interp(wave_reduc[idcs_obj[2]:idcs_obj[3]], wave_stellar[idcs_stellar[2]:idcs_stellar[3]], flux_stellar[idcs_stellar[2]:idcs_stellar[3]])
                                
                    #Calculate the line abundances
                    if 'He1' in lines_labels[j]:
                        atom = dz.He1_atom
                        atom_label = 'HeII'
                    elif 'He2' in lines_labels[j]:
                        atom = dz.He2_atom
                        atom_label = 'HeIII' 
                        
                    wave_label = int(round(reduc_lineslog_df.loc[lines_labels[j]].lambda_theo))
                    Helium_i_dist = random.normal(reduc_lineslog_df.loc[lines_labels[j]].line_Int.nominal_value, reduc_lineslog_df.loc[lines_labels[j]].line_Int.std_dev, MC_length)
                    abund_dist  = atom.getIonAbundance(int_ratio=Helium_i_dist, tem=Te, den=ne, wave=wave_label, Hbeta = Hbeta_dist)
                    abund_log   = ufloat(nanmean(abund_dist), nanstd(abund_dist))
                    abund_label = '{:L}'.format(abund_log)
                
                    #Plot the data
                    title_line_plot = """{label}:
                    $\\frac{{{at_label}}}{{HII}}={abund}$""".format(label=lines_labels[j], at_label=atom_label, abund=abund_label)
                    dz.data_plot(subWwave, subFlux, label='', linestyle='step', graph_axis=dz.Axis[j])   
                    dz.data_plot(subWwave_emis, subFlux_emis, label='', linestyle='step', graph_axis=dz.Axis[j])
                    dz.Axis[j].fill_between(wave_reduc[idcs_obj[2]:idcs_obj[3]], flux_reduc[idcs_obj[2]:idcs_obj[3]], interFlux_solar, step='mid', alpha=0.5)
                    if lines_labels[j] == 'He1_5016A':
                        dz.Axis[j].set_ylim(0, reduc_lineslog_df.loc[lines_labels[j]].A * 4)
                    dz.data_plot(subwave_solar, subFlux_solar, label='', linestyle='step', graph_axis=dz.Axis[j])
                    dz.FigWording(xlabel='', ylabel='', title=title_line_plot, graph_axis=dz.Axis[j])
                     
                plt.tight_layout()
                dz.fig_to_pdf(label='{} Helium lines:'.format(objName.replace('_','-')), add_page=True)
                dz.reset_fig()
        
    else:
        print '--There is not stellar spectrum'
        
dz.generate_pdf(True)

print 'Data treated'
        