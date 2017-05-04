from numpy                  import searchsorted, array, asarray, argsort, diff, concatenate, int8, where, zeros, max, median, round, exp, linspace, ones, sqrt
from scipy.optimize         import leastsq
from scipy.interpolate      import interp1d
import matplotlib.pyplot    as plt
from kapteyn import kmpfit

def my_model(p, x, cont, ncomp):
    #-----------------------------------------------------------------------
    # This describes the model and its parameters for which we want to find
    # the best fit. 'p' is a sequence of parameters (array/list/tuple).
    #-----------------------------------------------------------------------
    for i in range(ncomp):
        y = 0.0
        A, mu, sigma = p[i*3:(i+1)*3]
        y += A * exp(-(x-mu)*(x-mu)/(2.0*sigma*sigma)) + cont
    return y

def my_residuals(p, data):
    #-----------------------------------------------------------------------
    # This function is the function called by the fit routine in kmpfit
    # It returns a weighted residual. De fit routine calculates the
    # square of these values.
    #-----------------------------------------------------------------------
    x, y, err, cont, ncomp = data
    return (y-my_model(p,x,cont,ncomp)) / err

def ScientificData():
    Wave = array([3664.21,3665.03,3665.86,3666.68,3667.5, 3668.32,3669.15,3669.97
            ,3670.79,3671.61,3672.44,3673.26,3674.08,3674.91,3675.73,3676.55
            ,3677.37,3678.2, 3679.02,3679.84,3680.66,3681.49,3682.31,3683.13
            ,3683.95,3684.78,3685.6, 3686.42,3687.25,3688.07,3688.89,3689.71
            ,3690.54,3691.36,3692.18,3693.0,3693.83,3694.65,3695.47,3696.3
            ,3697.12,3697.94,3698.76,3699.59,3700.41,3701.23,3702.05,3702.88
            ,3703.7, 3704.52,3705.34,3706.17,3706.99,3707.81,3708.64,3709.46
            ,3710.28,3711.1, 3711.93,3712.75,3713.57,3714.39,3715.22,3716.04
            ,3716.86,3717.69,3718.51,3719.33,3720.15,3720.98,3721.8, 3722.62
            ,3723.44,3724.27,3725.09,3725.91,3726.74,3727.56,3728.38,3729.2
            ,3730.03,3730.85,3731.67,3732.49,3733.32,3734.14,3734.96,3735.78
            ,3736.61,3737.43,3738.25,3739.08,3739.9, 3740.72,3741.54,3742.37
            ,3743.19,3744.01,3744.83,3745.66,3746.48,3747.3, 3748.13,3748.95
            ,3749.77,3750.59,3751.42,3752.24,3753.06,3753.88,3754.71,3755.53
            ,3756.35,3757.18,3758.0,3758.82,3759.64,3760.47,3761.29,3762.11
            ,3762.93,3763.76,3764.58,3765.4, 3766.22,3767.05,3767.87,3768.69
            ,3769.52,3770.34,3771.16,3771.98,3772.81,3773.63,3774.45,3775.27
            ,3776.1, 3776.92,3777.74,3778.57,3779.39,3780.21,3781.03,3781.86
            ,3782.68,3783.5, 3784.32,3785.15,3785.97,3786.79,3787.61,3788.44
            ,3789.26])
    
    Flux = array([2.14494000e-16,2.25643000e-16,2.13680000e-16,2.11032000e-16
                    ,2.17382000e-16,2.15999000e-16,2.06204000e-16,2.08118000e-16
                    ,2.24451000e-16,2.14937000e-16,2.10287000e-16,2.20329000e-16
                    ,2.10438000e-16,2.23820000e-16,2.04692000e-16,2.14648000e-16
                    ,2.23597000e-16,2.09166000e-16,2.24512000e-16,2.13194000e-16
                    ,2.17345000e-16,2.16474000e-16,2.01755000e-16,2.28269000e-16
                    ,2.42876000e-16,2.20680000e-16,1.95941000e-16,1.96803000e-16
                    ,2.40526000e-16,2.52451000e-16,2.23833000e-16,1.83009000e-16
                    ,1.76466000e-16,2.28500000e-16,2.59811000e-16,2.35419000e-16
                    ,1.93029000e-16,1.87247000e-16,1.78781000e-16,1.92278000e-16
                    ,2.52476000e-16,2.79436000e-16,2.31588000e-16,1.84083000e-16
                    ,1.78930000e-16,1.97013000e-16,1.94891000e-16,1.92645000e-16
                    ,2.43458000e-16,3.04794000e-16,3.03952000e-16,2.38962000e-16
                    ,1.87307000e-16,1.72144000e-16,1.79054000e-16,1.81957000e-16
                    ,1.76392000e-16,2.00494000e-16,2.64998000e-16,3.12958000e-16
                    ,2.75239000e-16,2.04264000e-16,1.79797000e-16,1.81839000e-16
                    ,1.78118000e-16,1.71364000e-16,1.70805000e-16,1.87110000e-16
                    ,1.91237000e-16,2.33834000e-16,3.57551000e-16,4.82230000e-16
                    ,4.74116000e-16,4.64246000e-16,9.69321000e-16,2.40114000e-15
                    ,3.88097000e-15,3.80371000e-15,3.33540000e-15,4.42733000e-15
                    ,4.37940000e-15,2.32080000e-15,8.68166000e-16,4.04733000e-16
                    ,3.06476000e-16,3.30365000e-16,3.70026000e-16,3.55559000e-16
                    ,2.53349000e-16,1.90299000e-16,1.82450000e-16,1.78436000e-16
                    ,1.97997000e-16,1.64498000e-16,1.90334000e-16,1.98849000e-16
                    ,1.67139000e-16,1.75295000e-16,1.61735000e-16,1.65570000e-16
                    ,1.85281000e-16,1.67671000e-16,1.86147000e-16,2.21424000e-16
                    ,2.79711000e-16,4.27192000e-16,4.43075000e-16,3.08837000e-16
                    ,2.15379000e-16,1.84632000e-16,1.79010000e-16,1.77749000e-16
                    ,1.75093000e-16,1.99575000e-16,2.15289000e-16,1.99675000e-16
                    ,1.77702000e-16,1.79244000e-16,1.90122000e-16,1.73974000e-16
                    ,1.87450000e-16,1.93757000e-16,1.89667000e-16,1.88110000e-16
                    ,1.90049000e-16,1.90473000e-16,1.79417000e-16,1.91121000e-16
                    ,2.25564000e-16,3.37509000e-16,4.98562000e-16,4.77418000e-16
                    ,3.37369000e-16,2.42054000e-16,1.86360000e-16,1.79651000e-16
                    ,1.74415000e-16,1.65394000e-16,1.70504000e-16,1.84342000e-16
                    ,1.77910000e-16,1.65326000e-16,1.86521000e-16,1.83105000e-16
                    ,1.76164000e-16,1.82931000e-16,1.69198000e-16,1.91854000e-16
                    ,1.77330000e-16,1.78287000e-16,1.90082000e-16,1.74744000e-16
                    ,1.80090000e-16])
    
    Continuum = array([2.16659046e-16,2.16406172e-16,2.16150215e-16,2.15897342e-16
                    ,2.15644469e-16,2.15391596e-16,2.15135639e-16,2.14882766e-16
                    ,2.14629892e-16,2.14377019e-16,2.14121062e-16,2.13868189e-16
                    ,2.13615316e-16,2.13359359e-16,2.13106486e-16,2.12853612e-16
                    ,2.12600739e-16,2.12344782e-16,2.12091909e-16,2.11839036e-16
                    ,2.11586163e-16,2.11330206e-16,2.11077332e-16,2.10824459e-16
                    ,2.10571586e-16,2.10315629e-16,2.10062756e-16,2.09809883e-16
                    ,2.09553926e-16,2.09301052e-16,2.09048179e-16,2.08795306e-16
                    ,2.08539349e-16,2.08286476e-16,2.08033603e-16,2.07780729e-16
                    ,2.07524772e-16,2.07271899e-16,2.07019026e-16,2.06763069e-16
                    ,2.06510196e-16,2.06257323e-16,2.06004449e-16,2.05748492e-16
                    ,2.05495619e-16,2.05242746e-16,2.04989873e-16,2.04733916e-16
                    ,2.04481043e-16,2.04228169e-16,2.03975296e-16,2.03719339e-16
                    ,2.03466466e-16,2.03213593e-16,2.02957636e-16,2.02704763e-16
                    ,2.02451889e-16,2.02199016e-16,2.01943059e-16,2.01690186e-16
                    ,2.01437313e-16,2.01184440e-16,2.00928483e-16,2.00675609e-16
                    ,2.00422736e-16,2.00166779e-16,1.99913906e-16,1.99661033e-16
                    ,1.99408160e-16,1.99152203e-16,1.98899329e-16,1.98646456e-16
                    ,1.98393583e-16,1.98137626e-16,1.97884753e-16,1.97631880e-16
                    ,1.97375923e-16,1.97123049e-16,1.96870176e-16,1.96617303e-16
                    ,1.96361346e-16,1.96108473e-16,1.95855600e-16,1.95602726e-16
                    ,1.95346769e-16,1.95093896e-16,1.94841023e-16,1.94588150e-16
                    ,1.94332193e-16,1.94079320e-16,1.93826446e-16,1.93570489e-16
                    ,1.93317616e-16,1.93064743e-16,1.92811870e-16,1.92555913e-16
                    ,1.92303040e-16,1.92050166e-16,1.91797293e-16,1.91541336e-16
                    ,1.91288463e-16,1.91035590e-16,1.90779633e-16,1.90526760e-16
                    ,1.90273886e-16,1.90021013e-16,1.89765056e-16,1.89512183e-16
                    ,1.89259310e-16,1.89006437e-16,1.88750480e-16,1.88497606e-16
                    ,1.88244733e-16,1.87988776e-16,1.87735903e-16,1.87483030e-16
                    ,1.87230157e-16,1.86974199e-16,1.86721326e-16,1.86468453e-16
                    ,1.86215580e-16,1.85959623e-16,1.85706750e-16,1.85453877e-16
                    ,1.85201003e-16,1.84945046e-16,1.84692173e-16,1.84439300e-16
                    ,1.84183343e-16,1.83930470e-16,1.83677596e-16,1.83424723e-16
                    ,1.83168766e-16,1.82915893e-16,1.82663020e-16,1.82410147e-16
                    ,1.82154190e-16,1.81901316e-16,1.81648443e-16,1.81392486e-16
                    ,1.81139613e-16,1.80886740e-16,1.80633867e-16,1.80377910e-16
                    ,1.80125036e-16,1.79872163e-16,1.79619290e-16,1.79363333e-16
                    ,1.79110460e-16,1.78857587e-16,1.78604713e-16,1.78348756e-16
                    ,1.78095883e-16])
    
    return Wave, Flux, Continuum

