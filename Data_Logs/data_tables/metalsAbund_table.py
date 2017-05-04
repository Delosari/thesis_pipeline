from dazer_methods import Dazer
from uncertainties import unumpy
from collections import OrderedDict

#Import library object
dz = Dazer()

#Load observational data
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Define data to load
ext_data        = '_emis2nd'
pdf_address     = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/data/MetalsAbund_table'

#Headers
headers_dic  = OrderedDict()
headers_dic['SI_HI']     = r'$12 + log(\frac{S}{H})$'
headers_dic['SII_HII']   = r'$12 + log(\frac{S^{+}}{H^{+}})$'
headers_dic['SIII_HII']  = r'$12 + log(\frac{S^{+2}}{H^{+}})$'
headers_dic['SIV_HII']   = r'$12 + log(\frac{S^{+3}}{H^{+}})$'
headers_dic['ICF_SIV']   = r'$ICF(S^{+3})$'
headers_dic['ArIII_HII'] = r'$12 + log(\frac{Ar^{+2}}{H^{+}})$'
headers_dic['ArIV_HII']  = r'$12 + log(\frac{Ar^{+3}}{H^{+}})$'
headers_dic['OI_HI']     = r'$12 + log(\frac{O}{H})$'
headers_dic['OII_HII']   = r'$12 + log(\frac{O^{+}}{H^{+}})$'
headers_dic['OIII_HII']  = r'$12 + log(\frac{O^{+2}}{H^{+}})$'
headers_dic['NI_HI']     = r'$12 + log(\frac{N}{H})$'
headers_dic['NII_HII']   = r'$12 + log(\frac{N^{+}}{H^{+}})$'

properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
headers_format  = ['HII Galaxy', 'SDSS reference'] + headers_dic.values()

#Create a new list for the different entries
abund_entries   = properties_list[:]
del abund_entries[abund_entries.index('ICF_SIV' + ext_data)]

print 'Headers for table', headers_format
print 'Properties from df', properties_list
print 'Abund properties df', abund_entries

#Generate pdf
dz.create_pdfDoc(pdf_address, pdf_type='table')
 
#Set the pdf format
dz.pdf_insert_table(headers_format)

for objName in catalogue_df.index:
    
    try:
        
        objData     = catalogue_df.loc[objName]
        abundValues = objData[abund_entries].values
    #     print '--', objName
    #     for i in range(len(abund_entries)):
    #         print abund_entries[i], abundValues[i]
        
        objData[abund_entries]  = 12.0 + unumpy.log10(abundValues)
            
        row         = [objName.replace('_','-'), catalogue_df.loc[objName, 'SDSS_reference']] + list(objData[properties_list].values)
        dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True)
    
    except:
        print 'OBJECT', objName, 'FAILED'
        
    
dz.generate_pdf()



