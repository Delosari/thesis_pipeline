from dazer_methods import Dazer
from uncertainties import unumpy
from collections import OrderedDict
from pylatex import Package

#Import library object
dz = Dazer()

#Load observational data
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
dz.quick_indexing(catalogue_df)

#Define data to load
ext_data        = '_emis2nd'
pdf_address     = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/tables/ionicAbundancesTable_SAr'

#Headers
headers_dic  = OrderedDict()
headers_dic['SII_HII']          = r'$12 + log\left(\nicefrac{S^{+}}{H^{+}}\right)$'
headers_dic['SIII_HII']         = r'$12 + log\left(\nicefrac{S^{2+}}{H^{+}}\right)$'
headers_dic['ICF_SIV']          = r'$ICF\left(S^{3+}\right)$'
headers_dic['ArIII_HII']        = r'$12 + log\left(\nicefrac{Ar^{2+}}{H^{+}}\right)$'
headers_dic['ArIV_HII']         = r'$12 + log\left(\nicefrac{Ar^{3+}}{H^{+}}\right)$'

properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
headers_format  = ['HII Galaxy'] + headers_dic.values()

#Create a new list for the different entries
metals_list   = properties_list[:]
del metals_list[metals_list.index('ICF_SIV' + ext_data)]

#Set the pdf format
dz.pdf_insert_table(headers_format)

for objName in catalogue_df.loc[dz.idx_include].index:

    entry_name   = '{slash}href{{{url}}}{{{text}}}'.format(slash='\\',url=catalogue_df.loc[objName].SDSS_Web,text=catalogue_df.loc[objName].quick_index).replace('&','\&')
    
    objData     = catalogue_df.loc[objName]
    abundValues = objData[metals_list].values
    objData[metals_list] = 12.0 + unumpy.log10(abundValues)
     
    row         = [entry_name] 
    row         += list(objData[['SII_HII' + ext_data, 'SIII_HII' + ext_data, 'ICF_SIV' + ext_data, 'ArIII_HII' + ext_data, 'ArIV_HII' + ext_data]].values)
    
    dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=2)    
    
dz.generate_pdf(output_address=pdf_address)



