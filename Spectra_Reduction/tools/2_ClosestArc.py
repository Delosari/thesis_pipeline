import sys
import subprocess
import os
import pandas                   as pd
from itertools                  import cycle
from numpy                      import sqrt, argmin, cos, timedelta64
from pyfits                     import getval
from astropy                    import units as u, coordinates as coord
from pylatex                    import Document, Package, NoEscape, Tabular
from DZ_observation_reduction   import spectra_reduction
  
#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#--Set the time in the right units
#Load the time from the headers
id_originals = (dz.reducDf.file_location.str.contains('/raw_fits/'))
files_names  = dz.reducDf[id_originals].file_name.values
file_folders = dz.reducDf[id_originals].file_location.values

#Seems UT is not good for these, using UTOBS instead
for idx in range(len(dz.reducDf.index)):
    if '/raw_fits/' in dz.reducDf.iloc[idx].file_location:
        dz.reducDf.ix[idx,'UT'] = getval(dz.reducDf.iloc[idx].file_location + dz.reducDf.iloc[idx].file_name, 'DATE-OBS', 0) + getval(dz.reducDf.iloc[idx].file_location + dz.reducDf.iloc[idx].file_name, 'UTOBS', 0)

dz.reducDf['UT_time'] = pd.to_datetime(dz.reducDf['UT'])
dz.reducDf['UT_time'] = dz.reducDf['UT_time'] + (dz.reducDf.UT_time - dz.reducDf.iloc[0].UT_time < pd.Timedelta(0)) * pd.Timedelta(1, 'D')
   
idces_targets   = (dz.reducDf.frame_tag.isin(dz.observation_dict['objects'] + dz.observation_dict['Standard_stars'])) & (dz.reducDf.file_location.str.contains('/raw_fits/')) & (dz.target_validity_check()) 
frames_obj      = dz.reducDf[idces_targets].sort_values(['RUN']).frame_tag.unique()
  
#Loop through the targets to find the best match
matched_frames  = {}
  
#Dict with the colors to use
colors_dict     = {}
color_font      = ['Red', 'Orange', 'Purple', 'Blue', 'Green', 'Brown', 'MidnightBlue', 'Cyan', 'WildStrawberry', 'SeaGreen', 'Peach', 'Rhodamine', 'Orchid', 'Gray']
color_cycler    = cycle(color_font)
  
for i in range(len(frames_obj)):
               
    target_object = frames_obj[i]
    
    for color in ['Blue', 'Red']:
            
        sub_idxs                = (dz.reducDf.frame_tag == target_object) & (dz.reducDf.ISIARM == color + ' arm') & idces_targets
        idx_first               = sub_idxs[sub_idxs==True].first_valid_index()
        target_file             = dz.reducDf.loc[idx_first].file_name
        target_folder           = dz.reducDf.loc[idx_first].file_location
        target_obstime          = dz.reducDf.loc[idx_first].UT_time 
        target_observations     = sub_idxs.sum()
                       
        target_Exptime          = getval(target_folder + target_file, 'EXPTIME', 0)
        RA_obj, DEC_obj         = coord.Angle(dz.reducDf.loc[idx_first].RA, unit=u.hourangle),  coord.Angle(dz.reducDf.loc[idx_first].DEC, unit = u.degree)
             
        #Get calibration files properties
        idces_calibframes       = (dz.reducDf.frame_tag == 'arc') & (dz.reducDf.file_location.str.contains('/raw_fits/')) & (dz.reducDf.ISIARM == color + ' arm') & (dz.target_validity_check())  
                
        #Calculating angular separation 
        RA_calib_frames         = coord.Angle(dz.reducDf[idces_calibframes].RA.values, unit=u.hourangle)
        DEC_calib_frames        = coord.Angle(dz.reducDf[idces_calibframes].RA.values, unit=u.degree)   
        Delta_RA                = RA_calib_frames.degree - RA_obj.degree
        Delta_Dec               = DEC_calib_frames.degree - DEC_obj.degree
        cos_Dec                 = cos(DEC_obj.radian)
        Delta_Theta             = sqrt((Delta_RA * cos_Dec)**2 + (Delta_Dec)**2)
             
        #Add half the time of the total observation (this scheme does not work if the expositions have different lenght)
        time_interval = timedelta64(int(target_observations * target_Exptime / 2),'s')
        dz.reducDf.loc[idx_first, 'UT_time'] = dz.reducDf.loc[idx_first, 'UT_time'] + time_interval
             
        #Get closests values 
        calib_frame_by_time, calib_time    = dz.get_closest_time(dz.reducDf, idx_first, idces_calibframes, 'UT_time')
        calib_frame_by_sep, star_sep       = dz.reducDf.loc[idces_calibframes, 'file_name'].values[argmin(Delta_Theta)], Delta_Theta[argmin(Delta_Theta)]
                      
        #Save the data
        reference_key1 = '{codename}_{arm_color}_{calib_file}_bytime'.format(codename = target_object, arm_color = color, calib_file = 'arc')
        reference_key2 = '{codename}_{arm_color}_{calib_file}_calibtime'.format(codename = target_object, arm_color = color, calib_file = 'arc')
        reference_key3 = '{codename}_{arm_color}_{calib_file}_bySeparation'.format(codename = target_object, arm_color = color, calib_file = 'arc')
        reference_key4 = '{codename}_{arm_color}_{calib_file}_calibSeparation'.format(codename = target_object, arm_color = color, calib_file = 'arc')
        matched_frames[reference_key1] = calib_frame_by_time
        matched_frames[reference_key2] = calib_time      
        matched_frames[reference_key3] = calib_frame_by_sep
        matched_frames[reference_key4] = star_sep
                  
        if calib_frame_by_sep not in colors_dict:
            colors_dict[calib_frame_by_sep] = next(color_cycler)
                          
  
