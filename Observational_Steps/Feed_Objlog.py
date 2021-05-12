import os
import urllib2
from Plotting_Libraries.dazer_plotter       import Plot_Conf
import pylab as pl
from matplotlib import image
import math, ephem, pandas as pd
from numpy import int64
from astroquery.sdss                        import SDSS
from astroquery.alfalfa                     import Alfalfa
from collections                            import OrderedDict
from ManageFlow                             import DataToTreat
from CodeTools.PlottingManager              import myPickle
from uncertainties                          import ufloat
from astropy                                import coordinates as coords
from astroquery.sdss                        import SDSS

def _fetch(outfile, RA, DEC, scale=0.2, width=400, height=400):
    """Fetch the image at the given RA, DEC from the SDSS server"""
    url = ("http://casjobs.sdss.org/ImgCutoutDR7/getjpeg.aspx?ra=%.8f&dec=%.8f&scale=%.2f&width=%i&height=%i" % (RA, DEC, scale, width, height))
#     print "DOWNLOADING %s" % url
#     print " -> %s" % outfile
    fhandle = urllib2.urlopen(url)
    open(outfile, 'w').write(fhandle.read())

def fetch_image(RA, DEC, folder, Name):

    filename = os.path.join(folder + Name)
    if not os.path.exists(filename):
        _fetch(filename, RA, DEC)
    
    return image.imread(filename)


#Generate dazer object

pv                                          = myPickle()

#Generate dazer object
dz = Plot_Conf()

#Define figure format
dz.FigConf(n_colors = 2)

#Define operation
Catalogue_Dic                               = DataToTreat('WHT_CandiatesObjects_2016A')

#Generate the catalogue folders
pv.generate_catalogue_tree(Catalogue_Dic)

#Recover objects list
Table_Address = Catalogue_Dic['Data_Folder'] + 'WHT_Candidate_Objects_List'
Candiates_frame = pd.read_csv(Table_Address, delimiter = '; ', header = 0, index_col = 0)

print 'Using this file', Table_Address

#Labels with the data from Hbeta
Hbeta_label = 'H_beta'


for i in range(len(Candiates_frame.index)):
    
    #Get the frame row
    row = Candiates_frame.iloc[[i]]
     
    #Get the object SDSS parameters
    Name, Catalogue, mjd, plate, fiberID, alfalfa_code = Candiates_frame.index[i], row['catalogue'].values[0], row['mjd'].values[0], row['plate'].values[0], row['fiber'].values[0], row['alfalfa_name'].values[0] 
     
    #Generate object folder
    CodeName    = pv.generate_catalogue_tree(Catalogue_Dic, obj = Name)
    FileFolder  = Catalogue_Dic['Obj_Folder'] + CodeName + '/'
 
    #Store parameter in object log file
    pv.SetLogFile(CodeName + pv.ObjectLog_extension, FileFolder)
         
    #Query the object table
    #----------------Sloan objects----------------------
    if Catalogue == 'sloan':
        mjd, plate, fiberID = int(mjd), int(plate), int(fiberID)
        
        obj_table = SDSS.query_specobj(mjd = mjd, plate = plate, fiberID=fiberID)
        
        if obj_table != None:
            #print Name, str(ephem.hours(math.radians(obj_table['ra'][0]))), str(ephem.degrees(math.radians(obj_table['dec'][0]))), '\n'
            SDSS_RA         = obj_table['ra'][0]
            SDSS_DEC        = obj_table['dec'][0]
            SDSS_RA_hours   = str(ephem.hours(math.radians(obj_table['ra'][0])))
            SDSS_DEC_hours  = str(ephem.degrees(math.radians(obj_table['dec'][0])))
            
            co                  = coords.SkyCoord(float(SDSS_RA), float(SDSS_DEC), unit="deg")
            Obj_query           = SDSS.query_crossid(co, photoobj_fields=['modelMag_u', 'modelMag_g', 'modelMag_r'])
            mag_u, mag_g, mag_r = Obj_query['modelMag_u'][0], Obj_query['modelMag_g'][0], Obj_query['modelMag_r'][0]
            website = "http://dr12.sdss3.org/spectrumDetail?mjd={mjd}&fiber={fiber}&plateid={plateid}".format(mjd = mjd, fiber = fiberID, plateid = plate)
            
            print Name, website

            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_RA_deg', SDSS_RA)
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_DEC_deg', SDSS_DEC)
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_RA_Hour', SDSS_RA_hours)
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_DEC_Hour', SDSS_DEC_hours)
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_u_magModel', mag_u)
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_g_magModel', mag_g)
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_r_magModel', mag_r)
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_g_magModel', mag_g)
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'URL_SDSS', website)
            
            SDSS.cache_location = FileFolder
            
            spec = SDSS.get_spectra(plate=plate, fiberID=fiberID, mjd=mjd, timeout=60, cache=True, data_release=12)
            
