from dazer_methods import Dazer
from pylatex import Package
#Import library object
dz = Dazer()

#Load observational data
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Define data to load
ext_data        = '_emis2nd'
pdf_address     = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/data/properties_table'

#Headers
properties_list = ['neSII', 'TeSIII', 'TeOIII'] 
properties_list = map(( lambda x: x + ext_data), properties_list)
properties_list = ['SDSS_reference'] + properties_list
headers_format  = ['HII Galaxy',
                   'SDSS reference', 
                   r'$n_{e}[SII](cm^{-3})$',
                   r'$T_{e}[SIII](K)$',
                   r'$T_{e}[OIII](K)$']

#Generate pdf
dz.create_pdfDoc(pdf_address, pdf_type='table')
dz.pdfDoc.packages.append(Package('color', options=['usenames', 'dvipsnames',]))

#Set the pdf format
dz.pdf_insert_table(headers_format)
 
for objName in catalogue_df.index:
    row = [objName.replace('_','-')] + list(catalogue_df.loc[objName, properties_list].values)
    dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True)

dz.generate_pdf(clean_tex=False)

print 'Table generated'