#-----------Create the table
#Create the doc
pdf_address = dz.reducFolders['reduc_data'] + 'closest_arc'
doc = Document(pdf_address)
doc.packages.append(Package('geometry', options=['left=1cm', 'right=1cm', 'top=1cm', 'bottom=1cm']))
doc.packages.append(Package('preview', options=['active', 'tightpage']))
doc.packages.append(Package('color', options=['usenames', 'dvipsnames',]))
   
#Table pre-commands
doc.append(NoEscape(r'\begin{table*}[h]'))
doc.append(NoEscape(r'\begin{preview}')) 
doc.append(NoEscape(r'\centering'))
doc.append(NoEscape(r'\pagenumbering{gobble}'))
   
#Table header
table_format = 'llllllll'  
   
#Elements we want to put in the table
idces_table     = (dz.reducDf.frame_tag.isin(dz.observation_dict['objects'] + dz.observation_dict['Standard_stars'] + ['flat', 'arc'])) & (dz.reducDf.file_location.str.contains('/raw_fits/'))
file_names      = dz.reducDf[idces_table].sort_values(['RUN']).file_name.values
file_folders    = dz.reducDf[idces_table].sort_values(['RUN']).file_location.values
RA_values       = dz.reducDf[idces_table].sort_values(['RUN']).RA.values
DEC_values      = dz.reducDf[idces_table].sort_values(['RUN']).DEC.values
UT              = dz.reducDf[idces_table].sort_values(['RUN']).UT.values
objects         = dz.reducDf[idces_table].sort_values(['RUN']).frame_tag.values
color           = dz.reducDf[idces_table].sort_values(['RUN']).ISIARM.values
valid_values    = dz.reducDf[idces_table].sort_values(['RUN']).valid_file.values
   
#Fill the table
with doc.create(Tabular(table_format)) as table:
          
    #Adding the header
    headers = ['Object', 'Frame', 'Arm', 'UT', 'RA', 'DEC', 'Arc Blue', 'Arc Red']
    row_values = [None] * len(headers)
    table.add_row(headers, escape=False)
    table.add_hline()
   
    for i in range(len(file_names)):
           
        #Get the righ match if it is a target
        if objects[i] in (dz.observation_dict['Standard_stars'] + dz.observation_dict['objects']):
            blue_object     = matched_frames['{codename}_{arm_color}_{calib_file}_bySeparation'.format(codename = objects[i], arm_color = 'Blue', calib_file = 'arc')]
            red_object      = matched_frames['{codename}_{arm_color}_{calib_file}_bySeparation'.format(codename = objects[i], arm_color = 'Red', calib_file = 'arc')]
            match           = [blue_object, red_object]
               
            row_values[6]   = r'\textcolor{{{color}}}{{{filename}}}'.format(color = colors_dict[match[0]], filename=match[0])
            row_values[7]   = r'\textcolor{{{color}}}{{{filename}}}'.format(color = colors_dict[match[1]], filename=match[1])
        else:
            match = [' ', ' ']
            row_values[6]   = match[0]
            row_values[7]   = match[1]
   
          
        #Get the color of the row
        if file_names[i] in colors_dict:
            color_row = colors_dict[file_names[i]]
               
        else:
            color_row = 'black'
           
        #format_removed
        if valid_values[i] == True:
            entry_object_type = '{codename}'.format(codename = objects[i].replace('_',''))
        else:
            entry_object_type = r'\textbf{{{codename}}}'.format(codename = objects[i])
              
        #Add the row
        row_values[0] = entry_object_type
        row_values[1] = r'\textcolor{{{color}}}{{{filename}}}'.format(color = color_row, filename=file_names[i])
        row_values[2] = '{arm_color}'.format(arm_color=color[i])
        row_values[3] = UT[i]
        row_values[4] = RA_values[i]
        row_values[5] = DEC_values[i]
   
        table.add_row(row_values, escape=False)
       
        #Adding a double line for different section
        table.add_hline()
   
#Close the preview
doc.append(NoEscape(r'\end{preview}'))               
doc.append(NoEscape(r'\end{table*}'))  
           
#Generate the document
doc.generate_pdf(clean=True)    
     
#--- Save the matches to the observation dictionary
for i in range(len(frames_obj)):
    target_object = frames_obj[i]
    blue_file     = matched_frames['{codename}_{arm_color}_{calib_file}_bySeparation'.format(codename = target_object, arm_color = 'Blue', calib_file = 'arc')]
    red_file      = matched_frames['{codename}_{arm_color}_{calib_file}_bySeparation'.format(codename = target_object, arm_color = 'Red', calib_file = 'arc')]
    blue_run      = dz.reducDf[(dz.reducDf.file_name == blue_file)].RUN.values[0]
    red_run       = dz.reducDf[(dz.reducDf.file_name == red_file)].RUN.values[0]
    dz.observation_dict[target_object + '_arc'] = [blue_run, red_run]
   
dz.save_observation_dict()


