'''
Created on Jun 15, 2015

@author: vital
'''

# The following two lines are only needed as cosmic.py is not in this directory nor in the python path.
# They would not be required if you copy cosmics.py in this directory.
# import sys
# sys.path.append("/home/vital/Dropbox/Astrophysics/Tools/PyRaf/LaCosmic_Python/") # The directory that contains cosmic.py
# sys.path.append("/home/vital/Dropbox/Astrophysics/Tools/PyRaf/LaCosmic_Python/") # The directory that contains cosmic.py
# 
# Demo_Folder     = "/home/vital/Dropbox/Astrophysics/Tools/PyRaf/LaCosmic_Python/demo_2_withpng/"
# Demo_Input      = "euler.fits"
# 
# import cosmics, f2n

from Scientific_Lib import cosmics
from Scientific_Lib import f2n


Demo_Folder     = "/home/vital/Dropbox/Astrophysics/Tools/PyRaf/LaCosmic_Python/demo_2_withpng/"
Demo_Input      = "euler.fits"

Demo_Input      = "obj8_c_f.fits"

# Read the FITS :
(array, header) = cosmics.fromfits(Demo_Folder + Demo_Input, verbose = True)

# We can of course crop the numpy array :
#array = array[100:500,210:525]

# z1=170
# z2=5000
upsample = 1

# Build the object :

c = cosmics.cosmicsimage(array, pssl = 0.0, gain=1.16, readnoise=5,
    sigclip = 16, verbose = True)

# Run :
c.run(maxiter = 4, verbose = False)

# And now we use f2n.py to make several PNG images :

# The raw input array :
im = f2n.f2nimage(c.getrawarray(), verbose=False)
im.setzscale()
im.makepilimage("log")
im.upsample(upsample)
im.writetitle("Input image", colour = (0,255,0))
im.tonet(Demo_Folder + "0_raw.png")


# The mask of saturated stars, upon the raw image :
im = f2n.f2nimage(c.getrawarray(), verbose=False)
im.setzscale()
im.makepilimage("log")
im.drawmask(c.getsatstars(), colour=(255, 0, 255))
im.upsample(upsample)
im.writetitle("Saturated stars", colour = (0,255,0))
im.tonet(Demo_Folder + "1_satstars.png")

# We output a list of the positions of detected cosmic ray hits.
# This is made on purpose to be fed into f2n's drawstarslist :
labeldict = c.labelmask()
im = f2n.f2nimage(c.getrawarray(), verbose=False)
im.setzscale()
im.makepilimage("log")
im.drawmask(c.getsatstars(), colour=(255, 0, 255))
im.upsample(upsample)
im.drawstarslist(labeldict, colour=(255,0,0))
im.writetitle("Cosmic ray hits", colour = (0,255,0))
im.tonet(Demo_Folder + "2_labels.png")

# One png with the precise mask in green and a wider version in blue :
im = f2n.f2nimage(c.getrawarray(), verbose=False)
im.setzscale()
im.makepilimage("log")
im.drawmask(c.getdilatedmask(size=5), colour=(0, 0, 255))
im.drawmask(c.getmask(), colour=(0, 255, 0))
im.upsample(upsample)
im.writetitle("Mask", colour = (0,255,0))
im.tonet(Demo_Folder + "3_mask.png")

# And of course one png with the clean array :
im = f2n.f2nimage(c.getcleanarray(), verbose=False)
im.setzscale()
im.makepilimage("log")
im.upsample(upsample)
im.writetitle("Cleaned image", colour = (0,255,0))
im.tonet(Demo_Folder + "4_clean.png")











# The following two lines are only needed as cosmic.py is not in this directory nor in the python path.
# They would not be required if you copy cosmics.py in this directory.
# import sys
# sys.path.append("/home/vital/Dropbox/Astrophysics/Tools/PyRaf/LaCosmic_Python/") # The directory that contains cosmic.py
# 
# import cosmics
# 
# Demo_Folder     = "/home/vital/Dropbox/Astrophysics/Tools/PyRaf/LaCosmic_Python/demo_1_simple/"
# Demo_Input      = "input.fits"
# 
# # Read the FITS :
# array, header = cosmics.fromfits(Demo_Folder + Demo_Input)
# # array is a 2D numpy array
# 
# # Build the object :
# c = cosmics.cosmicsimage(array, gain=2.2, readnoise=10.0, sigclip = 5.0, sigfrac = 0.3, objlim = 5.0)
# # There are other options, check the manual...
# 
# # Run the full artillery :
# c.run(maxiter = 4)
# 
# # Write the cleaned image into a new FITS file, conserving the original header :
# cosmics.tofits(Demo_Folder + "clean.fits", c.cleanarray, header)
# 
# # If you want the mask, here it is :
# cosmics.tofits(Demo_Folder + "mask.fits", c.mask, header)
# # (c.mask is a boolean numpy array, that gets converted here to an integer array)