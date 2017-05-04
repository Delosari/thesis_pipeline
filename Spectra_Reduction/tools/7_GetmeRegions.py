import numpy                    as np
from astropy.io                 import fits
import matplotlib.pyplot        as plt
from astropy.visualization      import ZScaleInterval
from DZ_observation_reduction   import spectra_reduction
import matplotlib.patches       as patches
from os                         import remove, close
from shutil                     import move
from tempfile                   import mkstemp

def replace_observation_data(file_path, obs_dict):
    
    dict_keys = obs_dict.keys()
    
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                line_components = line.split(';')
                if line_components[0] in dict_keys:
                    new_line = '{dict_key}; {dict_value}\n'.format(dict_key = line_components[0], dict_value=' '.join(obs_dict[line_components[0]]))
                    new_file.write(line.replace(line, new_line))
                else:
                    new_line = line
                    new_file.write(line.replace(line, new_line))
                
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def on_click(event):
 
    if event.button == 3:
         
        if event.inaxes is not None:
             
            #Clear previous data
            plt.cla()
            
            #Plot the image
            Axis.imshow(image_data, cmap=dz.frames_colors[arm_color + ' arm'], origin='lower', vmin = int_min, vmax = int_max, interpolation='nearest')
 
            #Get event data
            x, y = event.xdata, event.ydata
            x_cords, y_cords = int(x + 0), int(y + 0)
            Axis.scatter(x_cords, y_cords, s=60, edgecolor='yellow', facecolor='none')
            
            #Plot max location
            max_values      = np.max(image_data)
            max_indeces_sec = np.where(image_data == max_values)
            Axis.scatter(max_indeces_sec[1], max_indeces_sec[0], s=30, facecolor='red')
 
            #Plot local maxima
            section         = image_data[y_cords-5:y_cords+5, x_cords-5:x_cords+5]
            max_value_sec   = np.max(section)
            max_indeces_sec = np.where(image_data == max_value_sec)
            x_max, y_max    = max_indeces_sec[1][0], max_indeces_sec[0][0]
            Axis.scatter(x_max, y_max, s=30, facecolor='black', edgecolor='yellow')
            dz.observation_dict[object_reference] = [str(x_max), str(y_max)]
            
            #Readjusting the area
            cropping_area[0], cropping_area[1] = x_max - 100, x_max + 100
            Axis.add_patch(patches.Rectangle((cropping_area[0], cropping_area[2]), cropping_area[1] - cropping_area[0], cropping_area[3] - cropping_area[2], linewidth = 2, color='red', fill=False))      # remove background
            dz.observation_dict['{Color}_cropping'.format(Color=arm_color)] = cropping_area
            Axis.set_xlim(x_cords-20, x_cords+20)
            Axis.set_ylim(y_cords-20, y_cords+20)
            plt.tight_layout(0)
            plt.draw()
 
#Load iraf pypeline object
dz = spectra_reduction()
  
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
  
#Loop through the arms 
colors = ['Blue', 'Red']
for arm_color in colors:
  
    indx_targetframes       = (dz.reducDf.reduc_tag == 'objTest_combine') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file) 
    files_name              = dz.reducDf[indx_targetframes].sort_values(['file_name']).file_name.values
    files_address           = dz.reducDf[indx_targetframes].sort_values(['file_name']).file_location.values
    files_object            = dz.reducDf[indx_targetframes].sort_values(['frame_tag']).frame_tag.values
     
    for i in range(len(files_name)):
         
        print files_name[i], str(i)+'/'+str(len(files_name))
         
        with fits.open(files_address[i] + files_name[i]) as hdu_list:
            image_data = hdu_list[0].data
          
        Pdf_Fig, Axis   = plt.subplots(1, 1, figsize=(8, 10))  
              
        #Get zscale limits for plotting the image
        IntensityLimits     = ZScaleInterval()
        int_min, int_max    = IntensityLimits.get_limits(image_data)[0], IntensityLimits.get_limits(image_data)[1]
        Axis.imshow(image_data, cmap=dz.frames_colors[arm_color + ' arm'], origin='lower', vmin = int_min, vmax = int_max, interpolation='nearest')
        Axis.set_xlim(0, image_data.shape[1])
        Axis.set_ylim(0, image_data.shape[0])
        
        Axis.set_title(files_object[i]+'\n'+files_name[i])
        
        try:
            #Plot cropping area
            Cropping_key    = dz.observation_dict['{Color}_cropping'.format(Color=arm_color)]
            cropping_area   = map(int, Cropping_key) 
            Axis.add_patch(patches.Rectangle((cropping_area[0], cropping_area[2]), cropping_area[1] - cropping_area[0], cropping_area[3] - cropping_area[2], linewidth = 2, color='red', fill=False))      # remove background
        except:
            print 'Need to load cropping regions'
             
        try: 
            #Plotting reference line
            object_reference = '{CodeName}_refline_{Color}'.format(CodeName=files_object[i], Color=arm_color)
            Store_cords = dz.observation_dict[object_reference]
            x_peak, y_peak = int(Store_cords[0]), int(Store_cords[1])
            Axis.scatter(x_peak, y_peak, s=30, facecolor='green')
        except:
            print 'Need to load reference line'
             
        try:    
            #Plotting the scaling region
            obj_scaling_key = '{Color}_scale_region'.format(Color=arm_color)
            scale_cords     = map(int, dz.observation_dict[obj_scaling_key])
            Axis.add_patch(patches.Rectangle((scale_cords[0], scale_cords[2]), scale_cords[1] - scale_cords[0], scale_cords[3] - scale_cords[2], linewidth = 2, color='black', fill=False))      # remove background
        except:
            print 'Need to load scaling regions'
           
        #Display the interactive plot
        plt.tight_layout()   
        plt.connect('button_press_event', on_click)
        plt.show()
         
#Replace the new point selections
dz.save_observation_dict()
#replace_observation_data(dz.Catalogue_folder + dz.observation_properties_file_name, dz.observation_dict)

#Plot the data
idx_to_print = (dz.reducDf.reduc_tag == 'objTest_combine')
dz.generate_step_pdf(idx_to_print, file_address = dz.reducFolders['reduc_data'] + 'test_target_combined', plots_type = 'fast_combine', ext = 0)

dz.beep_alarmn()

print 'Data treated'
