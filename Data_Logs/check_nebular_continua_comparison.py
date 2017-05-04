from dazer_methods  import Dazer
from pandas         import notnull
from numpy          import median, zeros, searchsorted, where, concatenate, array, power, empty, std, mean
from lmfit          import Parameters, minimize, report_fit, models
from libraries.Astro_Libraries.Nebular_Continuum import NebularContinuumCalculator
from uncertainties import ufloat

def RightListPoints():

    Righties = [
                (3740,3746),       
                (3760,3767),
                (3778,3789),
                (3803,3817),
                (3825,3832),
                (3844,3860),
                (3900,3958),
                (3980,4020),
                ]

    return Righties

def LeftListPoints():

    Lefties = [
               (3545,3630),        
               ]
    return Lefties



#Declare objects

def ExtractSubRegion(TotalWavelen, TotalInten, Wlow, Whigh):

    indmin, indmax = searchsorted(TotalWavelen, (Wlow, Whigh))
    indmax = min(len(TotalWavelen)-1, indmax)
    
    PartialWavelength = TotalWavelen[indmin:indmax]
    PartialIntensity = TotalInten[indmin:indmax]
    
    return PartialWavelength, PartialIntensity

def Concatenate(TotalWave, TotalInt, ListPoints):

    Waves_Comb  = array([])
    Flux_Comb   = array([])

    for i in range(len(ListPoints)):
        wlow                = ListPoints[i][0]
        whigh               = ListPoints[i][1]
        SubWave, SubInt     = ExtractSubRegion(TotalWave, TotalInt, wlow, whigh)
        Waves_Comb          = concatenate((Waves_Comb, SubWave))
        Flux_Comb           = concatenate((Flux_Comb, SubInt))
        
    return Waves_Comb, Flux_Comb

def mean_deviation(TotalWave, TotalInt, ListPoints):
    
    array_std = empty(len(ListPoints))
    
    for i in range(len(ListPoints)):
        wlow                = ListPoints[i][0]
        whigh               = ListPoints[i][1]
        SubWave, SubInt     = ExtractSubRegion(TotalWave, TotalInt, wlow, whigh)
        array_std[i]        = std(SubInt)
    
    return mean(array_std)


dz      = Dazer()
nebCalc = NebularContinuumCalculator()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'

#Reddening properties
R_v             = 3.4
red_curve       = 'G03'
cHbeta_type     = 'cHbeta_reduc'

BalmerJump_Wavelength   = 3646
Limit_Left              = 3545
Limit_Right             = 4000

#Define plot frame and colors
dz.FigConf()

#Locate the objects
objName                 = 'SHOC579'
ouput_folder            = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
fits_file               = catalogue_df.loc[objName].reduction_fits
lineslog_address        = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=AbundancesFileExtension)
    
#Load object data
object_data             = catalogue_df.loc[objName]
lineslog_frame          = dz.load_lineslog_frame(lineslog_address)
wave, flux, header_0    = dz.get_spectra_data(fits_file)
wave_E, flux_E, header_E = dz.get_spectra_data(catalogue_df.loc[objName].emission_fits)

