#!/usr/bin/env python
import matplotlib.pyplot as plt
import CodeTools.MethodsPyplot as mp
import CodeTools.vitools as vit
import AstroTools.AstroMethods as astro
from scipy.odr import *
import numpy as np
from AstroTools.AstroMethods import linfit
import matplotlib.ticker as mtq
import Tutorials.RegresionNemmen as RN
from collections import OrderedDict

def Linear_Func(p, x):
    m, c = p
    return m*x + c

RootFolder  = "/Users/INAOE_Vital/Dropbox/Astrophysics/Data/WHT_HII_Galaxies/"
Pattern = "_log.txt"
SavingFolder = '/Users/INAOE_Vital/Dropbox/Astrophysics/Thesis/LinearRegressions/WHT_DATA/'
# Pattern =                 'obj08_Blue_t_z_EBV.fits'
PlotVector = None

#Find and organize files from terminal command or .py file
FilesList, PlotVector = mp.FindAndOrganize(PlotVector, Pattern, RootFolder)

#Generate plot frame and colors
Fig1, Axis1, Colors, PlotVector = mp.PlotFormat(PlotVector, 'Day_Elemental')

TrendX = np.array([0,1])

Regresions= 3
ListofElements = []
ListofElements.append((r'$Y_{P\,(\frac{O}{H})}$ =',      "OI_HI",       r'$O/H\,[10^{5}]$',      "$O/H$ $Linear$ $regression$",         1e-5))
ListofElements.append((r'$Y_{P\,(\frac{N}{H})}$ =',      "NI_HI",       r'$N/H\,[10^{5}]$',      "$N/H$ $Linear$ $regression$",          1e-5))
ListofElements.append((r'$Y_{P\,(\frac{S}{H})}$ =',      "SI_HI",       r'$S/H\,[10^{5}]$',      "$S/H$ $Linear$ $regression$",        1e-5))

ElementsResults = []

Max_X = 0

#Loop through Regressions
for i in range(len(ListofElements)):
    #Store plot properties and command flags
    PlotVector = mp.PlotBackUp(PlotVector, 'Clean', None)                                   #Clean the non-constant part
    
    Object_Vector   = []
    Metal_Abund     = []
    Metal_Error     = []
    Y_Mass          = []
    Y_Mass_Error    = []
    Metal_Error_10  = []
    Y_Mass_Error_10  = []
    
    print 'Treating element ', ListofElements[i][2]
    for j in range(len(FilesList)):
        CodeName, FileName, FileFolder, PlotVector = mp.FileAnalyzer(FilesList[j][0], PlotVector)
        if (CodeName != '11') and (CodeName != '04v1'):
#             print '---', CodeName
            Valid_Objects = []
    
            Element = astro.Log_2_Parameter(FileFolder, CodeName, ListofElements[i][1])
            He =        astro.Log_2_Parameter(FileFolder, CodeName, "Y_Mass")
                        
            if (Element != 'None') and (Element != '-') and (He != 'None') and (He != '-'):
                Object_Vector.append(CodeName)        
                Metal_Abund.append(float(Element[0:Element.find('+/-')]))
                Metal_Error_10.append(float(Element[0:Element.find('+/-')])*0.1)
                Metal_Error.append(float(Element[Element.find('+/-') + 3:len(Element)]))                
                Y_Mass.append(float(He[0:He.find('+/-')]))
                Y_Mass_Error.append(float(He[He.find('+/-') + 3:len(He)]))
                Y_Mass_Error_10.append(float(He[0:He.find('+/-')])*0.1)
    
    Metal_Abund     = np.array(Metal_Abund)
    Metal_Error     = np.array(Metal_Error)
    Y_Mass          = np.array(Y_Mass)
    Y_Mass_Error    = np.array(Y_Mass_Error)  
    
    if np.max(Metal_Abund) > Max_X:
        Max_X = np.max(Metal_Abund)
        
    ElementsResults.append([Metal_Abund,Metal_Error,Y_Mass,Y_Mass_Error])
    
