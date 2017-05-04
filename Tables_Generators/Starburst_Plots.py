from CodeTools.PlottingManager              import myPickle
from Plotting_Libraries.dazer_plotter       import Plot_Conf
from numpy                                  import array, power, savetxt, transpose, unique, where, zeros,ones
from Math_Libraries                         import sigfig
from Scientific_Lib.IrafMethods             import Pyraf_Workflow 
from collections                            import OrderedDict
from os                                     import mkdir

#Declare Classes
pv      = myPickle()
dz      = Plot_Conf() 
py_w    = Pyraf_Workflow('WHT')

# #-----------------------------------------STARBURST EQUIVALENT WIDTH EVOLUTION----------------------------------------
FilesFolder     = '/home/vital/Dropbox/Astrophysics/Data/Starburst_Spectra_z0.004/' 
FilesPattern    = '_txt_LinesLog_v3.txt'
   
#Locate files on hard drive
FilesList       = pv.Folder_Explorer(FilesPattern, FilesFolder, CheckComputer=False)
     
# #Define figure format
dz.FigConf()
   
#Lines to plot
# H_Lines         = ['H1_3970A','H1_4102A','H1_4340A', 'H1_4861A', 'H1_6563A']
H_Lines       = ['He1_3188A','He1_4026A','He1_4471A','He2_4686A','He1_5016A','He1_5876A','He1_6678A']
 
#Define dictionary to store the data
Age_dict = OrderedDict() 
Eqw_dict = OrderedDict() 
   
# .fromkeys(H_Lines, zeros(len(FilesList)))
# .fromkeys(H_Lines, zeros(len(FilesList)))
   
for line in H_Lines:
    Age_dict[line] = zeros(len(FilesList))
    Eqw_dict[line] = zeros(len(FilesList)) 
   
#Loop through files
for i in range(len(FilesList)):
        
    #Analyze file address
    CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
        
    #Age number
    Age = float(CodeName[CodeName.rfind('_')+1:CodeName.find('Myr')])
        
    #loop through the lines in the list
    for j in range(len(H_Lines)):
           
        H_line = H_Lines[j]
           
        Eqw = pv.GetParameter_LineLog(CodeName, FileFolder, H_line, 'Eqw', LinesLog_suffix='_txt_LinesLog_v3.txt')
         
        if Eqw == None:
            Age_dict[H_line][i] = Age
            Eqw_dict[H_line][i] = None
        else:
            Age_dict[H_line][i] = Age
            Eqw_dict[H_line][i] = Eqw * -1
             
#Generate plot
for k in range(len(H_Lines)):
    line    = H_Lines[k]
    label   = line.replace('_',' ')
        
    dz.data_plot(Age_dict[line], Eqw_dict[line], label=label, markerstyle='o')
   
    
#Define figure wording
xtitle  = r'Age $(Myr)$'
ytitle  = r'Ew $(\AA)$'
title   = 'Starburst recombination lines absorption Ew evolution'
dz.FigWording(xtitle, ytitle, title, axis_Size=30, title_Size=30, legend_size=25, legend_loc='best')
dz.Axis.set_xlim(0, 120)

#save_fig
dz.display_fig()
dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/GTC_conference_2015/EWevolutin', extension='.eps')


