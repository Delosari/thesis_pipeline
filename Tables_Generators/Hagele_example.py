'''
Created on Nov 20, 2015

@author: vital
'''

from pylatex import Document, Section, Subsection, Tabular, MultiColumn, Table, MultiRow, Package, Figure

#Generate Document with its address and class
doc = Document('/home/vital/Desktop/myHageleTable', documentclass='mn2e')

#State preamble commands
doc.preamble.append(r'\setcounter{table}{0}')

#Load packages
doc.packages.append(Package('preview', options=['active', 'tightpage',])) #Package to crop pdf to a figure

#Table pre-commands

doc.append(r'\begin{table*}')
doc.append(r'\begin{preview}') 
doc.append(r'{\footnotesize')
doc.append(r'\centering')

#Declare table
with doc.create(Table('l c c c c c c c')) as tab:
    
    row1 = ['Date'  , 'Spectral range',     'Disp.' ,   'R$^a_{\rm{FWHM}}$',    'Spatial res.' ,            'PA',          'Exposure Time' ,  r'{seeing $_{\rm{FWHM}}$}']
    row2 = [' '     , '(\AA\,px$^{-1}$)',   ' ' ,       ' ',                    '("\,px$^{-1}$)' ,         '($ ^{o} $)',   '(sec)' ,         '($"$)']
    row3 = ['2000 February 4' ,             '4779-5199','0.21',                 '$\sim$\,12500'  ,          '0.38'  ,       '50'    ,        '3\,$\cdot$\,1200' , '{1.2}']
    row4 = ['',                             '8363-8763','0.39',                 '$\sim$\,12200'  ,          '0.36'  ,       '50'    ,        '3\,$\cdot$\,1200' , ' ']
    row5 = ['2000 February 5' ,             '4779-5199','0.21',                 '$\sim$\,12500'  ,          '0.38'  ,       '50'    ,        '3\,$\cdot$\,1200' , '{1.2}']
    row6 = ['',                             '8363-8763','0.39',                 '$\sim$\,12200'  ,          '0.36'  ,       '50'    ,        '3\,$\cdot$\,1200' , ' ']
    row7 = MultiRow(7, '|l|', '$^a$R$_{\rm{FWHM}}$\,=\,$\lambda$/$\Delta\lambda_{\rm{FWHM}}$') 
  
    tab.add_hline()
    tab.add_row(row1)
    tab.add_row(row2)
    tab.add_hline()
    tab.add_row(row3)
    tab.add_row(row4)
    tab.add_row(row5)
    tab.add_row(row6)
    tab.add_hline()
    tab.add_row(row7)

#Declare table after comands
doc.append('}')
doc.append(r'\end{preview}')               
doc.append(r'\end{table*}')

#Generate pdf files
doc.generate_pdf(clean=False)


# section = Section('Multirow Test')
#  
# test1 = Subsection('MultiColumn')
# test2 = Subsection('MultiRow')
# test3 = Subsection('MultiColumn and MultiRow')
# test4 = Subsection('Vext01')
#  
# table1 = Tabular('|c|c|c|c|')
# table1.add_hline()
# table1.add_row((MultiColumn(4, '|c|', 'Multicolumn'),))
# table1.add_hline()
# table1.add_row((1, 2, 3, 4))
# table1.add_hline()
# table1.add_row((5, 6, 7, 8))
# table1.add_hline()
# row_cells = ('9', MultiColumn(3, '|c|', 'Multicolumn not on left'))
# table1.add_row(row_cells)
# table1.add_hline()
#  
# table2 = Tabular('|c|c|c|')
# table2.add_hline()
# table2.add_row((MultiRow(3, '*', 'Multirow'), 1, 2))
# table2.add_hline(2, 3)
# table2.add_row(('', 3, 4))
# table2.add_hline(2, 3)
# table2.add_row(('', 5, 6))
# table2.add_hline()
# table2.add_row((MultiRow(3, '*', 'Multirow2'), '', ''))
# table2.add_empty_row()
# table2.add_empty_row()
# table2.add_hline()
#  
# table3 = Tabular('|c|c|c|')
# table3.add_hline()
# table3.add_row((MultiColumn(2, '|c|', MultiRow(2, '*', 'multi-col-row')), 'X'))
# table3.add_row((MultiColumn(2, '|c|', ''), 'X'))
# table3.add_hline()
# table3.add_row(('X', 'X', 'X'))
# table3.add_hline()
#  
# table4 = Tabular('|c|c|c|')
# table4.add_hline()
# col1_cell = MultiRow(4, '*', 'span-4')
# col2_cell = MultiRow(2, '*', 'span-2')
# table4.add_row((col1_cell, col2_cell, '3a'))
# table4.add_hline(3)
# table4.add_row(('', '', '3b'))
# table4.add_hline(2)
# table4.add_row(('', col2_cell, '3c'))
# table4.add_hline(3)
# table4.add_row(('', '', '3d'))
# table4.add_hline()
#  
# test1.append(table1)
# test2.append(table2)
# test3.append(table3)
# test4.append(table4)
#  
# section.append(test1)
# section.append(test2)
# section.append(test3)
# section.append(test4)
#  
# doc.append(section)
# doc.generate_pdf(clean=False)

