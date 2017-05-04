from os                         import makedirs, path
from shutil                     import move
from pandas                     import set_option
from DZ_observation_reduction   import spectra_reduction
import pyfits
from dazer_methods import Dazer

set_option('display.max_columns', None)
set_option('display.max_rows', None)
 
#Declare object
dzt = Dazer()
dz = spectra_reduction()

#Objects and file
pattern = '.fit'
 
#Load the catalogue
dz.declare_catalogue(dz.Catalogue_folder)
 
#Locate files
FilesList   = dz.Folder_Explorer(pattern, dz.Catalogue_folder, Sort_Output='alphabetically')
empty_array = [None] * len(dz.columns_reducDf)
  
#Create the raw data folder
if path.exists(dz.reducFolders['raw data']) == False:
    makedirs(dz.reducFolders['raw data'])
  
#Loop through files
for i in range(len(FilesList)):
        
    #Identify object
    CodeName, FileName, FileFolder = dz.Analyze_Address(FilesList[i], verbose=False)
    CodeName = FileName[0:FileName.find('.')]
  
    #Security check to make sure we always work on the default folders
    if (FileFolder == dz.Catalogue_folder) or  (FileFolder == dz.reducFolders['raw data']):
        
        #Read the data from the headers
        try:
            Header0 = pyfits.getheader(FileFolder + FileName, ext=0)
        except:
            Header0 = {}
        try:
            Header1 = pyfits.getheader(FileFolder + FileName, ext=1)
        except:
            Header1 = {}
              
        #Add variables
        for key in dz.columns_reducDf:
            if key in Header0:
                values_to_load = Header0[key]
            elif key in Header1:
                values_to_load = Header1[key]
             
            #Change value to proper format
            if key in ['RUN']:
                try:
                    values_to_load = int(values_to_load)
                except:
                    values_to_load = values_to_load
                
            #Load value
            dz.reducDf.loc[CodeName, key] = values_to_load
             
        #Move the files
        if FileFolder != dz.reducFolders['raw data']:
            move(FilesList[i], dz.reducFolders['raw data'] + FileName)
  
        #Load the name
        dz.reducDf.loc[CodeName, 'file_name'] = FileName
  
#Adding location column
dz.reducDf['file_location'] = dz.reducFolders['raw data']
  
#Check rejected files
dz.check_rejected_files(dz.reducDf, dz.Catalogue_folder)

print 'Catalogue frame:'
print dz.reducDf

#Check if the files is already there before overwritting
if path.isfile(dz.reduc_RootFolder + dz.frame_filename):
    delete_check = dzt.query_yes_no('Are you sure you want to delete reduction_dataframe?', 'no')
    if delete_check:
        dz.save_reducDF()
        print 'Log generated'
else:
    dz.save_reducDF()
    print 'Log generated'


