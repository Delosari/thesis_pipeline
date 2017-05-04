import pandas                   as pd
from itertools                  import cycle
from numpy                      import abs, sqrt, argmin, cos, timedelta64, loadtxt
from pyfits                     import getval
from astropy                    import units as u, coordinates as coord
from pylatex                    import Document, Package, Figure, NoEscape, Tabular
from collections                import OrderedDict
from DZ_observation_reduction   import spectra_reduction
  
#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

list_rejected = loadtxt(dz.Rejected_file, dtype = str, usecols = [0], ndmin=1)

for fits_file in list_rejected:
    idx = (dz.reducDf.file_name == fits_file)
    print fits_file, dz.reducDf.loc[idx, 'frame_tag'].values[0]
    

