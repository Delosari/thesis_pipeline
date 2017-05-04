import os
import pyfits
from DZ_observation_reduction   import spectra_reduction
from libraries.Astro_Libraries  import cosmics

#THIS ONE COULD GO AFTER THE FLATS

#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Arm colors
data_dict       = {'reduc_tag': 'cosmic_ray_removal_imComb'}
colors          = ['Blue', 'Red']

#Loop through the arms 
index_object    = (dz.reducDf.reduc_tag == 'obj_combine') & (dz.target_validity_check()) 
Files_Folder    = dz.reducDf.loc[index_object, 'file_location'].values
Files_Name      = dz.reducDf.loc[index_object, 'file_name'].values       
objects         = dz.reducDf.loc[index_object, 'frame_tag'].values
colors_arm      = dz.reducDf.loc[index_object, 'ISIARM'].values

for i in range(len(objects)):  
               
    #Get the data ready for the task                     
    fitsdata, hdr = cosmics.fromfits(Files_Folder[i] + Files_Name[i], verbose=False)   
       
    #Get the object configuration values:
    if objects[i] + '_lacosmic' in dz.observation_dict:
        sigclip = float(dz.observation_dict[objects[i] + '_lacosmic'][0])
    else:
        if objects[i] in dz.observation_dict['Standard_stars']:
            sigclip = 10.0
        else:
            if colors_arm[i] == 'Blue arm':
                sigclip = 10.0
            elif colors_arm[i] == 'Red arm':
                sigclip = 10.0
        
    print '\n-Treating:', Files_Name[i],' ', i, '/', len(Files_Name), objects[i] + '_lacosmic', sigclip, '\n'
            
    gain            = pyfits.getval(Files_Folder[i] + Files_Name[i], 'GAIN' ,0)
    readnoise       = pyfits.getval(Files_Folder[i] + Files_Name[i], 'READNOIS' ,0)
    lacosmic_param  = [gain, readnoise, sigclip]
            
    #Frame cosmic object
    c = cosmics.cosmicsimage(fitsdata, gain=lacosmic_param[0], readnoise=lacosmic_param[1], sigclip = lacosmic_param[2])
   
    #Run the fitting
    c.run(maxiter = 4)
               
    #Write the cleaned image into a new FITS file, conserving the original header :
    output_clean = Files_Folder[i] + Files_Name[i][0:Files_Name[i].rfind('.')] + '_cr.fits' 
    output_mask = Files_Folder[i] + Files_Name[i][0:Files_Name[i].rfind('.')] + '_mask.fits' 
        
    #Delete the file if it already exists
    if os.path.isfile(output_clean):
        os.remove(output_clean)
    if os.path.isfile(output_mask):
        os.remove(output_mask)        
                
    #Store the frames        
    hdu_clean = pyfits.PrimaryHDU(c.cleanarray.transpose(), hdr)
    hdu_clean.writeto(output_clean)
       
    masked_array = c.mask.transpose().astype(int)
    hdu_mask = pyfits.PrimaryHDU(masked_array, hdr)
    hdu_mask.writeto(output_mask)
         
    #Add objects to data frame with the new frame_tag
    dz.object_to_dataframe(output_clean, data_dict)
       
# #Generate pdf file
indeces_print = (dz.reducDf.reduc_tag == 'cosmic_ray_removal_imComb') & dz.reducDf.frame_tag.isin(dz.observation_dict['objects'] + dz.observation_dict['Standard_stars'])
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'targets_cosmic_removal', ext = 0, plots_type = 'cosmic_removal')

dz.beep_alarmn()

print 'Data treated'