def Estimate_Amplitude_CentralWavelength(xval, yval, MinLevel, ListLines, Number_Gaussians):
    xval                = asarray(xval)
    yval                = asarray(yval)
    GroupLines          = asarray(ListLines)
    
    sort_idx            = argsort(xval)
    yval                = yval[sort_idx]
    gradient            = diff(yval)
    maxima              = diff((gradient > 0).view(int8))
    ListIndeces         = concatenate((([0],) if gradient[0] < 0 else ()) + (where(maxima == -1)[0] + 1,) + (([len(yval)-1],) if gradient[-1] > 0 else ()))
    X_Maxima, Y_Maxima  = [], []
    Limits_Dictionary   = []
    
    for index in ListIndeces:
        if yval[index] > MinLevel:
            X_Maxima.append(xval[index])
            Y_Maxima.append(yval[index])
                
    A_List = []
    mu_List = []

    for i in range(Number_Gaussians):
        TheoWave = GroupLines[i]
        Closest_Index = abs(X_Maxima-TheoWave).argmin()
        A_List.append(Y_Maxima[Closest_Index])
        mu_List.append(X_Maxima[Closest_Index]) 
    
    A_max = max(A_List)
    Mean_x  = round(median(mu_List))
    
    for i in range(Number_Gaussians):
        if A_List[i] < 0.40 * A_max:
            Limits_Dictionary.append({})
            Limits_Dictionary.append({'limits':(mu_List[i]-Mean_x-0.25,mu_List[i]-Mean_x+0.25)})
            Limits_Dictionary.append({'limits':(0,1.2)})
        else:
            Limits_Dictionary.append({})
            Limits_Dictionary.append({})
            Limits_Dictionary.append({'limits':(0,3)})
                    
    return array(A_List), array(mu_List), Limits_Dictionary

