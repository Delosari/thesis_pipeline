#!/usr/bin/env python
import lineid_plot
from collections import OrderedDict
from dazer_methods import Dazer
from matplotlib import rcParams, pyplot as plt
from matplotlib._png        import read_png
from matplotlib.offsetbox   import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data

#Declare code classes
dz = Dazer()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
cHbeta_type             = 'cHbeta_reduc'
nebular_exten           = '_NebularContinuum.fits'
Stellar_ext             = '_StellarContinuum.fits'
emitting_ext            = '_Emission.fits'

#Treatment add quick index
dz.quick_indexing(catalogue_df)

#Define plot frame and colors
size_dict = {'figure.figsize':(12,5),'axes.labelsize':16, 'legend.fontsize':16, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':16, 'ytick.labelsize':16}
# dz.FigConf(plotSize = size_dict)

#Reddening properties
R_v = 3.4
red_curve = 'G03_average'
cHbeta_type = 'cHbeta_reduc'

obj_lines = {}
obj_lines['8']          = OrderedDict()
obj_lines['SHOC579']    = OrderedDict()
obj_lines['8'][r'$H\gamma$']                  = 4340.471
obj_lines['8'][r'$[OIII]5007\AA$']            = 5007.21

#obj_lines['8'][r'$[NII]6548\AA$']             = 6548
obj_lines['8'][r'$H\alpha$']                  = 6563
obj_lines['8'][r'$[SIII]9531\AA$']            = 9531
obj_lines['SHOC579']['Balmer jump']           = 3646.0
obj_lines['SHOC579'][r'$[OII]3726\AA$']       = 3726.0
obj_lines['SHOC579'][r'$[OII]3729\AA$']       = 3728.0
obj_lines['SHOC579'][r'$H\delta$']            = 4101.68
obj_lines['SHOC579'][r'$HeI4026\AA$']         = 4026.68
obj_lines['SHOC579'].update(obj_lines['8'])

ak = lineid_plot.initial_annotate_kwargs()
# ak['arrowprops']['arrowstyle'] = "->"
ak['arrowprops']['relpos'] = (0.5, 0.0)
ak['rotation'] = 90

pk = lineid_plot.initial_plot_kwargs()
pk['linewidth'] = 0.5

factor_norm = 1e-15

rcParams.update(size_dict)
fig = plt.figure()

format_plot = {'8' : {}, 'SHOC579' : {}}
format_plot['8']['xlims']           = {'left': 4300, 'right': 9800}
format_plot['SHOC579']['xlims']     = {'left': 3500, 'right': 9800}
format_plot['8']['ylims']           = {'bottom': -2e-16/factor_norm, 'top': 3.5e-15/factor_norm}
format_plot['SHOC579']['ylims']     = {'bottom': -2e-16/factor_norm, 'top': 3e-15/factor_norm}

format_plot['8']['OffsetImage']         = {'zoom':0.25}
format_plot['SHOC579']['OffsetImage']   = {'zoom':0.25}
format_plot['8']['AnnotationBbox']       = {'xy':(8635.0, 2.65), 'xybox':(0., 0.), 'xycoords':'data', 'boxcoords':"offset points", "pad":0.1}
format_plot['SHOC579']['AnnotationBbox'] = {'xy':(8625.0, 2.27),'xybox':(0., 0.), 'xycoords':'data', 'boxcoords':"offset points", "pad":0.1}

global_offset = {'zoom':0.15}
annotationBbox = {'xy':(0.65, 0.65),'xybox':(0., 0.), 'xycoords':'axes fraction', 'boxcoords':"offset points", "pad":0.1}

for objName in catalogue_df.loc[dz.idx_include].index:

    if objName == '8':

        local_refenrence = objName.replace('_','-')

        quick_reference = catalogue_df.loc[objName].quick_index

        print local_refenrence, '->', quick_reference

        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
        fits_file           = catalogue_df.loc[objName].reduction_fits

        blue_fits           = catalogue_df.loc[objName].Blue_file
        red_fits            = catalogue_df.loc[objName].Red_file
        fits_file           = catalogue_df.loc[objName].reduction_fits

        Wave_O, Int_O, ExtraData_T = dz.get_spectra_data(fits_file)

        Wave_B, Int_B, ExtraData_B = dz.get_spectra_data(blue_fits)
        Wave_R, Int_R, ExtraData_R = dz.get_spectra_data(red_fits)

        labels_format = 'SHOC579' if Wave_O[0] < 4000 else '8'

        line_wave       = obj_lines[labels_format].values()
        line_label1     = obj_lines[labels_format].keys()

        plt.plot(Wave_O, Int_O/factor_norm)
        ax = plt.gca()

        if quick_reference == 'FTDTR-10':
        #     ax.set_ylim(**format_plot[objName]['ylims'])
            ax.set_ylim(bottom=-1,top=150)
            ax.set_xlim(left=4220, right=9700)

        lineid_plot.plot_line_ids(Wave_O, Int_O/factor_norm, line_wave, line_label1,label1_size=7.5, ax = ax, annotate_kwargs=ak, plot_kwargs=pk)

        # Annotate the 2nd position with another image (a Grace Hopper portrait)
        fn = get_sample_data('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/8_SDSS_invert.png', asfileobj=False)
        arr_img = plt.imread(fn, format='png')
        imagebox = OffsetImage(arr_img, **global_offset)
        imagebox.image.axes = ax
        ab = AnnotationBbox(imagebox, **annotationBbox)
        ax.add_artist(ab)

        ax.update({'xlabel':r'Wavelength $(\AA)$', 'ylabel':'Flux ' + r'$(10^{-15} erg\,cm^{-2} s^{-1} \AA^{-1})$'})
        saving_location = '/home/vital/Dropbox/Astrophysics/Thesis/images/exampleHIIgalaxy.png'

        # plt.show()
        plt.savefig(saving_location, dpi=150, bbox_inches='tight')
#         plt.cla()
#
# #-----------------------------------------------------------------------------------------------------
# print 'All data treated', dz.display_errors()



# # Loop through files
# for i in range(len(catalogue_df.index)):
#
#     print '-- Treating {}'.format(catalogue_df.iloc[i].name)
#
#     if catalogue_df.iloc[i].name not in ['IZW18_A2', 'AGC198691', '6', '70', '4_n2', '3', '27', '71', '0564',
#                                          'SHOC575_n1', 'SHOC593', 'J2225']:
#         # Locate the objects
#         codeName = catalogue_df.iloc[i].quick_index
#         objName = catalogue_df.iloc[i].name
#
#         ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
#         fits_file = catalogue_df.iloc[i].reduction_fits
#
#         blue_fits = catalogue_df.iloc[i].Blue_file
#         red_fits = catalogue_df.iloc[i].Red_file
#         fits_file = catalogue_df.iloc[i].reduction_fits
#
#         Wave_O, Int_O, ExtraData_T = dz.get_spectra_data(fits_file)
#
#         Wave_B, Int_B, ExtraData_B = dz.get_spectra_data(blue_fits)
#         Wave_R, Int_R, ExtraData_R = dz.get_spectra_data(red_fits)
#
#         labels_format = 'SHOC579' if Wave_O[0] < 4000 else '8'
#
#         line_wave = obj_lines[labels_format].values()
#         line_label1 = obj_lines[labels_format].keys()
#
#         plt.plot(Wave_O, Int_O / factor_norm)
#         ax = plt.gca()
#         # ax.set_ylim(**format_plot[objName]['ylims'])
#         # ax.set_xlim(**format_plot[objName]['xlims'])
#
#         lineid_plot.plot_line_ids(Wave_O, Int_O / factor_norm, line_wave, line_label1, ax=ax, annotate_kwargs=ak,
#                                   plot_kwargs=pk)
#
#         # Annotate the 2nd position with another image (a Grace Hopper portrait)
#         fn = get_sample_data(
#             '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/extra_files/{}.png'.format(codeName),
#             asfileobj=False)
#         arr_img = plt.imread(fn, format='png')
#         imagebox = OffsetImage(arr_img, **global_offset)
#         imagebox.image.axes = ax
#         ab = AnnotationBbox(imagebox, **annotationBbox)
#         ax.add_artist(ab)
#
#         print codeName, '{}_label_plot.png'.format(codeName)
#
#         ax.update({'xlabel': r'Wavelength $(\AA)$', 'ylabel': 'Flux ' + r'$(10^{-15} erg\,cm^{-2} s^{-1} \AA^{-1})$'})
#
#         plt.savefig(
#             '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/online_material/{}_label_plot.png'.format(
#                 codeName), dpi=150, bbox_inches='tight')
#         plt.cla()
#
# # -----------------------------------------------------------------------------------------------------
# print 'All data treated', dz.display_errors()