TrendX = np.array([0,Max_X*1.10])



# AxHor1 = Axis1.twiny()
# AxHor2 = AxHor1.twiny()

AxHor2 = Axis1.twiny()
Fig1.subplots_adjust(bottom=0.20)

# Axis1.set_xlabel("Oxygen")
# xAxHor2.set_xlabel("Sulphur")
# AxHor0.legend()

# AxHor1.set_frame_on(True)
# AxHor1.patch.set_visible(False)
# AxHor1.xaxis.set_ticks_position('bottom')
# AxHor1.xaxis.set_label_position('bottom')
# AxHor1.spines['bottom'].set_position(('outward', 45))

AxHor2.set_frame_on(True)
AxHor2.patch.set_visible(False)
AxHor2.xaxis.set_ticks_position('bottom')
AxHor2.xaxis.set_label_position('bottom')
AxHor2.spines['bottom'].set_position(('outward', 45))

OxygenLine = Axis1.errorbar(ElementsResults[0][0], ElementsResults[0][2], xerr=ElementsResults[0][1], yerr=ElementsResults[0][3], linestyle='None', marker='x', color = Colors[2][0+1])
# NitrogenLine = AxHor1.errorbar(ElementsResults[1][0], ElementsResults[1][2], xerr=ElementsResults[1][1], yerr=ElementsResults[1][3], linestyle='None', marker='x', color = Colors[2][0+2])
SulphurLine = AxHor2.errorbar(ElementsResults[2][0], ElementsResults[2][2], xerr=ElementsResults[2][1], yerr=ElementsResults[2][3], linestyle='None', marker='x', color = Colors[2][0+3])

# Oxygen
O_Regression_Fit, O_Uncertainty_Matrix, Red_Chi_Sq, Residuals = linfit(np.array(ElementsResults[0][0]), np.array(ElementsResults[0][2]), np.array(ElementsResults[0][3]), cov=True, relsigma=False, chisq=True, residuals=True)
O_m_n_error = [np.sqrt(O_Uncertainty_Matrix[t,t]) for t in range(2)] 
O_n, O_n_error = O_Regression_Fit[1], O_m_n_error[1]

# Nitrogen
N_Regression_Fit, N_Uncertainty_Matrix, Red_Chi_Sq, Residuals = linfit(np.array(ElementsResults[1][0]), np.array(ElementsResults[1][2]), np.array(ElementsResults[1][3]), cov=True, relsigma=False, chisq=True, residuals=True)
N_m_n_error = [np.sqrt(N_Uncertainty_Matrix[t,t]) for t in range(2)] 
N_n, N_n_error = N_Regression_Fit[1], N_m_n_error[1]

# Sulphur
S_Regression_Fit, S_Uncertainty_Matrix, Red_Chi_Sq, Residuals = linfit(np.array(ElementsResults[2][0]), np.array(ElementsResults[2][2]), np.array(ElementsResults[2][3]), cov=True, relsigma=False, chisq=True, residuals=True)
S_m_n_error = [np.sqrt(S_Uncertainty_Matrix[t,t]) for t in range(2)] 
S_n, S_n_error = S_Regression_Fit[1], S_m_n_error[1]

Axis1.set_ylim(0.10, 0.50)
Axis1.set_xlim(0, np.max(ElementsResults[0][0])*1.10)
# AxHor1.set_xlim(0, np.max(ElementsResults[1][0])*1.10)
AxHor2.set_xlim(0, np.max(ElementsResults[2][0])*1.10)

TrendLine0 =  Axis1.plot(TrendX, O_Regression_Fit[0]*TrendX+O_n, '--', color="green", label='Oxygen regression')
# TrendLine1 =  AxHor1.plot(TrendX, N_Regression_Fit[0]*TrendX+N_n, '--', color="blue", label='Nitrogen regression')
TrendLine2 =  AxHor2.plot(TrendX, S_Regression_Fit[0]*TrendX+S_n, '--', color="orange", label='Sulphur regression')

