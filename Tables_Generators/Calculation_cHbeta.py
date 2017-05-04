import uncertainties.unumpy                             as unumpy  
from CodeTools.PlottingManager                          import myPickle
from Math_Libraries.FittingTools                        import NumpyRegression
from Math_Libraries.linfit_script                       import LinfitLinearRegression
from ManageFlow                                         import DataToTreat
from Astro_Libraries.Reddening_Corrections              import ReddeningLaws    
from numpy                                              import concatenate
from Plotting_Libraries.dazer_plotter           import Plot_Conf

#Declare coding classes
pv                          = myPickle()
Reddening                   = ReddeningLaws()
dz                          = Plot_Conf() 

#Declare data location and type
Catalogue_Dic               = DataToTreat()
Pattern                     = Catalogue_Dic['Datatype'] + '.fits'
DataLog_Extension           = '_' + Catalogue_Dic['Datatype'] + '_LinesLog_v3.txt'       #/First batch process for untreated spectra

#Define figure format
dz.FigConf(FigWidth =16 , FigHeight = 9)


#Find and organize files from terminal command or .py file
FilesList                   = pv.Folder_Explorer(Pattern,  Catalogue_Dic['Obj_Folder'], CheckComputer=False)

Object_Giving_errors = []

# Loop through files
for i in range(len(FilesList)):

    #Import spectrum data
    CodeName, FileName, FileFolder      = pv.Analyze_Address(FilesList[i])

    #Determine reddening coefficients
    x_inbound, y_inbound, EmLine_inBound, x_outbound, y_outbound, EmLine_outBound  = Reddening.RecombinationCoefficients(FileFolder, CodeName, DataLog_Extension, 'boundary')              
    
    #SDSS data
    if Catalogue_Dic['Datatype'] == 'dr10':
        
        #Calculate trendline
        cHbeta_inbound_MagEr, n_inbound_MagEr       = LinfitLinearRegression(x_inbound, y_inbound)
        y_inbound_trend                             = cHbeta_inbound_MagEr * x_inbound + n_inbound_MagEr
                
        #Plot the data accepted points
        pv.DataPloter_One(x_inbound,    unumpy.nominal_values(y_inbound_trend), 'Trend line: All points',           pv.Color_Vector[2][3],  LineStyle=':')
        pv.DataPloter_One(x_outbound,   unumpy.nominal_values(y_outbound),      'Points close to boundary',         pv.Color_Vector[2][0],  LineStyle=None, MarkerSize=200)
        
        #Plot the data rejected points
        pv.DataPloter_One(x_inbound,    unumpy.nominal_values(x_inbound),       'Observed recombination lines',     pv.Color_Vector[2][0],  MarkerStyle='o', YError=unumpy.std_devs(y_inbound), MarkerSize  = 10)        
        pv.TextPlotter(x_inbound,       unumpy.nominal_values(x_inbound),       EmLine_inBound,                     x_pad = 0.95,       y_pad = 1)


    #ISIS data    
    elif Catalogue_Dic['Datatype'] == 'WHT':
        
        #Blue Data                
        x_Blue, y_Blue, EmLine_blue, Blue_Normalizing_Ion   = Reddening.RecombinationCoefficients(FileFolder, CodeName, DataLog_Extension, 'Blue')
        cHbeta_blue_MagEr, n_blue_MagEr                     = LinfitLinearRegression(x_Blue, y_Blue)

        #Red data                 
        x_Red, y_Red, EmLine_Red, Red_Normalizing_Ion       = Reddening.RecombinationCoefficients(FileFolder, CodeName, DataLog_Extension, 'Red')
        cHbeta_red_MagEr, n_red_MagEr                       = LinfitLinearRegression(x_Red, y_Red)

        #Combine Blue and Red points
        
        #Case with observed blue and red lines
        if EmLine_Red != None:
            
            #Concatenate all points
            x_BlueRed, y_BlueRed                            = concatenate((x_Blue,x_Red)), concatenate((y_Blue,y_Red))     
            
            cHbeta_all_MagEr, n_all_MagEr                   = LinfitLinearRegression(x_BlueRed, y_BlueRed)
            cHbeta_NoError, n_NoError                       = NumpyRegression(x_BlueRed, unumpy.nominal_values(y_BlueRed))
            
            #Trendline with all points and error
            Trendline_all                                   = cHbeta_all_MagEr * x_BlueRed + n_all_MagEr
        
        #Case there are not enough red points
        else:
            
            #Create vector only with blue ones
            x_BlueRed, y_BlueRed                            = x_Blue, y_Blue
            
            #Get gradients
            cHbeta_all_MagEr, n_all_MagEr                   = LinfitLinearRegression(x_BlueRed, y_BlueRed)            
            cHbeta_NoError, n_NoError                       = NumpyRegression(x_BlueRed, unumpy.nominal_values(y_BlueRed))            
            
            #Trendline with all points and error
            Trendline_all                                   = cHbeta_all_MagEr * x_BlueRed + n_all_MagEr
        
        #Trendline for he case we do not consider the error
        y_NoError_trend                                     = cHbeta_NoError * x_BlueRed + n_NoError
         
        #Plot the data
        dz.data_plot(x_Blue,        unumpy.nominal_values(y_Blue), label='Blue arm emission lines', markerstyle='^', y_error=unumpy.std_devs(y_Blue))        
        dz.data_plot(x_BlueRed,     unumpy.nominal_values(Trendline_all),   label='Trend line: Including errors',  linestyle=':')
        dz.data_plot(x_Red,         unumpy.nominal_values(y_Red),  label='Red arm emission lines', markerstyle='o', y_error=unumpy.std_devs(y_Red))       
        dz.data_plot(x_BlueRed,     unumpy.nominal_values(y_NoError_trend), label='Trend line: Without including error', linestyle='--')
        
        dz.text_plot(EmLine_blue, x_Blue, unumpy.nominal_values(y_Blue), x_pad = 0.95, y_pad = 1.10, fontsize=10)
        dz.text_plot(EmLine_Red, x_Red, unumpy.nominal_values(y_Red), x_pad = 0.95, y_pad = 1.10, fontsize=10)
        #Plot the data
        #Points not used for the treatment
