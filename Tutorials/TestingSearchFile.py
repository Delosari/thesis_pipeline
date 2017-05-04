'''
Created on Dec 4, 2014

@author: delosari
'''

from Code_Lib.vitoolsclass import vitools

vit = vitools()

FilesList = vit.SearchFiles_Pattern('/home/delosari/Dropbox/Astrophysics/Data/WHT_HII_Galaxies/', '.plot', Sort_Output = 'Alpha')

for i in range(len(FilesList[0])):
    print '-', FilesList[0][i]
    for subfile in FilesList[1][i]:
        print '----', subfile