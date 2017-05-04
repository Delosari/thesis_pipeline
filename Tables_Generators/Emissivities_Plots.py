from CodeTools.PlottingManager              import myPickle
from Plotting_Libraries.dazer_plotter       import Plot_Conf
from numpy                                  import linspace
import seaborn as sns
import pyneb as pn

#Declare Classes
pv      = myPickle()
dz      = Plot_Conf() 

#Define figure format
dz.FigConf()

# Atom creation and definition of physical conditions
H1      = pn.RecAtom('H',1)
HeI     = pn.RecAtom('He', 1)

#Define physical conditions
tem = 10000
tem_range = linspace(10000, 25000, 100)
 
den = 0
den_range = linspace(0, 300, 200)

# Comment the second if you want all the lines to be plotted
HeI_Lines=[3889.0, 4026.0, 4471.0, 5876.0, 6678.0, 7065.0, 10830.0]


print 'Emissivity', HeI.getEmissivity(tem, 1, wave=3889.0)

#--------------------------Density case----------------------------------
#Plot the lines
for line in HeI_Lines:
    y_1000_100     = HeI.getEmissivity(tem, den_range, wave=line)
    y              = HeI.getEmissivity(tem, den, wave=line)
    dz.data_plot(den_range, y_1000_100/y, label=str(line) + r' $\AA$ line')4
       
# dz.Axis.set_xscale('log')
dz.Axis.tick_params(axis='both', labelsize=20.0)
dz.Axis.set_ylim(0.0,2.5)
# dz.Axis.patch.set_facecolor('white')
# dz.Fig.set_facecolor('black')
# dz.Fig.set_edgecolor('black')
   
#Plot wording
xtitle  = r'$n_{e}$ $(cm^{-3})$'
# ytitle  = r'j(T) [erg cm$^{-3}$ s${-1}$]'
ytitle  = 'Relative emissivity'
title   = 'HeI emissivities @ $T_e$={:.0f}'.format(tem)
dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)
   
#Display figure
dz.display_fig()
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/GTC_conference_2015/Emissivity_den', extension = '.png', reset_fig=True)

#--------------------------Temperature case----------------------------------
# #Plot the lines
# for line in HeI_Lines:
#     y           = HeI.getEmissivity(tem_range, den, wave=line)
#     y_1000_100  = HeI.getEmissivity(tem, den, wave=line)
#     dz.data_plot(tem_range, y_1000_100/y, label=str(line) + r' $\AA$ line')
#      
# # dz.Axis.set_xscale('log')
# dz.Axis.tick_params(axis='both', labelsize=20.0)
# # dz.Axis.set_ylim(0.0,2.5)
# # dz.Axis.patch.set_facecolor('white')
# # dz.Fig.set_facecolor('black')
# # dz.Fig.set_edgecolor('black')
#  
# #Plot wording
# xtitle  = r'$T_{e}$ $(K)$'
# # ytitle  = r'j(T) [erg cm$^{-3}$ s${-1}$]'
# ytitle  = 'Relative emissivity'
# title   = 'HeI emissivities @ $n_e$={:.0f}'.format(den)
# dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)
#  
# #Display figure
# dz.display_fig()
# # dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/GTC_conference_2015/Emissivity_tem', extension = '.png', reset_fig=True)

print 'Data treated'
