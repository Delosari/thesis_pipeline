
from pyraf import iraf

input_spec  = 'stdBD17_wide_cr_f_a_bg_s.fits'
Folder      = '/home/vital/Desktop/Flux_Calibration_Steps/Night1_Blue/'

iraf.onedspec.splot(images=Folder + input_spec)

