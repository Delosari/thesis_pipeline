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
pdf_address     = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/tables/ionicAbundancesTable'

#Headers
headers_dic  = OrderedDict()
headers_dic['HeII_HII_from_O']  = r'$\nicefrac{He^{+}}{H^{+}}$'
headers_dic['HeIII_HII_from_O'] = r'$\nicefrac{He^{2+}}{H^{+}}$'
headers_dic['OII_HII']          = r'$12 + log\left(\nicefrac{O^{+}}{H^{+}}\right)$'
headers_dic['OIII_HII']         = r'$12 + log\left(\nicefrac{O^{2+}}{H^{+}}\right)$'
headers_dic['NII_HII']          = r'$12 + log\left(\nicefrac{N^{+}}{H^{+}}\right)$'
headers_dic['SII_HII']          = r'$12 + log\left(\nicefrac{S^{+}}{H^{+}}\right)$'
headers_dic['SIII_HII']         = r'$12 + log\left(\nicefrac{S^{2+}}{H^{+}}\right)$'
headers_dic['ICF_SIV']          = r'$ICF\left(S^{3+}\right)$'
headers_dic['ArIII_HII']        = r'$12 + log\left(\nicefrac{Ar^{2+}}{H^{+}}\right)$'
headers_dic['ArIV_HII']         = r'$12 + log\left(\nicefrac{Ar^{3+}}{H^{+}}\right)$'

properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
headers_format  = ['HII Galaxy'] + headers_dic.values()[0:5]

#Create a new list for the different entries
metals_list   = properties_list[:]
del metals_list[metals_list.index('ICF_SIV' + ext_data)]
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

headers_format  = ['HII Galaxy'] + headers_dic.values()[5:]
dz.addTableRow(headers_format, last_row = True)

for objName in catalogue_df.loc[dz.idx_include].index:
    
    entry_name   = '{slash}href{{{url}}}{{{text}}}'.format(slash='\\',url=catalogue_df.loc[objName].SDSS_Web,text=catalogue_df.loc[objName].quick_index).replace('&','\&')
    
    objData     = catalogue_df.loc[objName]
    abundValues = objData[metals_list].values
    objData[metals_list] = 12.0 + unumpy.log10(abundValues)
     
    row         = [entry_name] 
    row         += list(objData[['SII_HII' + ext_data, 'SIII_HII' + ext_data, 'ICF_SIV' + ext_data, 'ArIII_HII' + ext_data, 'ArIV_HII' + ext_data]].values)
    
    dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=2)    
    
dz.generate_pdf(output_address=pdf_address)



