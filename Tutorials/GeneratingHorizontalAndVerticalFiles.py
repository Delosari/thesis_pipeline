'''
Created on Jun 16, 2014

@author: INAOE_Vital
'''

import numpy as np
import Code_Lib.vitools as vit

def SaveVector2File(PlotVector, SavingAddress):
    TextFileAddress = SavingAddress.replace(SavingAddress[SavingAddress.find('.'):len(SavingAddress)],".plot")
    TextFile = open(TextFileAddress,"w")
    for i in range(len(PlotVector)):
        CurrentLine = ''
        for j in range(len(PlotVector[i])):
            item = PlotVector[i][j]
            if isinstance(item,str) or isinstance(item,int) or isinstance(item,float):
                CurrentLine = CurrentLine + str(item) + "; "
            if isinstance(item,list) or isinstance(item,tuple) or isinstance(item, np.ndarray):
                CurrentLine = CurrentLine + " ".join(map(str,item)) + "; "

        TextFile.write(CurrentLine+'\n')       
    TextFile.close()



SavingFolder = "/Users/INAOE_Vital/Dropbox/Lore/Programming/Programming_Tests/"

X = range(1,20,1)
Y = range(1,20,1)

X_a = range(20,30,1)
Y_a = range(20,30,1)

X_b = (1.003, 1, 1.0, 1e-8, 1e20)
Y_b = (1.003, 1, 1.0, 1e-8, 1e8)

# for i in range(len(X)):
#     print X[i], Y[i]

X_Data = (X,np.array(X_a), X_b)
Y_Data = [Y, Y_a, Y_b]     

# print X_Data
vit.SaveXYTable_2_Text(X, Y, SavingFolder + "VerticalTable.txt")
PlotVector = [X_Data,Y_Data]
SaveVector2File(PlotVector,SavingFolder + "HorizontalTable.txt")