# #-----------------------------------------STARBURST EQUIVALENT WIDTH Normalized Hydrogen EVOLUTION----------------------------------------
# FilesFolder     = '/home/vital/Dropbox/Astrophysics/Data/Starburst_Spectra_z0.004/' 
# FilesPattern    = '_txt_LinesLog_v3.txt'
#   
# #Locate files on hard drive
# FilesList       = pv.Folder_Explorer(FilesPattern, FilesFolder, CheckComputer=False)
#     
# # #Define figure format
# dz.FigConf()
#   
# #Lines to plot
# H_Lines         = ['H1_6563A', 'H1_3970A','H1_4102A','H1_4340A', 'H1_4861A']
# # H_Lines       = ['He1_3188A','He1_4026A','He2_4686A','He1_5016A','He1_5876A','He1_6678A']
# 
# #Define dictionary to store the data
# Age_dict = OrderedDict() 
# Eqw_dict = OrderedDict() 
#   
# # .fromkeys(H_Lines, zeros(len(FilesList)))
# # .fromkeys(H_Lines, zeros(len(FilesList)))
#   
# for line in H_Lines:
#     Age_dict[line] = zeros(len(FilesList))
#     Eqw_dict[line] = zeros(len(FilesList)) 
#   
# #Loop through files
# for i in range(len(FilesList)):
#        
#     #Analyze file address
#     CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
#        
#     #Age number
#     Age = float(CodeName[CodeName.rfind('_')+1:CodeName.find('Myr')])
#        
#     #loop through the lines in the list
#     for j in range(len(H_Lines)):
#           
#         H_line = H_Lines[j]
#           
#         Eqw = pv.GetParameter_LineLog(CodeName, FileFolder, H_line, 'Eqw', LinesLog_suffix='_txt_LinesLog_v3.txt')
#         
#         if Eqw == None:
#             Age_dict[H_line][i] = Age
#             Eqw_dict[H_line][i] = None
#             
#         else:
#             Age_dict[H_line][i] = Age
#             if H_line == 'H1_6563A':
#                 Eqw_dict[H_line][i] = Eqw * -1
#             else:
#                 print 'y esto', Eqw, Eqw_dict['H1_6563A'][i]
#                 Eqw_dict[H_line][i] = Eqw * -1 / Eqw_dict['H1_6563A'][i]
#                 
#                 
# #Generate plot
# for k in range(len(H_Lines)):
#     line    = H_Lines[k]
#     label   = line.replace('_',' ') + ' evolution'
#       
#     if line == 'H1_6563A':
#         dz.data_plot(Age_dict[line], ones(len(Eqw_dict[line])), label=label, markerstyle='o')
#     else:
#         dz.data_plot(Age_dict[line], Eqw_dict[line], label=label, markerstyle='o')
#   
#    
# #Define figure wording
# xtitle  = r'Age $(Myr)$'
# ytitle  = r'Eqw $(\AA)$'
# title   = 'Starburst recombination lines absorption Eqw evolution'
# dz.FigWording(xtitle, ytitle, title)
#   
# #save_fig
# dz.display_fig()


# #-----------------------------------------STARBURST EQUIVALENT WIDTH NORMALIZED HELIUM EVOLUTION----------------------------------------
# FilesFolder     = '/home/vital/Dropbox/Astrophysics/Data/Starburst_Spectra_z0.004/' 
# FilesPattern    = '_txt_LinesLog_v3.txt'
#   
# #Locate files on hard drive
# FilesList       = pv.Folder_Explorer(FilesPattern, FilesFolder, CheckComputer=False)
#     
# # #Define figure format
# dz.FigConf()
#   
# #Lines to plot
# # H_Lines         = ['H1_6563A', 'H1_3970A','H1_4102A','H1_4340A', 'H1_4861A']
# H_Lines       = ['He1_5876A', 'He1_3188A','He1_4026A','He2_4686A','He1_5016A','He1_6678A']
# 
# #Define dictionary to store the data
# Age_dict = OrderedDict() 
# Eqw_dict = OrderedDict() 
#   
# # .fromkeys(H_Lines, zeros(len(FilesList)))
# # .fromkeys(H_Lines, zeros(len(FilesList)))
#   
# for line in H_Lines:
#     Age_dict[line] = zeros(len(FilesList))
#     Eqw_dict[line] = zeros(len(FilesList)) 
#   
# #Loop through files
# for i in range(len(FilesList)):
#        
#     #Analyze file address
#     CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
#        
#     #Age number
#     Age = float(CodeName[CodeName.rfind('_')+1:CodeName.find('Myr')])
#        
#     #loop through the lines in the list
#     for j in range(len(H_Lines)):
#           
#         H_line = H_Lines[j]
#           
#         Eqw = pv.GetParameter_LineLog(CodeName, FileFolder, H_line, 'Eqw', LinesLog_suffix='_txt_LinesLog_v3.txt')
#         
#         if Eqw == None:
#             Age_dict[H_line][i] = Age
#             Eqw_dict[H_line][i] = None
#             
#         else:
#             Age_dict[H_line][i] = Age
#             if H_line == 'He1_5876A':
#                 Eqw_dict[H_line][i] = Eqw * -1
#             else:
#                 Eqw_dict[H_line][i] = Eqw * -1 / Eqw_dict['He1_5876A'][i]
#                 
#                 
# #Generate plot
# for k in range(len(H_Lines)):
#     line    = H_Lines[k]
#     label   = line.replace('_',' ') + ' evolution'
#       
#     if line == 'He1_5876A':
#         dz.data_plot(Age_dict[line], ones(len(Eqw_dict[line])), label=label, markerstyle='o')
#     else:
#         dz.data_plot(Age_dict[line], Eqw_dict[line], label=label, markerstyle='o')
#   
#    
# #Define figure wording
# xtitle  = r'Age $(Myr)$'
# ytitle  = r'Eqw $(\AA)$'
# title   = 'Starburst recombination lines absorption Eqw evolution'
# dz.FigWording(xtitle, ytitle, title)
#   
# #save_fig
# dz.display_fig()


