from dazer_methods import Dazer
from uncertainties import unumpy
from collections import OrderedDict
from pylatex import Package, NoEscape

#Import library object
dz = Dazer()

#Load observational data
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
dz.quick_indexing(catalogue_df)

#Define data to load
ext_data        = '_emis2nd'
pdf_address     = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/AbundancesTable'

#Headers
headers_dic = OrderedDict()
headers_dic['HeI_HI']   = r'$\nicefrac{He}{H}$'
headers_dic['Ymass_O']  = r'$Y_{\left(\nicefrac{O}{H}\right)}$'
headers_dic['Ymass_S']  = r'$Y_{\left(\nicefrac{S}{H}\right)}$'
headers_dic['OI_HI']    = r'$12 + log\left(\nicefrac{O}{H}\right)$'
headers_dic['NI_HI']    = r'$12 + log\left(\nicefrac{N}{H}\right)$'
headers_dic['SI_HI']    = r'$12 + log\left(\nicefrac{S}{H}\right)$'
headers_dic['He-O']   = r'$He-O$'
headers_dic['He-N']   = r'$He-N$'
headers_dic['He-S']   = r'$He-S$'

properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
headers_format  = ['HII Galaxy'] + headers_dic.values()

#Create a new list for the different entries
metals_list   = properties_list[:]

del metals_list[metals_list.index('HeI_HI' + ext_data)]
del metals_list[metals_list.index('Ymass_O' + ext_data)]
del metals_list[metals_list.index('Ymass_S' + ext_data)]
del metals_list[metals_list.index('He-O' + ext_data)]
del metals_list[metals_list.index('He-N' + ext_data)]
del metals_list[metals_list.index('He-S' + ext_data)]

#Generate pdf
# dz.create_pdfDoc(pdf_address, pdf_type='table')
# dz.pdfDoc.packages.append(Package('nicefrac'))
# dz.pdfDoc.packages.append(Package('pifont'))
# dz.pdfDoc.append(NoEscape(r'\newcommand{\cmark}{\ding{51}}')) 
# dz.pdfDoc.append(NoEscape(r'\newcommand{\xmark}{\ding{55}}')) 

#Set the pdf format
dz.pdf_insert_table(headers_format)

for objName in catalogue_df.loc[dz.idx_include].index:
    
    entry_name      = '{slash}href{{{url}}}{{{text}}}'.format(slash='\\',url=catalogue_df.loc[objName].SDSS_Web,text=catalogue_df.loc[objName].quick_index).replace('&','\&')
    
    objData         = catalogue_df.loc[objName]
    abundValues     = objData[metals_list].values
    objData[metals_list] = 12.0 + unumpy.log10(abundValues)
    
    HeI_HI_entry    = dz.format_for_table(catalogue_df.loc[objName, 'HeII_HII_from_O' + ext_data], rounddig=3, rounddig_er=2)
    Ymass_O_entry   = dz.format_for_table(catalogue_df.loc[objName, 'Ymass_O' + ext_data], rounddig=3, rounddig_er=2)
    Ymass_S_entry   = dz.format_for_table(catalogue_df.loc[objName, 'Ymass_S' + ext_data], rounddig=3, rounddig_er=2)
    
    row             = [entry_name] + [HeI_HI_entry, Ymass_O_entry, Ymass_S_entry]
    row             += list(objData[['OI_HI' + ext_data, 'NI_HI' + ext_data, 'SI_HI' + ext_data]].values)
    
    for element in ['O', 'N', 'S']:
        validity_entry = catalogue_df.loc[objName, element + '_valid']
        if validity_entry not in ['ignored', 'NO_excess', 'Wide Component']:
            entry = '\ding{51}'
        else:
            entry = '\ding{55}'
        row += [entry]
            
    dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)

# dz.generate_pdf()   
dz.generate_pdf(output_address=pdf_address)

