from dazer_methods import Dazer

#Headers
plotting_Keys   = ['SDSS_reference',
                   'SDSS_Web',
                   'z_Blue', 
                   'RA',
                   'DEC',
                   'Dichroic']

headers         = ['Local reference',
                   'SDSS reference',
                   'z',
                   'RA (hh:{arcmin}:{arcsec})'.format(arcmin="'", arcsec='"'),
                   'DEC (deg:{arcmin}:{arcsec})'.format(arcmin="'", arcsec='"'),
                   'ISIS configuration']

#Import library object
dz = Dazer()

#Load observational data
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Define data to load
pdf_address     = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/tables/reference_table_noPreamble'

#Generate pdf
#dz.create_pdfDoc(pdf_address, pdf_type='table')
dz.pdf_insert_table(headers)

#Quick indexing
dz.quick_indexing(catalogue_df)

for objName in catalogue_df.loc[dz.idx_include].index:
       
    local_refenrence = objName.replace('_','-')
    
    quick_reference = catalogue_df.loc[objName].quick_index
    
    sdss_refenrence, sdss_web, redshift, ra, dec, dichroic = catalogue_df.loc[objName, plotting_Keys].values
    
    web_reference = '{slash}href{{{url}}}{{{text}}}'.format(slash='\\',url=sdss_web,text=sdss_refenrence).replace('&','\&')
    
    wht_conf = 'I' if dichroic == 7500 else 'II'
    
    #Add a new row
    row = [quick_reference, web_reference, redshift, ra, dec, wht_conf]
    dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True)

#dz.generate_pdf(clean_tex=False)
dz.generate_pdf(output_address=pdf_address)

print 'Table generated'