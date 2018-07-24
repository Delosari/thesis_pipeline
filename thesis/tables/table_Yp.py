import pandas as pd
from dazer_methods import Dazer
from pandas import ExcelWriter
from pandas import ExcelFile
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

#Import library object
dz = Dazer()

#Read table data
df = pd.read_excel('/home/vital/Dropbox/Astrophysics/Thesis/notes/table_yp_literature.xlsx', sheetname='Sheet1')

#print df.iloc[5].Author.replace("'", "\textquotesingle")

#Define data to load
pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/tables/Yp_references'
headers = ['Reference', 'Published value', 'Reference', 'Published value']


df1 = df[:27]
df2 = df[27:]

#Generate pdf
dz.create_pdfDoc(pdf_address, pdf_type='table')
dz.pdf_insert_table(headers)

for i in range(27):

    print df1.iloc[i].Author, df2.iloc[i].Author

    author1, value1, error1, year1, comments1, upper_limit1 = df1.iloc[i].values
    author2, value2, error2, year2, comments2, upper_limit2 = df2.iloc[i].values

    column1 = '{} ({})'.format(author1.replace('&','\&'), year1)#.replace("'",'\textquotesingle')
    column3 = '{} ({})'.format(author2.replace('&','\&'), year2)#.replace("'",'\textquotesingle')

    if upper_limit1 != 'yes':
        column2 = '${}\pm{}$'.format(value1,error1)
    else:
        column2 = '$\leq{}$'.format(value1)

    if upper_limit2 != 'yes':
        column4 = '${}\pm{}$'.format(value2,error2)
    else:
        column4 = '$\leq{}$'.format(value2)

    print column1, column2

    dz.addTableRow([column1, column2,column3,column4], last_row = False if i != 26 else True)

#dz.generate_pdf(clean_tex=False)
dz.generate_pdf(output_address=pdf_address)

#Define data to load
# pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/tables/Yp_references'
# headers = ['Reference', 'Measured value', ]
#
# print df.index.values
#
# #Generate pdf
# #dz.create_pdfDoc(pdf_address, pdf_type='table')
# dz.pdf_insert_table(headers)
#
# for reference in df.index:
#
#     author, value, error, year, comments, upper_limit = df.loc[reference, df.columns].values
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