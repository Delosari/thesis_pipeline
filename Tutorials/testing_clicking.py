import numpy as np
import matplotlib.pyplot as plt
 
# #Esta es la funcion que se ejecuta al hacer click
# def coordinates_on_click(event, axis= None, mousebottom = 3):
#     x, y = event.x, event.y
#      
#     #Este numero decide el boton del raton: 1 para izquierdo, 3 para derecho.
#     if event.button == mousebottom:   
#         if event.inaxes is not None:
#             print '-Coordiantes  {} {}'.format(event.xdata, event.ydata)  
#              
#             #Estas lineas intentan encontrar a que curva (si esta tiene label) pertenecen los datos                      
#             if axis != None: 
#                 for curve in axis.get_lines():
#                     if curve.contains(event)[0]:
#                         curve_label = curve.get_label()
#                         if curve_label[0] != '_':
#                             print '--Curve: {}'.format(curve_label)
#  
#  
# t = np.arange(0.0, 1.0, 0.01)
# s = np.sin(2*np.pi*t)
# s2 = np.sin(3*np.pi*t)
#  
# fig, ax = plt.subplots()
# ax.plot(t, s, label = 'sine 1')
# ax.plot(t, s2, label = 'sine 2')
#  
# mouse_button = {'left':1, 'right':3}
#  
# #Esta linea conecta tu plot a un proceso cando clickeas
# plt.connect('button_press_event', lambda event: coordinates_on_click(event, ax, mouse_button['right']))
#  
# plt.show()


# def sum(a,b):
#     return a+b
# 
# def minus(a,b):
#     return a-b
# 
# def multiply(a,b):
#     return a*b
# 
# def divide(a,b):
#     return a/b

class myOperations():
      
    def __init__(self):
          
        self.operation = {'suma':self.sum,
                     'resta':self.minus,
                     'mult':self.multiply,
                    'div':self.divide}

    def run_op(self, operation_name, param_tuple):
        
        operation = getattr(self, operation_name, None)
        if callable(operation):
            return operation(*param_tuple)
        else:
            return 'Operation not available'
    
    def run_op2(self, operation_name):
        
        operation = getattr(self, operation_name, None)
        if callable(operation) == False:
            print 'Operation not available'
        return operation
    
    def run_op3(self, operation_name, param_dict):

        operation = getattr(self, operation_name, None)
        if callable(operation) == False:
            print 'Operation not available'
        print operation(**param_dict), 'esto'
           
    def sum(self, a,b):
        return a+b
      
    def minus(self, a,b):
        return a-b
  
    def multiply(self, a,b):
        return a*b
      
    def divide(self, a,b):
        return a/b

op      = myOperations()
mytuple = (2,3)
mydict  = {'a':2, 'b':3 }
print 'method 1', op.run_op('sum', mytuple)
print 'method 2', op.run_op2('sum')(2,3)
print 'method 3', op.run_op3('sum', mydict)

 
# treatment = op.operation['suma']
# print op.opedict
# print 'AQUIII'
# print op.opedict.keys()
# 
# print op.opedict['suma'](2,3)


# class myOperations():
#       
#     def sum(self, a,b):
#         return a+b
#      
#     def minus(self, a,b):
#         return a-b
#  
#     def multiply(self, a,b):
#         return a*b
#      
#     def divide(self, a,b):
#         return a/b
#      
#     def treatment(self, function_name, a, b):
#         
#         if hasattr(self, function_name):
#             print getattr(self, function_name)(a, b)
# 
# op = myOperations()
# 
# op.treatment('sum', 3, 4)





