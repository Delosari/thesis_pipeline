from os         import mkdir
from os.path    import isdir

def create_catalogue_files(catalogue_dict = None, files_dict = None):
    
    if catalogue_dict != None:
         
        if isdir(catalogue_dict['Folder']) == False:
            mkdir(catalogue_dict['Folder'])
        
            if isdir(catalogue_dict['Obj_Folder']) == False:
                mkdir(catalogue_dict['Obj_Folder'])

            if isdir(catalogue_dict['Data_Folder']) == False:
                mkdir(catalogue_dict['Data_Folder'])

    
    
    
    return