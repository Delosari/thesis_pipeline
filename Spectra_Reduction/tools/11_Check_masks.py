from DZ_observation_reduction import spectra_reduction

#Load iraf pypeline object
dz = spectra_reduction()

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Random object to check the mask
first_object = dz.observation_dict['objects'][0]

#Indeces raw frames
indeces_mask = (dz.reducDf.reduc_tag == first_object) & (dz.reducDf.frame_tag == first_object)

#Indeces frame tag
dz.generate_step_pdf(indeces_mask, file_address = dz.reducFolders['reduc_data'] + 'masked_pixels', verbose=True, plots_type='masked_pixels', ext = 1)