def NormalizeGaussian(Wave, Flux, A_Values, mu_Values, sigma_Values, Continuum, Continuum_error, Number_Gaussians):
        
    Max_y   = max(A_Values)
    Mean_x  = round(median(mu_Values))
    
    x                  = round(Wave                 - Mean_x, 3)
    y                  = round(Flux                 / Max_y,  4)
    A_Norm             = round(A_Values             / Max_y,  4)
    mu_Norm            = round(mu_Values            - Mean_x, 3)
    sigma_Norm         = round(sigma_Values                 , 3)
    zerolev_Norm       = round(Continuum            / Max_y, 4)
    sigma_zerolev_Norm = round(Continuum_error      / Max_y, 4)
    
    p_0 = zeros(Number_Gaussians * 3)
    for i in range(Number_Gaussians):
        p_0[i*3:(i+1)*3] = A_Norm[i], mu_Norm[i], sigma_Norm[i]

    return x, y, p_0, zerolev_Norm, sigma_zerolev_Norm

def Residuals_GaussianMixture(p, data):
    x, y, zerolev, error = data[0], data[1], data[2], data[3]
    
    return (y - (Model_GaussianMixture((x, zerolev), p)))/error

def Model_GaussianMixture(Ind_Variables, p):
    y = 0.0
    for i in range( int(len(p) / 3)):
        A, mu, sigma = p[i*3:(i+1)*3]
        y += A * exp(-(Ind_Variables[0]-mu)*(Ind_Variables[0]-mu)/(2.0*sigma*sigma))
    return y + Ind_Variables[1]

