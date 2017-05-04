#!/usr/bin/python

import os
from sys            import argv, path
from numpy          import loadtxt
from collections    import OrderedDict

path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY']   = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY']    = '/home/vital/anaconda/python27/lib/tk8.5'

from DZ_observation_reduction   import equivalent_Iraf_comand, set_Iraf_package

#Get the task configuration location from argument
FileAddress             = argv[1]  
FolderName              = FileAddress[0:FileAddress.rfind("/")+1]
FileName                = FileAddress[FileAddress.rfind("/")+1:len(FileAddress)]
task                    = FileName[0:FileName.find('_')]

#Load the task configuration
dict_keys, dict_values  = loadtxt(FileAddress, dtype='str', delimiter = ';', usecols = (0,1), unpack = True)
task_conf               = OrderedDict(zip(dict_keys, dict_values))

#Display the IRAF commands we are using
equivalent_Iraf_comand(task, task_conf, printindividually=True, file_commands_address= '/home/vital/Desktop/Pypeline_lastcommands')

#Run the task
set_Iraf_package(task, task_conf)

print '--', task, ' implemented'   
    

