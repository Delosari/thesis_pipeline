'''
Created on Oct 25, 2015

@author: vital
'''
from collections                        import OrderedDict
from CodeTools.PlottingManager          import myPickle
from PipeLineMethods.ManageFlow         import DataToTreat
from Plotting_Libraries.bayesian_data   import bayes_plotter
import matplotlib.pyplot as plt
import pyneb

print '1'
S3 = pyneb.Atom('S',3)
print '2'
# 
# #Import classes
# pv                      = myPickle()
# bp                      = bayes_plotter()
# 
# #Define plot frame and colors
# pv.FigFormat_One(ColorConf = 'Day1')
# 
# #Define data type and location
# Catalogue_Dic           = DataToTreat()
# Pattern                 = Catalogue_Dic['Datatype'] + '.fits'
# 
# #Locate files on hard drive
# FilesList               = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
# 
# #Loop through objects to generate a list of number to which assign the labels
# Objects_Dict            = OrderedDict()
# HeIHI_DirectMethod      = OrderedDict()
# HeIHI_Inference         = OrderedDict() 
# 
# for i in range(len(FilesList)):
#                      
#     CodeName, FileName, FileFolder          = pv.Analyze_Address(FilesList[i])
#     
#     Objects_Dict[CodeName]                  = i
# #     HeIHI_DirectMethod[CodeName]            = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter='HeII_HII',            Assumption='float')
# #     HeIHI_Inference[CodeName]               = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter='y_plus_Inference',    Assumption='float')
#     HeIHI_DirectMethod[CodeName]            = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter='TOIII',            Assumption='float')
#     HeIHI_Inference[CodeName]               = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter='Te_Inference',    Assumption='float')
# #     HeIHI_DirectMethod[CodeName]            = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter='nSII',            Assumption='float')
# #     HeIHI_Inference[CodeName]               = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter='ne_Inference',    Assumption='float')
# 
# #List of objects organized
# HII_Galaxy_List = Objects_Dict.keys()
# HII_Galaxy_List.sort()
# 
# List_HeIHI_DirectMethod = [[], [], []]
# List_HeIHI_Inference    = [[], [], []]
# 
# #Loop through the data and input into the list those which are numerical values
# for j in range(len(HII_Galaxy_List)):
#     Galaxy = HII_Galaxy_List[j]
#     
#     if HeIHI_DirectMethod[Galaxy] != None:
#         print 'direct metiendo', j, HeIHI_DirectMethod[Galaxy]
#         List_HeIHI_DirectMethod[0].append(j)
#         List_HeIHI_DirectMethod[1].append(nominal_values(HeIHI_DirectMethod[Galaxy]))
#         List_HeIHI_DirectMethod[2].append(std_devs(HeIHI_DirectMethod[Galaxy]))
#         
#     if HeIHI_Inference[Galaxy] != None :
#         print 'inference metiendo', j, HeIHI_Inference[Galaxy]
#         List_HeIHI_Inference[0].append(j)
#         List_HeIHI_Inference[1].append(nominal_values(HeIHI_Inference[Galaxy]))
#         List_HeIHI_Inference[2].append(std_devs(HeIHI_Inference[Galaxy]))
# 
# #Plot the data
# pv.DataPloter_One(List_HeIHI_DirectMethod[0],   List_HeIHI_DirectMethod[1],     'Direct method: '   + r'$T_{OIII}$',       pv.Color_Vector[2][1],   ErrorBarsColor=pv.Color_Vector[2][1],   LineStyle=None,  YError=List_HeIHI_DirectMethod[2])
# pv.DataPloter_One(List_HeIHI_Inference[0],      List_HeIHI_Inference[1],        'Inference model: ' + r'$T_{e}$',          pv.Color_Vector[2][2],   ErrorBarsColor=pv.Color_Vector[2][2],   LineStyle=None,  YError=List_HeIHI_Inference[2])
# 
# #Plot the data
# pv.Labels_Legends_One(Plot_Title =  r'Direct and Inference methods comparison: $T_{e}$',  Plot_xlabel = 'HII Galaxies', Plot_ylabel = r'$n_{e}\,(cm^{-3})$', LegendLocation='best')         
# 
# plt.xticks(range(len(HII_Galaxy_List)), HII_Galaxy_List, rotation = 70)
# plt.gca().xaxis.grid(False)
# plt.gcf().subplots_adjust(bottom=0.20)
# 
# #Display figure
# pv.DisplayFigure()
