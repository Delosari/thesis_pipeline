'''
Created on Jan 16, 2017

@author: vital
'''

import pandas as pd

# Create a Pandas dataframe from some data.
df = pd.DataFrame(zip(
    [1010, 2020, 3030, 2020, 1515, 3030, 4545],
    [.1, .2, .33, .25, .5, .75, .45],
    [.1, .2, .33, .25, .5, .75, .45],
))

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('/home/vital/Desktop/test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter objects from the dataframe writer object.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Add some cell formats.
format1 = workbook.add_format({'num_format': '#,##0.00'})
format2 = workbook.add_format({'num_format': '0%'})
format3 = workbook.add_format({'num_format': 'h:mm:ss AM/PM'})

# Set the column width and format.
worksheet.set_column('B:B', 18, format1)

# Set the format but not the column width.
worksheet.set_column('C:C', None, format2)

worksheet.set_column('D:D', 16, format3)

# Close the Pandas Excel writer and output the Excel file.
writer.save()