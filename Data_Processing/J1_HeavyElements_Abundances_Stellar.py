from dazer_methods  import Dazer
from numpy          import nan as np_nan

#Generate dazer object
dz = Dazer()
dz.load_elements()

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Declare data for the analisis
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_emission_2nd.txt'
 
#Reddening properties
R_v         = 3.4
red_curve   = 'G03'
cHbeta_type = 'cHbeta_emis'
 
#Loop through objects:
for objName in catalogue_df.index:
        
        try:
        
            print '\n-Treating: {} {}/{}'.format(objName, catalogue_df.index.get_loc(objName), len(catalogue_df))
                        
            ouput_folder = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
            lineslog_address = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=AbundancesFileExtension)
                                       
            #Load lines frame
            lineslog_frame = dz.load_lineslog_frame(lineslog_address)
           
            #Perform the reddening correction
            cHbeta = catalogue_df.loc[objName, cHbeta_type]
            dz.deredden_lines(lineslog_frame, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
               
            #Set astronomical object
            dz.declare_object(lineslog_frame)
          
            #Calculate electron temperature and density for the diverse elements
            print '-Electron properties'
            dz.determine_electron_parameters(catalogue_df.loc[objName])
               
            #Load electron parameter from object characteristic
            ne          = dz.abunData.neSII if 'neSII' in dz.abunData else dz.generate_nan_array()
            Tlow_key    = catalogue_df.loc[objName, 'T_low']
            Thigh_key   = catalogue_df.loc[objName, 'T_high']
            T_low       = dz.abunData[Tlow_key] if Tlow_key in dz.abunData else dz.generate_nan_array()
            T_high      = dz.abunData[Thigh_key] if Thigh_key in dz.abunData else dz.generate_nan_array()
                                                
            #Argon
            dz.argon_abundance_scheme( T_low, T_high, ne)
                    
            #Sulfur
            dz.sulfur_abundance_scheme(T_low, ne, SIII_lines_to_use = catalogue_df.loc[objName].SIII_lines)
               
            #Oxygen
            dz.oxygen_abundance_scheme(T_low, T_high, ne)
               
            #Nitrogen
            dz.nitrogen_abundance_scheme(T_low, ne)
                
            print '-Helium abundances'
           
            if 'neSII' in dz.abunData: 
                dz.helium_abundance_elementalScheme(T_high, ne, lineslog_frame, metal_ext='O')
                dz.helium_abundance_elementalScheme(T_high, ne, lineslog_frame, metal_ext='S')
                
            #Store the abundances
            dz.store_abundances_excel(objName, catalogue_df, extension = '_emis2nd')
        
        except:
            print 'OBJ failed'
        
        
dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx', df_sheet_format = 'catalogue_data')
   
print '\nAll data treated\n', dz.display_errors()

