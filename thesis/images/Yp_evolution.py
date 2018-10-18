import pandas as pd
from dazer_methods import Dazer


#Import library object
dz = Dazer()

#Read table data
df = pd.read_excel('/home/vital/Dropbox/Astrophysics/Thesis/notes/table_yp_literature.xlsx', sheetname='Sheet1')

#Define plot frame and colors
size_dict = {'figure.figsize' : (18, 8), 'axes.labelsize':28, 'legend.fontsize':35, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':28, 'ytick.labelsize':28}
dz.FigConf(plotStyle='colorblind', plotSize = size_dict)

# Generate the color map
dz.gen_colorList(0, df.index.size)

marker_dict = {'Peimbert':'s', 'Skillman':'^', 'Izotov':'o'}

#Loop through the lines
for i in range(df.index.size):

    author, value, error, year, comments, upper_limit, group = df.iloc[i].values

    marker_type = '_' if group not in marker_dict else marker_dict[group]

    if error < 0.236:
        if author == 'Planck collaboration' and year == 2015:
            label = r'Planck collaboration 2018: $Y_{P}=0.24672^{-(0.00012)0.00061}_{ +(0.00011)0.00061}$'
            dz.Axis.axhspan(value-error, value + error, alpha = 0.5, label = label, color='saddlebrown')
        else:
            dz.data_plot(year, value, label = '', markerstyle=marker_type, markersize=50, y_error=error, color='black')

dz.Axis.set_ylim(0.18, 0.28)
dz.FigWording(r'Year', r'$Y_{P}$', '', loc=8)
#dz.savefig('/home/vital/Dropbox/Astrophysics/Thesis/images/Yp_references_evolution')
dz.display_fig()


# import pandas as pd
# from dazer_methods import Dazer
#
#
# #Import library object
# dz = Dazer()
#
# #Read table data
# df = pd.read_excel('/home/vital/Dropbox/Astrophysics/Thesis/notes/table_yp_literature.xlsx', sheetname='Sheet1')
#
# #Define plot frame and colors
# size_dict = {'axes.labelsize':28, 'legend.fontsize':18, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':28, 'ytick.labelsize':28}
# dz.FigConf(plotStyle='colorblind', plotSize = size_dict)
#
# # Generate the color map
# dz.gen_colorList(0, df.index.size)
#
# #Loop through the lines
# for i in range(df.index.size):
#
#     author, value, error, year, comments, upper_limit = df.iloc[i].values
#     if error < 0.236:
#         if author == 'Planck collaboration' and year == 2015:
#             dz.Axis.axhspan(value-error, value + error, alpha = 0.5, label = '{} ({})'.format(author, year), color='saddlebrown')
#         else:
#             dz.data_plot(year, value, label = '', markerstyle='o', y_error=error, color=dz.get_color(i))
#
# dz.Axis.set_ylim(0.18, 0.28)
# dz.FigWording(r'Year', r'$Y_{P}$', '', loc=4)
# dz.savefig('/home/vital/Dropbox/Astrophysics/Thesis/images/Yp_references_evolution')
# #dz.display_fig()