def Rescale_GaussianParameters(p_1_Norm, A_Values, mu_Values, Number_Gaussians):
    p_1 = zeros(len(p_1_Norm))
    Max_y   = max(A_Values)
    Mean_x  = median(mu_Values)

    for i in range(Number_Gaussians):
        A, mu, sigma                 = p_1_Norm[i*3:(i+1)*3]
        p_1[i*3:(i+1)*3]             = A * Max_y, mu + Mean_x, sigma

    return p_1

def ResampleGaussian(p_1, x, zerolev):
    WaveGaussian        = linspace(x[0], x[-1], 100, endpoint=True)
    Interpolation       = interp1d(x, zerolev, kind = 'slinear')        
    zerolev_Gaussian    = Interpolation(WaveGaussian)
    Flux_Gaussian       = Model_GaussianMixture((WaveGaussian, zerolev_Gaussian), p_1)
    return WaveGaussian, Flux_Gaussian, zerolev_Gaussian

Wave, Flux, Continuum                               = ScientificData()
Continuum_error                                     = 7.0153e-18

# Case One: In each case we declare the number of gaussians we should be detecting
GaussianEdge_Wave                                   = [3724, 3733]
Gaussian_Components                                 = [3726.032, 3728.815]

#Case two
# GaussianEdge_Wave                                 = [3724.05, 3738.05]
# Gaussian_Components                               = [3726.032, 3728.815, 3735.430]
 
# #Case three
# GaussianEdge_Wave                                 = [3718.05, 3738.05]
# Gaussian_Components                               = [3722.997, 3726.032, 3728.815]
#  
# Case Four
GaussianEdge_Wave                                   = [3718.05, 3738.05]
Gaussian_Components                                 = [3722.997, 3726.032, 3728.815, 3735.430]

Number_Gaussians                                    = len(Gaussian_Components)          

# Declare the location of the Gaussian mixture we are interested
Ind_left, Ind_right                                 = searchsorted(Wave, GaussianEdge_Wave)
Wave_Region, Flux_Region, Continuum_Region          = Wave[Ind_left:Ind_right],  Flux[Ind_left:Ind_right], Continuum[Ind_left:Ind_right]

#Estimate the initial values for the amplitude, central x (mu) and sigma for the gaussian mixture
A_Values, mu_Values,Limits_Dictionary               = Estimate_Amplitude_CentralWavelength(Wave_Region, Flux_Region, Continuum_error, Gaussian_Components, Number_Gaussians)
sigma_Values                                        = ones(len(A_Values))

#Normalize the parameters for the fitting: x, y, Amplitude, mu and the continuum and its sigma
x, y, p_0, continuum_norm, continuum_error_norm     = NormalizeGaussian(Wave_Region, Flux_Region, A_Values, mu_Values, sigma_Values, Continuum_Region, Continuum_error, Number_Gaussians)

#Use leastsqr to perform the fitting on Mixture Gaussian method
p_1_Norm, conv                                      = leastsq(Residuals_GaussianMixture, args=([x, y, continuum_norm, continuum_error_norm]),   x0 = p_0)

#Rescale the A, mu and sigma from p_1_Norm to better magnitudes of the plot
p_1                                                 = Rescale_GaussianParameters(p_1_Norm, A_Values, mu_Values, Number_Gaussians)

