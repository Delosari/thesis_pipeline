from pandas                     import set_option
from DZ_observation_reduction   import spectra_reduction
from os                         import path
from dazer_methods import Dazer

set_option('display.max_columns', None)
set_option('display.max_rows', None)
 
#Load iraf pypeline object
dzt = Dazer()
dz = spectra_reduction()
 
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
 
print '\nCATALOGUE OBJECT'
print dz.reducDf.OBJECT.unique()
print '\nCATALOGUE OBSTYPE'
print dz.reducDf.OBSTYPE.unique()
 
#Declare the empty column
Catalogue_objects   = dz.observation_dict['objects']
Catalogue_stdstars  = dz.observation_dict['Standard_stars']
 
emergency_case = False

print '\nScientific objects'
print dz.observation_dict['objects']
print '\nStandard stars'
print dz.observation_dict['Standard_stars']

transformation_dic = {}
if dz.Catalogue_folder == '/home/vital/Astrodata/WHT_2009_07/Night1/':
    transformation_dic['SHOC blue'] = 'SHOC575'
    transformation_dic['SP0031-124'] = 'sky'

if dz.Catalogue_folder == '/home/vital/Astrodata/WHT_2009_07/Night2/':
    transformation_dic['2225 blue'] = 'J2225'    

if dz.Catalogue_folder == '/home/vital/Astrodata/WHT_2011_01/Night2/':
    transformation_dic['0564-52224-216'] = '0564'   
    transformation_dic['0564-blue'] = '0564' 
      
if dz.Catalogue_folder == '/home/vital/Astrodata/WHT_2016_10/':
    transformation_dic['CuAr+CuNe'] = 'arc'    

#Loop through the frame and assign more data
len_frame = len(dz.reducDf.index)
for i in range(len_frame):
       
    ID_found = False
    if dz.reducDf.iloc[i].OBJECT in transformation_dic:
        object_i    = transformation_dic[dz.reducDf.iloc[i].OBJECT].lower()
        obstype_i   = dz.reducDf.iloc[i].OBSTYPE.lower()
        file_name_i = dz.reducDf.iloc[i].file_name.lower()
    else:
        object_i    = dz.reducDf.iloc[i].OBJECT.lower().replace(' ', '')
        obstype_i   = dz.reducDf.iloc[i].OBSTYPE.lower()
        file_name_i = dz.reducDf.iloc[i].file_name.lower() 
            
    if ('acq.' in object_i):
        ID_found = True
        dz.reducDf.ix[i,'reduc_tag'] = 'acq_image'
        dz.reducDf.ix[i,'frame_tag'] = 'acq_image'
       
    elif ('bias' == object_i) or ('bias' in object_i):
        ID_found = True
        dz.reducDf.ix[i,'reduc_tag'] = 'bias'
        dz.reducDf.ix[i,'frame_tag'] = 'bias'
           
    elif ('sky' == object_i) or ('sky' in object_i):
        ID_found = True
        dz.reducDf.ix[i,'reduc_tag'] = 'sky'
        dz.reducDf.ix[i,'frame_tag'] = 'sky'
             
    elif ('flat' == object_i) or ('flat' in object_i):
        ID_found = True
        dz.reducDf.ix[i,'reduc_tag'] = 'flat' 
        dz.reducDf.ix[i,'frame_tag'] = 'flat' 
                
    elif ('arc' in object_i) and (obstype_i == 'arc'): #Special case to avoid cases like 'BD+17 arc'
        ID_found = True
        dz.reducDf.ix[i,'reduc_tag'] = 'arc'
        dz.reducDf.ix[i,'frame_tag'] = 'arc'
           
    else:
        for j in range(len(Catalogue_objects)):
            object_code = Catalogue_objects[j].lower()
            if file_name_i == 'r1334204.fits':
                print object_i, object_code
                print object_code in object_i, object_code == object_i
    
            if (object_code in object_i) or (object_code == object_i):
                ID_found = True
                dz.reducDf.ix[i,'reduc_tag'] = Catalogue_objects[j] 
                dz.reducDf.ix[i,'frame_tag'] = Catalogue_objects[j]        
   
        for k in range(len(Catalogue_stdstars)):
            object_code = Catalogue_stdstars[k].lower()
            if (object_code in object_i) or (object_code == object_i):
                ID_found = True
                dz.reducDf.ix[i,'reduc_tag'] = Catalogue_stdstars[k] 
                dz.reducDf.ix[i,'frame_tag'] = Catalogue_stdstars[k]
      
    if ID_found == False:
        dz.reducDf.ix[i,'reduc_tag'] = 'not_found'
        dz.reducDf.ix[i,'frame_tag'] = 'not_found'
          
    if emergency_case:
          
        if '_shift.fits' in file_name_i:
            dz.reducDf.ix[i,'reduc_tag'] = 'frame_shifted'    
  
        elif ('_Blue.fits' in file_name_i) or ('_Red.fits' in file_name_i):
            dz.reducDf.ix[i,'reduc_tag'] = 'obj_combine'  
         
        elif '_w.fits' in file_name_i:
            dz.reducDf.ix[i,'reduc_tag'] = 'wave_calibrated'    
          
        elif '_c.fits' in file_name_i:
            dz.reducDf.ix[i,'reduc_tag'] = 'target_crop'    
          
        elif '_e.fits' in file_name_i:
            dz.reducDf.ix[i,'reduc_tag'] = 'extracted_spectrum'    
          
        elif '_bg.fits' in file_name_i:
            dz.reducDf.ix[i,'reduc_tag'] = 'background_removed'    
          
        elif '_fx.fits' in file_name_i:
            dz.reducDf.ix[i,'reduc_tag'] = 'flux_calibrated'
              
        elif file_name_i[0] != 'r':
            dz.reducDf.ix[i,'reduc_tag'] = 'not_recovered'


for i in range(len_frame):
    print i, obstype_i, dz.reducDf.iloc[i].file_name, dz.reducDf.iloc[i].OBJECT, '\t\t->', dz.reducDf.iloc[i].reduc_tag, '(', dz.reducDf.iloc[i].frame_tag, ')'
    
#Check if the files is already there before overwritting
if path.isfile(dz.reduc_RootFolder + dz.frame_filename):
    delete_check = dzt.query_yes_no('Are you sure you want to udate the reduction_dataframe?', 'no')
    if delete_check:
        dz.save_reducDF()
        print 'Log generated'
else:
    dz.save_reducDF()
    print 'Log generated'
  
