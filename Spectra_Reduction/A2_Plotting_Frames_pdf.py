from numpy import savetxt
from DZ_observation_reduction import spectra_reduction
   
#Objects and file
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
 
#Extensions
ext = 1
 
#-- Bias frames
indeces  = (dz.reducDf.frame_tag == 'bias') & (dz.reducDf.file_location.str.contains('/raw_fits/'))
list_files = dz.reducDf.loc[indeces, 'file_name'].values
print 'Bias frames:', len(list_files)
savetxt(dz.reducFolders['reduc_data'] + 'obs_bias.list', list_files, fmt='%s')
dz.generate_step_pdf(indeces, file_address = dz.reducFolders['reduc_data'] + 'bias_frames', include_graph=True, verbose=False, ext=ext)
print 'Bias pdf generated'
              
#-- Flat frames
indeces  = (dz.reducDf.frame_tag == 'flat')  & (dz.reducDf.file_location.str.contains('/raw_fits/'))
list_files = dz.reducDf.loc[indeces, 'file_name'].values
print 'Flat frames:', len(list_files)
savetxt(dz.reducFolders['reduc_data'] + 'obs_flat.list', list_files, fmt='%s')
dz.generate_step_pdf(indeces, file_address = dz.reducFolders['reduc_data'] + 'flat_frames', include_graph=True, verbose=False, ext=ext)
print 'Flat pdf generated'
              
#-- Sky frames 
indeces  = (dz.reducDf.frame_tag == 'sky') & (dz.reducDf.file_location.str.contains('/raw_fits/'))
list_files = dz.reducDf.loc[indeces, 'file_name'].values
print 'Sky frames:', len(list_files)
savetxt(dz.reducFolders['reduc_data'] + 'obs_sky.list', list_files, fmt='%s')
dz.generate_step_pdf(indeces, file_address = dz.reducFolders['reduc_data'] + 'sky_frames', include_graph=True, verbose=False, ext=ext)
print 'Sky pdf generated'
            
#-- Arc frames 
indeces  = (dz.reducDf.frame_tag == 'arc')  & (dz.reducDf.file_location.str.contains('/raw_fits/'))
list_files = dz.reducDf.loc[indeces, 'file_name'].values
print 'Arc frames:', len(list_files)
savetxt(dz.reducFolders['reduc_data'] + 'obs_arc.list', list_files, fmt='%s')
dz.generate_step_pdf(indeces, file_address = dz.reducFolders['reduc_data'] + 'arc_frames', include_graph=True, verbose=False, ext=ext)
print 'Arc pdf generated'
            
#--target frames
indeces     = (dz.reducDf.OBSTYPE == 'TARGET') & (dz.reducDf.file_location.str.contains('/raw_fits/'))
list_files  = dz.reducDf.loc[indeces, 'file_name'].values
savetxt(dz.reducFolders['reduc_data'] + 'obs_target.list', list_files, fmt='%s')
dz.generate_step_pdf(indeces, file_address = dz.reducFolders['reduc_data'] + 'targets_frames', verbose=False, ext=ext)
print 'targets pdf generated'
   
dz.beep_alarmn()
      
print 'All documents generated'






