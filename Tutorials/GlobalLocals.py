'''
Created on Aug 14, 2015

@author: vital
'''
def Metodo1():
    
    a = 3
    
    b = 6
    
    def Metodo2():
        
        c = 9
        
        return c
    
    d = Metodo2()
    
    return locals()


Cosos = Metodo1()

print 'cosos', type(Cosos)
print Cosos