#Using the prediction p_1 generate the x and y falues for the gaussian (increasing the resolution above the one in the plot.
Wave_Gaussian, Flux_Gaussian, zerolev_Gaussian      = ResampleGaussian(p_1, Wave[Ind_left:Ind_right], Continuum[Ind_left:Ind_right])

#---------Kmpfit method no normalized----------

fitobj = kmpfit.Fitter(residuals=Residuals_GaussianMixture, data=(x, y, continuum_norm, continuum_error_norm))

Dictionary_Conditions = [0] * (Number_Gaussians*3)
for i in range(Number_Gaussians):
    A_i, mu_i, sigma_i = p_0[i*3:(i+1)*3]
#     Dictionary_Conditions[i*3:(i+1)*3] = {'limits':(A_i*0.9,A_i*1.1)}, {'limits':(mu_i-0.5,mu_i+0.5)}, {'limits':(0,1)}
#     Dictionary_Conditions[i*3:(i+1)*3] = {}, {'limits':(mu_i-0.25,mu_i+0.25)}, {}
    Dictionary_Conditions[i*3:(i+1)*3] = {}, {'limits':(mu_i-0.25,mu_i+0.25)}, {}
    

print 'Dictionary_Conditions', Dictionary_Conditions
print 'Adapted dictionary', Limits_Dictionary

fitobj.parinfo = Limits_Dictionary
print 'y aqui tengo???', p_0, type(p_0)

try:
    fitobj.fit(params0 = p_0)
except Exception, mes:
    print "Something wrong with fit: ", mes
    raise SystemExit

p1_Norm_kmpfit  = fitobj.params
p1_kmpfit       = Rescale_GaussianParameters(p1_Norm_kmpfit, A_Values, mu_Values, Number_Gaussians)

print 'Comparing values:'
for i in range(Number_Gaussians):
    A_i, mu_i, sigma_i = p_1[i*3:(i+1)*3]
    A_kmpfit, mu_kmpfit, sigma_kmpfit = p1_kmpfit[i*3:(i+1)*3]
    print 'Gaussian',   i
    print 'Mine',       A_i, mu_i, sigma_i
    print 'Kmpf',       A_kmpfit, mu_kmpfit, sigma_kmpfit
    
#---------Making the plot----------
Fig     = plt.figure(figsize = (16, 10))
Axis    = Fig.add_subplot(111)
Axis.set_xlabel('Wavelength',fontsize=15)
Axis.set_ylabel('Flux', fontsize=15)
Fig.set_facecolor('w')
Axis.plot(Wave, Flux, color='Blue', label="Spectrum")
Axis.plot(Wave_Gaussian, Flux_Gaussian, color='Red',  label="Fitted Gaussian mixture")
Axis.plot(mu_Values, A_Values, 'o', color='orange',  label="Maxima initial guess")
Axis.fill_between(Wave_Region, Continuum_Region, Flux_Region, color='grey', alpha=0.25, label='SelectionRegion')

Axis.errorbar(Wave_Region, Flux_Region, yerr=Continuum_error, fmt='g', alpha=0.7, label="Noisy data")

Wave_kmpfit, Flux_kmpfit, zerolev_Gaussian = ResampleGaussian(p1_kmpfit, Wave[Ind_left:Ind_right], Continuum[Ind_left:Ind_right])
Axis.plot(Wave_kmpfit, Flux_kmpfit, color='green',  label="kmpfit")

for i in range(Number_Gaussians):
    A_i, mu_i, sigma_i = p_1[i*3:(i+1)*3]
    A_kmpfit, mu_kmpfit, sigma_kmpfit = p1_kmpfit[i*3:(i+1)*3]
 
    Wave_kmpfit_i, Flux_kmpfit_i, zerolev_Gaussian_i = ResampleGaussian([A_kmpfit, mu_kmpfit, sigma_kmpfit], Wave[Ind_left:Ind_right], Continuum[Ind_left:Ind_right])
    Axis.plot(Wave_kmpfit_i, Flux_kmpfit_i, color='green', linestyle=':', label='Gaussian_'+str(i))
    Axis.plot(mu_i, A_i + zerolev_Gaussian_i[(abs(Wave_kmpfit_i-mu_kmpfit)).argmin()], 'o', color='red')
    Axis.plot(mu_kmpfit, A_kmpfit+median(Continuum), 'o', color='green')

plt.legend()

plt.show()












