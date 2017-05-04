import numpy as np

XValues         = []
YValues         = []
MatrixResults   = []

x1 = np.array([1,2,3,4,5,6])
y1 = np.array([7,8,9,10,11,12])

x2 = np.array([0,1,2,3])
y2 = np.array([0,1,4,9])

x3 = np.array([0,1,2,3,4,5,6,7,8,9])
y3 = np.array([0,1,2,3,4,5,6,7,8,9])

MatrixResults.append(x1)
MatrixResults.append(y1)
MatrixResults.append(x2)
MatrixResults.append(y2)
MatrixResults.append(x3)
MatrixResults.append(y3)

XValues.append(x1)
XValues.append(x2)
XValues.append(x3)

YValues.append(y1)
YValues.append(y2)
YValues.append(y3)

LengthVector = []

LengthVector.append(len(x1))
LengthVector.append(len(y1))
LengthVector.append(len(x2))
LengthVector.append(len(y2))
LengthVector.append(len(x3))
LengthVector.append(len(y3))

LenMax = 0

for i in range(len(XValues)):
    if LenMax < len(XValues[i]):
        LenMax = len(XValues[i])
        
DefautlStringFormat         = '%20s'
DefaultScientificFormat     = '%20.5e'

DefautlStringFormat2         = '{20s}'
DefaultScientificFormat2     = '{20.5e}'

StringTitle = DefautlStringFormat + DefautlStringFormat + DefautlStringFormat + DefautlStringFormat + DefautlStringFormat + DefautlStringFormat
StringTitle = DefautlStringFormat + DefautlStringFormat + DefautlStringFormat + DefautlStringFormat + DefautlStringFormat + DefautlStringFormat
 
print StringTitle % ('x1', 'y1','x2', 'y2', 'x3', 'y3')

for i in range(LenMax): 
    LineFormat  = ''
    LineValue   = []  
    for k in range(len(MatrixResults)):
        if i < LengthVector[k]:
            LineFormat = LineFormat + DefaultScientificFormat
            LineValue.append(MatrixResults[k][i])
        else:
            LineFormat = LineFormat + DefautlStringFormat
            LineValue.append(' ')            
    print LineFormat % tuple(LineValue)
    

