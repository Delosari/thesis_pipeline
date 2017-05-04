from dazer_methods import Dazer
from uncertainties import unumpy
from collections import OrderedDict

#Import library object
dz = Dazer()

#Load observational data
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Define data to load
ext_data        = '_emis'
pdf_address     = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/data/HeliumAbund_table'

#Headers
headers_dic  = OrderedDict()
headers_dic['HeII_HII_from_S']  = r'$\big(\frac{He^{+}}{H^{+}}\big)_{S}$'
headers_dic['HeIII_HII_from_S'] = r'$\big(\frac{He^{+2}}{H^{+}}\big)_{S}$'
headers_dic['HeII_HII_from_O']  = r'$\big(\frac{He^{+}}{H^{+}}\big)_{O}$'
headers_dic['HeIII_HII_from_O'] = r'$\big(\frac{He^{+2}}{H^{+}}\big)_{O}$'
headers_dic['HeI_HI_from_O']    = r'$\big(\frac{He}{H}\big)_{O}$'
headers_dic['HeI_HI_from_S']    = r'$\big(\frac{He}{H}\big)_{S}$'
headers_dic['Ymass_O']          = r'$Y_{O}$'
headers_dic['Ymass_S']          = r'$Y_{S}$'

properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
headers_format  = ['HII Galaxy', 'SDSS reference'] + headers_dic.values()

print 'Headers for table', headers_format
print 'Properties from df', properties_list
 
#Generate pdf
dz.create_pdfDoc(pdf_address, pdf_type='table')
 
#Set the pdf format
dz.pdf_insert_table(headers_format)


for objName in catalogue_df.index:
    abundValues = catalogue_df.loc[objName, properties_list].values
    row         = [objName.replace('_','-'), catalogue_df.loc[objName, 'SDSS_reference']] + list(abundValues)
    dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True)
 
dz.generate_pdf()





