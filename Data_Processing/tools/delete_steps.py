#!/usr/bin/python
from time import time
from os import remove
from dazer_methods import Dazer
from DZ_observation_reduction import spectra_reduction

#Create class object
dz = Dazer()
 
FilesList = dz.Folder_Explorer('',  '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/', CheckComputer=False, verbose=False, Sort_Output='alphabetically')
 
files_to_keep   = []
files_to_delete = []

for file_address in FilesList:
      
    CodeName, FileName, FolderName = dz.Analyze_Address(file_address, verbose=False)
      
    if (FileName in ['WHT_Galaxies_properties.txt']) or ('run' in FileName) or ('_lick_indeces.txt' in FileName):
        files_to_keep.append(FolderName + FileName)
    else:
        files_to_delete.append(FolderName + FileName)
 
print '\n--These files will be deleted:'
for file_address in files_to_delete:
    print file_address, ' -> X'
 
print '\n--These files will be preserved:'
for file_address in files_to_keep:
    print file_address, ' -> V'
 
#Dialog box to confirm if we want to delete the files
delete_check = dz.query_yes_no('Are you sure you want to delete these files?', 'no')
  
#Proceed to delete
if delete_check:
    for file_address in files_to_delete:
        remove(file_address)
        print file_address, ' -> deleted'
 





