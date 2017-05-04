from dazer_methods import Dazer
from matplotlib import pyplot as plt
import pyneb as pn
from numpy import random, nan
from numpy import median, std

def plot_metallic_relation(catalogue_df, lines_ratio, theo_value, element, color, df_refer, label):

    valid_indeces = []
    valid_objects = []
   
    for i in range(len(catalogue_df.index)):
        
        #Object
        objName             = catalogue_df.iloc[i].name
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        lineslog_address    = '{objfolder}{codeName}_WHT_linesLog_emission.txt'.format(objfolder = ouput_folder, codeName=objName)
        lineslog_frame      = dz.load_lineslog_frame(lineslog_address)
        
        if (lines_ratio[0] in lineslog_frame.index) and (lines_ratio[1] in lineslog_frame.index):
            OIII_ratio  = lineslog_frame.loc[lines_ratio[0]]['line_Flux'] / lineslog_frame.loc[lines_ratio[1]]['line_Flux']
            valid_indeces.append(i)
            valid_objects.append(objName)
            catalogue_df.loc[objName, df_refer] = OIII_ratio
            dz.data_plot(i, OIII_ratio.nominal_value, label if i == 0 else "", markerstyle='o', color = color, y_error=OIII_ratio.std_dev)
        
        dz.Axis.axhline(y=theo_value, color = color, linestyle='-')
        dz.Axis.axhline(y=theo_value*1.05, color = color, linestyle='--', label = '5% limit', linewidth=1)
        dz.Axis.axhline(y=theo_value*0.95, color = color, linestyle='--', label = '5% limit', linewidth=1)
        dz.Axis.axhline(y=theo_value*1.1, color = color, linestyle=':', label = '10% limit', linewidth=1)
        dz.Axis.axhline(y=theo_value*0.9, color = color, linestyle=':', label = '10% limit', linewidth=1)
        
        dz.Axis.set_ylim(theo_value - 1, theo_value + 1)
    
    # dz.Axis.xticks(valid_indeces, valid_objects, rotation='vertical')
    
    dz.Axis.set_xticks(valid_indeces)
    dz.Axis.set_xticklabels(valid_objects, rotation='80')
    
    # plt.margins(0.2)
    plt.subplots_adjust(bottom=0.30)
    
    dz.FigWording('HII galaxies', 'Observed ratio', '{element} observed ratio in observational catalogue'.format(element=element))  #, XLabelPad = 20
         
#     output_pickle = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/data/{element}_lineRatio'.format(element = element)
#     dz.save_manager(output_pickle, save_pickle = True) 
    
    return

#Create class object

dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Set figure format
dz.FigConf()

#Atomic dictionaries
pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
O3 = pn.Atom('O', 3)
S3 = pn.Atom('S', 3)
N2 = pn.Atom('N', 2)
He1 = pn.RecAtom('He', 1)

S3_9000_ratio = S3.getEmissivity(10000, 1000, wave = 9531) / S3.getEmissivity(10000, 1000, wave = 9069)
O3_5000_ratio = O3.getEmissivity(10000, 1000, wave = 5007) / O3.getEmissivity(10000, 1000, wave = 4959)
N2_6500_ratio = N2.getEmissivity(10000, 1000, wave = 6584) / N2.getEmissivity(10000, 1000, wave = 6548)

# plot_helium_relation(catalogue_df, element = 'Helium', color = '#bcbd22', label = 'Helium abundance per line')
plot_metallic_relation(catalogue_df, ['O3_5007A', 'O3_4959A'], O3_5000_ratio, 'Oxygen', color='#009E73',  df_refer = '[OIII]5007A/[OIII]4959A_emis', label  = r'Oxygen $\frac{[OIII]50007\AA}{[OIII]4959\AA}$')
plot_metallic_relation(catalogue_df, ['S3_9531A', 'S3_9069A'], S3_9000_ratio, 'Sulfur', color='#D55E00',  df_refer = '[SIII]9531A/[SIII]9069A_emis', label = r'Sulfur $\frac{[SIII]9531\AA}{[SIII]9069\AA}$')
plot_metallic_relation(catalogue_df, ['N2_6584A', 'N2_6548A'], N2_6500_ratio, 'Nitrogen', color='#0072B2',df_refer = '[NII]6548A/[NII]6584A_emis',  label = r'Oxygen $\frac{[NII]6584\AA}{[NII]6548\AA}$')

# dz.display_fig()

dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx', df_sheet_format = 'catalogue_data')

print 'Data treated'