from itertools import izip, count


alist = ['a1', 'a2', 'a3']
blist = ['b1', 'b2']

for a, b in zip(alist, blist):
    print a, b
    
# more efficient version  

a = b = xrange(100000)

def foo():
    for i, x, y in izip(count(), a, b):
        pass

def bar():
    for i, (x, y) in enumerate(zip(a, b)):
        pass
#     
# >>> delta(foo)
# 0.0213768482208
# >>> delta(bar)
# 0.180979013443