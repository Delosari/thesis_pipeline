import  pandas              as pd
import  numpy               as np
import  matplotlib.pyplot   as plt
from    dazer_methods       import Dazer
from    matplotlib.ticker   import NullFormatter
from    matplotlib          import rcParams

def distinguis_error(error_entry):

    error_entry = str(error_entry)

    if '+' in error_entry:
        error_array = error_entry.split('-')
        uplim, lowlim = float(error_array[0]), float(error_array[1])
    else:
        uplim, lowlim = float(error_entry), (error_entry)
        
    return uplim, lowlim

def load_data_from_df(x_key, y_key, df):

    #Check how many entries are not null
    valid_regions       = np.sum(df[[x_key, y_key, x_key + '_error', y_key + '_error']].notnull().values)
    x_mag, y_mag        = np.zeros(valid_regions), np.zeros(valid_regions)
    x_uplim, y_uplim     = np.zeros(valid_regions), np.zeros(valid_regions) 
    x_lowlim, y_lowlim   = np.zeros(valid_regions), np.zeros(valid_regions) 
    
    for i in range(len(df.index)):
        
        region = df.iloc[i].name
        check_param_error = np.all(df.loc[region, [x_key, y_key, x_key + '_error', y_key + '_error']].notnull().values)
        
        if check_param_error:
            
            x_mag[i], y_mag[i], xerr_entry, yerr_entry = df.loc[region, [x_key, y_key, x_key + '_error', y_key + '_error']].values
            
            x_uplim[i], x_lowlim[i] = distinguis_error(xerr_entry)
            y_uplim[i], y_lowlim[i] = distinguis_error(yerr_entry)
            
    return x_mag, y_mag, [x_lowlim, x_uplim], [y_lowlim, y_uplim]

def load_data_from_df_limit(x_key, y_key, df):

    #Check how many entries are not null
    valid_regions       = np.sum(df[[x_key, y_key, x_key + '_error', y_key + '_error']].notnull().values)
    x_mag, y_mag        = np.zeros(valid_regions), np.zeros(valid_regions)
    x_uplim, y_uplim     = np.zeros(valid_regions), np.zeros(valid_regions) 
    x_lowlim, y_lowlim   = np.zeros(valid_regions), np.zeros(valid_regions) 
    
    for i in range(len(df.index)):
        
        region = df.iloc[i].name
        check_param_error = np.all(df.loc[region, [x_key, y_key, x_key + '_error', y_key + '_error']].notnull().values)
        
        if check_param_error:
            
            x_mag_ent, y_mag_ent, xerr_entry, yerr_entry = df.loc[region, [x_key, y_key, x_key + '_error', y_key + '_error']].values
            
            x_uplim_ent, x_lowlim_ent = distinguis_error(xerr_entry)
            y_uplim_ent, y_lowlim_ent = distinguis_error(yerr_entry)
            
            mean_xerror = ((x_uplim_ent + x_lowlim_ent) / 2.0) / x_mag_ent
            mean_yerror = ((y_uplim_ent + y_lowlim_ent) / 2.0) / y_mag_ent
            
            if (mean_xerror < 0.1) and (mean_yerror < 0.1):
                
                x_mag[i] 
            
    return x_mag, y_mag, [x_lowlim, x_uplim], [y_lowlim, y_uplim]

def figure_formatting():
  
    sizing_dict = {}
    sizing_dict['figure.figsize'] = (12, 9)
    sizing_dict['legend.fontsize']  = 15
    sizing_dict['axes.labelsize']   = 20
    sizing_dict['axes.titlesize']   = 24
    sizing_dict['xtick.labelsize']  = 14
    sizing_dict['ytick.labelsize']  = 14
    rcParams.update(sizing_dict)
    #plt.style.use('seaborn-colorblind')
 
    #Figure configuration
    left, width     = 0.1, 0.65
    bottom, height  = 0.1, 0.65
    bottom_h        = left_h = left + width + 0.02
     
    rect_scatter    = [left, bottom, width, height]
    rect_histx      = [left, bottom_h, width, 0.2]
    rect_histy      = [left_h, bottom, 0.2, height]
     
    Fig             = plt.figure(1)
    axScatter       = plt.axes(rect_scatter)
    axHistx         = plt.axes(rect_histx)
    axHisty         = plt.axes(rect_histy)
    axHistx.xaxis.set_major_formatter(NullFormatter())  #No x ticks labels
    axHisty.yaxis.set_major_formatter(NullFormatter())  #No x ticks labels 
     
    return Fig, axScatter, axHistx, axHisty
 
def histogram_bining(binsize, data):
     
    min_data, max_data = np.min(data), np.max(data)
    num_bins = np.floor((max_data - min_data) / binsize)
     
    return num_bins, min_data, max_data
 
#Import plotting class
  
