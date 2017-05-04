from os                         import remove, close
from shutil                     import move
from pandas                     import Timedelta, to_datetime
from numpy                      import abs, sqrt, argmin, cos, timedelta64
from pyfits                     import getval
from astropy                    import units as u, coordinates as coord
from pylatex                    import Document, Package, Figure, NoEscape, Tabular
from tempfile                   import mkstemp
from DZ_observation_reduction   import spectra_reduction

def get_closest(df, idx, bool_cond, to_this):
    others = df.loc[bool_cond, to_this].values
    target = df.loc[idx, to_this].values[0]
    idx_closest  =  (abs(others-target)).argmin()
    closet_value = others[idx_closest]
    return df.loc[bool_cond & (df[to_this] == closet_value)].frame_tag.values[0],  closet_value

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

#Load iraf pypeline object

dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
   
Time_key        = 'UT'
Exp_time_key    = 'EXPTIME'
Airmass_key     = 'AIRMASS'
Position_keys   = ['RA', 'DEC']
   
Standard_stars  = dz.observation_dict['Standard_stars']
Science_targets = dz.observation_dict['objects']
u.degree
 
len_df = len(dz.reducDf.index)
   
dz.reducDf['UT_time']   = to_datetime(dz.reducDf['UT'])
dz.reducDf['UT_time']   = dz.reducDf['UT_time'] + (dz.reducDf.UT_time - dz.reducDf.iloc[0].UT_time < Timedelta(0)) * Timedelta(1, 'D')
 
idxs_stars =  (dz.reducDf.frame_tag.isin(Standard_stars)) & (dz.reducDf.reduc_tag == 'extracted_spectrum') & (dz.reducDf.ISIARM == 'Blue arm') & (dz.reducDf.ISISLITW > 2)
  
print dz.reducDf.loc[idxs_stars, 'frame_tag'].values
print dz.reducDf.loc[idxs_stars, 'AIRMASS'].values
print dz.reducDf.loc[idxs_stars, 'UT'].values
print dz.reducDf.loc[idxs_stars, 'UT_time'].values
print dz.reducDf.loc[idxs_stars, 'RA'].values
print dz.reducDf.loc[idxs_stars, 'DEC'].values
print
print dz.reducDf.loc[idxs_stars, 'UT_time'].values[0], dz.reducDf.loc[idxs_stars, 'UT_time'].values[0] - timedelta64(60,'s')

#Create the doc
doc = Document(dz.reducFolders['reduc_data'] + 'table_matching')
doc.packages.append(Package('geometry', options=['left=1cm', 'right=1cm', 'top=1cm', 'bottom=1cm']))
doc.packages.append(Package('preview', options=['active', 'tightpage',]))
doc.packages.append(Package('color', options=['usenames', 'dvipsnames',]))
 
#Table pre-commands
doc.append(NoEscape(r'\begin{table*}[h]'))
doc.append(NoEscape(r'\begin{preview}')) 
doc.append(NoEscape(r'\centering'))
doc.append(NoEscape(r'\pagenumbering{gobble}'))
 
#Table header
# table_format = 'l' + 'c'.join([' c' for s in range(len(dz.reducDf.loc[idxs_stars, 'frame_tag'].values) - 1)])
table_format = 'lc'
 
#Create the table
with doc.create(Tabular(table_format)) as table:
     
    #table.add_row(['Science targets'] + list(dz.reducDf.loc[idxs_stars, 'frame_tag'].values), escape=False)
    table.add_row(['Science targets', 'Stars proximity by\n Airmass, Time, angle'], escape=False)
 
    for i in range(len(Science_targets)):
              
        target_object = Science_targets[i]
              
        idx_target_reference    = (dz.reducDf.frame_tag == target_object) & (dz.reducDf.reduc_tag == 'extracted_spectrum') & (dz.reducDf.ISIARM == 'Blue arm') & (dz.target_validity_check())
        idx_target_observations = (dz.reducDf.frame_tag == target_object) & (dz.reducDf.reduc_tag == target_object) & (dz.reducDf.ISIARM == 'Blue arm')
        target_address          = dz.reducDf[idx_target_reference].file_location.values[0] + dz.reducDf[idx_target_reference].file_name.values[0]
        
        
        #Get the target parameters  
        Exposition_time         = getval(target_address, 'EXPTIME', 0)
        Airmass                 = getval(target_address, Airmass_key, 0)
        first_obs_time          = dz.reducDf[idx_target_reference].UT_time.values[0] 
        RA_obj, DEC_obj         = coord.Angle(dz.reducDf[idx_target_reference].RA.values[0], unit=u.hourangle),  coord.Angle(dz.reducDf[idx_target_reference].DEC.values[0], unit = u.degree)
        
        #Add half the time of the total observation
        time_interval = timedelta64(int(idx_target_observations.sum() * Exposition_time / 2),'s')
        dz.reducDf.loc[idx_target_reference, 'UT_time'] = dz.reducDf.loc[idx_target_reference, 'UT_time'].values[0] + time_interval
          
        #Calculating angular separation 
        RA_stars                = coord.Angle(dz.reducDf[idxs_stars].RA.values, unit=u.hourangle)
        DEC_stars               = coord.Angle(dz.reducDf[idxs_stars].RA.values, unit=u.degree)
            
        Delta_RA                = RA_stars.degree - RA_obj.degree
        Delta_Dec               = DEC_stars.degree - DEC_obj.degree
        cos_Dec                 = cos(DEC_obj.radian)
        Delta_Theta             = sqrt((Delta_RA * cos_Dec)**2 + (Delta_Dec)**2)
           
        #Get closests values 
        star_by_airmass, airmass_star   = get_closest(dz.reducDf, idx_target_reference, idxs_stars, Airmass_key)
        star_by_time, star_time         = get_closest(dz.reducDf, idx_target_reference, idxs_stars, 'UT_time')
        star_by_sep, star_sep           = dz.reducDf.loc[idxs_stars, 'frame_tag'].values[argmin(Delta_Theta)], Delta_Theta[argmin(Delta_Theta)]
      
        #Store the star by time
        dz.observation_dict['{target_code}_calibration_star_blue'.format(target_code = target_object)] = [star_by_time]
        dz.observation_dict['{target_code}_calibration_star_red'.format(target_code = target_object)] = [star_by_time]
        replace_observation_data(dz.Catalogue_folder + dz.observation_properties_file_name, dz.observation_dict)
  
        #Add the row
        table.add_row([target_object.replace('[','').replace(']',''), '{by_airmass} {by_time} {by_sep}'.format(by_airmass = star_by_airmass, by_time = star_by_time, by_sep=star_by_sep)], escape=False)
  
    #Adding a double line for different section
    table.add_hline()
      
#Close the preview
doc.append(NoEscape(r'\end{preview}'))               
doc.append(NoEscape(r'\end{table*}'))  
       
#Generate the document
doc.generate_pdf(clean=True)   
  
print 'Data treated' 
    
    