#-----------------------------------------POPSTAR STELLAR AND NEBULAR SPECTRA----------------------------------------
# #Define operation
# Data_Folder     = '/home/vital/Desktop/spectrapopstar/Kroupa/'
# Saving_folder   = '/home/vital/Dropbox/Astrophysics/Papers/Elemental_RegressionsSulfur/starburst_absorptions/Popstar_Kroupa/'
# Data_Pattern    = 'spneb'
#  
# #Locate files on hard drive
# FilesList       = pv.Folder_Explorer(Data_Pattern, Data_Folder, CheckComputer=False)
#  
# # #Define figure format
# dz.FigConf()
#  
# # FilesList = [Data_Folder+'spneb_cha_0.15_100_z0040_t7.20']
# for i in range(len(FilesList)):
#      
#     #Analyze file address
#     CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
#      
#     #Extract data from text files 
#     Wavelength, Stellar_Flux, Nebular_Flux, total = pv.get_ColumnData([0,1,2,3], FileFolder + FileName, HeaderSize=0, StringIndexes=False, unpack_check=True)
#  
#     color               = next(dz.ColorVector[2])
#     label_stellar       = FileName[FileName.rfind('_t')+2:len(FileName)] + ' Myr: Stellar component'
#     label_nebular       = FileName[FileName.rfind('_t')+2:len(FileName)] + ' Myr: Nebular component'
#     label_total         = FileName[FileName.rfind('_t')+2:len(FileName)] + ' Myr: Total component'
#  
#     dz.data_plot(Wavelength, Stellar_Flux, label=label_stellar, color=color, linestyle='--', linewidth=2.5)
#     dz.data_plot(Wavelength, Nebular_Flux, label=label_nebular, color=color, linestyle=':',  linewidth=2.5)
#     dz.data_plot(Wavelength, total, label=label_total, color=color, linewidth=2.5)
#  
#     #Define figure labels
#     xtitle  = r'Wavelength $\AA$'
#     ytitle  = r'Flux'
#     title   = 'Popstar: Kroupa, Z = 0.004, age ' + FileName[FileName.rfind('_t')+2:len(FileName)]
#     dz.FigWording(xtitle, ytitle, title)    
#      
#     dz.Axis.set_xlim(0,12000)
#     dz.Axis.set_yscale('log')
#      
#     #Display figure
#     #     dz.display_fig()
#     saving_name     = 'Popstar_KroupaPadova_' + FileName[FileName.rfind('_t')+2:len(FileName)] + 'Myr'
#     object_folder   = Saving_folder + saving_name
#     mkdir(object_folder)
#     txt_columns = transpose((Wavelength, total))
#     savetxt(object_folder + '/' + saving_name + '.txt', txt_columns, fmt='%s')
#     
#     dz.savefig(Saving_folder + title)
    


#-----------------------------------------STELLAR HIGH RESOLUTION SPECTRUM----------------------------------------
# FileName        = 'Kroupa-PadovaAGB-0.004-full.hires1'
# FileFolder      = '/home/vital/Desktop/Untitled Folder 2/output29009/'
# FileHeaders     = ['TIME [YR]', 'WAVELENGTH', 'LOG(LUMINOSITY)', 'NORMALIZED SPECTRUM']
# FileHeaderSize  = 6
# Saving_folder   = '/home/vital/Dropbox/Astrophysics/Data/Starburst_Spectra_z0.004/'
#     
# TimeYr_column   = pv.get_ColumnData([0], FileFolder + FileName, FileHeaderSize, StringIndexes=False)
# Wavelen_Column  = pv.get_ColumnData([1], FileFolder + FileName, FileHeaderSize, StringIndexes=False)
# NormEspectrum   = pv.get_ColumnData([2], FileFolder + FileName, FileHeaderSize, StringIndexes=False)
# LogEspectrum    = pv.get_ColumnData([2], FileFolder + FileName, FileHeaderSize, StringIndexes=False)
# Flux_Calibrated = power(10, LogEspectrum)
#     
# Age_set         = unique(TimeYr_column)
# Age_Min         = Age_set[0]
# Age_Max         = Age_set[-1]
#  
# for age in Age_set:
#     print '{:.3f}'.format(age/1e6) + ' yrs'
#  
# # print 'Unique ages', Age_set   
# Ages_indeces = range(25)
#     
# #Define figure format
# dz.FigConf()
#     
# for i in Ages_indeces:
#          
#     Age_index   = where(Age_set[i] == TimeYr_column)[0]
#     label       = 'Age: ' + '{:.3e}'.format(Age_set[i]) + ' yrs'
#   
#     wave        = Wavelen_Column[Age_index]
#     flux        = Flux_Calibrated[Age_index]
#     
#     
#     dz.data_plot(wave, flux, label=label)
#     
#     #Define figure labels
#     xtitle = r'Wavelength $\AA$'
#     ytitle = r'Flux calibrated'
#     title = 'Starburst: Kroupa Padova z = 0.004, Age: ' + sigfig.round_sig(float(Age_set[i])/1e6, 3)+'Myr'
#     dz.FigWording(xtitle, ytitle, title)    
#           
#     # Display figure
#     dz.reset_fig()
#      
#     saving_txt_name = 'HighRes_KroupaPadova_' + sigfig.round_sig(float(Age_set[i])/1e6, 3)+'Myr'
#     object_folder   = Saving_folder + saving_txt_name
# #     dz.savefig(object_folder + '/' + title)
# #     mkdir(object_folder)
#     txt_columns     = transpose((wave, flux))
#     savetxt(object_folder + '/' + saving_txt_name + '.txt', txt_columns, fmt='%s')
    

