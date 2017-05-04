import pyfits
from DZ_observation_reduction   import spectra_reduction
from pandas                     import set_option
from numpy import array, zeros, max, where
from collections import OrderedDict

set_option('display.max_columns', None)
set_option('display.max_rows', None)

#Load iraf pypeline object
dz = spectra_reduction()
  
#Entries for new files
data_dict = {'reduc_tag': 'frame_shifted'}

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms
colors = ['Blue', 'Red']

tolerance = 10

for obj_target in dz.observation_dict['objects']:
    
    shifting_dict = OrderedDict()
    
    for arm_color in colors:

        #Get the indeces        
        indeces_objframes = (dz.reducDf.frame_tag == obj_target) & (dz.reducDf.reduc_tag == 'cosmic_ray_removal') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.target_validity_check())

        #Obj properties
        Files_Folders   = dz.reducDf.loc[indeces_objframes, 'file_location'].values
        Files_Names     = dz.reducDf.loc[indeces_objframes, 'file_name'].values
        Object_Names    = dz.reducDf.loc[indeces_objframes, 'frame_tag'].values
        runs            = dz.reducDf.loc[indeces_objframes, 'RUN'].values
        frame_number    = len(Files_Names)
        
        Reference_line  = dz.observation_dict['{obj}_refline_{color}'.format(obj = obj_target, color = arm_color)] 
        x_region        = array([int(Reference_line[0]) - 10, int(Reference_line[0]) + tolerance])
        y_region        = array([int(Reference_line[1]) - 10, int(Reference_line[1]) + tolerance])
        print '------',obj_target, Files_Names
        
        #Getting the maxima for each object
        shifting_dict = OrderedDict()
        
        for i in range(len(Files_Names)):
            
            File_Address    = Files_Folders[i] + Files_Names[i]
            Frame_code      = Files_Names[i][Files_Names[i].find('Frame'):Files_Names[i].find('Frame')+6:]
            data            = pyfits.getdata(File_Address,0)
            idx_frame       = (dz.reducDf.file_name == Files_Names[i])
                        
            shifting_dict[arm_color + '_region'] = [y_region[0],y_region[1],x_region[0],x_region[1]]
                                  
            coords    = shifting_dict[arm_color + '_region']
            section   = data[coords[0]:coords[1],coords[2]:coords[3]]
            max_value = max(section)
            max_indxs = where(data == max(section))
            
            if (obj_target == 'IZW18') and (arm_color == 'Red') and len(max_indxs[0]) > 1:
                indece_max_truco = 1
            else:
                indece_max_truco = 0

            shifting_dict[str(runs[i]) + '_'+ arm_color + '_max'] = max_value
            shifting_dict[str(runs[i]) + '_'+ arm_color + '_amax'] = array([max_indxs[0][indece_max_truco], max_indxs[1][indece_max_truco]])
        
              
        #then compare with respect to the first frame
        for j in range(frame_number):
            for coords in [0,1]:
                if coords == 0:
                    key_entry   = '{FrameNumber}_{line}_yshift'.format(FrameNumber = runs[j], line=arm_color)
                    value_entry = shifting_dict['{FrameNumber}_{line}_amax'.format(FrameNumber=runs[j], line=arm_color)][coords] - shifting_dict['{Frame1}_{line}_amax'.format(Frame1 = runs[0], line=arm_color)][coords]
                if coords == 1:
                    key_entry   = '{FrameNumber}_{line}_xshift'.format(FrameNumber = runs[j], line=arm_color)
                    value_entry = shifting_dict['{FrameNumber}_{line}_amax'.format(FrameNumber = runs[j], line=arm_color)][coords] - shifting_dict['{Frame1}_{line}_amax'.format(Frame1 = runs[0], line=arm_color)][coords]
                shifting_dict[key_entry] = value_entry
    
        #Choose the shifts
        xshifts = zeros(frame_number)
        yshifts = zeros(frame_number)
        for k in range(1,frame_number):
            xshifts[k] =  shifting_dict['{frameNumber}_{color}_xshift'.format(frameNumber = runs[k], color = arm_color)] * -1 
            yshifts[k] =  shifting_dict['{frameNumber}_{color}_yshift'.format(frameNumber = runs[k], color = arm_color)] * -1
            
        print 'Frames being shifted by'
        print 'x', xshifts
        print 'y', yshifts
        
        raw_input("\nPress Enter to start task...")
    
        #Perform imshift task
        for k in range(frame_number):                                
            dz.task_attributes['run folder']    = dz.reducFolders['objects']
            output_name                         = Files_Names[k][0:Files_Names[k].find('.')] + '_shift.fits'
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['input']         = Files_Folders[k] + Files_Names[k]
            dz.task_attributes['output']        = Files_Folders[k] + output_name
            dz.task_attributes['xshift']        = xshifts[k]
            dz.task_attributes['yshift']        = yshifts[k]

            #Run the task
            dz.run_iraf_task('imshift', run_externally=False)
                                    
            #Add objects to data frame with the new frame_tag
            dz.object_to_dataframe(dz.task_attributes['output'], data_dict)
                
#         for v in range(len(Files_Names)):
#             File_Address    = Files_Folders[i] + Files_Names[v][0:Files_Names[v].find('.')] + '_shift.fits'
#             Frame_code      = Files_Names[i][Files_Names[v].find('Frame'):Files_Names[i].find('Frame')+6:]
#             data            = pyfits.getdata(File_Address,0)
#             coords          = shifting_dict[arm_color + '_region']
#             section         = data[coords[0]:coords[1],coords[2]:coords[3]]
#             max_value       = max(section)
#             max_indxs       = where(data == max(section))
#             shifting_dict[Frame_code + '_'+ arm_color + '_max'] = max_value
#             print max_value, max_indxs
    
                                                 
#New files
idx_print = (dz.reducDf.reduc_tag == 'frame_shifted')
dz.generate_step_pdf(idx_print, file_address =dz.reducFolders['reduc_data'] + 'target_shiftedframes', ext = 0, plots_type = 'frame_combine')
        
print 'Data treated'


