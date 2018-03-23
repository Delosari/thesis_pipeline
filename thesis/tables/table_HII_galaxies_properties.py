import pandas as pd
from dazer_methods import Dazer

#Import library object
dz = Dazer()

#Read table data
df = pd.read_excel('/home/vital/Dropbox/Astrophysics/Thesis/notes/HII_galaxies_properties.xlsx', sheetname='Sheet1')

#print df.iloc[5].Author.replace("'", "\textquotesingle")

#Define data to load
pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/tables/HII_galaxies_properties'
headers = ['Parameters range']

#Generate pdf
#dz.create_pdfDoc(pdf_address, pdf_type='table')
dz.pdf_insert_table(headers, table_format='c')

for reference in df.index:

    low_limit, parameter, upper_limit, unit = df.loc[reference, df.columns].values

    if not pd.isnull(unit):
        unit = [unit.split(',')[0], unit.split(',')[1]] if ',' in unit else [unit, unit]
    else:
        unit = ['','']

    if not pd.isnull(upper_limit):
        entry = '${low}{unit0}$ < ${variable}$ < ${up}{unit1}$'.format(variable=parameter, low=low_limit, up=upper_limit, unit0=unit[0], unit1=unit[1])
    else:
        entry = '${variable}$ > ${low}{unit}$'.format(variable=parameter, low=low_limit, unit=unit[0])

    dz.addTableRow([entry], last_row = False if df.index[-1] != reference else True)

#dz.generate_pdf(clean_tex=False)
dz.generate_pdf(output_address=pdf_address)