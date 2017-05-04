import pyfits as pf
from numpy import linspace, array

filename = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue_SulfurRegression/Objects/08/obj08_WHT.fits'

FitsFile    = pf.open(filename) 
Header_0    = FitsFile[0].header
# Flux        = FitsFile[0].data[0][0]
# Header_0['WHTJOINW'] = 7420.0

print 'WHTJOINW' in Header_0


data, header = pf.getdata(filename, header=True)

StartingPix     = -1 * FitsFile[0].header['LTV1']                   # LTV1 = -261. 
Wmin_CCD        = FitsFile[0].header['CRVAL1']                      # dw = 0.862936 INDEF (Wavelength interval per pixel)
dw              = FitsFile[0].header['CD1_1']                       # dw = 0.862936 INDEF (Wavelength interval per pixel)
pixels          = FitsFile[0].header['NAXIS1']                      
Wmin            = Wmin_CCD + dw * StartingPix
Wmax            = Wmin + dw * pixels
WavelenRange    = linspace(Wmin,Wmax,pixels,endpoint=False)

FitsFile.close()

Column1     = pf.Column(name='Wave', format='E', array=WavelenRange)
Column2     = pf.Column(name='Int', format='E',  array=Flux)
Columns     = pf.ColDefs([Column1, Column2])
Table_HDU   = pf.TableHDU.from_columns(Columns, header=Header_0)

Table_HDU.writeto('/home/vital/Desktop/testing.fits', clobber = True)


FitsFile2 = pf.open('/home/vital/Desktop/testing.fits')
Header2 = FitsFile[0].header

for coso in Header_0:
    print coso, Header_0[coso]

print 'WHTJOINW' in Header2
