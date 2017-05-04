import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction import spectra_reduction

'''
Run from terminal
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/C4_Response_objectsFlats.py
'''

#Load iraf pypeline object
dz = spectra_reduction()
  
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)   

#Loop through the arms
extension   = 0
colors      = ['Blue','Red']
ordenes     = ['High', 'Low']
orden_mag   = {'High' : 200, 'Low' : 15}

for orden_type in ordenes:
    for arm_color in colors:
              
        list_targets = dz.observation_dict['objects'] + dz.observation_dict['Standard_stars']
                 
        for i in range(len(list_targets)):
              
            print '--Treating:', list_targets[i], i,'/', len(list_targets), orden_mag[orden_type]
  
            #Get orden magnitude
            obj_target  = list_targets[i]
            orden       = orden_mag[orden_type]
                        
            #Getting the flat idx
            run_id         = dz.observation_dict[obj_target + '_flat'][dz.plots_dict[arm_color]]
            print run_id
            if run_id != 'flat_combine_{color}'.format(color = arm_color):
                index_ObjFlat   = (dz.reducDf.RUN == float(run_id)) & (dz.reducDf.reduc_tag == 'biascorr') & (dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color)) & (dz.reducDf.valid_file) 
            else: 
                index_ObjFlat = (dz.reducDf.reduc_tag == 'flatcombine') & (dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color)) & (dz.reducDf.valid_file) 
             
            objflat_address = dz.reducDf.loc[index_ObjFlat, 'file_location'].values[0] + dz.reducDf.loc[index_ObjFlat, 'file_name'].values[0]
            print objflat_address
            
            #Treat the data    
            dz.task_attributes['color']             = arm_color
            dz.task_attributes['run folder']        = '{folder_run}'.format(folder_run = dz.reducFolders['flat lamp'])
            dz.task_attributes['input']             = dz.reducDf.loc[index_ObjFlat, 'file_location'].values[0] + dz.reducDf.loc[index_ObjFlat, 'file_name'].values[0]
            dz.task_attributes['output']            = '{folder_output}{object}_flatobj_n_{color}_{orden_type}order.fits'.format(folder_output = dz.task_attributes['run folder'], object = obj_target, color = dz.task_attributes['color'], orden_type=orden_type).replace('[','').replace(']','')
            dz.task_attributes['threshold']         = '1'
            dz.task_attributes['order']             = orden
                          
            #task attributes
            dz.task_attributes['normalizing_flat']  = dz.task_attributes['input']
                      
            #Run the task
            dz.run_iraf_task('response', run_externally=False)
                                    
            #Add objects to data frame with the new frame_tag
            data_dict = {'reduc_tag': '{flat_code}_{orden_type}order'.format(flat_code = obj_target + '_nflatobj', orden_type=orden_type)}
            dz.object_to_dataframe(dz.task_attributes['output'], data_dict)
            
    #Pause until key is pressed
    message_order_cycle = 'Finished treating {orden_cycle} order cycle. Press enter'.format(orden_cycle = orden_type)
    raw_input(message_order_cycle)
            
# #Generate pdf file
indeces_to_pdf = (dz.reducDf.reduc_tag.str.contains('_nflatobj'))
dz.generate_step_pdf(indeces_to_pdf, file_address = dz.reducFolders['reduc_data'] + 'object_flats_Highlow_orders', plots_type = 'flats', ext = 0, include_graph=True)

dz.beep_alarmn()

print 'Data treated'