# Axis1.set_xlabel(r'$O/H\,[10^{5}]$', fontsize=15, color= "green", y=0.50)
# AxHor1.set_xlabel(r'$N/H\,[10^{5}]$', fontsize=15, color= "blue", y = 0.95)
# AxHor2.set_xlabel(r'$S/H\,[10^{5}]$', fontsize=15, color= "orange")

Axis1.set_xlabel(r'$O/H$', fontsize=15, color= "green", y=0.50)
# AxHor1.set_xlabel(r'$N/H$', fontsize=15, color= "blue", y = 0.95)
AxHor2.set_xlabel(r'$S/H$', fontsize=15, color= "orange")

# lns = TrendLine0 + TrendLine1 + TrendLine2
lns = TrendLine0 + TrendLine2



labs = [l.get_label() for l in lns]
Axis1.legend(lns,labs,loc=1)

# print handles[0], type(handles)
# print by_label, type(by_label)

# legend = Axis1.legend(loc=1, prop={'size':20}, scatterpoints=1) 
# Axis.set_xlabel(Plot_xlabel,fontsize=20, color= Colors[1])
Axis1.set_ylabel(r'$Y_{P}$',fontsize=20, color= Colors[1])
Axis1.set_title('Primordial Helium Linear Regression', fontsize=25, color= Colors[1], y = 1.02)    
 
mp.PlotSaveManager(PlotVector,Colors,SavingName ='Combined_Regression.pdf', SavingFolder = SavingFolder)   #Save PlotVector

# 
# for i in range(len(ListofElements)):
#     
#     Metal_Abund     = np.array(Metal_Abund)
#     Metal_Error     = np.array(Metal_Error)
#     Y_Mass          = np.array(Y_Mass)
#     Y_Mass_Error    = np.array(Y_Mass_Error)  
#     
#     plt.errorbar(Metal_Abund, Y_Mass, xerr=Metal_Error, yerr=Y_Mass_Error, linestyle='None', marker='x', color = Colors[2][i+1])
#         
#     #   New method
#     Regression_Fit, Uncertainty_Matrix, Red_Chi_Sq, Residuals = linfit(np.array(Metal_Abund), np.array(Y_Mass), np.array(Y_Mass_Error), cov=True, relsigma=False, chisq=True, residuals=True)
#     m_n_error = [np.sqrt(Uncertainty_Matrix[t,t]) for t in range(2)] 
#     n, n_error = Regression_Fit[1], m_n_error[1]
#     
#     print Regression_Fit
#     print 'm', Regression_Fit[0]
#     print 'n', Regression_Fit[1]
#     TrendLine2 = Axis1.plot(TrendX, Regression_Fit[0]*TrendX + Regression_Fit[1], color=Colors[2][i+1], label=ListofElements[i][3], linestyle='--')
#     
#     for k in range(len(Object_Vector)):
#         Label_point = Object_Vector[k]
#         Axis1.annotate(Label_point, xy=(Metal_Abund[k],Y_Mass[k]), xytext = (Metal_Abund[k],Y_Mass[k]+0.01), textcoords= 'data',fontsize=8, color = Colors[1])
#         ''
#     # Plot Format
#     Title = '%s $%0.4f$ $\pm$ $%0.4f$' % (ListofElements[i][0], Regression_Fit[1], m_n_error[1])
#     
#     PlotVector = mp.TextFormat(Axis1, PlotVector, Colors, 1, Plot_Title=Title, Plot_xlabel=ListofElements[i][2], Plot_ylabel=r'$Y$')
#     
#     # Plot Format
#     
#     mp.PlotSaveManager(PlotVector,Colors,SavingName = ListofElements[i][1]+'_Regression.pdf', SavingFolder = SavingFolder)   #Save PlotVector