#         d.TextPlotter(x_outbound,  unumpy.nominal_values(y_outbound), EmLine_outBound, x_pad = 0.95, y_pad = 1)
        dz.text_plot(EmLine_outBound, x_outbound, unumpy.nominal_values(y_outbound), fontsize=10)
        #--Blue arm
#         dz.data_plot(x_Blue,   unumpy.nominal_values(y_Blue),                                          'Blue arm',         pv.Color_Vector[2][2],      YError=unumpy.std_devs(y_Blue))        
#         dz.data_plot(x_Blue,   unumpy.nominal_values(cHbeta_blue_MagEr * x_Blue + n_blue_MagEr), label='Trend line blue', linestyle=':')
         
#       #--Red arm

    #Increase the display range
#     dz.Axis.set_ylim(-0.4,0.4)

    #Insert labels and legends    
    Title       = "HII galaxy " + CodeName + " " + r'$c(H\beta)$' + ' coefficient calculation'
    y_Title     = r'$log(I/I_{H\beta})_{th}-log(F/F_{H\beta})_{Obs}$'
    x_Title     = r'$f(\lambda)-f(\lambda_{H\beta})$'
    dz.FigWording(x_Title, y_Title, Title)    
    
    #Save data
#         pv.SaveManager(SavingName = pv.ScriptCode + '_' + CodeName + '_IntrinsicReddening', SavingFolder = FileFolder, ForceSave=True)
#     dz.display_fig()
    dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Elemental_RegressionsSulfur/Images/' + 'SHOC579_cHbeta')
        
print 'All data treated', pv.display_errors()