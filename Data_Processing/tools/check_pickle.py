'''
Created on Jan 12, 2017

@author: vital
'''

'''IZW18_A1
MRK36_A1
MRK36_A2
MAR1324
MAR2071
4_n2
51991-224
52235-602'''

from dazer_interface import App_pickleWindow

rootfolder      = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects'
object_to_Check = 'IZW18_A1'
pickle_address  = '{rootfolder}/{objfolder}/E1_{obj}_Sl_MasksFlags.dz_pickle'.format(rootfolder = rootfolder, objfolder=object_to_Check, obj=object_to_Check)

app = App_pickleWindow(pickle_address)
app.MainLoop()

# /home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/M2232/E1_M2232_Sl_MasksFlags.dz_pickle
# /home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/IZW18_A1/IZW18_A1_Sl_MasksFlags.dz_pickle
# /home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/IZW18_A1/E1_IZW18_A1_Sl_MasksFlags.dz_pickle