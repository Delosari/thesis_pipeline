import corner
import matplotlib.pyplot                as plt
from uncertainties                      import ufloat
from CodeTools.PlottingManager          import myPickle
from ManageFlow                         import DataToTreat
from Plotting_Libraries.bayesian_data   import bayes_plotter
from Astro_Libraries.Abundances_Class   import Chemical_Analysis
from uncertainties.umath                import log10 as uma_log10, pow as uma_pow
from numpy                              import array, mean, median, percentile, std

def Store_inferencedata(FileFolder, CodeName):
    
    Storing_Dict = {}
    
    Storing_Dict['ChiSq_inf']       = bp.statistics_dict['ChiSq']['mean']
    
    Storing_Dict['y_plus_inf']      = bp.statistics_dict['He_abud']['mean']
    Storing_Dict['y_plus_SD']       = bp.statistics_dict['He_abud']['standard deviation']
    Storing_Dict['y_plus_lowHPD']   = bp.statistics_dict['He_abud']['95% HPD interval'][0]
    Storing_Dict['y_plus_highHPD']  = bp.statistics_dict['He_abud']['95% HPD interval'][1]
    Storing_Dict['y_plus_16th_p']   = bp.statistics_dict['He_abud']['16th_p']
    Storing_Dict['y_plus_84th_p']   = bp.statistics_dict['He_abud']['84th_p']

    Storing_Dict['Te_inf']          = bp.statistics_dict['T_e']['mean']
    Storing_Dict['Te_SD']           = bp.statistics_dict['T_e']['standard deviation']
    Storing_Dict['Te_lowHPD']       = bp.statistics_dict['T_e']['95% HPD interval'][0]
    Storing_Dict['Te_highHPD']      = bp.statistics_dict['T_e']['95% HPD interval'][1]
    Storing_Dict['Te_16th_p']       = bp.statistics_dict['T_e']['16th_p']
    Storing_Dict['Te_84th_p']       = bp.statistics_dict['T_e']['84th_p']
    
    Storing_Dict['ne_inf']          = bp.statistics_dict['n_e']['mean']
    Storing_Dict['ne_SD']           = bp.statistics_dict['n_e']['standard deviation']
    Storing_Dict['ne_lowHPD']       = bp.statistics_dict['n_e']['95% HPD interval'][0]
    Storing_Dict['ne_highHPD']      = bp.statistics_dict['n_e']['95% HPD interval'][1]
    Storing_Dict['ne_16th_p']       = bp.statistics_dict['n_e']['16th_p']
    Storing_Dict['ne_84th_p']       = bp.statistics_dict['n_e']['84th_p']
   
    Storing_Dict['cHbeta_inf']      = bp.statistics_dict['c_Hbeta']['mean']
    Storing_Dict['cHbeta_SD']       = bp.statistics_dict['c_Hbeta']['standard deviation']
    Storing_Dict['cHbeta_lowHPD']   = bp.statistics_dict['c_Hbeta']['95% HPD interval'][0]
    Storing_Dict['cHbeta_highHPD']  = bp.statistics_dict['c_Hbeta']['95% HPD interval'][1]
    Storing_Dict['cHbeta_16th_p']   = bp.statistics_dict['c_Hbeta']['16th_p']
    Storing_Dict['cHbeta_84th_p']   = bp.statistics_dict['c_Hbeta']['84th_p']
        
    Storing_Dict['ftau_inf']        = bp.statistics_dict['Tau']['mean']
    Storing_Dict['ftau_SD']         = bp.statistics_dict['Tau']['standard deviation']
    Storing_Dict['ftau_lowHPD']     = bp.statistics_dict['Tau']['95% HPD interval'][0]
    Storing_Dict['ftau_highHPD']    = bp.statistics_dict['Tau']['95% HPD interval'][1] 
    Storing_Dict['ftau_16th_p']     = bp.statistics_dict['Tau']['16th_p']
    Storing_Dict['ftau_84th_p']     = bp.statistics_dict['Tau']['84th_p'] 
    
    Storing_Dict['Xi_inf']          = bp.statistics_dict['Xi']['mean']
    Storing_Dict['Xi_SD']           = bp.statistics_dict['Xi']['standard deviation']
    Storing_Dict['Xi_lowHPD']       = bp.statistics_dict['Xi']['95% HPD interval'][0]
    Storing_Dict['Xi_highHPD']      = bp.statistics_dict['Xi']['95% HPD interval'][1]     
    Storing_Dict['Xi_16th_p']       = bp.statistics_dict['Xi']['16th_p']
    Storing_Dict['Xi_84th_p']       = bp.statistics_dict['Xi']['84th_p']
            
    for entry in Storing_Dict:
        pv.SaveParameter_ObjLog(CodeName,   FileFolder,   Parameter = entry, Magnitude = Storing_Dict[entry], Error = '-')       

    return

#Import classes

