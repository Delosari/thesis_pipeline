from dazer_methods import Dazer

#Declare object
dz = Dazer()

dz.FigConf(n_colors=5)

CodeName1 = '70'
CodeName2 = 'SDSS2'
extension = '_WHT.fits'

Folder_1 = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue_SulfurRegression/Objects/' + CodeName1 + '/'
Folder_2 = '/home/vital/Dropbox/Astrophysics/Data/WHT_Catalogue_SulfurRegression/Objects/' + CodeName2 + '/'
 
Wave1, Flux1, ExtraData1 = dz.File_to_data(Folder_1, 'obj' + CodeName1 + extension)
Wave2, Flux2, ExtraData2 = dz.File_to_data(Folder_2, 'obj' + CodeName2 + extension)

dz.Axis.set_yscale('log')

print Flux1
print Flux2

dz.data_plot(Wave1, Flux1, label = CodeName1, color=dz.ColorVector[2][0])
dz.data_plot(Wave2, Flux2, label = CodeName2, color=dz.ColorVector[2][1])
dz.FigWording(r'Wavelength $(\AA)$', 'Flux ' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', 'Objects {obj1} and {obj2} comparison'.format(obj1= CodeName1, obj2= CodeName2))
dz.display_fig()


