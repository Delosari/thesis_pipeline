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
headers = ['Reference', 'Measured value']

#Generate pdf
#dz.create_pdfDoc(pdf_address, pdf_type='table')
dz.pdf_insert_table(headers)

for reference in df.index:

    author, value, error, year, comments, upper_limit = df.loc[reference, df.columns].values
    print upper_limit,
    column1 = '{} ({})'.format(author.replace('&','\&'), year)#.replace("'",'\textquotesingle')
    if upper_limit != 'yes':
        column2 = '${}\pm{}$'.format(value,error)
    else:
        column2 = '$\leq{}$'.format(value)

    print column1, column2

    dz.addTableRow([column1, column2], last_row = False if df.index[-1] != reference else True)

#dz.generate_pdf(clean_tex=False)
dz.generate_pdf(output_address=pdf_address)