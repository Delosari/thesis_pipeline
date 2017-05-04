'''
Created on Feb 4, 2016

@author: vital
'''
import pyneb                    as pn
from numpy                      import insert, savetxt, c_
from CodeTools.PlottingManager  import myPickle
from ManageFlow                 import DataToTreat
from matplotlib                 import rc, pyplot as plt

#Try to adjust all the plot wording in one go
font = {'family' : 'Times New Roman','size' : 30}
rc('font', **font)

def Adjust_Pyneb_DiagsPlot_format(CodeName, Fig1, Axis1):

    Fig1.set_facecolor('white')

    Axis1.spines['bottom'].set_color('black')
    Axis1.spines['top'].set_color('black') 
    Axis1.spines['right'].set_color('black')
    Axis1.spines['left'].set_color('black')
    Axis1.yaxis.label.set_color('black')
    Axis1.xaxis.label.set_color('black')    
    
    Axis1.tick_params(axis='x', length=7,width=2,labelsize = 30,colors='black')
    Axis1.tick_params(axis='y', length=7,width=2,labelsize = 30,colors='black')
        
    Axis1.set_ylabel(r'Temperature, $T_{e}$ $(K)$',fontsize=30)
    Axis1.set_xlabel(r'Density, $log(n_{e})$ $(cm^{-3})$',fontsize=30)
    Axis1.set_title('Diagnostics diagram for HII Galaxy ' + CodeName, fontsize=30,color='Black')
    
    return

#Import classes

pv = myPickle()

pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')

#Define data type and location
Catalogue_Dic                       = DataToTreat()
Pattern                             = '_dered_Neb_Stellar_LinesLog_v3.txt'
Pattern_pyneb_log                   = '_pyneb_fluxes.log'

#Locate files on hard drive
FilesList                           = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
 
#Loop through files only if we are dealing the WHT data and only scientific objects:
for i in range(len(FilesList)):
    
    #Analyze file address
    CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
    
    #Get the corresponding columns for the analysis (al columns are imported as strings
    Labels                      = pv.get_ColumnData(['Line_Label'], FileFolder + FileName, HeaderSize = 2, datatype=str)
    Line_Fluxes, Line_Errors    = pv.get_ColumnData(['FluxGauss','ErrorEL_MCMC'], FileFolder + FileName, HeaderSize = 2, datatype=str)
    
    #Insert pynebs table headers
    Labels      = insert(arr = Labels,       obj = 0, values = 'LINE')
    Line_Fluxes = insert(arr = Line_Fluxes,  obj = 0, values = CodeName)
    Line_Errors = insert(arr = Line_Errors,  obj = 0, values = 'err')
    
    #Save data into an acceptable pynebs lines log format
    PyNeb_Log_Address = FileFolder + CodeName + Pattern_pyneb_log
    savetxt(PyNeb_Log_Address, c_[Labels, Line_Fluxes, Line_Errors], fmt='%20s')
    
    #Declare an observation
    obs = pn.Observation()
    
    #Import the data 
    obs.readData(PyNeb_Log_Address, fileFormat='lines_in_rows_err_cols', corrected = True, errIsRelative=False)
    
    #Unique atoms
    print 'Ions found on HII galaxy', obs.getUniqueAtoms() 
    
    #Initiate the diagnostics 

    #Load all possible diagnostics
    #diags = pn.Diagnostics(addAll=True)
    
    #Load only the diagnostics you want:
    diags = pn.Diagnostics()
    diags.addDiag(['[SII] 6731/6716', '[OII] 3726/3729', '[NII] 5755/6584+', '[SIII] 6312/9200+', '[OIII] 4363/5007+', '[SII] 4072+/6720+'])#     diags.addDiagsFromObs(obs)
    
    #Change default labels  
    diags.addClabel('[SII] 6731/6716',      r'$n_{e}\left[SII\right]\left(\frac{\lambda6731\AA}{\lambda6716\AA}\right)$')
    diags.addClabel('[OII] 3726/3729',      r'$n_{e}\left[OII\right]\left(\frac{\lambda3726\AA}{\lambda3729\AA}\right)$')
    diags.addClabel('[SIII] 6312/9200+',    r'$T_{e}\left[SIII\right]\left(\frac{\lambda9069\AA+\lambda9531\AA}{\lambda6312\AA}\right)$')
    diags.addClabel('[NII] 5755/6584+',     r'$T_{e}\left[NII\right]\left(\frac{\lambda6548\AA+\lambda6584\AA}{\lambda5577\AA}\right)$')
    diags.addClabel('[OIII] 4363/5007+',    r'$T_{e}\left[OIII\right]\left(\frac{\lambda4959\AA+\lambda5007\AA}{\lambda4363\AA}\right)$')
    diags.addClabel('[SII] 4072+/6720+',    r'$T_{e}\left[SII\right]\left(\frac{\lambda4069\AA+\lambda4076\AA}{\lambda6716\AA+\lambda6731\AA}\right)$')
    
    #Generate the observation grid
    emisgrids = pn.getEmisGridDict(atomDict=diags.atomDict)

    #Generate a figure for the plot
    Fig1=plt.figure(figsize=(16,16))
    Fig1.set_dpi(600)
    Axis1 = Fig1.add_subplot(111)
    
    #Load emissivity grid
    diags.plot(emisgrids, obs, i_obs = 0, ax=Axis1)
    
    #Load Change the format of the plot
    Adjust_Pyneb_DiagsPlot_format(CodeName, Fig1, Axis1)
    
    #Save the figure
    plt.savefig(FileFolder + CodeName + '_pyneb_diagnostics.png', bbox_inches='tight', pad_inches=0.1)
    
print 'Data treated'

    
    
