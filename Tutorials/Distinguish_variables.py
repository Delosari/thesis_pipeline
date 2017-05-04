from numpy                                  import ndarray, log10 as num_log10
from math                                   import log10 as math_log10
from collections                            import OrderedDict, Sequence
from uncertainties.unumpy                   import uarray, nominal_values, std_devs, log10 as unum_log10
from uncertainties                          import UFloat, ufloat
from Math_Libraries.sigfig                  import round_sig
from uncertainties.umath                    import log10 as umath_log10, pow as uma_pow

a = None
b = 5
c = 5.0
d = [5,0]
e = ndarray([5,0])
f = 'coso'
g = uarray(5.5, 0.1)
h = ndarray([3.0])
i = uarray([1, 2], [0.01, 0.002])
j = ufloat(5.5, 0.1)
k = uarray([5.5], [0.1])

logSI_OI = ufloat(-1.53, 0.05)
print logSI_OI
SI_OI = uma_pow(10, logSI_OI)
print SI_OI
OI_SI = 1 / SI_OI
print OI_SI
OI_SI2 = uma_pow(10, -logSI_OI)
print OI_SI2

# print unum_log10(j), type(unum_log10(j))
# print umath_log10(j), type(umath_log10(j))
# print math_log10(j), type(math_log10(j))
# print num_log10(j), 'este no fona'





# print j.nominal_value, nominal_values(j), type(j.nominal_value), type(nominal_values(j))
# print j.std_dev, std_devs(j),type(j.std_dev), type(std_devs(j))
# 
# print 'g', isinstance(g, (Sequence, np.ndarray))
# print 'g', isinstance(g, UFloat), type(g)
# print g, asscalar(g), type(asscalar(g))
# 
# entry = a
# 
# print 'a', isinstance(a, (Sequence, np.ndarray))
# print 'b', isinstance(b, (Sequence, np.ndarray))
# print 'c', isinstance(c, (Sequence, np.ndarray))
# print 'd', isinstance(d, (Sequence, np.ndarray)), len(d)
# print 'e', isinstance(e, (Sequence, np.ndarray)), len(e)
# print 'f', isinstance(f, (Sequence, np.ndarray)), len(f)
# print 'g', isinstance(g, (Sequence, np.ndarray))
# print 'h', isinstance(h, (Sequence, np.ndarray)), len(h)
# print 'i', isinstance(i, (Sequence, np.ndarray)), len(i)
# print 'j', isinstance(j, (Sequence, np.ndarray))
# print 'k', isinstance(k, (Sequence, np.ndarray)), len(k)
# 
# print asscalar
# print g, asscalar(g), type(asscalar(g))
# print g, asscalar(g), type(asscalar(g))
# print 'g', isinstance(g, UFloat), type(g)
# 
# 
# print 'a', isinstance(a, UFloat), type(a)
# print 'b', isinstance(b, UFloat), type(b)
# print 'c', isinstance(c, UFloat), type(c)
# print 'd', isinstance(d, UFloat), type(d)
# print 'e', isinstance(e, UFloat), type(e)
# print 'f', isinstance(f, UFloat), type(f)
# print 'g', isinstance(g, UFloat), type(g)
# print 'h', isinstance(h, UFloat), type(h)
# print 'i', isinstance(i, UFloat), type(i)
# print 'j', isinstance(j, UFloat), type(j)
# print 'k', isinstance(k, UFloat), type(k)
# 
# print std_devs(a), type(std_devs(a))
# print std_devs(b), type(std_devs(b))
# print std_devs(c), type(std_devs(c))
# print std_devs(d), type(std_devs(d))
# print std_devs(e), type(std_devs(e))
# print std_devs(f), type(std_devs(f))
# print std_devs(g), type(std_devs(g))
# print std_devs(g), type(std_devs(g))
# 
# # print float(a), type(std_devs(a))
# print float(b), type(std_devs(b))
# print float(c), type(std_devs(c))
# # print float(d), type(std_devs(d))
# # print float(e), type(std_devs(e))
# # print float(f), type(std_devs(f))
# # print float(g), type(std_devs(g))
# # print float(h), type(float(h))
# 
# # print asscalar(a), type(asscalar(a))
# # print asscalar(b), type(asscalar(b))
# # print asscalar(c), type(asscalar(c))
# # print asscalar(d), type(asscalar(d))
# # print asscalar(e), type(asscalar(e))
# # print asscalar(f), type(asscalar(f))
# print asscalar(g), type(asscalar(g))
# 
# #Check None entry
# if entry != None:
#         
#     #Check string entry
#     if type(entry) == str: 
#         formatted_entry = entry
#        
#     #Case of Numerical entry
#     else:
#              
#         #Case of an array: we just put all together in a "_' joined string        
#         if isinstance(entry, (Sequence, np.ndarray)):
#             formatted_entry = '_'.join(entry)
#                 
#         #Case single scalar (CAREFULL WITH SINGLE VALUE ARRAYS)
#         else:
#              
#             #Case with error quantified
#             if isinstance(a, UFloat):
#                 formatted_entry = round_sig(nominal_values(entry), rounddig, scien_notation = scientific_notation) + r'$\pm$' +  round_sig(std_devs(entry), rounddig, scien_notation = scientific_notation)
#                  
#             #Case single float
#             else:
#                 formatted_entry = round_sig(entry, rounddig, scien_notation = scientific_notation)
#                         
# else:
#     #None entry is converted to None
#     formatted_entry = 'None'
#     
# return formatted_entry