#             print Name, SDSS_RA, SDSS_DEC

            #Download the object spectrum
            Spec_data   = spec[0][2].data
            sn_median   = Spec_data['SN_MEDIAN_ALL'][0]
            z_sdss      = Spec_data['Z'][0]
            Lines_data  = spec[0][3].data
            index_Hbeta = (Lines_data['LINENAME'] == Hbeta_label) 
            Flux_Hbeta  = Lines_data['LINEAREA'][index_Hbeta]
            Er_Hbeta    = Lines_data['LINEAREA_ERR'][index_Hbeta]
            Ew_Hbeta    = Lines_data['LINEEW'][index_Hbeta]
            EwEr_Hbeta  = Lines_data['LINEEW_ERR'][index_Hbeta]

            #print Name, mjd, plate, fiberID, sn_median, z_sdss, Flux_Hbeta, Ew_Hbeta

            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_Flux_Hbeta', ufloat(float(Flux_Hbeta), float(Er_Hbeta))*10e-17)
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_Eqw_Hbeta', ufloat(float(Ew_Hbeta), float(EwEr_Hbeta)))
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_z', z_sdss, Error='-')
            pv.SaveParameter_ObjLog(CodeName, FileFolder, 'SDSS_SNmedian', sn_median, Error='-')
            
            # Check that PIL is installed for jpg support

#             #Download images
#             I = fetch_image(SDSS_RA, SDSS_DEC, FileFolder, CodeName)
#             dz.Axis.imshow(I)
#             dz.savefig(FileFolder + CodeName + '_grid', reset_fig = True)
                                 
        else:    
            print 'WARNING: Object', Name, 'query failed'
             
    #----------------ALFALFA objects----------------------
    elif Catalogue == 'ALFALFA':
        alfalfa_catalogue   = Alfalfa.get_catalog()
        name_type           = 'str'
        
        name_type = 'str'
        try:
            float(alfalfa_code)
            name_type = 'int'
        except ValueError:
            print 'String ALFALFA code:', alfalfa_code
        
        try:
            object_found = False
            if name_type == 'str':
                if alfalfa_code in alfalfa_catalogue['AGCNr']:
                    object_found = True
            else:
                if int64(alfalfa_code) in alfalfa_catalogue['AGCNr']:
                    object_found = True
            
            if object_found:
                print 'Object found!'
                pv.SaveParameter_ObjLog(CodeName, FileFolder, 'Obj_RA', obj_table['ra'][0])
                pv.SaveParameter_ObjLog(CodeName, FileFolder, 'Obj_DEC', obj_table['dec'][0])
                
            else:
                print 'WARNING: Object', alfalfa_code, 'query failed'
        except:
            print 'Query failed'
    
    #----------------NED objects----------------------

print 'Data treated'

# chararray(['Ly_alpha', 'N_V 1240', 'C_IV 1549', 'He_II 1640', 'C_III] 1908',
#        'Mg_II 2799', '[O_II] 3725', '[O_II] 3727', '[Ne_III] 3868',
#        'H_epsilon', '[Ne_III] 3970', 'H_delta', 'H_gamma', '[O_III] 4363',
#        'He_II 4685', 'H_beta', '[O_III] 4959', '[O_III] 5007',
#        'He_II 5411', '[O_I] 5577', '[O_I] 6300', '[S_III] 6312',
#        '[O_I] 6363', '[N_II] 6548', 'H_alpha', '[N_II] 6583',
#        '[S_II] 6716', '[S_II] 6730', '[Ar_III] 7135'])


# ['PLATE',
#  'MJD',
#  'FIBERID',
#  'LINENAME',
#  'LINEWAVE',
#  'LINEZ',
#  'LINEZ_ERR',
#  'LINESIGMA',
#  'LINESIGMA_ERR',
#  'LINEAREA',
#  'LINEAREA_ERR',
#  'LINEEW',
#  'LINEEW_ERR',
#  'LINECONTLEVEL',
#  'LINECONTLEVEL_ERR',
#  'LINENPIXLEFT',
#  'LINENPIXRIGHT',
#  'LINEDOF',
#  'LINECHI2']