# #----------------------------------------------STELLAR NEBULAR SPECTRUM---------------------------------------------------
# FileName        = 'Kroupa-PadovaAGB-0.004-full.spectrum1'
# FileFolder      = '/home/vital/Desktop/Untitled Folder 2/output29009/'
# FileHeaders     = [ 'TIME [YR]', 'WAVELENGTH [A]', 'LOG TOTAL', 'LOG STELLAR', 'LOG NEBULAR', '[ERG/SEC/A]']
# FileHeaderSize  = 6
# Saving_folder   = '/home/vital/Dropbox/Astrophysics/Papers/Elemental_RegressionsSulfur/starburst_absorptions/'
#   
# TimeYr_column   = pv.get_ColumnData([0], FileFolder + FileName, FileHeaderSize, StringIndexes=False)
# Wavelen_Column  = pv.get_ColumnData([1], FileFolder + FileName, FileHeaderSize, StringIndexes=False)
# Nebular_Column  = pv.get_ColumnData([4], FileFolder + FileName, FileHeaderSize, StringIndexes=False)
# Stellar_Column  = pv.get_ColumnData([3], FileFolder + FileName, FileHeaderSize, StringIndexes=False)
#  
# Age_set         = unique(TimeYr_column)
# Age_Min         = Age_set[0]
# Age_Max         = Age_set[-1]
# Ages_list       = array([Age_Min, Age_Max])
#   
# # print 'Unique ages', Age_set
#   
# Ages_indeces = [0, 1, 2, 3]
#   
# #Define figure format
# dz.FigConf()
#   
# for i in Ages_indeces:
#       
#     color = next(dz.ColorVector[2])
#       
#     Age_index   = where(Age_set[i] == TimeYr_column)[0]
#     label       = 'Stellar emission Age: ' + '{:.3e}'.format(Age_set[i]) + ' yrs'
#     dz.data_plot(Wavelen_Column[Age_index], Stellar_Column[Age_index], label=label, color=color, linewidth=3)
#     label       = 'Nebular emission Age: ' + '{:.3e}'.format(Age_set[i]) + ' yrs'
#     dz.data_plot(Wavelen_Column[Age_index], Nebular_Column[Age_index], label=label, color=color, linestyle=':', linewidth=3)
#      
#     #Define figure labels
#     xtitle = r'Wavelength $\AA$'
#     ytitle = r'Nebular flux $log(erg\cdots^{-1}\cdot\AA^{-1})$'
#     title = 'Starburst: Kroupa padoba z = 0.004, full spectrum, age: ' + '{:.3e}'.format(Age_set[i]) + ' yrs'
#      
#     # dz.Axis.set_yscale('log')
#     dz.Axis.set_xlim(0,10000)
#     dz.Axis.set_ylim(34,40)
#         
#     dz.FigWording(xtitle, ytitle, title)    
#        
#     #Display figure
#     # dz.display_fig()
#     dz.savefig(Saving_folder + title)
#     saving_name = 'Starburst_kroupa_' + sigfig.round_sig(float(Age_set[i])/1e6, 3)+'Myr'
#     txt_columns = transpose((Wavelen_Column[Age_index], power(10,Stellar_Column[Age_index])))
#     savetxt(Saving_folder + saving_name, txt_columns, fmt='%s')
    
    
    
    
            