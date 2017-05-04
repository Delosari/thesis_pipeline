from dazer_methods import Dazer
from matplotlib import pyplot as plt
import pyneb as pn
from numpy import random, nan
from numpy import median, std

def plot_metallic_relation(catalogue_df, lines_ratio, theo_value, element, color, label):

    valid_indeces = []
    valid_objects = []
   
    for i in range(len(catalogue_df.index)):
        
        #Object
        objName             = catalogue_df.iloc[i].name
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        lineslog_address    = '{objfolder}{codeName}_WHT_linesLog_emission.txt'.format(objfolder = ouput_folder, codeName=objName)
        
        #Load object data
        lineslog_frame      = dz.load_lineslog_frame(lineslog_address)
    
        #Load electron temperature and density (if not available it will use Te = 10000K and ne = 100cm^-3)                        
        T_e = catalogue_df.iloc[i].TeSIII if catalogue_df.iloc[i].TeSIII != nan else 10000.0
        n_e = catalogue_df.iloc[i].TeSII if catalogue_df.iloc[i].TeSII != nan else 100.0   
        
        HeI_idx = (lineslog_frame.Ion.str.contains('HeI_')) & (lineslog_frame.index != 'He1_8446A') & (lineslog_frame.index != 'He1_7818A')
        
        if (lines_ratio[0] in lineslog_frame.index) and (lines_ratio[1] in lineslog_frame.index):
            OIII_ratio  = lineslog_frame.loc[lines_ratio[0]]['line_Flux'] / lineslog_frame.loc[lines_ratio[1]]['line_Flux']
            valid_indeces.append(i)
            valid_objects.append(objName)
    
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

def plot_helium_relation(catalogue_df, element, color, label, size_array = 500):

#     #Load electron temperature and density (if not available it will use Te = 10000K and ne = 100cm^-3)                        
#     T_e = catalogue_df.iloc[i].Te_SIII if catalogue_df.iloc[i].Te_SIII != None else 10000.0
#     n_e = catalogue_df.iloc[i].ne_SII if catalogue_df.iloc[i].ne_SII != None else 100.0  

    T_e_dist = random.normal(10000, 500, size = size_array)
    n_e_dist = random.normal(100, 20, size = size_array)

    valid_indeces = []
    valid_objects = []
    
    for i in range(len(catalogue_df.index)):
        
        #Object
        objName             = catalogue_df.iloc[i].name
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        lineslog_address    = '{objfolder}{codeName}_WHT__linesLog_reduc.txt'.format(objfolder = ouput_folder, codeName=objName)
        objdata             =  catalogue_df.iloc[i]

        #Load object data
        lineslog_frame      = dz.load_lineslog_frame(lineslog_address)
        dz.deredden_lines('cHbeta_reduc', lineslog_frame, objdata)
    
        Flux_Hbeta = lineslog_frame.loc['H1_4861A', 'line_Int'].nominal_value
        
        HeI_idx = (lineslog_frame.Ion.str.contains('HeI_')) & (~lineslog_frame.index.isin(['He1_8446A', 'He1_7065A', 'He1_7281A', 'He1_4713A', 'He1_4922A', 'He1_3889A', 'He1_4388A', 'He1_4026A']))
        HeI_labels = lineslog_frame.loc[HeI_idx].index

        He_fluxes = lineslog_frame.loc[HeI_labels].line_Int.values
        ions = lineslog_frame.loc[HeI_labels].Ion.values
     
        print '--', objName
        for j in range(len(HeI_labels)):
                
            pyneb_code  = ions[j][ions[j].find('_')+1:len(ions[j])] 
            line_distribution = random.normal(He_fluxes[j].nominal_value, He_fluxes[j].std_dev, size = size_array)
            abundance = He1.getIonAbundance(int_ratio = line_distribution, tem=T_e_dist, den=n_e_dist, wave = pyneb_code, Hbeta = Flux_Hbeta)
            dz.data_plot(i, median(abundance), markerstyle='o', label = HeI_labels[j], color = marker_dict[HeI_labels[j]], y_error=std(abundance))
            
        valid_indeces.append(i)
        valid_objects.append(objName)
    
    dz.Axis.set_ylim(0.00, 0.3)     
    dz.Axis.set_xticks(valid_indeces)
    dz.Axis.set_xticklabels(valid_objects, rotation='80')
    plt.subplots_adjust(bottom=0.30)
     
    dz.FigWording('HII galaxies', 'Helium abundance', 'HeI abundance from each line'.format(element=element), sort_legend=True)  #, XLabelPad = 20
               
    output_pickle = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/data/{element}_lineRatio'.format(element = element)
    dz.save_manager(output_pickle, save_pickle = True) 
    
    return

# random.normal(mean(HeII_HII_array), mean(HeII_HII_error), size = self.MC_array_len)


#Create class object

dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Set figure format
dz.FigConf()

marker_dict = {
'He1_3889A':dz.colorVector['iron'],
'He1_4026A':dz.colorVector['silver'],
'He1_4388A':dz.colorVector['skin'],
'He1_4438A':dz.colorVector['cyan'],
'He1_4472A':dz.colorVector['olive'],
'He1_4713A':dz.colorVector['green'],
'He1_4922A':dz.colorVector['iron'],
'He1_5016A':dz.colorVector['yellow'],
'He1_5876A':dz.colorVector['orangish'],
'He1_6678A':dz.colorVector['dark blue'],
'He1_7065A':'black',
'He1_7281A':'#CC79A7'}

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
# plot_metallic_relation(catalogue_df, ['O3_5007A', 'O3_4959A'], O3_5000_ratio, 'Oxygen', color='#009E73', label  = r'Oxygen $\frac{[OIII]50007\AA}{[OIII]4959\AA}$')
plot_metallic_relation(catalogue_df, ['S3_9531A', 'S3_9069A'], S3_9000_ratio, 'Sulfur', color='#D55E00', label = r'Sulfur $\frac{[SIII]9531\AA}{[SIII]9069\AA}$')
# plot_metallic_relation(catalogue_df, ['N2_6584A', 'N2_6548A'], N2_6500_ratio, 'Nitrogen', color='#0072B2', label = r'Oxygen $\frac{[NII]6584\AA}{[NII]6548\AA}$')

dz.display_fig()

print 'Data treated'
    