def Compute_HeliumAbundance(FileFolder, CodeName):

    OI_HI       = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter='OI_HI_pn', Assumption='float')
    SI_HI       = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter='SI_HI_ArCorr_pn', Assumption='float')
    HeIII_HII   = pv.GetParameter_ObjLog(CodeName, FileFolder, Parameter='HeIII_HII_pn', Assumption='float')

    if OI_HI != None:
        HeII_HII_Inference = ufloat(bp.statistics_dict['He_abud']['mean'], bp.statistics_dict['He_abud']['standard deviation'])
        
        #Add the HeIII component if observed
        if HeIII_HII != None:
            HeI_HI = HeII_HII_Inference + HeIII_HII
        else:
            HeI_HI = HeII_HII_Inference
        
        Y_mass_InferenceO = (4 * HeI_HI * (1 - 20 * OI_HI)) / (1 + 4 * HeI_HI)
    
    else:
        Y_mass_InferenceO = None
      
    if SI_HI != None:
        HeII_HII_Inference = ufloat(bp.statistics_dict['He_abud']['mean'], bp.statistics_dict['He_abud']['standard deviation'])
        
        #Add the HeIII component if observed
        if HeIII_HII != None:
            HeI_HI = HeII_HII_Inference + HeIII_HII
        else:
            HeI_HI = HeII_HII_Inference
            
        Y_mass_InferenceS = (4 * HeI_HI * (1 - 20 * ch_an.OI_SI * SI_HI)) / (1 + 4 * HeI_HI)
    
    else:
        Y_mass_InferenceS = None    
        
    return Y_mass_InferenceO, Y_mass_InferenceS

pv                      = myPickle()
bp                      = bayes_plotter()
ch_an                   = Chemical_Analysis()

#Define data type and location
Catalogue_Dic           = DataToTreat()
Pattern                 = Catalogue_Dic['Datatype'] + '.fits'

#Databases format
AbundancesFileExtension = '_WHT_LinesLog_v3.txt'
database_extension      = '_extandar_30000_5000_10_Revision3'
globalfile_extension    = '_global_30000_5000_10_Revision3.csv'

#Variables to plot
Traces_code             = ['He_abud', 'T_e', 'n_e', 'c_Hbeta', 'Tau', 'Xi', 'ChiSq'] #['He_abud', 'T_e', 'n_e', 'abs_H', 'abs_He', 'c_Hbeta', 'Tau', 'Xi', 'ChiSq']
Traces_labels           = [r'$y^{+}$', r'$T_{e}$',  r'$n_{e}$', r'$c(H\beta)$', r'$\tau$', r'$\xi$', r'$\chi^{2}$'] #[r'$y^{+}$', r'$T_{e}$',  r'$n_{e}$', r'$a_{H}$', r'$a_{He}$' r'$c(H\beta)$',  r'$\tau$', r'$\xi$', r'$\chi^{2}$']

#Locate files on hard drive
FilesList               = pv.Folder_Explorer(globalfile_extension, Catalogue_Dic['Obj_Folder'], CheckComputer=False)

#Define plot frame and colors
pv.FigFormat_One(ColorConf = 'Day1')

#Loop through files
for i in range(len(FilesList)):

#     try:

    #Analyze file address
    CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
    db_Address                      = FileFolder + 'J0_' +  CodeName + database_extension
    
    #Make sure the object logs ready
    pv.SetLogFile(CodeName + pv.ObjectLog_extension, FileFolder)        
    
    #Load database
    bp.load_pymc_database(db_Address)       
    
    #Extract variable stats
    bp.extract_traces_statistics(Traces_code)
    
    #Store Inference parameters predictions
    Store_inferencedata(FileFolder, CodeName)
     
    #Calculate the total Helium abundance from the regression data
    Y_mass_InferenceO, Y_mass_InferenceS = Compute_HeliumAbundance(FileFolder, CodeName)
  
    #Store the Y mass fractions
    pv.SaveParameter_ObjLog(CodeName, FileFolder,   Parameter = 'Y_Inference_O_pn',    Magnitude=Y_mass_InferenceO)       
    pv.SaveParameter_ObjLog(CodeName, FileFolder,   Parameter = 'Y_Inference_S_pn',    Magnitude=Y_mass_InferenceS)
    
         
#         bp.plot_tracers(Traces_code, Traces_labels)
#         pv.SaveManager(pv.ScriptCode + '_' + CodeName + '_TracesEvolution', FileFolder, ForceSave=True, ForceDisplay=False, savevectorfile=False)
#         pv.ResetPlot()
#      
#         bp.plot_posteriors_histagram(Traces_code, Traces_labels)        
#         pv.SaveManager(pv.ScriptCode + '_' + CodeName + '_PosteriorHistograms', FileFolder, ForceSave=True, ForceDisplay=False, savevectorfile=False)
#         pv.ResetPlot()
#             
#         bp.plot_acorrelation(Traces_code, Traces_labels)
#         pv.SaveManager(pv.ScriptCode + '_' + CodeName + '_TracesAcorr', FileFolder, ForceSave=True, ForceDisplay=False, savevectorfile=False)
#         pv.ResetPlot()
#      
#         bp.plot_triangle_histContours(['He_abud', 'T_e', 'n_e', 'c_Hbeta', 'Tau', 'Xi'], [r'$y^{+}$', r'$T_{e}\,(K)$',  r'$n_{e}\,(cm^{-3})$', r'$c(H\beta)$', r'$\tau$', r'$\xi$'])
#         bp.savefig(FileFolder + pv.ScriptCode + '_' + CodeName + '_triangleContourAll', reset_fig=True)
#         pv.ResetPlot()
#       
#         bp.plot_triangle_histContours(['He_abud', 'T_e', 'n_e'], [r'$y^{+}$', r'$T_{e}\,(K)$',  r'$n_{e}\,(cm^{-3})$'])
#         bp.savefig(FileFolder + pv.ScriptCode + '_' + CodeName + '_triangleContourTene', reset_fig=True)
#         pv.ResetPlot()

#     except:
#         pv.log_error(CodeName) 

print 'Data treated'
        