#Perform the reddening correction
cHbeta = catalogue_df.loc[objName, cHbeta_type]
dz.deredden_lines(lineslog_frame, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
spectrum_dered = dz.derreddening_spectrum(wave, flux, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
Int_E = dz.derreddening_spectrum(wave_E, flux_E, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)

#Import physical data    
Tlow_key    = catalogue_df.loc[objName, 'T_high'] + '_emis'
nHeII_HII   = 'HeII_HII_from_O' + '_emis'
nHeIII_HII  = 'HeIII_HII_from_O' + '_emis'

Te          = object_data[Tlow_key].nominal_value if notnull(object_data[Tlow_key]) else 10000.0  
nHeII_HII   = object_data[nHeII_HII].nominal_value if notnull(object_data[nHeII_HII]) else 0.1
nHeIII_HII  = object_data[nHeIII_HII].nominal_value if notnull(object_data[nHeIII_HII]) else 0.0 
Hbeta_Flux  = lineslog_frame.loc['H1_4861A', 'line_Int']
Halpha_Flux = lineslog_frame.loc['H1_6563A', 'line_Int']

print '--Using physical parameters', Te, nHeII_HII, nHeIII_HII, Hbeta_Flux, Halpha_Flux

#-- Calculate nebular continuum
nebCalc.PropertiesfromUser(Te, Hbeta_Flux.nominal_value, nHeII_HII, nHeIII_HII, wave, Calibration = 'Zanstra')

#-- Calculate continuous emissino coefficients:
Gamma_Total, Gamma_lambda, Gamma_FB_HI, Gamma_FB_HeI, Gamma_FB_HeII, Gamma_2q, Gamma_FF = nebCalc.Calculate_Nebular_gamma()

#-- Caculate nebular flux with different calibration methods
NebularInt_Hbeta = nebCalc.Zanstra_Calibration('Hbeta', Hbeta_Flux.nominal_value, Gamma_Total)

#Removing nebular component
Int_dedNeb  = spectrum_dered - NebularInt_Hbeta
Int_gas = Int_E + NebularInt_Hbeta

#Plotting the data
dz.data_plot(wave, spectrum_dered,      'Reduced spectrum (without reddening)')
dz.data_plot(wave, NebularInt_Hbeta,    'Nebular flux')
dz.data_plot(wave_E, Int_gas, 'Pure emission + Nebular')

LeftPoints = LeftListPoints()
RightPoints = RightListPoints()

#For spectrum 1
for i in range(len(LeftPoints)):
    x_range, y_range = ExtractSubRegion(wave, spectrum_dered, LeftPoints[i][0], LeftPoints[i][1])
    dz.Axis.fill_between(x_range, zeros(len(x_range)), y_range, label= "Blue Continuum", facecolor='blue',alpha = 0.2)

for i in range(len(RightPoints)):
    x_range, y_range = ExtractSubRegion(wave, spectrum_dered, RightPoints[i][0], RightPoints[i][1])
    dz.Axis.fill_between(x_range, zeros(len(x_range)), y_range, label= "Red Continuum", facecolor='red',alpha = 0.2)

x_blue_regression, y_blue_regression = Concatenate(wave, spectrum_dered, LeftPoints)
x_red_regression, y_red_regression = Concatenate(wave, spectrum_dered, RightPoints)
bj_dev = mean_deviation(wave, spectrum_dered, LeftPoints + RightPoints) 

x_blue, y_blue, blue_parameters = dz.lmfit_linear(x_blue_regression, y_blue_regression)
x_red, y_red, red_parameters = dz.lmfit_linear(x_red_regression, y_red_regression)

x_Bluecontinuum = wave[where(wave<=BalmerJump_Wavelength)]
y_BlueContinuum = blue_parameters['lineal_slope'].value * x_Bluecontinuum + blue_parameters['lineal_intercept'].value
dz.data_plot(x_Bluecontinuum, y_BlueContinuum, "Blue continuum", 'blue', linestyle='--')

x_Redcontinuum = wave[where(wave>=BalmerJump_Wavelength)]
y_RedContinuum = red_parameters['lineal_slope'].value * x_Redcontinuum + red_parameters['lineal_intercept'].value
dz.data_plot(x_Redcontinuum, y_RedContinuum, "Red continuum", 'red', linestyle='--')

BJ  = ufloat(y_BlueContinuum[-1] - y_RedContinuum[0], bj_dev)
H11 = lineslog_frame.loc['H1_3770A'].line_Int

TBac = 368 * (1 + 0.259*nHeII_HII + 3.409*nHeIII_HII) * power(BJ/H11, -3.0/2.0)
print 'Balmer jump', BJ
print 'Balmer temperature please', TBac
print 'TSIII', Te

#For spectrum 2
for i in range(len(LeftPoints)):
    x_range, y_range = ExtractSubRegion(wave, Int_gas, LeftPoints[i][0], LeftPoints[i][1])
    dz.Axis.fill_between(x_range, zeros(len(x_range)), y_range, label= "Blue Continuum", facecolor='blue',alpha = 0.2)

for i in range(len(RightPoints)):
    x_range, y_range = ExtractSubRegion(wave, Int_gas, RightPoints[i][0], RightPoints[i][1])
    dz.Axis.fill_between(x_range, zeros(len(x_range)), y_range, label= "Red Continuum", facecolor='red',alpha = 0.2)

x_blue_regression, y_blue_regression = Concatenate(wave, Int_gas, LeftPoints)
x_red_regression, y_red_regression = Concatenate(wave, Int_gas, RightPoints)
bj_dev = mean_deviation(wave, Int_gas, LeftPoints + RightPoints) 

x_blue, y_blue, blue_parameters = dz.lmfit_linear(x_blue_regression, y_blue_regression)
x_red, y_red, red_parameters = dz.lmfit_linear(x_red_regression, y_red_regression)

x_Bluecontinuum = wave[where(wave<=BalmerJump_Wavelength)]
y_BlueContinuum = blue_parameters['lineal_slope'].value * x_Bluecontinuum + blue_parameters['lineal_intercept'].value
dz.data_plot(x_Bluecontinuum, y_BlueContinuum, "Blue continuum", 'blue', linestyle='--')

x_Redcontinuum = wave[where(wave>=BalmerJump_Wavelength)]
y_RedContinuum = red_parameters['lineal_slope'].value * x_Redcontinuum + red_parameters['lineal_intercept'].value
dz.data_plot(x_Redcontinuum, y_RedContinuum, "Red continuum", 'red', linestyle='--')

#Calculate the balmer temperature

BJ  = ufloat(y_BlueContinuum[-1] - y_RedContinuum[0], bj_dev)
H11 = lineslog_frame.loc['H1_3770A'].line_Int

TBac = 368 * (1 + 0.259*nHeII_HII + 3.409*nHeIII_HII) * power(BJ/H11, -3.0/2.0)
print 'Balmer jump', BJ
print 'Balmer temperature please', TBac
print 'TSIII', Te

#Format the graphs
PlotTitle = r'Object {} Nebular continuum substraction'.format(objName)
dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)
dz.display_fig()




