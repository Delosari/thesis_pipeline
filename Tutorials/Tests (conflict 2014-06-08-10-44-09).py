'''
Created on Mar 19, 2014

@author: vital
'''


def Bilinear_Interpolation(X,Y,Q_11,Q_12,Q_21,Q_22):
    
    if len(Q_11) != 3 or len(Q_12) != 3 or len(Q_21) != 3 or len(Q_22) != 3:
        print "WARNING: Elements do not have the right size"

    x_1 = Q_11[1]
    x_2 = Q_22[1]

    y_1 = Q_11[2]
    y_2 = Q_22[2]
        
    Q = 1 / ((x_2 - x_1) * (y_2 - y_1)) * (
                                          Q_11[0] * (x_2 - X) * (y_2 - Y)
                                        + Q_21[0] * (X - x_1) * (y_2 - Y)
                                        + Q_12[0] * (x_2 - X) * (Y - y_1)
                                        + Q_22[0] * (X - x_1) * (Y - y_1)  
                                          )
             
    return Q

print "Hola"

Y1 = 0.00999457
Y2 = 0.01233898
X1 = 2.9
X2 = 3.0

Q_11 = [0.5756,X1,Y1]
Q_12 = [0.5812,X1,Y2]
Q_21 = [0.6479,X2,Y1]
Q_22 = [0.6540,X2,Y2]

Te = 2.9
Energy = 0.01000

Gamma = Bilinear_Interpolation(Te,Energy,Q_11,Q_12,Q_21,Q_22)

print Gamma
print "Se acabo"