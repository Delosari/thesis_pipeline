from dazer_methods                      import Dazer
from collections                        import OrderedDict
from numpy                              import empty, random, median, percentile, array, linspace, zeros
from scipy                              import stats
from uncertainties                      import ufloat
from uncertainties.unumpy               import nominal_values, std_devs
from libraries.Math_Libraries.sigfig    import round_sig
from libraries.Math_Libraries.bces_script   import bces, bcesboot

def latex_float(f):
    float_str = "{0:.2g}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
#         return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
        return r"10^{{{}}}".format(int(exponent))
    else:
        return float_str
    
#Create class object
dz = Dazer()
script_code = dz.get_script_code()

#Plot configuration
dz.FigConf()

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Regressions properties
MC_iterations   = 5000
WMAP_coordinates = array([ufloat(0.0, 0.0), ufloat(0.24709, 0.00025)])

#Generate the indeces
Regresions_dict = OrderedDict()
Regresions_dict['Regressions']      = ['Oxygen object abundance', 'Nitrogen object abundance', 'Sulfur object abundance']
Regresions_dict['metal x axis']     = ['OI_HI_emis2nd', 'NI_HI_emis2nd', 'SI_HI_emis2nd']
Regresions_dict['helium y axis']    = ['Ymass_O_emis2nd',  'Ymass_O_emis2nd', 'Ymass_S_emis2nd']
Regresions_dict['element']          = ['O', 'N', 'S']
Regresions_dict['factor']           = [1e5, 1e6, 1e6]
Regresions_dict['title']            = ['Helium mass fraction versus oxygen abundance', 'Helium mass fraction versus nitrogen abundance', 'Helium mass fraction versus sulfur abundance']

Regresions_dict['x label']          = [r'$\frac{{O}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][0])),  r'$\frac{{N}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][1])), r'$\frac{{S}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][2]))]
Regresions_dict['y label']          = [r'$Y_{\frac{O}{H}}$',  r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{S}{H}}$']
Regresions_dict['Colors']           = [dz.colorVector['green'], dz.colorVector['dark blue'], dz.colorVector['orangish']]

#Additional regression label
regr_dict       = {}
regr_dict['0']  = ['y|x']
regr_dict['3']  = ['Orthogonal']

#Get the objects which contain both abundances
for i in range(len(Regresions_dict['Regressions'])):
    
    print '--Doing regression',  Regresions_dict['element'][i]
    
    #Get right regression values properties
    element     = Regresions_dict['element'][i]
    regression  = Regresions_dict['Regressions'][i]
    metal_x     = Regresions_dict['metal x axis'][i]
    helium_y    = Regresions_dict['helium y axis'][i]
    reject_idx  = catalogue_df[element + '_valid'].isnull()
    reject_objs = catalogue_df[element + '_valid'][~reject_idx].index.values
    
    #Get objects which meet regression conditions
    idces_metal = (catalogue_df[metal_x].notnull()) & (catalogue_df[helium_y].notnull()) & (~catalogue_df.index.isin(reject_objs))
    objects     = catalogue_df.loc[idces_metal].index.values
    x           = catalogue_df.loc[idces_metal, metal_x].values * Regresions_dict['factor'][i]
    y           = catalogue_df.loc[idces_metal, helium_y].values
    
    #Create containers
    metal_matrix, Y_matrix  = empty((len(objects), MC_iterations)), empty((len(objects), MC_iterations))
    m_vector, n_vector      = empty(MC_iterations), empty(MC_iterations)
    
    #Generate the distributions
    for j in range(len(objects)): 
        metal_matrix[j,:]   = random.normal(x[j].nominal_value, x[j].std_dev, size = MC_iterations)
        Y_matrix[j,:]       = random.normal(y[j].nominal_value, y[j].std_dev, size = MC_iterations)
    
    #Run the fits
    for k in range(MC_iterations):
        x_i = metal_matrix[:,k]
        y_i = Y_matrix[:,k]

        m, n, r_value, p_value, std_err = stats.linregress(x_i, y_i)
        m_vector[k], n_vector[k] = m, n
    
    #Get fit mean values
    n_Median, n_16th, n_84th = median(n_vector), percentile(n_vector,16), percentile(n_vector,84)
    m_Median, m_16th, m_84th = median(m_vector), percentile(m_vector,16), percentile(m_vector,84)

    #Bootstrap BCES
    m, n, m_err, n_err, cov = bcesboot(nominal_values(x), std_devs(x), nominal_values(y), std_devs(y), cerr=zeros(len(x)), nsim=10000)
    
    #--Objects summary
    print '--- Using {}:'.format(len(objects)), ', '.join(list(objects))
    print '--- Rejecting {}:'.format(len(reject_objs)), ', '.join(list(reject_objs))
    
    print 'BCES Bootstrap'
    print m[0], m[1], m[2], m[3]
    print m_err[0], m_err[1], m_err[2], m_err[3]
    print n[0], n[1], n[2], n[3]
    print n_err[0], n_err[1], n_err[2], n_err[3]

    print 'My bootstrap'
    print n_Median, round_sig(n_Median-n_16th,2, scien_notation=False), round_sig(n_84th-n_Median,2, scien_notation=False)
    
    #Linear data
    x_regression_range  = linspace(0.0, max(nominal_values(x)) * 1.10, 20)
    y_regression_range  = m_Median * x_regression_range + n_Median      
    label_regr          = 'SCIPY bootstrap: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
    
    #Plotting the data, 
    dz.data_plot(nominal_values(x), nominal_values(y), color = Regresions_dict['Colors'][i], label=regression, markerstyle='o', x_error=std_devs(x), y_error=std_devs(y))
    dz.data_plot(WMAP_coordinates[0].nominal_value, WMAP_coordinates[1].nominal_value, color = dz.colorVector['pink'], label=r'WMAP prediction: $Y = 0.24709\pm0.00025$', markerstyle='o', x_error=WMAP_coordinates[0].std_dev, y_error=WMAP_coordinates[1].std_dev)    
    dz.data_plot(x_regression_range, y_regression_range, label = label_regr, color = Regresions_dict['Colors'][i], linestyle = '--')
    dz.plot_text(nominal_values(x), nominal_values(y), objects)
    
    for z in [0,3]:
        n_z, n_err_z  = n[z], n_err[z]
        m_z           = m[z]
        label       = r'Method {title}: $Y_{{P}} = {n}\pm{n_err}$'.format(title = regr_dict[str(z)], n = round_sig(n_z, 4, scien_notation=False), n_err = round_sig(n_err_z, 2, scien_notation=False))
        regre_z     = m_z * x_regression_range + n_z
        dz.data_plot(x_regression_range, regre_z, label = label, linestyle = '--')
        
    plotTitle = r'{title}: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
    dz.FigWording(Regresions_dict['x label'][i], Regresions_dict['y label'][i], plotTitle, loc='lower right')

    output_pickle = '{objFolder}{element}_MCMC_regression_2nd'.format(objFolder=catalogue_dict['Data_Folder'], element = element)
    dz.save_manager(output_pickle, save_pickle = True)


