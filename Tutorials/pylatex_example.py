# '''
# Created on Oct 12, 2015
# 
# @author: vital
# '''
# import numpy as np
#  
# from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
#     Plot, Figure, Package
# from pylatex.numpy import Matrix
# from pylatex.utils import italic, escape_latex
#  
# doc = Document()
# doc.packages.append(Package('geometry', options=['tmargin=1cm',
#                                                  'lmargin=10cm']))
#  
# with doc.create(Section('The simple stuff')):
#     doc.append('Some regular text and some ' + italic('italic text. '))
#     doc.append(escape_latex('\nAlso some crazy characters: $&#{}'))
#     with doc.create(Subsection('Math that is incorrect')) as math:
#         doc.append(Math(data=['2*3', '=', 9]))
#  
#     with doc.create(Subsection('Table of something')):
#         with doc.create(Table('rc|cl')) as table:
#             table.add_hline()
#             table.add_row((1, 2, 3, 4))
#             table.add_hline(1, 2)
#             table.add_empty_row()
#             table.add_row((4, 5, 6, 7))
#  
# a = np.array([[100, 10, 20]]).T
# M = np.matrix([[2, 3, 4],
#                [0, 0, 1],
#                [0, 0, 2]])
#  
# with doc.create(Section('The fancy stuff')):
#     with doc.create(Subsection('Correct matrix equations')):
#         doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M*a)]))
#  
#     with doc.create(Subsection('Beautiful graphs')):
#         with doc.create(TikZ()):
#             plot_options = 'height=6cm, width=6cm, grid=major'
#             with doc.create(Axis(options=plot_options)) as plot:
#                 plot.append(Plot(name='model', func='-x^5 - 242'))
#  
#                 coordinates = [
#                     (-4.77778, 2027.60977),
#                     (-3.55556, 347.84069),
#                     (-2.33333, 22.58953),
#                     (-1.11111, -493.50066),
#                     (0.11111, 46.66082),
#                     (1.33333, -205.56286),
#                     (2.55556, -341.40638),
#                     (3.77778, -1169.24780),
#                     (5.00000, -3269.56775),
#                 ]
#  
#                 plot.append(Plot(name='estimate', coordinates=coordinates))
#  
# #     with doc.create(Subsection('Cute kitten pictures')):
# #         with doc.create(Figure(position='h!')) as kitten_pic:
# #             kitten_pic.add_image('docs/static/kitten.jpg', width='120px')
# #             kitten_pic.add_caption('Look it\'s on its back')
#  
# doc.generate_pdf()
#Table example

from pylatex import Document, Section, Subsection, Tabular, MultiColumn,\
    MultiRow
 
doc = Document("multirow")
section = Section('Multirow Test')
 
test1 = Subsection('MultiColumn')
test2 = Subsection('MultiRow')
test3 = Subsection('MultiColumn and MultiRow')
test4 = Subsection('Vext01')
test5 = Subsection('Otra')

table1 = Tabular('|c|c|c|c|')
table1.add_hline()
table1.add_row((MultiColumn(4, '|c|', 'Multicolumn'),))
table1.add_hline()
table1.add_row((1, 2, 3, 4))
table1.add_hline()
table1.add_row((5, 6, 7, 8))
table1.add_hline()
row_cells = ('9', MultiColumn(3, '|c|', 'Multicolumn not on left'))
table1.add_row(row_cells)
table1.add_hline()
 
table2 = Tabular('|c|c|c|')
table2.add_hline()
table2.add_row((MultiRow(3, '*', 'Multirow'), 1, 2))
table2.add_hline(2, 3)
table2.add_row(('', 3, 4))
table2.add_hline(2, 3)
table2.add_row(('', 5, 6))
table2.add_hline()
table2.add_row((MultiRow(3, '*', 'Multirow2'), '', ''))
table2.add_empty_row()
table2.add_empty_row()
table2.add_hline()
 
table3 = Tabular('|c|c|c|')
table3.add_hline()
table3.add_row((MultiColumn(2, '|c|', MultiRow(2, '*', 'multi-col-row')), 'X'))
table3.add_row((MultiColumn(2, '|c|', ''), 'X'))
table3.add_hline()
table3.add_row(('X', 'X', 'X'))
table3.add_hline()
 
table4 = Tabular('|c|c|c|')
table4.add_hline()
col1_cell = MultiRow(4, '*', 'span-4')
col2_cell = MultiRow(2, '*', 'span-2')
table4.add_row((col1_cell, col2_cell, '3a'))
table4.add_hline(3)
table4.add_row(('', '', '3b'))
table4.add_hline(2)
table4.add_row(('', col2_cell, '3c'))
table4.add_hline(3)
table4.add_row(('', '', '3d'))
table4.add_hline()

my_line = [1,2,3,4]
table5 = Tabular('c|c|c|c')
table5.add_hline()
table5.add_row((1, 2.589, 3, 4))
table5.add_empty_row()
table5.add_row((4, 5, 6, 7)) 
 
test1.append(table1)
test2.append(table2)
test3.append(table3)
test4.append(table4)
test5.append(table5)
  
section.append(test1)
section.append(test2)
section.append(test3)
section.append(test4)
section.append(test5)

doc.append(section)
doc.generate_pdf(clean=False)
