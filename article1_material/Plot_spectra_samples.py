#!/usr/bin/env python
from collections import OrderedDict

from dazer_methods import Dazer
from numpy import linspace, zeros, hstack, array
import lineid_plot
import lineid_plot
from scipy.interpolate import interp1d
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from matplotlib import rcParams, pyplot as plt

from matplotlib._png        import read_png
from matplotlib.offsetbox   import OffsetImage, AnnotationBbox

#Declare code classes
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
cHbeta_type             = 'cHbeta_reduc'
nebular_exten           = '_NebularContinuum.fits'
Stellar_ext             = '_StellarContinuum.fits'
emitting_ext            = '_Emission.fits'

#Define plot frame and colors
size_dict = {'figure.figsize':(26,10), 'axes.labelsize':20, 'legend.fontsize':20, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':20, 'ytick.labelsize':20}
#dz.FigConf(plotSize = size_dict)

#Reddening properties
R_v = 3.4
red_curve = 'G03_average'
cHbeta_type = 'cHbeta_reduc'

obj_lines = {}
obj_lines['8']          = OrderedDict()
obj_lines['SHOC579']    = OrderedDict()
obj_lines['8'][r'$H\gamma$']                  = 4340.471
obj_lines['8'][r'$[OIII]4363\AA$']            = 4363.21
obj_lines['8'][r'$HeI4472\AA$']               = 4472
obj_lines['8'][r'$HeII4686\AA$']              = 4686
obj_lines['8'][r'$[ArIV]4740\AA$']            = 4740
obj_lines['8'][r'$H\beta$']                   = 4863.68
obj_lines['8'][r'$[OIII]4959\AA$']            = 4958.8
obj_lines['8'][r'$[OIII]5007\AA$']            = 5007.21
obj_lines['8'][r'$[SIII]9069\AA$']            = 6312
obj_lines['8'][r'$HeI5876\AA$']               = 5876
obj_lines['8'][r'$[SIII]6312\AA$']            = 6312
obj_lines['8'][r'$[NII]6548\AA$']             = 6548
obj_lines['8'][r'$H\alpha$']                  = 6563
obj_lines['8'][r'$[NII]6584\AA$']             = 6584.0
obj_lines['8'][r'$[NII]6584\AA$']             = 6584.0
obj_lines['8'][r'$HeI6678\AA$']               = 6678.0
obj_lines['8'][r'$[SII]6716\AA$']             = 6716.0
obj_lines['8'][r'$[SII]6731\AA$']             = 6731.0
obj_lines['8'][r'$[OII]7319\AA$']             = 7319.0
obj_lines['8'][r'$[OII]7330\AA$']             = 7330.0
obj_lines['8'][r'$[ArIII]7136\AA$']           = 7136.0
obj_lines['8'][r'$[ArIII]7751\AA$']           = 7751.0
obj_lines['8'][r'Paschen jump']               = 8207
obj_lines['8'][r'$[SIII]9069\AA$']            = 9069
obj_lines['8'][r'$[SIII]9531\AA$']            = 9531
obj_lines['SHOC579']['Balmer jump']           = 3646.0
obj_lines['SHOC579'][r'$[OII]3726\AA$']       = 3726.0
obj_lines['SHOC579'][r'$[OII]3728\AA$']       = 3728.0
obj_lines['SHOC579'][r'$H\delta$']            = 4101.68
obj_lines['SHOC579'][r'$HeI4026\AA$']         = 4026.68
obj_lines['SHOC579'].update(obj_lines['8'])



ak = lineid_plot.initial_annotate_kwargs()
# ak['arrowprops']['arrowstyle'] = "->"
ak['arrowprops']['relpos'] = (0.5, 0.0)
ak['rotation'] = 90
print ak

pk = lineid_plot.initial_plot_kwargs()
pk['linewidth'] = 0.8
print pk

rcParams.update(size_dict)

#Loop through files
for i in range(len(catalogue_df.index)):
    
    print '-- Treating {}'.format(catalogue_df.iloc[i].name)
 
    #Locate the objects
    objName             = catalogue_df.iloc[i].name
    
    if objName in ['SHOC579', '8']:
    
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        fits_file           = catalogue_df.iloc[i].reduction_fits
        
        blue_fits           = catalogue_df.iloc[i].Blue_file
        red_fits            = catalogue_df.iloc[i].Red_file
        fits_file           = catalogue_df.iloc[i].reduction_fits

        #Get reduce spectrum data
        Wave_O, Int_O, ExtraData_T = dz.get_spectra_data(fits_file)
        Wave_N, Int_N, ExtraData_N = dz.get_spectra_data(ouput_folder + objName + nebular_exten)
        Wave_S, Int_S, ExtraData_S = dz.get_spectra_data(ouput_folder + objName + Stellar_ext)    
        Wave_E, Int_E, ExtraData_E = dz.get_spectra_data(ouput_folder + objName + emitting_ext)    
        
        Wave_B, Int_B, ExtraData_B = dz.get_spectra_data(blue_fits)
        Wave_R, Int_R, ExtraData_R = dz.get_spectra_data(red_fits)

        line_wave       = obj_lines[objName].values()
        line_label1     = obj_lines[objName].keys()

        # lim                     = 8e-15
        # idx_greater             = Int_O > 8e-15
        # Int_O[idx_greater]      = 8e-15
        fig, ax = lineid_plot.plot_line_ids(Wave_O, Int_O, line_wave, line_label1, annotate_kwargs=ak, plot_kwargs=pk)
        #ax.set_ylim(top=lim)

        arr_hand = read_png('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/SHOC579_invert.png')
        Image_Frame = OffsetImage(arr_hand, zoom=0.25)
        ab = AnnotationBbox(Image_Frame, [0,0],
            xybox=(20,-20),
            xycoords='data',
            boxcoords='axes fraction')
        ax.add_artist(ab)
        ax.update({'xlabel':r'Wavelength $(\AA)$', 'ylabel':'Flux ' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$'})

        #, 'axes.labelsize':20, 'legend.fontsize':20, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':20, 'ytick.labelsize':20
        #dz.Axis.set_ylim(top=8e-15)
        #Set titles and legend
        #PlotTitle = ''
        #dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle, loc='upper right', ncols_leg=2)

        dz.display_fig()
        # plt.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/{}_label_plot.png'.format(objName), dpi=150, bbox_inches='tight')


        # >> > import numpy as np
        # >> > from matplotlib import pyplot as plt
        # >> > import lineid_plot
        #
        # >> > wave = 1240 + np.arange(300) * 0.1
        # >> > flux = np.random.normal(size=300)
        #
        # >> > line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
        # >> > line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
        #
        # >> > lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1)
        # >> > plt.show()




        #dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Stasinska conference/' + objName + '_TwOarms')
        
#-----------------------------------------------------------------------------------------------------
print 'All data treated', dz.display_errors()
