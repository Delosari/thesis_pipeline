from dazer_methods import Dazer
from uncertainties import unumpy
from collections import OrderedDict
from pylatex import Package

#Import library object
dz = Dazer()

#Load observational data
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
dz.quick_indexing(catalogue_df)

#Headers
headers_dic  = OrderedDict()
headers_dic['HeII_HII_from_O']  = r'$\nicefrac{He^{+}}{H^{+}}$'
headers_dic['HeIII_HII_from_O'] = r'$\nicefrac{He^{2+}}{H^{+}}$'
headers_dic['OII_HII']          = r'$12 + log\left(\nicefrac{O^{+}}{H^{+}}\right)$'
headers_dic['OIII_HII']         = r'$12 + log\left(\nicefrac{O^{2+}}{H^{+}}\right)$'
headers_dic['NII_HII']          = r'$12 + log\left(\nicefrac{N^{+}}{H^{+}}\right)$'

redding_laws                = ['G03_average', 'G03_bar', 'G03_supershell']
extensioin_table            = ['_G03average', '_G03bar', '_G03superS']

for i in range(len(redding_laws)):

    pdf_address = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/tables/He_N_O_abundances_table' + extensioin_table[i] 
    
    dz.create_pdfDoc(pdf_address, pdf_type='table')
    
    ext_data = extensioin_table[i]
    
    properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
    headers_format  = ['HII Galaxy'] + headers_dic.values()
    
    #Create a new list for the different entries
    metals_list   = properties_list[:]
    del metals_list[metals_list.index('HeII_HII_from_O' + ext_data)]
    del metals_list[metals_list.index('HeIII_HII_from_O' + ext_data)]
    
    #Set the pdf format
    dz.pdf_insert_table(headers_format)
    
    for objName in catalogue_df.loc[dz.idx_include].index:
        
        entry_name   = '{slash}href{{{url}}}{{{text}}}'.format(slash='\\',url=catalogue_df.loc[objName].SDSS_Web,text=catalogue_df.loc[objName].quick_index).replace('&','\&')
        
        objData     = catalogue_df.loc[objName]
        abundValues = objData[metals_list].values
        objData[metals_list] = 12.0 + unumpy.log10(abundValues)
        
        HeII_HII_from_O_entry = dz.format_for_table(catalogue_df.loc[objName, 'HeII_HII_from_O' + ext_data], rounddig=3, rounddig_er=2)
        HeIII_HII_from_O_entry = dz.format_for_table(catalogue_df.loc[objName, 'HeIII_HII_from_O' + ext_data], rounddig=2, rounddig_er=1)
         
        row         = [entry_name] + [HeII_HII_from_O_entry, HeIII_HII_from_O_entry]
        row         += list(objData[['OII_HII' + ext_data, 'OIII_HII' + ext_data, 'NII_HII' + ext_data]].values)
        
        dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)
        
    dz.generate_pdf()