def hist_scattering_plot(x_data, y_data, label_data, x_error, y_error, color='black', objects = None):
     
    #Bining for histograms
    num_x_bins, min_x_data, max_x_data = histogram_bining(500, x_data) 
    num_y_bins, min_y_data, max_y_data = histogram_bining(1000, y_data)
     
    #Make plots
    axScatter.errorbar(x_data, y_data, label=label_data, xerr = x_error, yerr = y_error, color = color, ecolor='grey', fmt='o')
    
    if objects != None:        
        dz.plot_text(x_data, y_data, objects, axis_plot=axScatter)        
    
    axHistx.hist(x_data, bins=num_x_bins, color = color)
    axHisty.hist(y_data, bins=num_y_bins, orientation='horizontal', color = color)
     
    return
 
def axis_formatting(x_lim_min, x_lim_max, y_lim_min, y_lim_max, x_label, y_label):
     
#     axScatter.set_xlim(x_lim_min, x_lim_max)
#     axScatter.set_ylim(y_lim_min, y_lim_max)
    
#     axScatter.set_xscale('log')
#     axScatter.set_yscale('log')
#     
#     axHistx.set_xlim(x_lim_min, x_lim_max)
#     axHisty.set_ylim(y_lim_min, y_lim_max)

#     axHistx.set_yscale('log')
#     axHisty.set_xscale('log')

    axScatter.set_xlabel(x_label)
    axScatter.set_ylabel(y_label)
    axHistx.set_title('Planetary nebula physical properties', y=0.98)
     
    axScatter.legend(loc='best')
     
    return
 
dz = Dazer()
 
Fig, axScatter, axHistx, axHisty = figure_formatting()
 
#Load PN database
table_address   = '/home/vital/Dropbox/Astrophysics/Papers/Determination 2photon continua/Master_table.xlsx'
pn_df           = pd.read_excel(table_address, index_col=0, header=0)

#----Using oxygen
x_key           = 'neSII'
y_key           = 'TOIII'

x_mag, y_mag, x_error, y_error = load_data_from_df(x_key, y_key, pn_df)
x_mean_error    = ((x_error[0] + x_error[1]) / 2.0) / x_mag
y_mean_error    = ((y_error[0] + y_error[1]) / 2.0) / y_mag
idx             = (x_mean_error < 0.10) & (y_mean_error < 0.10)
objects         = pn_df.loc[idx,'Simbad_name'].values
references      = pn_df.loc[idx,'Ref_code'].values
labels          = []

for i in range(len(objects)):
    label_i = '{} ({})'.format(objects[i], references[i])
    labels.append(label_i)
    print objects[i]

print objects

hist_scattering_plot(x_mag[idx], y_mag[idx], '{} - {} (error below 10% on both parameters)'.format(x_key, y_key), [x_error[0][idx], x_error[1][idx]], [y_error[0][idx], y_error[1][idx]], color = '#0072B2', objects=labels)

# x_mag, y_mag, x_error, y_error = load_data_from_df(x_key, y_key, pn_df)
# hist_scattering_plot(x_mag, y_mag, '{} - {}'.format(x_key, y_key), x_error, y_error, color = '#0072B2')

#----Using sulfur
x_key           = 'neSII'
y_key           = 'TSIII'

# x_mag, y_mag, x_error, y_error = load_data_from_df(x_key, y_key, pn_df)
# hist_scattering_plot(x_mag, y_mag, '{} - {}'.format(r'$T_e[SIII]$', r'$n_e[SII]$'), x_error, y_error, color = '#D55E00')

# x_mag, y_mag, x_error, y_error = load_data_from_df(x_key, y_key, pn_df)
# x_mean_error = ((x_error[0] + x_error[1]) / 2.0) / x_mag
# y_mean_error = ((y_error[0] + y_error[1]) / 2.0) / y_mag
# idx          = (x_mean_error < 0.15) & (y_mean_error < 0.1)
# hist_scattering_plot(x_mag[idx], y_mag[idx], '{} - {}'.format(x_key, y_key), [x_error[0][idx], x_error[1][idx]], [y_error[0][idx], y_error[1][idx]], color = '#0072B2')

#----Format of the plot
xlabel, ylabel = r'Density $(cm^{-3}$)', r'Temperature (K)'
axis_formatting(x_lim_min=0, x_lim_max=30000, y_lim_min=2000, y_lim_max=50000, x_label=xlabel, y_label=ylabel)
     
plt.show()


#         self.colorVector = {
#         'iron':'#4c4c4c',
#         'silver':'#cccccc',                  
#         'dark blue':'#0072B2',
#         'green':'#009E73', 
#         'orangish':'#D55E00',
#         'pink':'#CC79A7',
#         'yellow':'#F0E442',
#         'cyan':'#56B4E9',
#         'olive':'#bcbd22',
#         'grey':'#7f7f7f',
#         'skin':'#FFB5B8'}
        