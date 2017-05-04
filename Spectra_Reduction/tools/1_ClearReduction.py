#!/usr/bin/python
from time import time
from os import remove
from dazer_methods import Dazer
from DZ_observation_reduction import spectra_reduction

#Import libraries
t2 = time()  # start time
dz = Dazer()
t3 = time() # end time
print '--TOTAL Init', (t3 - t2)  

sr = spectra_reduction()
 
FilesList = dz.Folder_Explorer('',  sr.Catalogue_folder, CheckComputer=False, verbose=False, Sort_Output='alphabetically')
 
files_to_keep   = []
files_to_delete = []
 
for file_address in FilesList:
      
    CodeName, FileName, FolderName = dz.Analyze_Address(file_address, verbose=False)
      
    if (FileName in ['badpix_Bluemask', 'badpix_Redmask', 'observation_properties.txt', 'rejected_files.txt']) or ('run' in FileName) or ('/raw_fits/' in FolderName) or ('database/id' in file_address) or ('database/ap_' in file_address):         
        files_to_keep.append(FolderName + FileName)
    else:
        files_to_delete.append(FolderName + FileName)
 
print '\n--These files will be deleted:'
for file_address in files_to_delete:
    print file_address, ' -> X'
 
print '\n--These files will be preserved:'
for file_address in files_to_keep:
    print file_address, ' -> V'
 
# #Dialog box to confirm if we want to delete the files
# delete_check = dz.query_yes_no('Are you sure you want to delete these files?', 'no')
#  
# #Proceed to delete
# if delete_check:
#     for file_address in files_to_delete:
#         remove(file_address)
#         print file_address, ' -> deleted'
 
print 'Data treated'