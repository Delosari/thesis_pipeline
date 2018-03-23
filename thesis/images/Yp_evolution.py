import pandas as pd
from dazer_methods import Dazer


#Import library object
dz = Dazer()

#Read table data
df = pd.read_excel('/home/vital/Dropbox/Astrophysics/Thesis/notes/table_yp_literature.xlsx', sheetname='Sheet1')

#Define plot frame and colors
size_dict = {'axes.labelsize':28, 'legend.fontsize':18, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':28, 'ytick.labelsize':28}
dz.FigConf(plotStyle='colorblind', plotSize = size_dict)

#Loop through the lines
for reference in df.index:

    author, value, error, year, comments, upper_limit = df.loc[reference, df.columns].values

    if author == 'Planck collaboration' and year == 2015:
        dz.Axis.axhspan(value-error, value + error, alpha = 0.5, label = '{} ({})'.format(author, year))
    else:
        dz.data_plot(year, value, label = '', markerstyle='o', y_error=error)

dz.Axis.set_ylim(0.18, 0.28)
dz.FigWording(r'Year', r'$Y_{P}$', '', loc=4)
# dz.display_fig()
dz.savefig('/home/vital/Dropbox/Astrophysics/Thesis/images/Yp_references_evolution')








#     print upper_limit,
#     column1 = '{} ({})'.format(author.replace('&','\&'), year)#.replace("'",'\textquotesingle')
#     if upper_limit != 'yes':
#         column2 = '${}\pm{}$'.format(value,error)
#     else:
#         column2 = '$\leq{}$'.format(value)
#
#     print column1, column2
#
#     dz.addTableRow([column1, column2], last_row = False if df.index[-1] != reference else True)
#
# #dz.generate_pdf(clean_tex=False)
# dz.generate_pdf(output_address=pdf_address)

