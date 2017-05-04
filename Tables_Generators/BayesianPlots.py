import corner
from uncertainties                      import ufloat
from CodeTools.PlottingManager          import myPickle
from ManageFlow                         import DataToTreat
from Plotting_Libraries.bayesian_data   import bayes_plotter
from uncertainties.umath                import log10 as uma_log10, pow as uma_pow
from Astro_Libraries.Abundances_Class   import Chemical_Analysis
from numpy                              import array, mean, median, percentile, std
import matplotlib.pyplot                as plt

pv                      = myPickle()
bp                      = bayes_plotter()
ch_an                   = Chemical_Analysis()

#Define data type and location
Pattern_low_ne          = 'he_Abundance__30000_5000_10_NoNuissanceParameters_8_Model4_continuous'
Pattern_High_ne         = 'he_Abundance__30000_5000_10_NoNuissanceParameters_EqwHbetaPrior5_Model3_VeryGood_4649sec'

Folder                  = '/home/vital/workspace/X_Data/'

#Variables to plot
# Traces_code             = ['He_abud', 'T_e', 'n_e', 'abs_H', 'abs_He', 'c_Hbeta', 'Tau', 'Xi'] #['He_abud', 'T_e', 'n_e', 'c_Hbeta', 'Tau', 'Xi', 'ChiSq'] #['He_abud', 'T_e', 'n_e', 'abs_H', 'abs_He', 'c_Hbeta', 'Tau', 'Xi', 'ChiSq']
# Traces_labels           = [r'$y^{+}$', r'$T_{e}\,(K)$',  r'$n_{e}\,(cm^{-3})$', r'$a_{H}$', r'$a_{He}$', r'$c(H\beta)$',  r'$\tau$', r'$\xi$']#[r'$y^{+}$', r'$T_{e}$',  r'$n_{e}$', r'$c(H\beta)$', r'$\tau$', r'$\xi$', r'$\chi^{2}$'] #[r'$y^{+}$', r'$T_{e}$',  r'$n_{e}$', r'$a_{H}$', r'$a_{He}$' r'$c(H\beta)$',  r'$\tau$', r'$\xi$', r'$\chi^{2}$']
# True_LowDen             = [0.08, 18000.0, 100.0, 1.0, 1.0, 0.1, 0.2, 1.0]
# True_HighDen            = [0.085, 16000.0, 500.0, 1.0, 0.5, 0.1, 1.0, 1.0]

# pattern         = Pattern_High_ne
# true_values     = True_HighDen
# Name            = 'Test_highDensity'
# article_folder  = '/home/vital/Dropbox/Astrophysics/Papers/Elemental_RegressionsSulfur/Images/'

Traces_code             = ['m','n'] #['He_abud', 'T_e', 'n_e', 'c_Hbeta', 'Tau', 'Xi', 'ChiSq'] #['He_abud', 'T_e', 'n_e', 'abs_H', 'abs_He', 'c_Hbeta', 'Tau', 'Xi', 'ChiSq']
Traces_labels           = ['m', 'n']#[r'$y^{+}$', r'$T_{e}$',  r'$n_{e}$', r'$c(H\beta)$', r'$\tau$', r'$\xi$', r'$\chi^{2}$'] #[r'$y^{+}$', r'$T_{e}$',  r'$n_{e}$', r'$a_{H}$', r'$a_{He}$' r'$c(H\beta)$',  r'$\tau$', r'$\xi$', r'$\chi^{2}$']
True_LowDen             = [1, 5,]
True_HighDen            = [1, 5,]

pattern         = 'linear_regression_inference2'
true_values     = True_HighDen
Name            = 'lr2'
article_folder  = '/home/vital/workspace/X_Data/'

#Locate files on hard drive
FilesList               = pv.Folder_Explorer(pattern, Folder, CheckComputer=False)

#Define plot frame and colors
pv.FigFormat_One(ColorConf = 'Day1')

#Loop through files
for i in range(len(FilesList)):

    #Analyze file address
    CodeName, FileName, FileFolder  = pv.Analyze_Address(FilesList[i])
    db_Address                      = FileFolder + FileName
    CodeName = Name
      
    #Load database
    print 'estas es', db_Address
    bp.load_pymc_database(db_Address)       
    
    #Extract variable stats
    statistics_dict = bp.extract_traces_statistics(Traces_code)
        
    bp.plot_tracers(Traces_code, Traces_labels)
    pv.SaveManager(CodeName + '_TracesEvolution', FileFolder, ForceSave=True, ForceDisplay=False, savevectorfile=False)
    pv.ResetPlot()
 
    bp.plot_posteriors_histagram(Traces_code, Traces_labels)        
    pv.SaveManager(CodeName + '_PosteriorHistograms', FileFolder, ForceSave=True, ForceDisplay=False, savevectorfile=False)
    pv.ResetPlot()
         
    bp.plot_acorrelation(Traces_code, Traces_labels, n_columns=2, n_rows=1)
#     bp.plot_acorrelation(Traces_code, Traces_labels)
    pv.SaveManager(CodeName + '_TracesAcorr', FileFolder, ForceSave=True, ForceDisplay=False, savevectorfile=False)
    pv.ResetPlot()
 
    bp.plot_triangle_histContours(Traces_code, Traces_labels, true_values=true_values)
    bp.savefig(article_folder + CodeName + '_triangleContourAll', reset_fig=True)
    pv.ResetPlot()
 
#     bp.plot_triangle_histContours(['He_abud', 'T_e', 'n_e'], [r'$y^{+}$', r'$T_{e}\,(K)$',  r'$n_{e}\,(cm^{-3})$'], true_values=true_values[:3])
#     bp.savefig(article_folder + CodeName + '_triangleContourTene', reset_fig=True)
#     pv.ResetPlot()

    for trace in Traces_code:

        traces_yplus = bp.pymc_database.trace(trace)[:]
        Median = median(traces_yplus)
        print trace
        print 'Median numpy',  
        print Median
        print 'percentiles: 16, 84' 
        print percentile(traces_yplus,84) - Median
        print Median - percentile(traces_yplus,16),'\n' 

print 'Data treated'
        
